from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import inspect

from app.database.database import Base, engine
from app.database import models


def main():
    print("Connecting to PostgreSQL...")

    # Create all database tables
    Base.metadata.create_all(bind=engine)

    print("PostgreSQL connection successful.")
    print("Checking database tables...")

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print()
    print("Tables found:")

    for table in tables:
        print("-", table)

    required_tables = [
        "users",
        "conversations",
        "messages",
        "support_tickets",
        "feedback",
        "audit_logs",
    ]

    print()

    missing_tables = [
        table
        for table in required_tables
        if table not in tables
    ]

    if missing_tables:
        print("Missing tables:")
        for table in missing_tables:
            print("-", table)

        raise RuntimeError(
            "Some required PostgreSQL tables are missing."
        )

    print("All required PostgreSQL tables exist.")


if __name__ == "__main__":
    main()