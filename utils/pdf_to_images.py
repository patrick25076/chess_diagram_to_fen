from pdf2image import convert_from_path
import os

def save_pdf_images(pdf_path, output_folder,first=None, last=None):
    """
    Convert a PDF file into images and save them in the specified output folder in batches.
    
    Parameters:
    pdf_path (str): The path to the input PDF file.
    output_folder (str): The path to the folder where the images will be saved.
    batch_size (int, optional): The number of pages to convert in each batch. Default is 30.
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    # Iterate through the PDF pages in batches
    for start_page in range(first, last, 20):
        end_page = min(start_page + 20 - 1, last)
        batch_pages = convert_from_path(pdf_path, first_page=start_page, last_page=end_page ,dpi=500)
        
        # Save images to the output folder
        for idx, page in enumerate(batch_pages):
            image_path = os.path.join(output_folder, f'out{start_page + idx}.jpg')
            page.save(image_path, 'JPEG')

