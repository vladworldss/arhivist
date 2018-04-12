# coding: utf-8
import os

# Google API keys
HOME_DIR = os.environ["HOME"]
API_DIR = os.path.join(HOME_DIR, ".google")
API_KEY_FILE_NAME = "api_key"
API_KEY_PATH = os.path.join(API_DIR, API_KEY_FILE_NAME)

if not os.path.exists(API_KEY_PATH):
    raise IOError("Api key doesn't exist")

API_KEY = "".join(line for line in open(API_KEY_PATH)).strip()
