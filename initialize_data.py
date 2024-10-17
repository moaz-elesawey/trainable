import os

from app import create_app
from app.config import get_config
from app.init_db import init_db_data

print("Initializing Database...")

config = get_config(os.getenv("ENVIRONMENT", "local"))
app = create_app(config=config)

init_db_data(app=app)

print("Database initialized...")
