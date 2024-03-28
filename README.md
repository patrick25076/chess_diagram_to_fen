# Chess Diagram Detector! 
![BOARD](https://github.com/patrick25076/chess_diagram_to_fen/assets/113384811/a961608c-3932-483b-ae26-e936e4b90308)


This repository contains a Python program for detecting and analyzing chess diagrams from PDF files. The program utilizes advanced computer vision techniques to accurately identify chess diagrams and then applies a deep learning algorithm to recognize the chess pieces and generate the FEN notation along with a Lichess link for each diagram.

## Process Overview

1. **PDF Processing**: The program processes the PDF file and converts all images into JPG format for further analysis.
2. **Chessboard Detection**: Utilizing advanced computer vision algorithms, the program accurately locates chessboards within images, ensuring precise identification of chess diagrams.
3. **Piece Recognition and FEN Generation**: Employing deep learning models, the program recognizes individual chess pieces with an exceptional accuracy rate of 99.93%. It then computes the FEN notation and provides Lichess links for each diagram.

## Instructions

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/patrick25076/chess_diagram_to_fen.git
cd chess_diagram_to_fen
```

### Step 2: Install Dependencies

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

If you're using conda, install Poppler for PDF processing (this is needed for processing the PDF !) :

```bash
conda install -c conda-forge poppler
```

### Step 3: Run the Program

Run the program with the following command, replacing [PDF_PATH] with the path to the PDF file containing chess diagrams. Optionally, specify the start and last page numbers for processing.

```bash

python main.py [PDF_PATH] --start_page [START_PAGE] --last_page [LAST_PAGE]
```

## Open for Collaboration and Improvement!

Feel free to contribute and enhance this project together! 🚀🔧


