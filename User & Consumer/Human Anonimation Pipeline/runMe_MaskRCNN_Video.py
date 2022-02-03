import cv2
import numpy as np
import time
import math
import os

# User can choose between using a video or a live stream
list = []
video_flag = 0
video_name = "video_test.mp4"

# Gets all classes names
def getListOfNames(file_name):
    my_file = open(file_name, 'r')
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()

    return content_list


# User can choose between using a video or a live stream
if video_flag == 1:
    cap = cv2.VideoCapture(video_name)
else:
    cap = cv2.VideoCapture(0)

# Define the codec for video saving
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define name and location of saved file
list = os.listdir("Results")
file_count = len(list)
output_file_name = "Results/" + str(int(file_count+ 1)) + "_" + video_name[:-4] + ".avi"
out = cv2.VideoWriter(output_file_name, fourcc, 30, (frame_width, frame_height))


# Loading Mask RCNN
class_names = getListOfNames("Aux_Files/coco_names.txt")
net = cv2.dnn.readNetFromTensorflow("Aux_Files/frozen_inference_graph_coco.pb",
                                    "Aux_Files/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")

# Gets first image
ok, img = cap.read()
cTime = time.time()

# Main loop
while True:

    ok, img = cap.read()
    if not ok:
        break

    height, width, _ = img.shape

    # Create black image
    final_mask_not = np.zeros((height, width, 3), np.uint8)

    # Detect objects
    blob = cv2.dnn.blobFromImage(img, swapRB=True)
    net.setInput(blob)

    boxes, masks = net.forward(["detection_out_final", "detection_masks"])
    detection_count = boxes.shape[2]

    for i in range(detection_count):
        box = boxes[0, 0, i]
        class_id = int(box[1])
        score = box[2]

        # If the confidence is very low, ignores the object
        if score < 0.5:
            continue

        # Get box Coordinates
        x, y = int(box[3] * width), int(box[4] * height)
        x2, y2 = int(box[5] * width), int(box[6] * height)

        #if class_id >= 0:
        #    cv2.putText(final_mask_not, str(class_names[class_id]), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 0),2)

        roi = final_mask_not[y: y2, x: x2]
        roi_height, roi_width, _ = roi.shape

        # Get the my_mask
        mask = masks[i, int(class_id)]
        mask = cv2.resize(mask, (roi_width, roi_height))
        _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)

        # Get my_mask coordinates
        contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            cv2.fillPoly(roi, [cnt], (255, 255, 255))

    final_mask_not = np.bitwise_not(final_mask_not)
    final_mask_yes = np.bitwise_not(final_mask_not)

    final_mask_not = np.array(final_mask_not, dtype="uint8")
    final_mask_yes = np.array(final_mask_yes, dtype="uint8")

    final_img = np.array(img, dtype="uint8")
    output_with_objs = cv2.add(final_img, final_mask_not)
    output_without_objs = cv2.add(final_img, final_mask_yes)

    # Save occluded video
    out.write(output_without_objs)

    # Get frame rate
    nTime = time.time()
    fps = math.ceil(1 / (nTime - cTime))
    cTime = nTime

    cv2.putText(output_with_objs, str(fps), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Both images together for simplicity
    cv2.imshow("Results", cv2.resize(cv2.hconcat([output_with_objs, output_without_objs]), (900, 500)))
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()
