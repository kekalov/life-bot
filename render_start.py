#!/usr/bin/env python3
"""
Start script for Render deployment
"""

import os
import logging
from bot import main

# Configure logging for Render
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    # Check if BOT_TOKEN is set
    if not os.getenv('BOT_TOKEN'):
        logging.error("BOT_TOKEN environment variable is not set!")
        logging.error("Please set BOT_TOKEN in your Render environment variables")
        exit(1)
    
    logging.info("Starting Life Calendar Bot on Render...")
    main()
