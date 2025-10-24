# Stock Sentiment Analysis API - Deployment & OpenAI GPT Integration Guide

## Overview
This guide will help you deploy your sentiment analysis API and integrate it with OpenAI's GPT Builder.

---

## 📁 Files Created

1. **app.py** - Main Flask application with your sentiment analysis code
2. **requirements.txt** - Python dependencies
3. **openapi_schema.json** - API specification for GPT integration
4. **README.md** - This file

---

## 🚀 Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Why Railway?** Simple deployment, free tier available, automatic HTTPS

**Steps:**
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub account and create a new repo with these files
4. Railway will auto-detect Python and deploy
5. Add environment variables if needed (none required for basic setup)
6. Your API will be live at: `https://your-project.railway.app`

**Cost:** Free tier: $5 credit/month, then ~$5-20/month depending on usage

---

### Option 2: Heroku

**Steps:**
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create a `Procfile` in your project root:
   ```
   web: gunicorn app:app
   ```
3. Initialize git and deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```
4. Your API will be at: `https://your-app-name.herokuapp.com`

**Cost:** ~$7/month for basic dyno

---

### Option 3: PythonAnywhere (Good for Python-specific hosting)

**Steps:**
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files via the Files tab
3. Create a new web app (Flask)
4. Configure WSGI file to point to your app
5. Install requirements: `pip install -r requirements.txt --user`

**Cost:** Free tier available, $5/month for custom domain

---

### Option 4: Google Cloud Run (Serverless - Best for scaling)

**Steps:**
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
   ```
2. Deploy using gcloud CLI:
   ```bash
   gcloud run deploy sentiment-api --source .
   ```

**Cost:** Free tier: 2M requests/month, then pay-per-use

---

## 🧪 Testing Your API Locally

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Test endpoints (in another terminal)
curl http://localhost:5000/

# Test sentiment analysis
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple stock is performing exceptionally well today"}'

# Test stock sentiment analysis
curl -X POST http://localhost:5000/analyze-stock \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "news_articles": [
      "Apple announces record profits",
      "iPhone sales exceed expectations"
    ]
  }'
```

---

## 🤖 Integrating with OpenAI GPT Builder

### Step 1: Deploy Your API
Follow one of the deployment options above and get your live URL.

### Step 2: Update OpenAPI Schema
1. Open `openapi_schema.json`
2. Replace `"url": "https://your-app-url.com"` with your actual deployed URL
3. Save the file

### Step 3: Create Your Custom GPT

1. Go to [chat.openai.com](https://chat.openai.com)
2. Click your profile → "My GPTs" → "Create a GPT"
3. Fill in the **Configure** tab:
   - **Name**: "Stock Sentiment Analyzer"
   - **Description**: "Analyzes sentiment of financial news and text using FinBERT"
   - **Instructions**: 
   ```
   You are a financial sentiment analysis expert. You help users analyze the sentiment of financial news, articles, and text related to stocks and markets.
   
   When a user asks about sentiment:
   1. For single texts, use the /analyze endpoint
   2. For multiple news articles about a stock, use the /analyze-stock endpoint
   3. Interpret the sentiment scores and provide clear explanations
   4. Explain what positive, negative, or neutral sentiment means in a financial context
   
   Always present results in an easy-to-understand format.
   ```
   - **Conversation starters**:
     - "Analyze the sentiment of this financial news..."
     - "What's the sentiment around [STOCK SYMBOL]?"
     - "Check the sentiment of these articles about..."
     - "Is this financial text positive or negative?"

### Step 4: Add Your API as an Action

1. Scroll down to **Actions** section
2. Click "Create new action"
3. Click "Import from URL" or paste your OpenAPI schema
4. **If importing from URL**: Use `https://your-deployed-url.com/openapi.json` (you'd need to add an endpoint to serve the schema)
5. **Or paste the schema**: Copy the entire contents of `openapi_schema.json` and paste it
6. Click "Test" to verify the connection works
7. Set authentication to "None" (or add API key authentication if you implement it)

### Step 5: Test Your GPT

Try these test prompts:
- "Analyze this: Apple's Q4 earnings exceeded expectations with strong iPhone sales"
- "What's the sentiment of these TSLA articles: [paste articles]"
- "Is this text positive or negative: The company faces regulatory challenges"

### Step 6: Publish

1. Click "Save" in the top right
2. Choose who can access:
   - **Only me** - Private use
   - **Anyone with a link** - Share with specific people
   - **Public** - List in GPT store (requires GPT Plus)

---

## 🔒 Adding Authentication (Optional but Recommended)

To secure your API with an API key:

### 1. Modify `app.py`:

Add this after the imports:

```python
import os
from functools import wraps

API_KEY = os.environ.get('API_KEY', 'your-secret-key-here')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({"error": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Add @require_api_key decorator to your endpoints
@app.route('/analyze', methods=['POST'])
@require_api_key
def analyze_single():
    # ... rest of code
```

### 2. Update OpenAPI Schema:

Add this under `"openapi": "3.1.0"`:

```json
"components": {
  "securitySchemes": {
    "ApiKeyAuth": {
      "type": "apiKey",
      "in": "header",
      "name": "X-API-Key"
    }
  }
},
"security": [
  {
    "ApiKeyAuth": []
  }
]
```

### 3. In GPT Builder:

When adding the action, select "API Key" authentication and enter your key.

---

## 📊 Monitoring & Optimization

### Things to Consider:

1. **Model Loading Time**: The FinBERT model takes time to load. Consider:
   - Keeping one instance always running (not serverless)
   - Using model caching
   - Implementing a warm-up endpoint

2. **Rate Limiting**: Add rate limiting to prevent abuse:
   ```bash
   pip install flask-limiter
   ```

3. **Logging**: Add logging to track usage:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

4. **Error Handling**: Already included in the API, but monitor errors

---

## 🐛 Troubleshooting

### API not responding
- Check server logs
- Verify the URL is correct and accessible
- Test with curl or Postman first

### GPT can't connect to API
- Ensure CORS is enabled (already done in app.py)
- Verify OpenAPI schema matches your endpoints exactly
- Check authentication settings

### Model loading errors
- Ensure sufficient memory (FinBERT needs ~1GB RAM)
- Check internet connection for model download
- Verify transformers and torch versions

### Slow responses
- FinBERT inference can take 1-3 seconds per text
- Consider batching requests
- Use GPU instance for faster inference (optional)

---

## 📝 Next Steps

1. ✅ Test API locally
2. ✅ Deploy to your chosen platform
3. ✅ Update OpenAPI schema with your URL
4. ✅ Create your GPT in OpenAI
5. ✅ Test the integration
6. ✅ (Optional) Add authentication
7. ✅ Share or publish your GPT!

---

## 💡 Enhancement Ideas

- Add historical sentiment tracking
- Integrate with real-time news APIs
- Add stock price correlation analysis
- Create sentiment trend visualization
- Support multiple languages
- Add batch processing for large datasets

---

## 📚 Resources

- [OpenAI GPT Actions Documentation](https://platform.openai.com/docs/actions)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FinBERT Model](https://huggingface.co/ProsusAI/finbert)
- [OpenAPI Specification](https://swagger.io/specification/)

---

## Need Help?

Common issues and solutions are in the Troubleshooting section above. For deployment-specific issues, check the documentation for your chosen hosting platform.

Good luck with your Stock Sentiment Analyzer GPT! 🚀📈
