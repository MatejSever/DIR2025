import cv2
import numpy as np

# Define chessboard pattern size (internal corners)
pattern_size = (10, 7)  # Adjust based on your chessboard

# Open webcam
cap = cv2.VideoCapture(1)  # Use 0 for default webcam

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Press SPACE to capture an image, or 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    # Show live video
    cv2.imshow("Camera Feed", frame)

    # Press SPACE to capture an image
    key = cv2.waitKey(1) & 0xFF
    if key == ord(" "):  
        print("Image captured.")
        break
    elif key == ord("q"):
        cap.release()
        cv2.destroyAllWindows()
        exit()

# Convert to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detect chessboard corners
found, corners = cv2.findChessboardCorners(gray, pattern_size, None)

if found:
    # Refine corner positions for better accuracy
    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                               (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001))

    # Draw red dots on each corner
    for i, corner in enumerate(corners):
        x, y = int(corner[0][0]), int(corner[0][1])
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # Red dot
        cv2.putText(frame, f"{x},{y}", (x + 10, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Display the modified image
    cv2.imshow("Chessboard Corners", frame)
    cv2.waitKey(0)

    # Print coordinates in the terminal
    print("Corner coordinates:")
    for i, corner in enumerate(corners):
        print(f"Corner {i}: {corner[0]}")
else:
    print("No chessboard corners found.")

# Release resources
cap.release()
cv2.destroyAllWindows()