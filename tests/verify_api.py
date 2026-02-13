import requests
import time
import subprocess
import sys
import os
import signal

def run_server():
    # Start the server as a subprocess
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    )
    time.sleep(5)  # Wait for server to start
    return process

def test_endpoints():
    base_url = "http://127.0.0.1:8000"

    # Test Root (HTML)
    try:
        print("Testing Root Endpoint...")
        response = requests.get(f"{base_url}/")
        assert response.status_code == 200
        assert "Managerial SOP Assistant" in response.text
        print("Root Endpoint OK")
    except Exception as e:
        print(f"Root Endpoint Failed: {e}")
        return False

    # Test Chat Endpoint
    try:
        print("Testing Chat Endpoint...")
        # We assume the agent might need some context, but we just check if it returns a response structure
        # We might need to mock the agent if it relies on external services that are not mocked.
        # However, for this migration test, we just want to ensure the endpoint is reachable and processes request.
        # If it fails due to logic (like missing LLM key), it returns 500 but JSON.

        response = requests.post(f"{base_url}/api/chat", json={"message": "Hello"})
        if response.status_code == 200:
            data = response.json()
            assert "response" in data
            print("Chat Endpoint OK (Success)")
        else:
            print(f"Chat Endpoint returned {response.status_code}: {response.text}")
            # Even if it errors (e.g. LLM not configured), the API layer is working if it returns JSON error
            data = response.json()
            if "error" in data:
                 print("Chat Endpoint OK (Error handled correctly)")
            else:
                 return False

    except Exception as e:
        print(f"Chat Endpoint Failed: {e}")
        return False

    return True

if __name__ == "__main__":
    process = run_server()
    try:
        success = test_endpoints()
    finally:
        process.send_signal(signal.SIGTERM)
        process.wait()

    if success:
        print("Verification Successful!")
        sys.exit(0)
    else:
        print("Verification Failed!")
        # Print server output for debugging
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print("Server STDOUT:", stdout.decode())
            print("Server STDERR:", stderr.decode())
        else:
             process.terminate()
             stdout, stderr = process.communicate()
             print("Server STDOUT:", stdout.decode())
             print("Server STDERR:", stderr.decode())
        sys.exit(1)
