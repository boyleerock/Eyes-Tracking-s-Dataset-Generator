import numpy as np
import cv2                
import dlib               #face recognition library, dlib
import os
import distance_cal 
import convert_yoloformat

def findeyes(path):
    #load dlib's models for a predictor
    detector = dlib.get_frontal_face_detector()    
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat') 

    # read image
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    ## eyes' landmarks:
    #       Left eyes         Right eyes
    #         37 38                  43 44
    # 36                  39  42              45
    #         41 40                  47  46

    # Find the number of face
    number_of_face = detector(img_gray, 0)
    # print(number_of_face)

    if not number_of_face:
        print("No detected...")
        return None, None, None
    else: 
        for i in range(len(number_of_face)):
            # find all the facial landmarks of each face
            landmarks = np.matrix([[p.x, p.y] for p in predictor(img, number_of_face[i]).parts()])  
            
            # calculate the distance of left eyes' coordinate
            d41_40 = distance_cal.cal((landmarks[41][0,0], landmarks[41][0,1]), (landmarks[40][0,0], landmarks[40][0,1]))
            d37_38 = distance_cal.cal((landmarks[37][0,0], landmarks[37][0,1]), (landmarks[38][0,0], landmarks[38][0,1]))
            max_width = max(d41_40, d37_38)
            d37_41 = distance_cal.cal((landmarks[37][0,0], landmarks[37][0,1]), (landmarks[41][0,0], landmarks[41][0,1]))
            d38_40 = distance_cal.cal((landmarks[38][0,0], landmarks[38][0,1]), (landmarks[40][0,0], landmarks[40][0,1]))
            max_length = max(d37_41, d38_40)
            
            padding_value = 1.4 # The ratio of distance between the bounding box and landmarks

            # draw bounding box （function cv2.rectangle can only take Integer parameter）
            draw_start_left =  (int(landmarks[36][0,0] - max_width*padding_value), int(landmarks[36][0,1] + max_length*padding_value))
            draw_end_left = (int(landmarks[39][0,0] + max_width*padding_value), int(landmarks[39][0,1] -  max_length*padding_value))
            cv2.rectangle(img, draw_start_left, draw_end_left, (0,255,0), 2)

            # calculate the distance of right eyes' coordinate
            d47_46 = distance_cal.cal((landmarks[47][0,0], landmarks[47][0,1]), (landmarks[46][0,0], landmarks[46][0,1]))
            d43_44 = distance_cal.cal((landmarks[43][0,0], landmarks[43][0,1]), (landmarks[44][0,0], landmarks[44][0,1]))
            max_length = max(d47_46, d43_44)
            d43_47 = distance_cal.cal((landmarks[43][0,0], landmarks[43][0,1]), (landmarks[47][0,0], landmarks[47][0,1]))
            d44_46 = distance_cal.cal((landmarks[44][0,0], landmarks[44][0,1]), (landmarks[46][0,0], landmarks[46][0,1]))
            max_width = max(d43_47, d44_46)
            
            # draw bounding box （cv2.rectangle只能取整數值）
            draw_start_right =  (int(landmarks[42][0,0] - max_length), int(landmarks[42][0,1] + max_width*padding_value)) 
            draw_end_right = (int(landmarks[45][0,0] + max_length*padding_value), int(landmarks[45][0,1] -  max_width*padding_value))
            # print(draw_start_right, draw_end_right)
            cv2.rectangle(img, draw_start_right, draw_end_right, (0,255,0), 2)

            return img, (draw_start_left[0], draw_end_left[0], draw_start_left[1], draw_end_left[1]), (draw_start_right[0], draw_end_right[0], draw_start_right[1], draw_end_right[1])
    
def loop_directory(directory: str):
    # 建立yolo訓練資料夾
    datapath = "bounded_image"
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    datapath = "labels"
    if not os.path.exists(datapath):
        os.makedirs(datapath)

    # initialize the number of detection and the number of NOT detection
    count_not_detected = 0
    count_bounding = 0

    for filename in os.listdir(directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            file_directory = os.path.join(directory, filename)
            
            img = cv2.imread(file_directory)
            img_size = [img.shape[0], img.shape[1]]

            # bounding each image
            result, box_left, box_right = findeyes(file_directory)
            
            if box_left is not None:    # skip the process if eyes not detected in an image
                if box_right is not None:
                    if result is not None:
                        count_bounding += 1
                        print('Bounding', count_bounding)
                        print(file_directory)
                        
                        # coordinate of left eye
                        xmin_left = int(min(box_left[0], box_left[1]))
                        xmax_left = int(max(box_left[0], box_left[1]))
                        ymin_left = int(min(box_left[2], box_left[3]))
                        ymax_left = int(max(box_left[2], box_left[3]))
                        box_left_input = [xmin_left, xmax_left, ymin_left, ymax_left]

                        # coordinate of right eye
                        xmin_right = int(min(box_right[0], box_right[1]))
                        xmax_right = int(max(box_right[0], box_right[1]))
                        ymin_right = int(min(box_right[2], box_right[3]))
                        ymax_right = int(max(box_right[2], box_right[3]))
                        box_right_input = [xmin_right, xmax_right, ymin_right, ymax_right]

                        # convert coordinate of both eyes into  YOLO format
                        print('coordinate of left eyes:', box_left_input)
                        yolo_bbox_left = convert_yoloformat.convert(img_size, box_left_input)
                        print('yolo_bbox_left:', yolo_bbox_left)
                        print('coordinate of right eyes:', box_right_input)
                        yolo_bbox_right = convert_yoloformat.convert(img_size, box_right_input)
                        print('yolo_bbox_right:', yolo_bbox_right)

                        # write YOLO format's eyes and save it into "labels" folder
                        yolo_bbox_left = ''.join("0 " + str(yolo_bbox_left[0]) + " " + str(yolo_bbox_left[1]) + " " + str(yolo_bbox_left[2]) + " " + str(yolo_bbox_left[3]) + "\n")
                        yolo_bbox_right = ''.join("0 " + str(yolo_bbox_right[0]) + " " + str(yolo_bbox_right[1]) + " " + str(yolo_bbox_right[2]) + " " + str(yolo_bbox_right[3]))
                        f = open('labels/' +  file_directory.split('/')[-1].split('.')[0] + ".txt", "x")
                        f.write(yolo_bbox_left+yolo_bbox_right)
                        print('\n')
                        f.close()

                        #save an eyes-bounding image into "bounded_image" folder
                        cv2.imwrite('bounded_image/' + file_directory.split('/')[-1].split('.')[0] +'.jpg', result)
                        
            else:  # delete the image if the eyes are not detected
                count_not_detected += 1
                print('The no. of NOT detected:', count_not_detected)
                print('deleting', file_directory, '...\n')
                os.remove(file_directory)

    print('The total number of images NOT detected: ', count_not_detected)

if __name__=='__main__':
    loop_directory("images/")
