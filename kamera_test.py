import cv2
import numpy as np

# Konfiguracija radija
reference_radius = 42
tolerance = 0.15
min_radius = reference_radius * (1 - tolerance)
max_radius = reference_radius * (1 + tolerance)

print(f"🛡️ Radij mora biti med {min_radius:.2f}px in {max_radius:.2f}px")

# Zagon kamere
cap = cv2.VideoCapture(1)
ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Napaka pri zajemu slike.")
    exit()

# 🔹 Prikaz originalne zajete slike
cv2.imshow("Zajeta slika (original)", frame)
cv2.waitKey(0)

# Nadaljuj z zaznavo
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)

kernel = np.ones((8, 8), np.uint8)
eroded = cv2.erode(thresh, kernel, iterations=1)

contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"🔍 Najdenih kontur: {len(contours)}")

results = []

for cnt in contours:
    if cv2.contourArea(cnt) < 500:
        continue

    (x, y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = float(radius)

    if radius < min_radius or radius > max_radius:
        continue

    rect = cv2.minAreaRect(cnt)
    angle = rect[2]
    if rect[1][0] < rect[1][1]:
        angle += 90

    results.append([int(x), int(y), round(angle, 2)])

    # Nariši samo moder krog
    cv2.circle(frame, center, int(radius), (255, 0, 0), 2)

# Prikaz slike z detekcijo
cv2.imshow("Slika z detekcijo (bounding krogi)", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Izpis arrayja
print("\n📦 Shrani array s podatki o figuricah:")
for i, (x, y, angle) in enumerate(results):
    print(f"Figurica {i+1}: x={x}, y={y}, orientacija={angle}°")
