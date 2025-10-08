# config.py

# --- NeuroSky / BlueMuse Settings ---
# BlueMuse broadcasts data on this port by default
HOST = "127.0.0.1"  # Localhost
PORT = 13854         # BlueMuse's default port

# --- Experiment Settings ---
# The user will be instructed to "think" of this card
SECRET_CARD = "Ace of Spades" 

# The other cards that will be shown
DECK = [
    "10 of Hearts",
    "Queen of Clubs",
    "King of Diamonds",
    "Jack of Hearts",
    "7 of Clubs",
    "Ace of Spades", # The secret card is in the deck
    "2 of Diamonds",
    "9 of Spades"
]

# Timing (in milliseconds)
CARD_DISPLAY_TIME = 2000  # How long each card is shown
INTER_STIMULUS_INTERVAL = 1000 # Pause between cards

# --- Lie Detection Settings ---
# NeuroSky's "Attention" is a value from 0 to 100.
# We will flag a response as "significant" if the attention
# crosses this threshold when the secret card is shown.
ATTENTION_THRESHOLD = 60 

# We will take the average attention over the card display time
# to smooth out noise.
