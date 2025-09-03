# 🚀 Start Commands for Life Calendar Bot

## 📋 Recommended Start Commands

### 🎯 **For Render Background Worker (Recommended)**
```bash
python render_start.py
```

**Why this is best:**
- ✅ Includes health check before starting
- ✅ Better error handling and logging
- ✅ Validates environment variables
- ✅ Graceful error reporting

### 🔧 **Alternative Start Commands**

#### **Direct Bot Start**
```bash
python bot.py
```
**Use when:** You want to start the bot directly without health checks

#### **With Python Module**
```bash
python -m bot
```
**Use when:** You want to run as a module (if configured)

#### **With Specific Python Version**
```bash
python3.9 render_start.py
```
**Use when:** You need to specify exact Python version

#### **With Debug Logging**
```bash
python render_start.py --debug
```
**Use when:** You need detailed debugging information

## 🎯 **Render Configuration**

### **render.yaml (Current)**
```yaml
services:
  - type: worker
    name: life-calendar-bot
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python render_start.py  # ← This is correct!
    envVars:
      - key: BOT_TOKEN
        sync: false
```

### **Why `python render_start.py` is Perfect:**

1. **Health Check**: Validates environment variables first
2. **Error Handling**: Catches and reports startup errors
3. **Logging**: Provides clear startup information
4. **Graceful Exit**: Exits cleanly if something is wrong
5. **Render Compatible**: Works perfectly with Render's worker environment

## 🔍 **Startup Process**

### **What Happens When You Run `python render_start.py`:**

1. **🚀 Script starts** and logs initialization
2. **🔍 Health check** validates BOT_TOKEN
3. **📦 Imports bot** modules
4. **🤖 Starts bot** and connects to Telegram
5. **📱 Bot runs** continuously listening for messages

### **Expected Logs:**
```
🚀 Starting Life Calendar Bot on Render Background Worker...
✅ Health check passed
📅 Current time: 2024-09-03 10:00:00
🤖 Bot token: 1234567890...abcdefghij
✅ Bot imported successfully, starting...
```

## 🚨 **Troubleshooting Start Commands**

### **If Bot Won't Start:**

#### **Check Environment Variables:**
```bash
# Test health check locally
python health_check.py
```

#### **Test Bot Import:**
```bash
# Test if bot can be imported
python -c "from bot import main; print('Bot imports successfully')"
```

#### **Check Dependencies:**
```bash
# Verify all packages are installed
pip list | grep -E "(telegram|matplotlib|Pillow)"
```

### **Common Issues:**

#### **1. Module Not Found**
```bash
# Error: No module named 'telegram'
# Solution: pip install -r requirements.txt
```

#### **2. BOT_TOKEN Not Set**
```bash
# Error: BOT_TOKEN environment variable is not set!
# Solution: Set BOT_TOKEN in Render environment variables
```

#### **3. Import Error**
```bash
# Error: Failed to import bot
# Solution: Check file structure and dependencies
```

## 🎯 **Final Recommendation**

**Use this start command for Render:**
```bash
python render_start.py
```

**This command:**
- ✅ Is tested and working
- ✅ Includes all necessary checks
- ✅ Provides clear error messages
- ✅ Works perfectly with Render Background Worker
- ✅ Follows best practices for production deployment

---

**Your bot will start reliably with `python render_start.py`! 🚀**
