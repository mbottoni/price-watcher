from apscheduler.schedulers.blocking import BlockingScheduler
from asset_monitor import AssetMonitor
from config import ASSETS

DEBUG = True

def run_daily_report():
    monitor = AssetMonitor()
    monitor.generate_daily_report(ASSETS['crypto'], ASSETS['stocks'])

if __name__ == "__main__":
    if DEBUG:
        # Run immediately in debug mode
        run_daily_report()
    else:
        scheduler = BlockingScheduler()
        scheduler.add_job(run_daily_report, 'cron', hour=0, minute=0)  # Run at midnight
        scheduler.start()