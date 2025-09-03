#!/usr/bin/env python3
"""
Start script for Render Background Worker deployment
"""

import os
import logging
import sys
from health_check import health_check

# Configure logging for Render
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main startup function"""
    
    logging.info("🚀 Starting Life Calendar Bot on Render Background Worker...")
    
    # Perform health check
    if not health_check():
        logging.error("❌ Health check failed. Exiting...")
        sys.exit(1)
    
    try:
        # Import and start bot
        from bot import main as bot_main
        logging.info("✅ Bot imported successfully, starting...")
        bot_main()
        
    except ImportError as e:
        logging.error(f"❌ Failed to import bot: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
