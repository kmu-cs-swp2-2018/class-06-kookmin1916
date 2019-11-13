#!/usr/bin/env python

import cv2, time
import numpy as np
import math

cap = cv2.VideoCapture('2.avi')

value_threshold = 60

image_width = 640
scan_width, scan_height = 200, 20
lmid, rmid = scan_width, image_width - scan_width
#area_width, area_height = 20, 10
area_width, area_height = 3, 3
# pixel of both side is 3 pixels
#roi_vertical_pos = 430
roi_vertical_pos = 290
row_begin = (scan_height - area_height) // 2
row_end = row_begin + area_height
pixel_cnt_threshold = 0.8 * area_width * area_height

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if cv2.waitKey(1) & 0xFF == 27:
        break

    roi = frame[roi_vertical_pos:roi_vertical_pos + scan_height, :]
    """frame = cv2.rectangle(frame, (0, roi_vertical_pos),
        (image_width - 1, roi_vertical_pos + scan_height),
        (255, 0, 0), 1)"""
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # average
    left_hsv_sum = 0
    for i in range(roi_vertical_pos, roi_vertical_pos + scan_height):
        for j in range(len(frame[0]) // 3):
            left_hsv_sum += frame[i][j][2]
    left_value_threshold = min([(left_hsv_sum // (scan_height * len(frame[0]) // 3)) * 1.5, 255])
    print("left: ", left_value_threshold)
    
    right_hsv_sum = 0
    for i in range(roi_vertical_pos, roi_vertical_pos + scan_height):
        for j in range(len(frame[0]) // 3 * 2, len(frame[0])):
            right_hsv_sum += frame[i][j][2]
    right_value_threshold = min([(right_hsv_sum // (scan_height * len(frame[0]) // 3)) * 1.5, 255])
    print("right: ", right_value_threshold)
    #

    lbound = np.array([0, 0, value_threshold], dtype=np.uint8)
    #ubound = np.array([131, 255, 255], dtype=np.uint8)
    ubound = np.array([255, 255, 255], dtype=np.uint8)

    left_lbound = np.array([0, 0, left_value_threshold], dtype=np.uint8)
    right_lbound = np.array([0, 0, right_value_threshold], dtype=np.uint8)

    left_bin = cv2.inRange(hsv, left_lbound, ubound)
    left_bin = cv2.GaussianBlur(left_bin, (3, 3), 0)
    left_bin = cv2.GaussianBlur(left_bin, (3, 3), 0)
    right_bin = cv2.inRange(hsv, right_lbound, ubound)
    right_bin = cv2.GaussianBlur(right_bin, (3, 3), 0)
    right_bin = cv2.GaussianBlur(right_bin, (3, 3), 0)
    #bin = cv2.inRange(hsv, lbound, ubound)
    view = cv2.cvtColor(right_bin, cv2.COLOR_GRAY2BGR)
    
    left, right = -1, -1

    """for l in range(area_width, lmid):
        area = bin[row_begin:row_end, l - area_width:l] 
        if cv2.countNonZero(area) > pixel_cnt_threshold:
            left = l
            break

    for r in range(image_width - area_width, rmid, -1):
        area = bin[row_begin:row_end, r:r + area_width]
        if cv2.countNonZero(area) > pixel_cnt_threshold:
            right = r
            break"""
    for l in range(area_width, lmid):
        area = left_bin[row_begin:row_end, l - area_width:l] 
        if cv2.countNonZero(area) > pixel_cnt_threshold:
            left = l
            break

    for r in range(image_width - area_width, rmid, -1):
        area = right_bin[row_begin:row_end, r:r + area_width]
        if cv2.countNonZero(area) > pixel_cnt_threshold:
            right = r
            break

    if left != -1:
        lsquare = cv2.rectangle(view,
                                (left - area_width, row_begin),
                                (left, row_end),
                                (0, 255, 0), 3)
    else:
        print("Lost left line")

    if right != -1:
        rsquare = cv2.rectangle(view,
                                (right, row_begin),
                                (right + area_width, row_end),
                                (0, 255, 0), 3)
    else:
        print("Lost right line")

    cv2.imshow("origin", frame)
    cv2.imshow("view", view)

    #time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()
