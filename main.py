## Author: John Miller
## Date: July 1, 2024
## Description: Capture image from camera module, create outline, save as SVG
##              For use with CAD modeling
## Sources:
## https://stackoverflow.com/questions/49133484/how-to-convert-edged-image-in-opencv-to-svg-file
##
###############################################################################################################################

from flask import Flask, send_file, jsonify
import cv2
import svgwrite
import numpy as np
from io import BytesIO

app = Flask(__name__)

@app.route('/capture', methods=['GET'])
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

        # # Convert image to grayscale
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # # Convert to binary
        # _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        
        # # Find contours
        # contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # # Create an SVG drawing
        # #dwg = svgwrite.Drawing(size=(frame.shape[1], frame.shape[0]))
        
        # height, width = frame.shape[:2]
        # dwg = svgwrite.Drawing(size=(width, height))
        
        # for contour in contours:
        #     points = [(point[0][0], point[0][1]) for point in contour]
        #     print(points)
        #     dwg.add(dwg.polygon(points, fill='black'))

        # # Save the SVG file to a BytesIO object
        # svg_data = BytesIO()
        # dwg.write(svg_data)
        # svg_data.seek(0)

        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray_image, 100, 200)

        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        svg_io = BytesIO()

        ## converting image to .svg
        width, height = frame.shape[1], frame.shape[0]
        # f = open('tom.svg', 'w+') ## saved file .svg
        # f.write('<svg width="'+str(width)+'" height="'+str(height)+'" xmlns="http://www.w3.org/2000/svg">')
        svg_io.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'.encode('utf-8'))

        for poly in contours:
            new_str = '<polyline points="'
            for x, y in poly[:,0]:
                new_str = new_str + str(x)+','+str(y)+' '
            new_str = new_str + '" style="fill:none;stroke:black;stroke-width:1" />'
            svg_io.write(new_str.encode('utf-8'))
            # f.write(new_str)
            # pass

        # f.write('</svg>')
        # f.close()
        svg_io.write('</svg>'.encode('utf-8'))

        # Reset the cursor of BytesIO object to the beginning
        svg_io.seek(0)

        # Read the SVG content from BytesIO
        svg_content = svg_io.getvalue()

        print(svg_content.decode('utf-8'))

        return send_file(svg_io, mimetype='image/svg+xml', as_attachment=True, download_name='image.svg')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

