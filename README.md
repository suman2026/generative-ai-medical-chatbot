# 🏥 Medical AI Chatbot - Advanced Healthcare Assistant

An intelligent medical chatbot powered by RAG (Retrieval-Augmented Generation) technology, featuring multiple AI models including Groq and Google Gemini, with Pinecone vector database for enhanced medical knowledge retrieval.

## 🚀 Live Demo
- **Vercel Deployment**: Coming soon!
- **Local Development**: Follow setup instructions below

## 🌟 Features
- **Multi-Model AI**: Groq (llama-3.1-8b-instant) + Google Gemini fallback
- **RAG Technology**: Pinecone vector database with 11,718+ medical documents
- **Professional UI**: Medical-themed responsive web interface
- **Quality Metrics**: Response quality indicators and medical disclaimers
- **Secure**: Environment-based API key management

## 🛠️ Technology Stack
- **Backend**: Python Flask + Flask-CORS
- **AI Models**: Groq LLM, Google Gemini AI
- **Vector Store**: Pinecone with sentence-transformers embeddings
- **Frontend**: HTML5, CSS3, JavaScript with medical theme
- **Deployment**: Vercel serverless architecture

## 📋 Quick Setup

### 1. Clone Repository
```bash
git clone https://github.com/suman2026/generative-ai-medical-chatbot.git
cd generative-ai-medical-chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create `.env` file with your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

### 4. Run Application
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

## 🌐 Vercel Deployment

### Prerequisites
- Vercel account
- GitHub repository
- API keys configured

### Deploy Steps
1. **Fork/Import to Vercel**:
   ```bash
   npx vercel
   ```

2. **Set Environment Variables**:
   In Vercel dashboard, add:
   - `GROQ_API_KEY`
   - `GOOGLE_API_KEY` 
   - `PINECONE_API_KEY`

3. **Deploy**:
   ```bash
   vercel --prod
   ```

### Automatic Deployment
- Connect GitHub repo to Vercel
- Auto-deploys on every push to main branch
- Environment variables configured in Vercel dashboard

## 🔐 API Keys Setup

### Groq API
1. Visit [console.groq.com](https://console.groq.com)
2. Create account and generate API key
3. Add to environment variables

### Google Gemini API  
1. Go to [ai.google.dev](https://ai.google.dev)
2. Get API key from Google AI Studio
3. Add to environment variables

### Pinecone API
1. Sign up at [pinecone.io](https://pinecone.io)
2. Create index named `medical-chatbot`
3. Get API key and add to environment

## 📁 Project Structure
```
├── app.py                 # Main Flask application
├── api/
│   └── index.py          # Vercel serverless entry point
├── templates/
│   └── index.html        # Web interface
├── src/
│   ├── helper.py         # Utility functions
│   └── prompt.py         # AI prompt templates
├── research/
│   └── trials.ipynb      # Development notebook
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── README.md            # Documentation
```

## 🏥 Usage

1. **Ask Medical Questions**: Type health-related queries
2. **Get AI Responses**: Powered by advanced LLMs with medical context
3. **Quality Indicators**: Response quality metrics displayed
4. **Medical Disclaimer**: Always consult healthcare professionals

## 🔧 Development

### Local Development
```bash
# Activate virtual environment (optional)
python -m venv medicalbot
medicalbot\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Research & Development
- Jupyter notebook available in `research/trials.ipynb`
- 67+ development cells with experiments
- Data processing and model testing

## ⚠️ Important Disclaimers

- **Medical Advice**: For informational purposes only
- **Professional Consultation**: Always consult qualified healthcare providers
- **Emergency**: Contact emergency services for urgent medical needs
- **Data Privacy**: API keys and conversations handled securely

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

- **Issues**: GitHub Issues tab
- **Documentation**: This README
- **API References**: Check respective AI provider docs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎯 Ready for Production Deployment on Vercel!**

Built with ❤️ for advancing AI-powered healthcare assistance.
