import numpy as np 
import cv2


def sort_rois_by_position(rois, corners_list):
    """Sort ROIs based on their position on the chessboard
    
    Parameters:
    rois (list) -- List of cropped regions of interest (ROIs)
    corners_list (list) -- List of lists containing the corners of each detected square

    Returns:
    sorted_rois (list) -- List of ROIs sorted based on their position
    sorted_corners_list (list) -- List of lists containing the sorted corners of each detected square
    """    
    # Get the top-left corner coordinates for each ROI
    top_left_corners = [(min(corner[0] for corner in corners), min(corner[1] for corner in corners)) 
                        for corners in corners_list]
    
    # Sort ROIs based on the top-left corner coordinates
    sorted_indices = np.argsort([corner[1] * 1000 + corner[0] for corner in top_left_corners])
    sorted_rois = [rois[i] for i in sorted_indices]
    sorted_corners_list = [corners_list[i] for i in sorted_indices]
    
    return sorted_rois, sorted_corners_list


def board_detection(chessboard):
    """Applying Computer Vision techniques to detect the 4 corners of the table
    
    Parameters:
    chessboard (image) -- The image of the chessboard

    Returns:
    rois (list) -- List of cropped regions of interest (ROIs)
    corners_list (list) -- List of lists containing the corners of each detected square
    """    
    gray_image = cv2.cvtColor(chessboard, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, image_result = cv2.threshold(
        blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )
    edges = cv2.Canny(image_result, 100, 200)
    kernel = np.ones((3, 3), np.uint8)

    # Perform dilation
    dilated_image = cv2.dilate(edges, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rois = []
    corners_list = []
    
    # Iterate through all contours (squares) and detect corners
    for contour in contours:
        # Skip contours with small area
        if cv2.contourArea(contour) < 45000:
            continue
        
        # Calculate the angles of the lines connecting the corners to the center
        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        hull = cv2.convexHull(approx)
        corners = [tuple(hull[i][0]) for i in range(4)]
        corners_list.append(corners)

        # Crop ROI
        x, y, w, h = cv2.boundingRect(contour)
        roi = chessboard[y:y+h, x:x+w]
        rois.append(roi)
    
    rois, corners_list = sort_rois_by_position(rois, corners_list)

    return rois, corners_list 

def show_all_corners(image, corners_list, output_path):
    """Drawing all the corners for testing 
    
    Parameters:
    image (image) -- The original image
    corners_list (list) -- List of lists containing the corners of each detected square
    output_path (str) -- Path to save the output image

    Returns:
    Showing the image with red highlighted corners of all chessboard squares and saving it as a JPG file
    """
    for corners in corners_list:
        for corner in corners:
            cv2.circle(image, (corner[0], corner[1]), 5, (0, 0, 255), -1)

    cv2.imshow("Image with corners", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save the image as a JPG file
    cv2.imwrite(output_path, image)

def show_all_rois(rois):
    """Display all the ROIs
    
    Parameters:
    rois (list) -- List of cropped regions of interest (ROIs)
    """
    for i, roi in enumerate(rois):
        cv2.imshow(f"ROI {i+1}", roi)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    
   
