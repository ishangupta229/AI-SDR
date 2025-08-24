# AI SDR - AI Sales Development Representative

## Overview
Complete AI-powered sales development system that automates prospect research, email outreach, follow-ups, and meeting scheduling — achieving up to a **35% engagement boost**.

## Features
- **AI Prospect Researcher**: Automated lead discovery and enrichment
- **AI Email Generator**: Personalized outreach campaigns
- **Follow-up Automation**: Smart sequence management
- **Meeting Scheduler**: AI-powered scheduling assistant
- **Knowledge Base**: Searchable sales materials and insights
- **Analytics Dashboard**: Performance tracking and optimization

## Quick Start
1. `pip install -r requirements.txt`  
2. Configure `.env` with your API keys  
3. Run: `python -m uvicorn src.main:app --reload`  
4. Visit: [http://localhost:8000/docs](http://localhost:8000/docs)  

## Architecture
- **FastAPI**: REST API backend  
- **LangChain / OpenAI**: AI processing  
- **Pinecone**: Vector database for knowledge base  
- **SQLAlchemy**: Data persistence  
