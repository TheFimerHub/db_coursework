import os
from dotenv import load_dotenv

load_dotenv()
dbname = os.getenv("dbname")
host = os.getenv("host")
user = os.getenv('user')
password = os.getenv('password')
port = os.getenv('port')