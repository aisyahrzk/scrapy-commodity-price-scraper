from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from datetime import datetime
import subprocess
import logging

def asyncio_schedule():
    
    """schedule tasks"""
    def run_spider(): 
        # Start 
        logging.info('Started crawling {}...'.format(datetime.now()))
        # Run scrapy crawl
        subprocess.run(['scrapy', 'crawl', 'fama'])
        # End
        logging.info('Finished crawling {}...'.format(datetime.now()))


    scheduler = AsyncIOScheduler()
    # Add task to crawl per hour between 7a.m to 7p.m
    scheduler.add_job(func=run_spider, trigger='cron', hour='1',minute = '7')
    # Add task to clean old log, keep logs for last 14 days only, run at 11:30p.m
    #scheduler.add_job(func=remove_old_log, trigger='cron', hour='23', minute='30')
    # Start process
    scheduler.start()
    print('Press Ctrl+C to exit')

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass 
        
if __name__ == '__main__':
    # Running message
    print('Started application {}'.format(datetime.now()))
    print('****************************** CRAWLER IS RUNNING ******************************')
    # Run process
    asyncio_schedule()