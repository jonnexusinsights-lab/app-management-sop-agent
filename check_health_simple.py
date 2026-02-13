import requests
import sys

try:
    response = requests.get("http://127.0.0.1:8000/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Health Check Passed!")
        sys.exit(0)
    else:
        print("Health Check Failed!")
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
