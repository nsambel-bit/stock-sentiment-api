# 🚀 QUICK START GUIDE

## What We've Built

Your Python sentiment analysis code is now wrapped in a Flask API with two endpoints:

1. **`/analyze`** - Analyze a single piece of financial text
2. **`/analyze-stock`** - Analyze multiple news articles about a stock

---

## ⚡ Fast Track to OpenAI GPT (5 Steps)

### Step 1: Test Locally (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API
python app.py

# In another terminal, test it
python test_api.py
```

You should see "ALL TESTS PASSED!"

---

### Step 2: Deploy to Railway (10 minutes) ⭐ RECOMMENDED

**Why Railway?** Easiest deployment, free tier, automatic HTTPS

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Create a new GitHub repo and push these files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   # Create repo on GitHub, then:
   git remote add origin https://github.com/yourusername/sentiment-api.git
   git push -u origin main
   ```
4. Select your repo in Railway
5. Railway auto-detects Python and deploys
6. Copy your live URL (looks like: `https://sentiment-api-production.up.railway.app`)

**Your API is now live!** 🎉

---

### Step 3: Update OpenAPI Schema (2 minutes)

1. Open `openapi_schema.json`
2. Find line 12: `"url": "https://your-app-url.com"`
3. Replace with your Railway URL
4. Save the file

---

### Step 4: Create Your GPT (5 minutes)

1. Go to [chat.openai.com](https://chat.openai.com)
2. Click your profile → **"My GPTs"** → **"Create a GPT"**
3. Go to the **"Configure"** tab
4. Fill in:
   - **Name:** Stock Sentiment Analyzer
   - **Description:** Analyzes financial news sentiment using FinBERT
   - **Instructions:** (copy from README.md or write your own)

5. Scroll to **"Actions"** section
6. Click **"Create new action"**
7. Paste the entire contents of your updated `openapi_schema.json`
8. Click **"Test"** - you should see successful connection

---

### Step 5: Test Your GPT (2 minutes)

Try these prompts in your GPT:

```
"Analyze this text: Tesla stock surged 15% after announcing record deliveries"

"What's the sentiment of these AAPL articles:
- Apple announces new iPhone with breakthrough features
- Supply chain concerns weigh on Apple's guidance
- Apple Services revenue hits all-time high"
```

**Done!** Your GPT is now analyzing sentiment using your Python code! 🎊

---

## 🎯 Alternative: Quick Deploy Options

### Option A: Heroku (if you prefer Heroku)
```bash
heroku create your-app-name
git push heroku main
```

### Option B: Google Cloud Run (for serverless)
```bash
gcloud run deploy sentiment-api --source .
```

---

## 📊 What Each File Does

- **app.py** - Your Flask API (the brain)
- **requirements.txt** - Python packages needed
- **openapi_schema.json** - Tells OpenAI how to use your API
- **test_api.py** - Tests to verify everything works
- **Procfile** - Tells Heroku how to run your app
- **Dockerfile** - For containerized deployment
- **README.md** - Full documentation

---

## 🆘 Troubleshooting

**API won't start locally?**
- Make sure you have Python 3.8+ installed
- Try: `pip install --upgrade pip` then reinstall requirements

**GPT can't connect?**
- Double-check the URL in openapi_schema.json
- Verify your API is accessible (visit the URL in a browser)
- Make sure you clicked "Test" in the Actions section

**Tests failing?**
- Ensure API is running: `python app.py`
- Wait 30 seconds for model to load
- Check if port 5000 is available

**Deployment issues?**
- Railway: Check build logs in the Railway dashboard
- Heroku: Run `heroku logs --tail`

---

## 💰 Cost Estimate

- **Railway:** $0-5/month (free tier covers basic usage)
- **Heroku:** $7/month (basic dyno)
- **Google Cloud Run:** ~$0-5/month (pay per use)
- **OpenAI GPT:** Free with ChatGPT Plus ($20/month)

---

## 🎉 You're Done!

In ~25 minutes, you've:
✅ Converted Python code to an API
✅ Deployed it to the cloud
✅ Created a custom GPT
✅ Can now analyze financial sentiment with natural language!

**Next:** Share your GPT link with others or make it public in the GPT store!

---

Need the full details? Check **README.md** for comprehensive documentation.
