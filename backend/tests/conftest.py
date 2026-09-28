import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_healthcare.db")
os.environ.setdefault("DEV_AUTH_BYPASS", "true")

