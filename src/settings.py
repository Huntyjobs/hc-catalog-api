import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    ROOT_PATH = "" if os.getenv("LOCAL") == "True" else "/hc-catalog"

