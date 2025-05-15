import nltk

def download_nltk_data():
    try:
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        print("✅ Successfully downloaded NLTK data")
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {str(e)}")

if __name__ == '__main__':
    download_nltk_data() 