import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
count = 0

while True:
    success, reference_image = cap.read()
    count += 1
    if count == 10:
        break
reference_image = cv.flip(reference_image, 1)
cv.imshow("First", reference_image )

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None,
                                               scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def onChange(x):
    print(x)


cv.namedWindow("Video")
cv.createTrackbar("Val Min", "Video", 0, 255, onChange)
cv.createTrackbar("Val Max", "Video", 255, 255, onChange)

cv.createTrackbar("Hue Min", "Video", 0, 179, onChange)
cv.createTrackbar("Hue Max", "Video", 179, 179, onChange)
cv.createTrackbar("Sat Min", "Video", 0, 255, onChange)
cv.createTrackbar("Sat Max", "Video", 255, 255, onChange)

while True:
    success, frame = cap.read()
    frame = cv.flip(frame, 1)
    hsvframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    hue_min = cv.getTrackbarPos("Hue Min", "Video")
    hue_max = cv.getTrackbarPos("Hue Max", "Video")
    sat_min = cv.getTrackbarPos("Sat Min", "Video")
    sat_max = cv.getTrackbarPos("Sat Max", "Video")
    val_min = cv.getTrackbarPos("Val Min", "Video")
    val_max = cv.getTrackbarPos("Val Max", "Video")

    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])

    mask = cv.inRange(hsvframe, lower, upper)
    mask_inv = cv.bitwise_not(mask)

    blanket_ki_jagah_khali = cv.bitwise_and(frame,frame, mask=mask_inv)
    blanket_area = cv.bitwise_and(reference_image,reference_image,mask=mask)
    blanket_ki_jagah_reference = cv.bitwise_or(blanket_ki_jagah_khali,blanket_area)

    # imgStack = stackImages(0.5, [reference_image, frame, hsvframe, mask, mask_inv, blanket_ki_jagah_khali,blanket_area, blanket_ki_jagah_reference])
    imgStack = stackImages(0.5, [frame, blanket_ki_jagah_reference])

    cv.imshow("Video", imgStack)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
