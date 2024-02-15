import os
import cv2
import pandas as pd
import tempfile
import argparse
from utils.chess_diagram_detector import board_detection
from utils.diagram2FEN import predict_fen
from utils.pdf_to_images import save_pdf_images
from utils.diagram2FEN import generate_lichess_link


def process_pdf(pdf_path, start_page=None, last_page=None):
    """
    Process a PDF file containing chess diagrams, extract FEN notations, and generate Lichess links.
    
    Parameters:
    pdf_path (str): Path to the PDF file.
    start_page (int, optional): Start page number. Default is None (start from the first page).
    last_page (int, optional): Last page number. Default is None (process until the last page).
    """
    # Create a temporary directory to store the images
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save PDF images
        number = 1
        df_data = []

        save_pdf_images(pdf_path, temp_dir, start_page, last_page)

        # Iterate through the images in the temporary directory
        for filename in os.listdir(temp_dir):
            if filename.endswith('.jpg'):
                image_path = os.path.join(temp_dir, filename)
                
                # Apply board detection
                image = cv2.imread(image_path)
                rois, _ = board_detection(image)

                for _, roi in enumerate(rois):
                    fen = predict_fen(roi)
                    lichess_link = generate_lichess_link(fen)
                    df_data.append([number, fen, lichess_link])
                    number += 1

        # Create a DataFrame
        df = pd.DataFrame(df_data, columns=['Diagram Number', 'FEN Notation', 'Lichess Link'])
        
        # Save the DataFrame to CSV
        df.to_csv('output_data.csv', index=False)


def main():
    
    if os.path.exists("output_data.csv"):
        os.remove("output_data.csv")

    parser = argparse.ArgumentParser(description="Process a PDF containing chess diagrams.")
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    parser.add_argument("--start_page", type=int, help="Start page number.")
    parser.add_argument("--last_page", type=int, help="Last page number.")
    args = parser.parse_args()

    if args.pdf_path:
        if args.start_page is None and args.last_page is None:
            process_pdf(args.pdf_path)
        else:
            process_pdf(args.pdf_path, args.start_page, args.last_page)
    else:
        print("Please provide a PDF file path")

if __name__ == '__main__':
    main()
