import os

from app import create_app
from app.config import get_config

config = get_config(os.getenv("ENVIRONMENT", "local"))
app = create_app(config=config)


def main():
    app.run(host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()
