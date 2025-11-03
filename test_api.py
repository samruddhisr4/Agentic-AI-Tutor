import requests
import time

def test_api():
    """Test the backend API"""
    # Wait a moment for the server to start
    time.sleep(5)
    
    try:
        # Test the root endpoint
        print("Testing root endpoint...")
        response = requests.get("http://localhost:8000/")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test the generate_response endpoint
        print("\nTesting generate_response endpoint...")
        payload = {
            "query": "What is artificial intelligence?",
            "style": "in_depth"
        }
        response = requests.post(
            "http://localhost:8000/generate_response",
            json=payload
        )
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Success! Response received:")
            print(result["response"][:200] + "..." if len(result["response"]) > 200 else result["response"])
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    test_api()