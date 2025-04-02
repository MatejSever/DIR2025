import numpy as np
import cv2

#zajem 10 slik
kamera = cv2.VideoCapture(2)
i = 0
while True:
    
    ret,frame = kamera.read()
    cv2.imshow("okno", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        continue

    if cv2.waitKey(1) & 0xFF == ord(' '):
        cv2.imwrite("slika" + str(i)+ ".jpg",frame)
        i += 1
        if i >= 9:
            break

kamera.release()
cv2.destroyAllWindows()


chessboard_size = (10, 7)  # Number of internal corners
square_size = 24  # Size of each square in mm

# Prepare object points (3D coordinates in real world)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

# Arrays to store object points and image points
objpoints = []
imgpoints = []

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

# Load calibration images
#imshow ni prava funkcija, ker ni iterable...preveri katera je prava
images = cv2.imread("*.jpg")

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

# Calibrate camera
ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera Matrix:\n", camera_matrix)
print("Distortion Coefficients:\n", dist_coeffs)

