import time
import threading
from sqlmodel import Session, select
from database import engine
from models import Account
from services.mail_service import sync_inbox

def run_sync_loop():
    while True:
        try:
            with Session(engine) as session:
                statement = select(Account).where(Account.is_active == True)
                accounts = session.exec(statement).all()
                
                for account in accounts:
                    print(f"Syncing {account.email}...")
                    try:
                        sync_inbox(account)
                    except Exception as e:
                        print(f"Error syncing {account.email}: {e}")
                        
        except Exception as e:
            print(f"Sync Worker Error: {e}")
            
        time.sleep(60) # Sync every 60 seconds

def start_sync_worker():
    thread = threading.Thread(target=run_sync_loop, daemon=True)
    thread.start()
