from __future__ import annotations

import sys

def main() -> int:
    try:
        from dotenv import load_dotenv, find_dotenv
        load_dotenv(find_dotenv(), override=False)
    except Exception:
        pass

    from app.config import get_settings
    from app.db import create_engine_from_settings, init_db_schema, check_db_connection

    settings = get_settings()
    if not settings.database_url:
        print("ERROR: DATABASE_URL is not set.")
        return 2

    engine = create_engine_from_settings(settings)
    check_db_connection(engine)
    init_db_schema(engine)

    print("OK: DB connection verified and schema initialized.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())