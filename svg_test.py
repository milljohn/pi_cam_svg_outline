import cv2
import svgwrite
import numpy as np
from io import BytesIO

# Initialize the camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print('camera busy')

# Capture frame-by-frame
ret, frame = cap.read()

# When everything done, release the capture
cap.release()

if not ret:
    print('error')

# Convert image to grayscale
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