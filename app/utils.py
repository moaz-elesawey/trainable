from urllib.parse import quote


def assemble_database_url(
    driver: str, user: str, password: str, host: str, port: int, database: str
) -> str:
    """Assemble Database URL"""

    conn_string = f"{quote(driver)}://{quote(user)}:{quote(password)}@{quote(host)}:{port}/{quote(database)}"

    return conn_string


POST = "POST"
GET = "GET"
PUT = "PUT"

INSERT_FLAG = 1
UPDATE_FLAG = 2
DELETE_FLAG = 3

SECONDS_TO_HOURS = 1 / (60 * 60)
