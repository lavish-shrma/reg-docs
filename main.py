import argparse
import sys
import os

# Ensure directories are in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.ingest import ingest
from retrieval.chat import start_chat

def main():
    parser = argparse.ArgumentParser(description="RAG Application CLI")
    parser.add_argument(
        "--mode", 
        choices=["ingest", "chat"], 
        required=True, 
        help="Mode to run the application in: 'ingest' to process documents, 'chat' to start the Q&A loop."
    )
    
    args = parser.parse_args()
    
    if args.mode == "ingest":
        ingest()
    elif args.mode == "chat":
        start_chat()

if __name__ == "__main__":
    main()
