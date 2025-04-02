import cv2
import numpy as np

# Parametri za filtriranje radija (glede na tvoje podatke)
reference_radius = 42
tolerance = 0.15
min_radius = reference_radius * (1 - tolerance)
max_radius = reference_radius * (1 + tolerance)

print(f"🛡️ Sprejemljiv radij: {min_radius:.2f} px – {max_radius:.2f} px")

# Zajemi sliko iz kamere
cap = cv2.VideoCapture(1)
ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Napaka pri zajemu slike.")
    exit()
else:
    print("✅ Slika uspešno zajeta.")

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

# Morfološko čiščenje
kernel = np.ones((8, 8), np.uint8)
eroded = cv2.erode(thresh, kernel, iterations=1)

contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"🔍 Najdenih kontur: {len(contours)}")

valid_count = 0

for cnt in contours:
    if cv2.contourArea(cnt) < 500:
        continue

    # Najdi minimalni obdajajoči krog (za filtriranje po velikosti)
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = float(radius)

    if radius < min_radius or radius > max_radius:
        print(f"⛔️ Figurica izločena (radij: {radius:.2f} px)")
        continue

    valid_count += 1

    # 📍 Lokacija in 🔄 orientacija
    rect = cv2.minAreaRect(cnt)  # (center, (width, height), angle)
    angle = rect[2]

    # Korekcija kota (da je od 0–180 stopinj)
    if rect[1][0] < rect[1][1]:
        angle = 90 + angle

    print(f"✅ Figurica {valid_count}: center=({int(x)}, {int(y)}), orientacija={angle:.2f}°")

    # Nariši krog
    cv2.circle(frame, center, int(radius), (255, 0, 0), 2)
    cv2.circle(frame, center, 4, (255, 255, 0), -1)

    # Dopiši orientacijo na sliko
    cv2.putText(frame, f"{angle:.1f} deg", (center[0] + 10, center[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

# Shrani in prikaži rezultat
cv2.imwrite("C:/users/acisa/Desktop/dir_2025/oznake.jpg", frame)
print("💾 Slika shranjena kot 'oznake.jpg'.")

cv2.imshow("Detekcija z lokacijo in orientacijo", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
