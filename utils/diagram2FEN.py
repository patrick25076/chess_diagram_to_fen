import re
import cv2
import glob
import random as rd
import warnings
import numpy as np
from tensorflow import keras
import os

# Define piece symbols for chess FEN notation
piece_symbols = 'prbnkqPRBNKQ'

def image_to_squares(img, heights, widths):
    """
    Convert an image into a list of smaller square images representing individual chessboard squares.
    
    Parameters:
    img (numpy.ndarray): The input image.
    heights (int): The height of the input image.
    widths (int): The width of the input image.
    
    Returns:
    numpy.ndarray: An array containing smaller square images representing individual chessboard squares.
    """
    squares = []
    for i in range(0, 8):
        for j in range(0, 8):
            squares.append(img[i * heights // 8:i * heights // 8 + heights // 8, j * widths // 8:j * widths // 8 + widths // 8])
    return np.array(squares)


def preprocess_image(img):
    """
    Preprocess an image for input into a chessboard detection model.
    
    Parameters:
    img (numpy.ndarray): The input image.
    
    Returns:
    numpy.ndarray: The preprocessed image.
    """
    height = 400
    width = 400

    # Convert image to grayscale if it's not already
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    gray_image = cv2.resize(img, (width, height))
    # Normalize the image
    gray_image = (gray_image - np.min(gray_image)) / (np.max(gray_image) - np.min(gray_image))

    squares = image_to_squares(gray_image, height, width)
    
    return squares


def fen_from_onehot(one_hot):
    """
    Convert one-hot encoded predictions into FEN (Forsyth–Edwards Notation) format.
    
    Parameters:
    one_hot (numpy.ndarray): The one-hot encoded predictions.
    
    Returns:
    str: The FEN notation string.
    """
    output = ''
    for j in range(8):
        for i in range(8):
            if(one_hot[j][i] == 12):
                output += ' '  # Empty square
            else:
                output += piece_symbols[one_hot[j][i]]  # Piece symbol
        if(j != 7):
            output += '-'

    for i in range(8, 0, -1):
        output = output.replace(' ' * i, str(i))

    return output

def generate_lichess_link(fen):
    """
    Generate a Lichess link for a given FEN (Forsyth–Edwards Notation).
    
    Parameters:
    fen (str): The FEN notation string.
    
    Returns:
    str: The Lichess link.
    """
    base_link = "https://lichess.org/editor/"
    lichess_link = base_link + fen.replace("-", "/")
    return lichess_link

# Load the trained chessboard detection model
model_path = os.path.join('assets', 'chess_modelv15_classic_dense_5ep.h5')

model = keras.models.load_model(model_path)

def predict_fen(image):   
    """
    Predict the FEN (Forsyth–Edwards Notation) of a chessboard given an input image.
    
    Parameters:
    image (numpy.ndarray): The input image of a chessboard.
    
    Returns:
    str: The predicted FEN notation of the chessboard.
    """
    pred = model.predict(preprocess_image(image)).argmax(axis=1).reshape(-1, 8, 8)
    fen = fen_from_onehot(pred[0])
    return fen

