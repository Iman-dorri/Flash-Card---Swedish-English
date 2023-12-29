from tkinter import *
import pandas
import random
timer = None
random_word = ""
translation = ""
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashy")
window.config(width=850, height=576, padx=50, pady=50, bg=BACKGROUND_COLOR)

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/swedish_words.csv")

data_to_dict = {row.Swedish: row.English for (index, row) in data.iterrows()}
list_of_sv_words = list(data_to_dict.keys())
list_of_en_words = list(data_to_dict.values())
number_of_words_left = len(list_of_sv_words)


def remove_known_words():
    try:
        list_of_sv_words.remove(random_word)
        list_of_en_words.remove(translation)
        new_number_of_words_left = len(list_of_sv_words)
        canvas.itemconfig(number_of_words, text=f"Number of words left to learn: {new_number_of_words_left}")
    except ValueError:
        pass


def right_button_pressed():
    remove_known_words()
    choose_random_word()
    new_data_to_dict = {
        "Swedish": [sv_word for sv_word in list_of_sv_words],
        "English": [en_word for en_word in list_of_en_words],
    }
    new_data = pandas.DataFrame(new_data_to_dict)
    new_data.to_csv("data/words_to_learn.csv", index=False)


def choose_random_word():
    canvas.itemconfig(canvas_image, image=card_front)
    global timer
    global translation
    global random_word
    random_word = random.choice(list_of_sv_words)
    canvas.itemconfig(title, text="Swedish", fill="black")
    canvas.itemconfig(word, text=f"{random_word}", fill="black")
    for (key, value) in data_to_dict.items():
        if random_word == key:
            translation = value
    timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=f"{translation}", fill="white")


# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
title = canvas.create_text(400, 150, text="Swedish-English Flash Cards", fill="black", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 300, text="Press Start", fill="black", font=("Arial", 60, "bold"))
number_of_words = canvas.create_text(400, 450, text=f"Number of words left to learn: {number_of_words_left}",
                                     font=("Arial", 15, "italic"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=right_button_pressed)
right_button.grid(column=1, row=1)
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=choose_random_word)
wrong_button.grid(column=0, row=1)


window.mainloop()
if __name__ == '__main__':
    window.mainloop()

