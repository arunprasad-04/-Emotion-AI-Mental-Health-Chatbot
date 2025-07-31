import speech_recognition as sr
from gtts import gTTS
import time
import os
import cohere
import random
import webbrowser 
import pygame
from youtubesearchpython import VideosSearch
from emotion_storage import get_latest_emotion
from emotion_storage import get_latest_emotion, get_last_few_emotions  # Import mood tracking functions


# Initialize Cohere API
co = cohere.Client("ZTdv5Ag2yh5skEusg4kXFwhQkWQyfAoR9hSW4aHi")  # 🔹 Replace with your actual Cohere API key
fallback_responses = {
    "happy": [
        "That's amazing! What made you happy today? 😊",
        "I'm glad to hear that! Want to share the good news?",
        "Happiness is contagious! What’s making you smile today? ✨"
    ],
    "sad": [
        "I'm here for you. Do you want to talk about what’s making you sad? 💙",
        "It’s okay to feel down sometimes. What usually makes you feel better?",
        "You are not alone. Talking helps! What's on your mind?"
    ],
    "angry": [
        "I understand. Would you like to try a breathing exercise to calm down? 🧘",
        "Anger is natural, but expressing it in a healthy way helps. What happened?",
        "Sometimes a good song helps! Want me to suggest a calming track? 🎵"
    ],
    "neutral": [
        "Just a normal day, huh? How can I make it better for you? 😊",
        "Let’s talk! What’s been on your mind lately?",
        "How about some fun music to brighten your mood? 🎶"
    ]
}
#functions


def speak_response(text):
    """Convert chatbot response to speech using Google TTS and avoid permission issues."""
    filename = "response.mp3"

    # Stop any previous playback before creating a new audio file
    pygame.mixer.init()
    pygame.mixer.music.stop()

    # Ensure old file is deleted before overwriting
    if os.path.exists(filename):
        try:
            os.remove(filename)  # Delete old file
            time.sleep(1)  # Small delay to allow deletion
        except PermissionError:
            print("⚠️ File in use. Retrying in 1 second...")
            time.sleep(1)
            return  # Skip playing if still locked

    # Convert text to speech and save the file
    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    # Ensure the file is fully saved before playing
    time.sleep(1)

    # Load and play the response
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
def chatbot_reply(user_input):
    """Generates a chatbot response using Cohere API, based on detected emotion."""
    detected_emotion = get_latest_emotion()  # Fetch latest detected emotion

    # Construct a conversation-style prompt
    prompt = f"""
    You are a supportive chatbot that helps users based on their emotions.
    The user's detected emotion is: {detected_emotion}.
    Respond kindly and keep the conversation going.

    User: {user_input}
    Chatbot:
    """

    try:
        # Generate a response using Cohere
        response = co.generate(
            model="command",  # Use Cohere's chat model
            prompt=prompt,
            max_tokens=100
        )
        return response.generations[0].text.strip()

    except Exception as e:
        print("⚠️ Cohere API Error:", e)
        return random.choice(fallback_responses.get(detected_emotion, ["I'm here for you! 💙"]))
def show_mood_history():
    """Displays the last few stored emotions."""
    past_emotions = get_last_few_emotions(5)  # Get last 5 emotions
    if not past_emotions:
        return "No mood history available yet."

    history = "\n".join([f"{entry['timestamp']}: {entry['emotion']}" for entry in past_emotions])
    return f"📊 Here’s your recent mood history:\n{history}"
def relaxation_guide():
    """Provides a guided breathing exercise to help users relax."""
    breathing_steps = [
        "🫁 Take a deep breath in... (4 seconds) 🌬",
        "Hold your breath... (4 seconds) ⏳",
        "Slowly exhale... (4 seconds) 😌",
        "Pause before inhaling again... (4 seconds) 🌿"
    ]

    print("\n🌿 Let's do a simple breathing exercise to help you relax! 🌿")
    
    for step in breathing_steps:
        print(step)
        time.sleep(4)  # Wait for 4 seconds before next step
    
    print("\n🌟 How do you feel now? You can repeat this exercise anytime! 🌟")
    
def get_daily_affirmation():
    """Returns a random positive affirmation or mental wellness tip."""
    affirmations = [
        "You are strong, capable, and resilient. 💪",
        "Every day is a new beginning. Stay positive! 🌟",
        "You are enough just as you are. ❤️",
        "Your feelings are valid. It's okay to take things one step at a time. 🌿",
        "Believe in yourself. You have the power to create change! ⚡",
        "Your mental health matters. Take a deep breath and be kind to yourself. 😊",
        "Progress, not perfection. Small steps still move you forward. 🚀",
        "You are loved and appreciated more than you know. 💙"
    ]
    return random.choice(affirmations)  # Select a random affirmation




def main():
    """Interactive chatbot loop."""
    print("🤖 Mental Health Chatbot Activated! (Type 'exit' to stop)")
    daily_motivation = get_daily_affirmation()
    print(f"💡 Daily Motivation: {daily_motivation}")

    detected_emotion = get_latest_emotion()
    print(f"🤖 Detected Emotion: {detected_emotion}")
    user_choice = None
    if detected_emotion in ["angry", "sad"]:
        print("\n💡 It looks like you might be feeling a bit stressed. Would you like to try a short breathing exercise? (yes/no)")
        user_choice = input("👉 Your response: ").strip().lower()

    if user_choice == "yes":
        relaxation_guide()
    else:
        print("💙 No problem! I'm here to chat if you need me. 😊")
    while True:
        user_input = input("You: ")  # Let user type a message
        if user_input.lower() in ["give me motivation", "motivate me", "inspire me"]:
            motivation = get_daily_affirmation()
            print(f"💡 {motivation}")
            continue
         # Check if the user asks for mood history
        if user_input.lower() == "show my mood history":
            mood_history = show_mood_history()
            print(f"📊 {mood_history}")
            continue 
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye! Take care 😊")
            break  # Stop the chatbot if user types 'exit'

        bot_response = chatbot_reply(user_input)
        print(f"🗣 Chatbot: {bot_response}")
        speak_response(bot_response)  # Make chatbot speak response

if __name__ == "__main__":
    main()

