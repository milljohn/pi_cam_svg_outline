import cv2

def check_camera():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        cap.release()
        return True
    return False

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera.")
        return

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to capture image.")
        return

    cv2.imwrite("test.jpg", frame)
    print("Image captured and saved as test.jpg")

if __name__ == "__main__":
    if check_camera():
        capture_image()
    else:
        print("Camera is not available.")

