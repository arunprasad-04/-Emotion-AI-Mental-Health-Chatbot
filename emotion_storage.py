import json
import os
from datetime import datetime
import pandas as pd

# Define the JSON file to store emotions
JSON_FILE = "emotions.json"

def save_emotion_to_json(emotion):
    """Saves detected emotion along with a timestamp to a JSON file."""
    emotion_data = {"emotion": emotion, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    # Load existing data if the file exists
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                emotions_list = json.load(file)
            except json.JSONDecodeError:
                emotions_list = []
    else:
        emotions_list = []

    # Append new emotion to the list
    emotions_list.append(emotion_data)

    # Save updated emotions list to the JSON file
    with open(JSON_FILE, "w") as file:
        json.dump(emotions_list, file, indent=4)
        
def get_emotion_history():
    """Retrieve saved emotions as a pandas DataFrame."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                emotions_list = json.load(file)
                return pd.DataFrame(emotions_list)
            except json.JSONDecodeError:
                return pd.DataFrame(columns=["emotion", "timestamp"])
    return pd.DataFrame(columns=["emotion", "timestamp"])

def get_latest_emotion():
    """Retrieves the most recent detected emotion from the JSON file."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                emotions_list = json.load(file)
                if emotions_list:
                    return emotions_list[-1]["emotion"]  # Get last recorded emotion
            except json.JSONDecodeError:
                return None
    return None# Return None if no emotions are stored

def get_last_few_emotions(n=5):
    """Retrieves the last 'n' detected emotions from the JSON file."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                emotions_list = json.load(file)
                return emotions_list[-n:]  # Get last 'n' emotions
            except json.JSONDecodeError:
                return []
    return []

# Example usage (You can remove this part in the final implementation)
if __name__ == "__main__":
    save_emotion_to_json("happy")  # Test saving an emotion
    print("Latest emotion:", get_latest_emotion())  # Test retrieving the latest emotion
    print("Recent emotions:", get_last_few_emotions(5))
