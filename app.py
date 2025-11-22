# 🏥 Medical Chatbot Flask Application
# AI-Powered Medical Assistant with Beautiful Web Interface

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables for AI models (will be initialized)
groq_chatbot = None
gemini_chatbot = None
retriever = None

# Initialize AI models when the module is imported (for serverless)
def init_app():
    """Initialize the application"""
    global groq_chatbot, gemini_chatbot, retriever
    if groq_chatbot is None and gemini_chatbot is None and retriever is None:
        initialize_ai_models()

def initialize_ai_models():
    """Initialize all AI models and components"""
    global groq_chatbot, gemini_chatbot, retriever
    
    try:
        # Import required modules
        from langchain_groq import ChatGroq
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_pinecone import PineconeVectorStore
        from langchain_huggingface import HuggingFaceEmbeddings
        from pinecone import Pinecone
        
        print("🔧 Initializing AI models...")
        
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )
        
        # Initialize Pinecone
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        index = pc.Index('medical-chatbot')
        
        # Create vector store and retriever
        vector_store = PineconeVectorStore(index=index, embedding=embeddings)
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        
        # Initialize Groq chatbot
        try:
            groq_chatbot = ChatGroq(
                groq_api_key=os.getenv('GROQ_API_KEY'),
                model="llama-3.1-8b-instant",
                temperature=0.2,
                max_tokens=350
            )
            print("✅ Groq chatbot initialized")
        except Exception as e:
            print(f"⚠️ Groq initialization failed: {e}")
        
        # Initialize Gemini chatbot as backup
        try:
            gemini_chatbot = ChatGoogleGenerativeAI(
                google_api_key=os.getenv('GOOGLE_API_KEY'),
                model="gemini-pro",
                temperature=0.2,
                max_output_tokens=350
            )
            print("✅ Gemini chatbot initialized")
        except Exception as e:
            print(f"⚠️ Gemini initialization failed: {e}")
            
        if groq_chatbot or gemini_chatbot:
            print("🎉 All AI models initialized successfully!")
            return True
        else:
            print("❌ No AI models could be initialized")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing AI models: {e}")
        return False

def get_medical_response(question, model_preference="groq"):
    """Enhanced medical response with accuracy and conciseness focus"""
    try:
        # Get context from Pinecone if available
        context = ""
        if retriever:
            try:
                relevant_docs = retriever.invoke(question)
                context = "\n\n".join([doc.page_content for doc in relevant_docs[:2]])
                print(f"✅ Retrieved {len(relevant_docs)} relevant medical documents")
            except Exception as e:
                print(f"⚠️ Vector search failed: {e}")
                context = ""
        
        # Enhanced prompt for accurate and concise responses
        medical_prompt = f"""You are an expert medical AI assistant. Provide ACCURATE and CONCISE medical information.

MEDICAL CONTEXT:
{context[:1200] if context else "General medical knowledge"}

QUESTION: {question}

INSTRUCTIONS:
- Maximum 250 words
- Use bullet points for clarity
- Focus on essential information only
- Include specific actionable advice
- Always mention when to seek professional help

RESPONSE FORMAT:
• **Overview:** Brief explanation
• **Key Symptoms:** (if applicable)
• **Prevention/Treatment:** Essential steps only
• **⚠️ See Doctor:** Specific warning signs

Response:"""
        
        # Try Groq first (optimized for accuracy)
        if model_preference == "groq" and groq_chatbot:
            try:
                response = groq_chatbot.invoke(medical_prompt)
                answer = response.content.strip()
                
                # Add concise medical disclaimer
                disclaimer = "\n\n🔒 **IMPORTANT:** This is educational information only. Always consult healthcare professionals for personal medical advice."
                
                # Calculate response metrics
                word_count = len(answer.split())
                concise_rating = "Excellent" if word_count <= 150 else "Good" if word_count <= 250 else "Verbose"
                
                return {
                    "answer": answer + disclaimer,
                    "model": f"Groq (Fast & Accurate)",
                    "status": "success",
                    "metrics": {
                        "words": word_count,
                        "conciseness": concise_rating,
                        "knowledge_base": "Enhanced" if context else "Standard"
                    }
                }
            except Exception as e:
                print(f"Groq error: {e}")
                
        # Try Gemini as backup with same optimization
        if gemini_chatbot:
            try:
                response = gemini_chatbot.invoke(medical_prompt)
                answer = response.content.strip()
                
                disclaimer = "\n\n🔒 **IMPORTANT:** This is educational information only. Always consult healthcare professionals for personal medical advice."
                
                word_count = len(answer.split())
                concise_rating = "Excellent" if word_count <= 150 else "Good" if word_count <= 250 else "Verbose"
                
                return {
                    "answer": answer + disclaimer,
                    "model": "Google Gemini (Reliable)",
                    "status": "success", 
                    "metrics": {
                        "words": word_count,
                        "conciseness": concise_rating,
                        "knowledge_base": "Enhanced" if context else "Standard"
                    }
                }
            except Exception as e:
                print(f"Gemini error: {e}")
        
        # Enhanced fallback response
        return {
            "answer": f"""⚠️ AI temporarily unavailable for: "{question[:50]}..."

**Immediate Steps:**
• Consult a healthcare professional
• Visit nearest medical clinic
• Call medical helpline
• Use trusted medical websites (Mayo Clinic, WebMD)

🔒 **Always seek professional medical advice for health concerns.**""",
            "model": "System Fallback",
            "status": "fallback",
            "metrics": {
                "words": 0,
                "conciseness": "N/A",
                "knowledge_base": "Unavailable"
            }
        }
        
    except Exception as e:
        print(f"System error: {e}")
        return {
            "answer": f"❌ System error. Please consult a healthcare professional for medical questions.\n\n🔒 For urgent medical concerns, contact emergency services.",
            "model": "System Error",
            "status": "error",
            "metrics": {
                "words": 0,
                "conciseness": "N/A", 
                "knowledge_base": "Error"
            }
        }

@app.route('/')
def index():
    """Main page"""
    init_app()  # Initialize AI models for serverless
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    init_app()  # Initialize AI models for serverless
    try:
        data = request.get_json()
        question = data.get('message', '').strip()
        model_preference = data.get('model', 'groq').lower()
        
        if not question:
            return jsonify({
                "answer": "Please ask a medical question.",
                "model": "System",
                "status": "error"
            })
        
        # Get response from AI
        response = get_medical_response(question, model_preference)
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "answer": f"Server error: {str(e)}",
            "model": "System",
            "status": "error"
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "groq_available": groq_chatbot is not None,
        "gemini_available": gemini_chatbot is not None,
        "retriever_available": retriever is not None
    })

if __name__ == '__main__':
    print("🏥 Starting Medical Chatbot Web Application...")
    print("🔧 Initializing AI components...")
    
    # Initialize AI models
    if initialize_ai_models():
        print("🚀 Starting Flask server...")
        print("🌐 Open http://localhost:5000 in your browser")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize AI models. Please check your configuration.")