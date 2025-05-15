# Supply Chain Management Chatbot

A Flask-based intelligent chatbot application that provides information and answers questions about supply chain management. The application uses Natural Language Processing (NLP) to understand user queries and provide relevant responses from a knowledge base stored in Supabase.

## Features

- 🤖 Intelligent chatbot with NLP capabilities
- 🔐 User authentication system
- 💾 Persistent chat history
- 🧠 Extensible knowledge base
- 🌐 RESTful API endpoints
- 🔄 Real-time response processing
- 📊 Chat history tracking

## Tech Stack

- **Backend**: Python, Flask
- **Database**: Supabase
- **NLP**: NLTK, scikit-learn
- **Authentication**: Flask-Login, bcrypt
- **Frontend**: HTML, CSS, JavaScript
- **API**: RESTful architecture

## Prerequisites

- Python 3.10 or higher
- Supabase account
- Node.js and npm (for frontend development)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SECRET_KEY=your_secret_key_here
```

5. Set up the database:
```bash
python setup_db.py
```

## Database Setup

The application requires three tables in Supabase:
- `users`: Stores user authentication information
- `knowledge_base`: Contains the chatbot's knowledge base
- `chat_history`: Logs all conversations

The `setup_db.py` script will automatically create these tables and populate the knowledge base with sample data.

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

## API Endpoints

- `POST /api/register`: Register a new user
- `POST /api/login`: User login
- `POST /api/chat`: Send a message to the chatbot
- `GET /api/chat-history`: Retrieve chat history
- `GET /api/check-tables`: Check database table status

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NLTK for natural language processing capabilities
- Supabase for database services
- Flask community for the excellent web framework
- All contributors who have helped to improve this project 
