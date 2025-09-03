#!/usr/bin/env python3
"""
Scheduler module for automatic weekly reports
"""

import logging
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from telegram import Bot
from telegram.error import TelegramError
from life_visualizer import LifeVisualizer
import os

logger = logging.getLogger(__name__)

class WeeklyReportScheduler:
    def __init__(self, bot_token, channel_id=None):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.scheduler = AsyncIOScheduler()
        self.visualizer = LifeVisualizer()
        
    def start_scheduler(self):
        """Start the scheduler with weekly report job"""
        try:
            # Configure job to run every Monday at 00:00 (midnight) Portugal time
            # Portugal uses Europe/Lisbon timezone
            portugal_tz = pytz.timezone('Europe/Lisbon')
            
            # Add weekly report job - every Monday at 00:00 Portugal time
            self.scheduler.add_job(
                func=self.send_weekly_report,
                trigger=CronTrigger(
                    day_of_week='mon',
                    hour=0,
                    minute=0,
                    timezone=portugal_tz
                ),
                id='weekly_report',
                name='Weekly Life Calendar Report',
                replace_existing=True
            )
            
            # Start the scheduler
            self.scheduler.start()
            logger.info("✅ Weekly report scheduler started successfully")
            logger.info("📅 Reports will be sent every Monday at 00:00 Portugal time")
            
        except Exception as e:
            logger.error(f"❌ Failed to start scheduler: {e}")
    
    async def send_weekly_report(self):
        """Send weekly life calendar report to channel"""
        try:
            logger.info("🚀 Starting weekly report generation...")
            
            # Create bot instance
            bot = Bot(token=self.bot_token)
            
            # Get current date for report
            current_date = datetime.now()
            current_week = current_date.isocalendar()[1]
            current_year = current_date.year
            
            # Create report message
            report_message = f"""📅 **Weekly Life Calendar Report**

🗓️ **Week {current_week}, {current_year}**
⏰ **Generated:** {current_date.strftime('%B %d, %Y at %H:%M')}
🌍 **Time Zone:** Portugal (Europe/Lisbon)

💡 **This week's reminder:**
Every square represents one week of your life.
Red squares = weeks you've lived
White squares = weeks ahead of you

🎯 **Use /start in the bot to see your personal calendar!**

#LifeCalendar #WeeklyReminder #TimeManagement"""
            
            # Send text report
            if self.channel_id:
                await bot.send_message(
                    chat_id=self.channel_id,
                    text=report_message,
                    parse_mode='Markdown'
                )
                logger.info(f"✅ Weekly report sent to channel {self.channel_id}")
            else:
                logger.warning("⚠️ No channel ID configured, skipping report send")
            
        except TelegramError as e:
            logger.error(f"❌ Telegram error sending weekly report: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected error in weekly report: {e}")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("🛑 Weekly report scheduler stopped")
    
    def get_next_run_time(self):
        """Get the next scheduled run time"""
        try:
            job = self.scheduler.get_job('weekly_report')
            if job:
                next_run = job.next_run_time
                if next_run:
                    # Convert to Portugal timezone for display
                    portugal_tz = pytz.timezone('Europe/Lisbon')
                    next_run_pt = next_run.astimezone(portugal_tz)
                    return next_run_pt
            return None
        except Exception as e:
            logger.error(f"❌ Error getting next run time: {e}")
            return None
    
    def get_scheduler_status(self):
        """Get current scheduler status"""
        try:
            return {
                'running': self.scheduler.running,
                'next_run': self.get_next_run_time(),
                'job_count': len(self.scheduler.get_jobs()),
                'timezone': 'Europe/Lisbon (Portugal)',
                'schedule': 'Every Monday at 00:00 (midnight)'
            }
        except Exception as e:
            logger.error(f"❌ Error getting scheduler status: {e}")
            return {'error': str(e)}
