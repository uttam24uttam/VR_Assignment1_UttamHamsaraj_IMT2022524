import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
import os

image_paths = ["images/left.jpg", "images/center.jpg", "images/right.jpg"]
image_list = [cv2.imread(path) for path in image_paths]

# Part A: Extracting Key Points 
gray_images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in image_list]

sift = cv2.SIFT_create()
keypoints, descriptors = zip(*[sift.detectAndCompute(img, None) for img in gray_images])

# Keypoints matching 
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

matches12 = flann.knnMatch(descriptors[0], descriptors[1], k=2)
matches23 = flann.knnMatch(descriptors[1], descriptors[2], k=2)

good_matches12 = [m for m, n in matches12 if m.distance < 0.75 * n.distance]
good_matches23 = [m for m, n in matches23 if m.distance < 0.75 * n.distance]

os.makedirs("output_images", exist_ok=True)

match_img12 = cv2.drawMatches(image_list[0], keypoints[0], image_list[1], keypoints[1], good_matches12, None, matchColor=(0, 255, 0), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imwrite("output_images/keypoint_matching_left_center.jpg", match_img12)
match_img23 = cv2.drawMatches(image_list[1], keypoints[1], image_list[2], keypoints[2], good_matches23, None, matchColor=(0, 255, 0), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imwrite("output_images/keypoint_matching_center_right.jpg", match_img23)

inv_gamma = 1.0 / 1.2
table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(0, 256)]).astype("uint8")
image_list = [cv2.LUT(img, table) for img in image_list]

cv2.imshow("Keypoint Matching (Left - Center)", match_img12)
cv2.imshow("Keypoint Matching (Center - Right)", match_img23)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Part B: Image Stitching 
stitcher = cv2.Stitcher_create()
status, stitched_img = stitcher.stitch(image_list)

if status == 0:
    bordered_img = cv2.copyMakeBorder(stitched_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    gray_img = cv2.cvtColor(bordered_img, cv2.COLOR_BGR2GRAY)
    binary_thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)[1]
    
    # Detecting the largest contour
    contours = cv2.findContours(binary_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    main_contour = max(imutils.grab_contours(contours), key=cv2.contourArea)
    
    # Bounding box around the detected key points
    bounding_box = cv2.boundingRect(main_contour)
    
    mask = np.zeros_like(binary_thresh)
    cv2.rectangle(mask, (bounding_box[0], bounding_box[1]), (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]), 255, -1)
    refined_mask = mask.copy()
    while cv2.countNonZero(cv2.subtract(refined_mask, binary_thresh)) > 0:
        refined_mask = cv2.erode(refined_mask, None)
    
    # Contour on the refined mask
    cropped_contours = cv2.findContours(refined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final_box = cv2.boundingRect(max(imutils.grab_contours(cropped_contours), key=cv2.contourArea))

    final_result = bordered_img[final_box[1]:final_box[1]+final_box[3], final_box[0]:final_box[0]+final_box[2]]
    
    cv2.imwrite("output_images/stitchedOutputProcessed.png", final_result)
    cv2.imshow("Final Stitched Image", final_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Cannot stitch images")
