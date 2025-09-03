#!/usr/bin/env python3
"""
Health check script for Render Background Worker
"""

import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def health_check():
    """Perform health check for the bot"""
    
    # Check environment variables
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        logging.error("❌ BOT_TOKEN not found in environment variables")
        return False
    
    # Check if token looks valid (basic validation)
    if not bot_token.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')) or ':' not in bot_token:
        logging.error("❌ BOT_TOKEN format appears invalid")
        return False
    
    # Log successful health check
    logging.info("✅ Health check passed")
    logging.info(f"📅 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"🤖 Bot token: {bot_token[:10]}...{bot_token[-10:]}")
    
    return True

if __name__ == "__main__":
    health_check()
