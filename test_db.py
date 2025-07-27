#!/usr/bin/env python3
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("Testing Supabase connection...")
print(f"DATABASE_URL: {DATABASE_URL[:50]}...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connection successful!")
    
    # Test a simple query
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"✅ PostgreSQL version: {version[0]}")
    
    # Test table creation
    cur.execute('''
        CREATE TABLE IF NOT EXISTS test_problems (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    print("✅ Table creation successful!")
    
    cur.close()
    conn.close()
    print("✅ All tests passed!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting steps:")
    print("1. Check if your Supabase project is active")
    print("2. Verify the password is correct")
    print("3. Check if your IP is allowed (Supabase should allow all by default)")
    print("4. Try resetting your database password in Supabase dashboard")
