# 🚀 Railway Deployment Guide

## Why Railway is the Best Free Option

✅ **$5 credit/month** (effectively free for small projects)  
✅ **Automatic HTTPS** - secure by default  
✅ **Auto-detects Python** - minimal configuration  
✅ **Easy GitHub integration** - deploy from repo  
✅ **Fast and reliable** - great for APIs  

## 📋 Step-by-Step Deployment

### Step 1: Push to GitHub

1. **Create a new repository on GitHub:**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `stock-sentiment-api`
   - Make it **Public** (required for Railway free tier)
   - Don't initialize with README (we already have files)

2. **Push your code to GitHub:**
   ```bash
   # Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
   git remote add origin https://github.com/YOUR_USERNAME/stock-sentiment-api.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Railway

1. **Go to Railway:**
   - Visit [railway.app](https://railway.app)
   - Sign up with your GitHub account

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `stock-sentiment-api` repository

3. **Railway Auto-Configuration:**
   - Railway will automatically detect it's a Python project
   - It will use the `requirements.txt` file
   - The `app.py` file will be used as the entry point
   - Configuration files (`railway.toml`, `nixpacks.toml`) are included for proper deployment

4. **Deploy:**
   - Click "Deploy Now"
   - Wait for deployment to complete (5-10 minutes for first deployment)

### Step 3: Get Your API URL

1. **Find your deployment URL:**
   - In Railway dashboard, click on your project
   - Go to "Settings" → "Domains"
   - Your API will be available at: `https://your-project-name.railway.app`

2. **Test your API:**
   ```bash
   # Health check
   curl https://your-project-name.railway.app/
   
   # Test sentiment analysis
   curl -X POST https://your-project-name.railway.app/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "Apple stock is performing exceptionally well today"}'
   ```

## 🔧 Configuration (Optional)

### Environment Variables
Railway will work with the default configuration, but you can add environment variables if needed:

1. In Railway dashboard → Settings → Variables
2. Add any environment variables (none required for basic setup)

### Custom Domain (Optional)
1. In Railway dashboard → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

## 💰 Cost Breakdown

- **Free Tier**: $5 credit/month
- **Typical Usage**: ~$0-2/month for small API usage
- **Model Loading**: One-time cost during deployment
- **Requests**: Very low cost per request

## 🚨 Important Notes

1. **First Deployment**: Takes 5-10 minutes due to FinBERT model download
2. **Cold Starts**: May take 30-60 seconds if the API hasn't been used recently
3. **Memory Usage**: FinBERT requires ~1GB RAM (Railway free tier supports this)
4. **Rate Limits**: No built-in rate limits, add them if needed for production

## 🔍 Troubleshooting

### Deployment Issues
- Check Railway logs in the dashboard
- Ensure `requirements.txt` is in the root directory
- Verify `app.py` exists and is properly configured

### API Not Responding
- Check if deployment completed successfully
- Verify the URL is correct
- Test with curl or Postman

### Model Loading Errors
- Check Railway logs for memory issues
- Ensure sufficient memory allocation
- Verify transformers library version compatibility

## 🎯 Next Steps After Deployment

1. **Update OpenAI GPT Integration:**
   - Update `openapi_schema.json` with your Railway URL
   - Use the schema to create your custom GPT

2. **Monitor Usage:**
   - Check Railway dashboard for usage metrics
   - Monitor costs and performance

3. **Scale if Needed:**
   - Upgrade Railway plan if you exceed free tier
   - Consider adding authentication for production use

## 📞 Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- GitHub Issues: Create issues in your repository

---

🎉 **Your Stock Sentiment Analysis API will be live and ready to use!**
