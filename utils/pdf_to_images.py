from pdf2image import convert_from_path
import os

def save_pdf_images(pdf_path, output_folder, first=None, last=None):
    """
    Convert a PDF file into images and save them in the specified output folder.
    
    Parameters:
    pdf_path (str): The path to the input PDF file.
    output_folder (str): The path to the folder where the images will be saved.
    first (int, optional): The first page number to convert (inclusive). Default is None (convert from the first page).
    last (int, optional): The last page number to convert (inclusive). Default is None (convert until the last page).
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to images
    pages = convert_from_path(pdf_path, first_page=first, last_page=last , dpi=500)

    # Save images to the output folder
    for count, page in enumerate(pages):
        image_path = os.path.join(output_folder, f'out{count}.jpg')
        page.save(image_path, 'JPEG')
