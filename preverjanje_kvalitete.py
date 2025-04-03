import cv2
import numpy as np

# Parametri radija
reference_radius = 42
tolerance = 0.2
min_radius = reference_radius * (1 - tolerance)
max_radius = reference_radius * (1 + tolerance)

# Zagon kamere
cap = cv2.VideoCapture(1)
ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Napaka pri zajemu slike.")
    exit()

# Pripravi za obdelavo
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)

# Erozija za odpravo šuma
kernel = np.ones((8, 8), np.uint8)
eroded = cv2.erode(thresh, kernel, iterations=1)

# Najdi konture
contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Kopija slike za risanje
output_img = cv2.cvtColor(eroded, cv2.COLOR_GRAY2BGR)

count = 0

for cnt in contours:
    if cv2.contourArea(cnt) < 500:
        continue

    (x, y), radius = cv2.minEnclosingCircle(cnt)

    if min_radius <= radius <= max_radius:
        count += 1
        center = (int(x), int(y))
        cv2.circle(output_img, center, int(radius), (255, 0, 0), 2)

# 🔢 Izpis v terminal
print(f"\n🔍 Zaznanih izdelkov: {count}")

# 🖼️ Prikaz slike z bounding krogi (na threshold podlagi)
cv2.imshow("Threshold + Bounding Spheres", output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

