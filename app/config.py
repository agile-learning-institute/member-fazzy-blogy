# backend/config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.mrhazjgjbxnssyvklcwr:YOUR-PASSWORD@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
