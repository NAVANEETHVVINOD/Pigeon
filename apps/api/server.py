import uvicorn
import os
import sys

# Ensure current directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Explicit imports to help PyInstaller find them (though hidden-import is usually better)
from main import app
import routers.auth
import routers.mail
import routers.localdrop
import routers.media
import services.localdrop_service
import services.crypto_service
import services.mail_service
import models
import database

if __name__ == "__main__":
    # Use the app object directly to avoid import string issues in frozen environment
    uvicorn.run(app, host="127.0.0.1", port=8000)
