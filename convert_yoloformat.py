import numpy as np
import cv2                #影象處理庫OpenCV
import dlib               #人臉識別庫dlib
import distance_cal #計算兩點距離
import os

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    
    x = x*dw
    x1 = '%f' % x

    w = w*dw
    w1 = '%f' % w
    
    y = y*dh
    y1 = '%f' % y
    
    h = h*dh
    h1 = '%f' % h
    return (x1,y1,w1,h1)
# def convert(size, box):
#     #in case when labelling, box points are not in the right order
#     xmin = min(box[0],box[2])
#     xmax = max(box[0],box[2])
#     ymin = min(box[1],box[3])
#     ymax = max(box[1],box[3])
#     b = (xmin, xmax, ymin, ymax)

#     dw = 1./size[0]
#     dh = 1./size[1]
    
#     x = (b[0] + b[1])/2.0
#     y = (b[2] + b[3])/2.0
#     w = b[1] - b[0]
#     h = b[3] - b[2]
#     x = x*dw
#     x = '%f' % x
#     w = w*dw
#     w = '%f' % w
#     y = y*dh
#     y = '%f' % y
#     h = h*dh
#     h = '%f' % h
#     return (x,y,w,h)

# def findeyes(path):
#     #dlib預測器
#     detector = dlib.get_frontal_face_detector()    #使用dlib庫提供的人臉提取器
#     predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')   #構建特徵提取器

#     # cv2讀取影象
#     img = cv2.imread(path)

#     # 取灰度
#     img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#     #         37 38                  43 44
#     # 36                  39  42              45
#     #         41 40                  47  46
#     #         左眼                      右眼

#     # 人臉數rects
#     rects = detector(img_gray, 0)
#     for i in range(len(rects)):
        
#         landmarks = np.matrix([[p.x, p.y] for p in predictor(img,rects[i]).parts()])  #人臉關鍵點識別
#         # left eyes
#         d41_40 = distance_cal.cal((landmarks[41][0,0], landmarks[41][0,1]), (landmarks[40][0,0], landmarks[40][0,1]))
#         d37_38 = distance_cal.cal((landmarks[37][0,0], landmarks[37][0,1]), (landmarks[38][0,0], landmarks[38][0,1]))
#         max_length = max(d41_40, d37_38)
        
#         d37_41 = distance_cal.cal((landmarks[37][0,0], landmarks[37][0,1]), (landmarks[41][0,0], landmarks[41][0,1]))
#         d38_40 = distance_cal.cal((landmarks[38][0,0], landmarks[38][0,1]), (landmarks[40][0,0], landmarks[40][0,1]))
#         max_width = max(d37_41, d38_40)
        
#         d36_39 = distance_cal.cal((landmarks[36][0,0], landmarks[36][0,1]), (landmarks[39][0,0], landmarks[39][0,1]))

#         padding_value = 2 #bounding box 到landmarks的空間距離
#         #左上座標
#         box_upper_left = (landmarks[36][0,0] - max_length*padding_value, landmarks[36][0,1] - max_width*padding_value)
#         # print('box upper left - left eyes', box_upper_left)
#         # 左下座標
#         box_btn_left = (landmarks[36][0,0] - max_length*padding_value, landmarks[39][0,1] +  max_width*padding_value)
#         # print('box btn left - left eyes', box_btn_left)
#         # 右上座標
#         box_upper_right = (landmarks[39][0,0] + max_length, landmarks[36][0,1] - max_width*padding_value)
#         # print('box btn left - left eyes', box_upper_right)
#         # 右下座標
#         box_btn_right = (landmarks[39][0,0] + max_length, landmarks[39][0,1] +  max_width*padding_value)
#         # print('box btn right - left eyes', box_btn_right)

#         # draw bounding box
#         draw_start =  (int(landmarks[36][0,0] - max_length*padding_value), int(landmarks[36][0,1] - max_width*padding_value))
#         draw_end = (int(landmarks[39][0,0] + max_length), int(landmarks[39][0,1] +  max_width*padding_value))
#         cv2.rectangle(img, draw_start, draw_end, (0,255,0), 1)
#         print(draw_start[0], draw_start[1], draw_end[0], draw_end[1])
#     return (draw_start[0], draw_start[1], draw_end[0], draw_end[1])

# im=cv2.imread("1.jpg")
# size = im.shape
# box = findeyes("1.jpg")

# # https://stackoverflow.com/questions/56115874/how-to-convert-bounding-box-x1-y1-x2-y2-to-yolo-style-x-y-w-h

