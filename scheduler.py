# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from jobs import run_daily_order_report, fulfill_pending_orders, run_inventory_sync

def start_scheduler():
    """Starts the job scheduler."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_daily_order_report, 'interval', days=1)
    scheduler.add_job(fulfill_pending_orders, 'interval', hours=1)
    scheduler.add_job(run_inventory_sync, 'interval', hours=6)
    scheduler.start()
