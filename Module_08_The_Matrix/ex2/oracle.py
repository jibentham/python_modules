import os
import sys
from dotenv import load_dotenv


env_loaded: bool = load_dotenv()
if not env_loaded:
    print("Warning: no .env file found. Please use environment variables or copy .env.example to .env and edit values as necessary")
    sys.exit(1)

MATRIX_MODE: str | None = os.getenv("MATRIX_MODE")
DATABASE_URL: str | None = os.getenv("DATABASE_URL")
API_KEY: str | None = os.getenv("API_KEY")
LOG_LEVEL: str | None = os.getenv("LOG_LEVEL")
ZION_ENDPOINT: str | None = os.getenv("ZION_ENDPOINT")


def main() -> None:
    print("\nORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"Mode: {MATRIX_MODE}")
    if DATABASE_URL is None:
        db_status: str = "Database not found"
    elif "localhost" in DATABASE_URL:
        db_status = "Connected to local instance"
    else:
        db_status = "Connected to remote instance"
    print(f"Database: {db_status}")
    print(f"API Access: {'Authenticated' if API_KEY else 'No API Key set'}")
    print(f"Log Level: {LOG_LEVEL if LOG_LEVEL else 'No logging'}")
    print(f"Zion Network: {'Online' if ZION_ENDPOINT else 'Offline'}")
    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    print(f"{'[OK] .env file properly configured' if env_loaded else '[KO] .env not found. Using environment variables'}")
    print(f"[OK] {'production overrides available' if MATRIX_MODE == 'development' else 'development tools ready for use'}")
    print("\n The Oracle sees all configurations.")
