set -e

ruff check . --fix
ruff format .
