import psycopg2
import os

DATABASE_URL = "postgresql://postgres.iengedmmoblcwozdzmwf:sVc9LMRvp.bdc%24V@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
print(os.getenv('DATABASE_URL'))  # Should print the database URL from the .env file


try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Connection successful")
    conn.close()
except Exception as e:
    print("Connection failed")
    print(e)
