# 🚀 Deploy Life Calendar Bot on Render (Background Worker)

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be on GitHub
2. **Telegram Bot Token**: Get it from [@BotFather](https://t.me/BotFather)
3. **Render Account**: Sign up at [render.com](https://render.com)

## 🔧 Deployment Steps

### 1. Connect GitHub Repository

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Background Worker"**
3. Connect your GitHub account
4. Select the `life-bot` repository

### 2. Configure Service

- **Name**: `life-calendar-bot` (or any name you prefer)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty (root of repo)

### 3. Build & Deploy Settings

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python render_start.py`

### 4. Environment Variables

Add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `BOT_TOKEN` | `your_bot_token_here` | Your Telegram bot token |
| `PYTHON_VERSION` | `3.9.16` | Python version (auto-set) |

### 5. Deploy

Click **"Create Web Service"** and wait for deployment.

## 🔍 Monitoring

### Logs
- View logs in Render dashboard
- Monitor bot startup and errors
- Check for successful deployment

### Health Check
- Bot should start without errors
- Check logs for "Starting Life Calendar Bot on Render..."
- Verify bot responds to commands

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Failures
```bash
# Check requirements.txt compatibility
pip install -r requirements.txt
```

#### 2. Bot Not Starting
- Verify `BOT_TOKEN` is set correctly
- Check logs for error messages
- Ensure all dependencies are installed

#### 3. Import Errors
- Verify file structure matches repository
- Check Python version compatibility
- Ensure all files are committed to GitHub

### Debug Commands

```bash
# Test locally first
python render_start.py

# Check Python version
python --version

# Verify dependencies
pip list
```

## 📱 Testing After Deploy

1. **Start Command**: `/start`
2. **Set Gender**: `/setgender male` or `/setgender female`
3. **Set Birth Date**: `/setbirth 15.03.1990`
4. **Show Calendar**: `/show`
5. **Test Other Commands**: `/age`, `/week`, `/percentage`

## 🔄 Updates

To update your bot:

1. **Push changes** to GitHub `main` branch
2. **Render auto-deploys** on new commits
3. **Monitor deployment** in Render dashboard
4. **Test bot** after successful deployment

## 💰 Costs

- **Free Tier**: 750 hours/month
- **Bot runs continuously** (24/7) as background worker
- **No web interface needed** - perfect for Telegram bots
- **Upgrade** if you need more hours

## 🎯 Success Indicators

✅ **Build completes** without errors  
✅ **Worker starts** successfully  
✅ **Bot responds** to commands  
✅ **Logs show** normal operation  
✅ **No errors** in Render dashboard

## 🚀 Why Background Worker?

### ✅ **Perfect for Telegram Bots:**
- **No web interface** - bot runs in background
- **Continuous operation** - 24/7 availability
- **Resource efficient** - only runs when needed
- **Auto-restart** - recovers from errors automatically

### 🔄 **How it Works:**
1. **Background Worker** starts your bot
2. **Bot connects** to Telegram API
3. **Listens for messages** continuously
4. **Processes commands** and sends responses
5. **Runs indefinitely** until stopped  

## 🆘 Support

- **Render Docs**: [docs.render.com](https://docs.render.com)
- **GitHub Issues**: Create issue in your repository
- **Render Support**: Available in dashboard

---

**Your bot will be available 24/7 on Render! 🚀**
