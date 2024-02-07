import json
import tkinter
from gtts import gTTS
import pygame

win = tkinter.Tk()
win.geometry("250x250")
win.title("House Price Prediction")

l1 = tkinter.Label(win, text="Location")
l1.grid(row=0,column=0, padx=10, pady=5)
e1 = tkinter.Entry(win)
e1.grid(row = 0,column=1, padx=10, pady=5)

l2 = tkinter.Label(win, text="Sq. Ft.")
l2.grid(row=1,column=0, padx=10, pady=5)
e2 = tkinter.Entry(win)
e2.grid(row = 1,column=1, padx=10, pady=5)

l3 = tkinter.Label(win, text="Bath")
l3.grid(row=2,column=0, padx=10, pady=5)
e3 = tkinter.Entry(win)
e3.grid(row = 2,column=1, padx=10, pady=5)

l4 = tkinter.Label(win, text="BHK")
l4.grid(row=3,column=0, padx=10, pady=5)
e4 = tkinter.Entry(win)
e4.grid(row = 3,column=1, padx=10, pady=5)

def predict():
    import pickle
    import numpy as np

    # Load the model from the pickle file
    with open('bangalore_home_price_model.pickle', 'rb') as file:
        loaded_model = pickle.load(file)

    global  __data_columns
    global __locations

    with open(".\columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk


    # Assuming 'predict_price' is the function you defined earlier
    def predict_price(location, sqft, bath, bhk, model):
        try:
            loc_idx = __data_columns.index(location.lower())
        except:
            loc_idx = -1
        x = np.zeros(len(__data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk
        if loc_idx >= 0:
            x[loc_idx] = 1
        return model.predict([x])[0]

    # Custom input values
    custom_location = e1.get()
    custom_sqft = float(e2.get())
    custom_bath = float(e3.get())
    custom_bhk = float(e4.get())

    # Predict the price using the loaded model and custom values
    predicted_price = int(predict_price(custom_location, custom_sqft, custom_bath, custom_bhk, loaded_model))

    # Display the predicted price
   # print(f"Predicted Price: {predicted_price}")
    ans = tkinter.Label(win,text=f"Predicted Price: {predicted_price} Cr")
    ans.grid(row=5,column=1, padx=10, pady=10)

    # Convert predicted price to speech
    text_to_speech = f"Predicted Price: {predicted_price} crore"
    tts = gTTS(text=text_to_speech, lang='en')
    tts.save("prediction.mp3")

    # Play audio using pygame
    pygame.mixer.init()
    pygame.mixer.music.load("prediction.mp3")
    pygame.mixer.music.play()

button = tkinter.Button(win, text="Predict", command=predict)
button.grid(row=4, column=1, pady=10)

win.mainloop()