from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import Client, create_client
from dotenv import load_dotenv
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import bcrypt
from datetime import datetime
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user

# Load environment variables
load_dotenv()

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Initialize Supabase client with error handling
try:
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL or Key not found in environment variables")
    
    supabase = create_client(supabase_url, supabase_key)
    # Test connection
    supabase.table('knowledge_base').select('*').limit(1).execute()
    print("✅ Successfully connected to Supabase")
except Exception as e:
    print(f"❌ Error connecting to Supabase: {str(e)}")
    supabase = None

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.email = user_data['email']
        self.username = user_data['username']

@login_manager.user_loader
def load_user(user_id):
    response = supabase.table('users').select('*').eq('id', user_id).execute()
    if response.data:
        return User(response.data[0])
    return None

# NLP Processing Class
class NLPProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer()
        
    def preprocess_text(self, text):
        # Tokenize
        tokens = word_tokenize(text.lower())
        # Remove stop words and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token.isalnum() and token not in self.stop_words]
        return ' '.join(tokens)

    def find_best_response(self, user_input, knowledge_base):
        processed_input = self.preprocess_text(user_input)
        all_responses = []
        categories = []
        
        for category, data in knowledge_base.items():
            for response in data['responses']:
                all_responses.append(response)
                categories.append(category)
        
        if not all_responses:
            return "I'm still learning about supply chain management. Please try asking about inventory, logistics, procurement, or forecasting."
        
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform([processed_input] + all_responses)
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        best_match_index = np.argmax(similarity_scores)
        
        if similarity_scores[0][best_match_index] < 0.1:
            return "I'm not sure about that. Could you please rephrase your question about supply chain management?"
            
        return all_responses[best_match_index]

nlp_processor = NLPProcessor()

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        response = supabase.table('users').insert({
            'email': email,
            'password': hashed_password.decode('utf-8'),
            'username': username
        }).execute()
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    try:
        # Query user from Supabase
        print(f"Attempting to login user: {email}")  # Debug log
        response = supabase.table('users').select('*').eq('email', email).execute()
        
        if not response.data:
            print(f"No user found with email: {email}")  # Debug log
            return jsonify({'error': 'User not found'}), 401
            
        user_data = response.data[0]
        
        try:
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                user = User(user_data)
                login_user(user)
                print(f"User logged in successfully: {email}")  # Debug log
                return jsonify({
                    'message': 'Login successful',
                    'user': {
                        'email': user.email,
                        'username': user.username
                    }
                }), 200
            else:
                print(f"Invalid password for user: {email}")  # Debug log
                return jsonify({'error': 'Invalid password'}), 401
        except Exception as e:
            print(f"Password verification error: {str(e)}")  # Debug log
            return jsonify({'error': 'Password verification failed'}), 500
            
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug log
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    if not supabase:
        return jsonify({'error': 'Database connection not available'}), 503
        
    data = request.json
    user_input = data.get('message')
    
    try:
        # Load knowledge base from Supabase
        response = supabase.table('knowledge_base').select('*').execute()
        knowledge_base = {}
        for item in response.data:
            knowledge_base[item['category']] = {
                'keywords': item['keywords'],
                'responses': item['responses']
            }
        
        # Process message using NLP
        response = nlp_processor.find_best_response(user_input, knowledge_base)
        
        # Log conversation with anonymous user
        try:
            supabase.table('chat_history').insert({
                'user_message': user_input,
                'bot_response': response,
                'timestamp': datetime.utcnow().isoformat()
            }).execute()
        except Exception as e:
            print(f"Warning: Failed to log chat history: {str(e)}")
            # Continue even if logging fails
        
        return jsonify({
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': f'Failed to process message: {str(e)}'}), 500

@app.route('/api/chat-history', methods=['GET'])
def get_chat_history():
    if not supabase:
        return jsonify({'error': 'Database connection not available'}), 503
        
    try:
        response = supabase.table('chat_history')\
            .select('*')\
            .order('timestamp', desc=True)\
            .limit(50)\
            .execute()
            
        return jsonify(response.data)
    except Exception as e:
        print(f"Error fetching chat history: {str(e)}")
        return jsonify({'error': f'Failed to fetch chat history: {str(e)}'}), 500

@app.route('/api/check-tables')
def check_tables():
    if not supabase:
        return jsonify({'error': 'Database connection not available'}), 503
        
    try:
        # Check knowledge_base table
        kb_response = supabase.table('knowledge_base').select('*').limit(1).execute()
        kb_exists = len(kb_response.data) >= 0
        
        # Check chat_history table
        ch_response = supabase.table('chat_history').select('*').limit(1).execute()
        ch_exists = len(ch_response.data) >= 0
        
        return jsonify({
            'status': 'success',
            'tables': {
                'knowledge_base': {
                    'exists': kb_exists,
                    'sample_data': kb_response.data
                },
                'chat_history': {
                    'exists': ch_exists,
                    'sample_data': ch_response.data
                }
            }
        })
    except Exception as e:
        print(f"Error checking tables: {str(e)}")
        return jsonify({'error': f'Failed to check tables: {str(e)}'}), 500

@app.route('/')
def home():
    status = "✅ Connected to Supabase" if supabase else "❌ Not connected to Supabase"
    return f'Flask backend is running. Database status: {status}'

if __name__ == '__main__':
    app.run(debug=True) 