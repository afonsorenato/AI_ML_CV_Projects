import cv2
import numpy as np

def getListOfNames(file_name):
    my_file = open(file_name, 'r')
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()

    return content_list


# Loading Mask RCNN
class_names = getListOfNames("coco_names.txt")
net = cv2.dnn.readNetFromTensorflow("frozen_inference_graph_coco.pb", "mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")

#size = (500, 500)
#video_output = cv2.VideoWriter("CleanVideo1.mp4", cv2.VideoWriter_fourcc(*'MJPG'), 10, size)

video_flag = 0

if video_flag == 1:
    cap = cv2.VideoCapture("Video1.mp4")
else:
    cap = cv2.VideoCapture(0)

ok, img = cap.read()
while ok:

    ok, img = cap.read()
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

        if class_id >= 0:
            cv2.putText(final_mask_not, str(class_names[class_id]), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 0), 2)

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
    #video_output.write(output_without_objs)

    # Both images together for simplicity
    cv2.imshow("Results", cv2.resize(cv2.hconcat([output_with_objs, output_without_objs]), (900, 500)))
    cv2.waitKey(1)

#video_output.release()