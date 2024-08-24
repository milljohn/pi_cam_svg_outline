# from cv2_enumerate_cameras import enumerate_cameras

# for camera_info in enumerate_cameras():
#     print(f'{camera_info.index}: {camera_info.name}')

import cv2
import svgwrite
import numpy as np
from io import BytesIO


def capture_image():
    try:
        # Initialize the camera
        cap = cv2.VideoCapture(0)

        # Check if the camera opened successfully
        if not cap.isOpened():
            return jsonify({"error": "Could not open camera."}), 500

        # Capture frame-by-frame
        ret, frame = cap.read()

        # When everything done, release the capture
        cap.release()

        if not ret:
            return jsonify({"error": "Failed to capture image."}), 500

        # Convert image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Convert to binary
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create an SVG drawing
        #dwg = svgwrite.Drawing(size=(frame.shape[1], frame.shape[0]))
        
        height, width = frame.shape[:2]
        dwg = svgwrite.Drawing(size=(width, height))
        
        for contour in contours:
            points = [(point[0][0], point[0][1]) for point in contour]
            dwg.add(dwg.polygon(points, fill='black'))

        print('here')
        # Save the SVG file to a BytesIO object
        svg_data = BytesIO()
        dwg.write(svg_data)
        svg_data.seek(0)

        # return send_file(svg_data, mimetype='image/svg+xml', as_attachment=True, download_name='image.svg')

    except Exception as e:
        print(e)

if __name__ == '__main__':
    capture_image()