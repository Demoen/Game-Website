from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", 'yc875b67cn6c346b6vb6c53b6cn6xnmnx3nm6xn5nbbn3bb3baslfdasd')
app.config['DEBUG'] = True
from game import routes