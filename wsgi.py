import os

from app import create_app
from app.config import get_config
from app.init_db import init_db_data

config = get_config(os.getenv("ENVIRONMENT", "local"))
app = create_app(config=config)

if __name__ == "__main__":
    init_db_data(app=app)
    app.run(host="0.0.0.0", port=80)
