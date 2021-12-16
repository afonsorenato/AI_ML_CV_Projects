import cv2
import numpy as np
import os, os.path

# START HERE: Chose an image
image_name = "human.png"
img = cv2.imread('Aux_Files/' + image_name)


# getListOfNames function that gets a txt file with classes names and outputs a list with those names
# Input: file_name --> name of the txt file
# Output: list of strings
def getListOfNames(file_name):
    my_file = open(file_name, 'r')
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()

    return content_list


# List of all classes names
class_names = getListOfNames("Aux_Files/coco_names.txt")

# Generate random colors for further printing
colors = np.random.randint(0, 255, (80, 3))

# Specs of chosen image
height, width, _ = img.shape

# Create black image
final_mask_not = np.zeros((height, width, 3), np.uint8)

# Loading Mask RCNN
net = cv2.dnn.readNetFromTensorflow("Aux_Files/frozen_inference_graph_coco.pb",
                                    "Aux_Files/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")
blob = cv2.dnn.blobFromImage(img, swapRB=True)
net.setInput(blob)

# Returns bounding boxes and masks arrays
boxes, masks = net.forward(["detection_out_final", "detection_masks"])
detection_count = boxes.shape[2]

# Loops al founded boxes on the image
for i in range(detection_count):
    box = boxes[0, 0, i]
    class_id = int(box[1])
    score = box[2]

    # Gets the name of the class
    if box[2] > 0:
        print("Class name: " + str(class_names[class_id]) + "-> " + str(int(score * 100)) + "%")

    # If the confidence is very low, ignores the object
    if score < 0.5:
        continue

    # Get box Coordinates
    x, y = int(box[3] * width), int(box[4] * height)
    x2, y2 = int(box[5] * width), int(box[6] * height)
    cv2.putText(final_mask_not, str(class_names[class_id]), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 0), 2)

    roi = final_mask_not[y: y2, x: x2]
    roi_height, roi_width, _ = roi.shape

    # Get the my_mask
    mask = masks[i, int(class_id)]
    mask = cv2.resize(mask, (roi_width, roi_height))
    _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)

    # Get my_mask coordinates
    contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    color = colors[int(class_id)]

    # Draws mask polygon for the founded object
    for cnt in contours:
        cv2.fillPoly(roi, [cnt], (255, 255, 255))

# Performs bitwise operations
final_mask_not = np.bitwise_not(final_mask_not)
final_mask_yes = np.bitwise_not(final_mask_not)

# Converts to uint types for further operations
final_mask_not = np.array(final_mask_not, dtype="uint8")
final_mask_yes = np.array(final_mask_yes, dtype="uint8")
final_img = np.array(img, dtype="uint8")

# Gets final images outputs: with and without mask
output_with_objs = cv2.add(final_img, final_mask_not)
output_without_objs = cv2.add(final_img, final_mask_yes)

# Both images together for simplicity
output = cv2.resize(cv2.hconcat([output_with_objs, output_without_objs]), (900, 500))
cv2.imshow("Results", output)

# Saves new file on Results folder with an index
list = os.listdir("Results")
file_count = len(list)

#print("Files in Results directory: " + str(file_count))
output_file_name = "Results/" + str(int(file_count+ 1)) + "_" + image_name[:-4] + ".jpg"
print("Saved file: " + str(output_file_name))
cv2.imwrite(output_file_name, output)
cv2.waitKey(0)
