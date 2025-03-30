from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Attempt to load words that the user hasn't learned yet
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # If the file is not found, load the original word list
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")  # Convert data to dictionary format
else:
    to_learn = data.to_dict(orient="records")  # Convert loaded data to dictionary format

# Initialize flip timer
flip_timer = None

def next_card():
    """Displays a new random word from the list in French."""
    global current_card, flip_timer

    if flip_timer:
        window.after_cancel(flip_timer)  # Cancel any previous flip timer

    current_card = random.choice(to_learn)  # Select a random word
    canvas.itemconfig(card_title, text="French", fill="black")  # Reset text color
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)  # Show the front card image
    flip_timer = window.after(3000, func=flip_card)  # Schedule the flip after 3 seconds


def flip_card():
    """Flips the card to show the English translation."""
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)  # Show the back card image


def is_known():
    """Removes the known word from the list and updates the file."""
    to_learn.remove(current_card)  # Remove the learned word from the list
    data = pandas.DataFrame(to_learn)  # Convert back to DataFrame
    data.to_csv("data/words_to_learn.csv", index=False)  # Save the updated list
    next_card()  # Show the next word


# --------------------------- UI SETUP --------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Canvas for displaying the flashcard
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

# Corrected image paths
card_front_image = PhotoImage(file="C:/Users/Dell/OneDrive/Desktop/Python/Tkinter/Flash card/images/card_front.png")
card_back_image = PhotoImage(file="C:/Users/Dell/OneDrive/Desktop/Python/Tkinter/Flash card/images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# "Wrong" button to skip to the next word
cross_image = PhotoImage(file="C:/Users/Dell/OneDrive/Desktop/Python/Tkinter/Flash card/images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

# "Right" button to mark the word as known
check_image = PhotoImage(file="C:/Users/Dell/OneDrive/Desktop/Python/Tkinter/Flash card/images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# Start the game with the first card
next_card()

# Run the Tkinter event loop
window.mainloop()
