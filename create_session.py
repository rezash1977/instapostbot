import os
from instagrapi import Client
from dotenv import load_dotenv

# بارگذاری اطلاعات از .env
load_dotenv()
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

cl = Client()
cl.login(USERNAME, PASSWORD)
cl.dump_settings("session.json")
print("Session saved!") 