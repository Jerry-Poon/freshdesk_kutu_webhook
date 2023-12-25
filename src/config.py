import os
from dotenv import load_dotenv
from dataclasses import dataclass
from pathlib import Path

current_path = Path('__file__')
dotenv_path = current_path.parent.parent.resolve() / '.env'
load_dotenv(dotenv_path=dotenv_path)

@dataclass
class Settings:
    db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_password: str = os.getenv('DB_PASSWORD')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')
    table_name: str = os.getenv('TABLE_NAME')

settings = Settings()