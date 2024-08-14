import random

messages = {
  "correct" : [
    "You got it right!",
    "Wow, correct answer!",
    "Bingo! You nailed it!",
    "Great guess! That's it!",
    "Spot on! Well done!",
    "Yay! You figured it out!",
    "Awesome job! That's correct!",
    "Perfect guess! You win!",
    "You're right on the money!",
    "Bullseye! Great guessing!",
    "Ding ding ding! We have a winner!",
    "Excellent! You solved it!",
    "Amazing guess! You're right!",
    "Hooray! You got the answer!",
    "Brilliant! You guessed correctly!",
    "Fantastic job! That's the one!",
    "You cracked the code! Well done!",
    "Super guess! You're correct!",
    "Winner winner! You got it!",
    "Ta-da! You solved the puzzle!"
  ],
  "welcome" : [
    "Let's play a fun guessing game!",
    "Can you guess what I'm thinking of?",
    "Join our guessing game - it's super fun!",
    "Who wants to play a cool guessing game?",
    "Ready for a game of guesses?",
    "Guess with us and have a blast!",
    "Time for a fun guessing challenge!",
    "Want to test your guessing skills?",
    "Come play our awesome guessing game!",
    "Guess what? We're playing a game!",
    "Join in - can you guess right?",
    "Let's see how good you are at guessing!",
    "Guessing game time - are you ready?",
    "Play along and make your best guess!",
    "Who's up for a quick guessing game?",
    "Try our fun game of guesses!",
    "Guess with friends - it's game time!",
    "Think you're good at guessing? Prove it!",
    "Jump in and start guessing with us!",
    "Let's have fun guessing together!"
  ],
  "medium_questions" : [
    "Please ask only yes or no questions.",
    "Can you ask questions for yes/no answers?",
    "I'd like yes or no questions only, please.",
    "Kindly stick to yes/no questions only.",
    "Could you ask just yes or no questions?",
    "Please limit questions to yes/no responses.",
    "I prefer questions with yes/no answers only.",
    "Can we do only yes or no questions, please?",
    "Ask questions that need yes/no answers only.",
    "Please keep it to yes or no questions.",
    "I'd appreciate only yes/no type questions.",
    "Let's stick to yes or no questions, okay?",
    "Can you ask questions for simple yes/no replies?",
    "Please ask questions requiring yes/no answers.",
    "How about only yes or no questions for now?",
    "I'd like to answer with just yes or no, please.",
    "Could we limit it to yes/no questions only?",
    "Please ask questions needing only yes/no responses.",
    "Let's try only yes or no questions, shall we?",
    "Can you ask questions for yes/no answers only, please?"
  ]
}



import streamlit as st
import csv, os
import pandas as pd

@st.cache_data
def load_words():
    return pd.read_csv('resource/words.csv')

def get_random_answer_word():
    df = load_words()
    random_row = df.sample(n=1).iloc[0]
    return random_row['word'], random_row['category']

def get_random_welcome_message():
    return random.choice(messages["welcome"]) + random.choice(messages["medium_questions"])

def get_random_correct_message():
    return random.choice(messages["correct"])