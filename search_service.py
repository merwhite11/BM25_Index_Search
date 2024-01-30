import requests
from bm25_worker import BM25Query
import argparse

# URL of the Flask server
url = "http://127.0.0.1:5000/search"

def main():
    #Parse the args from the command line to get phrase and index
    parser = argparse.ArgumentParser(description='Get search phrase and index')
    parser.add_argument('--phrase', type=str, help='Your search query', required=True)
    parser.add_argument('--index', type=str, help='Scrape index to search', required=True)
    args = parser.parse_args()
    payload = {"phrase": args.phrase, "index": args.index}

    # Send the POST request to the Flask server
    response = requests.post(url, json=payload)
    # Check the response
    if response.status_code == 200:
        print("POST request successful!")
        print("Response content:", response.json())
    else:
        print(f"POST request failed with status code {response.status_code}")
        print("Error content:", response.text)

if __name__ == "__main__":
    main()