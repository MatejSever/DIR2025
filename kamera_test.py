import cv2
import numpy as np

cap = cv2.VideoCapture(1)  # ali 0, če imaš integrirano kamero

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1) Pretvori v sivine in binarno sliko
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV)
    kernel1 = np.ones((5,5),np.uint8)
    thresh = cv2.erode(thresh,kernel1,iterations = 1)

    # 2) Morfološko razširimo (dilate) za ozadje
    kernel = np.ones((3,3), np.uint8)
    sure_bg = cv2.dilate(thresh, kernel, iterations=3)

    # 3) Distance transform za iskanje “jedra” objektov
    dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    # Zmanjšaj ali zvišaj 0.5, če se zate stvari ne ločijo
    _, sure_fg = cv2.threshold(dist_transform, 0.5*dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 4) Ustvari "markerje" z connectedComponents
    ret2, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1  # da bo ozadje = 1
    markers[unknown == 255] = 0

    # 5) Watershed
    markers = cv2.watershed(frame, markers)

    # 6) Izris rezultatov
    output = frame.copy()

    # Vsak objekt ima svojo marker vrednost (2..ret2+1)
    for marker_val in range(2, ret2+2):
        # Naredimo masko za ta marker
        mask = np.where(markers == marker_val, 255, 0).astype('uint8')

        # Poiščemo konture samo tega markerja
        ccontours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in ccontours:
            if cv2.contourArea(cnt) > 300:
                rect = cv2.minAreaRect(cnt)
                center = tuple(map(int, rect[0]))
                box = cv2.boxPoints(rect).astype(int)
                print(center)
                #naredi da poslje sliko

                # Moder outline
                cv2.drawContours(output, [box], 0, (255, 0, 0), 2)
                # Turkizna pika v sredini
                cv2.circle(output, center, 4, (255, 255, 0), -1)

    cv2.imshow("Watershed", output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
