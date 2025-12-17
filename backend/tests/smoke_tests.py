import httpx
import time
import os
import sys

# Get URL from env or default to localhost
url = os.getenv("APP_URL", "http://localhost:8000")

print(f"Starting smoke tests against {url}...")

max_retries = 10
for i in range(max_retries):
    try:
        response = httpx.get(f"{url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {response.json()}")
            sys.exit(0)
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
            
    except httpx.RequestError as e:
        print(f"⚠️ Connection attempt {i+1} failed: {e}. Retrying in 5s...")
        time.sleep(5)

print("❌ Smoke tests failed after multiple retries.")
sys.exit(1)
