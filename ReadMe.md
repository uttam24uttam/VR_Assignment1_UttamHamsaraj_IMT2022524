# Visual Recognition Assignment 1



## TASKS

This assignment consists of two parts:

- **Part 1: Coin Detection and Segmentation** – Detecting, segmenting, and counting coins from an image containing scattered Indian coins.
- **Part 2: Panorama Creation** – Creating a stitched panorama from multiple overlapping images.


## Prerequisites

Install Python 3.10. The following Python libraries are required: cv2, numpy, matplotlib, and imutils.

Install all dependencies using:
```bash
pip install opencv-python numpy matplotlib imutils
```

## Repository Structure

```
VR_Assignment1_UttamHamsaraj_IMT2022524/
│
├── PART_1/
│   ├── coins.py              # The code
│   ├── coin_image/           # The input image
│   ├── output_images/        # Created when the script is run, contains all output images
│
├── PART_2/
│   ├── images/               # Folder containing all input images
│   ├── image_stitching.py    # The code
│   ├── output_images/        # Created when the script is run, contains all output images
```

## Steps to Run

1. Clone this repository:
```bash
git clone https://github.com/uttam24uttam/VR_Assignment1_UttamHamsaraj_IMT2022524.git
cd VR_Assignment1_UttamHamsaraj_IMT2022524
```

2. To run **Part 1** (Coin Detection):
```bash
cd PART_1
python3 coins.py
```

3. To run **Part 2** (Panorama Creation):
```bash
cd PART_2
python3 image_stitching.py
```

---

# Part 1: Coin Detection and Segmentation

## Input Image

![coin_image](https://github.com/user-attachments/assets/02247926-4780-4d31-8e87-98350f4f737b)

**Figure 1:** Input coin image



### Methods Used

- **Preprocessing:** The image is converted to grayscale and Gaussian Blur is applied to reduce noise and smooth the image.  
- **Edge Detection:** Canny Edge Detection is used to detect the edges. Otsu’s thresholding is applied to create a binary image for better edge contrast. Morphological closing is used to refine object boundaries by filling small gaps.  
- **Segmentation:** Region-based segmentation using contour detection extracts individual coin regions.  
- **Contours Detection:** `findContours()` is applied to the edge-detected image to extract shape outlines. This helps distinguish coins from background noise.  
- **Counting:** Contours are filtered using an area threshold to exclude small artifacts. The valid contours (coins) are counted to determine the total number of coins.  


### Output Images

![Edge Detection Output](https://github.com/user-attachments/assets/0c231754-ba71-4d4a-81a3-4fb74c29a15d)  
**Figure 2:** Edge Detection Output  

![Segmentation Output](https://github.com/user-attachments/assets/0ac797fe-11b6-4b74-bfcb-27e7dfc913fd)  
**Figure 3:** Segmentation Output  

![Contour Output](https://github.com/user-attachments/assets/a22430ee-b6ba-41ce-99f2-cb018e84e744)  
**Figure 4:** Contour Output  

![Count Coin Output](https://github.com/user-attachments/assets/0ef13b58-8429-4976-ad05-0e1fa10c6e43)  
**Figure 5:** Count Coin Output  




# Observations

- Some internal parts were mistakenly detected as edges, so morphological closing was applied to refine the segmentation.
- Edge detection depends on the image taken and the lighting of the image.
- The segmentation method depends on the arrangement of coins; region-based segmentation was found to be the most suitable approach.

---

# Part 2: Panorama Creation

## Input Images
![left](https://github.com/user-attachments/assets/86bde86b-e23c-457f-aca3-9a76b0a477c4)
**Figure 6:** Left-Input Image  

![center](https://github.com/user-attachments/assets/1ee1c3f7-05b1-4bb8-927e-0a1ad8695163)
**Figure 7:** Center-Input Image  

![right](https://github.com/user-attachments/assets/960b32c0-94ac-4347-bd33-f20b5780fa97)
**Figure 8:** Right-Input Image  


### Methods Used

- **Preprocessing:** Image is converted to grayscale.
- **Keypoint Detection:** Keypoints are detected using SIFT.
- **Keypoint Matching:** Keypoints are matched using FLANN-based matcher.
- **Stitching:** `Stitcher` function is used to create the panorama.
- **Thresholding:** Image is segmented using binary thresholding.

### Output Images

![keypoints_matching_left_center](https://github.com/user-attachments/assets/6d4b02e6-b0a1-4b8f-ac3c-6159ee59100c)
**Figure 9:** Keypoints Matching 

![keypoints_matching_center_right](https://github.com/user-attachments/assets/294c8aae-4b3d-4584-aa8c-cb68eae459cf)
**Figure 10:** Keypoints Matching 

![stitchedOutputProcessed](https://github.com/user-attachments/assets/ffcb9cbf-563f-4867-9488-8c8e92ab07ca)
**Figure 11:**  Final Stitched Panaroma

---

# Observations

- Proper image overlap improves stitching accuracy.
- Lighting and angle differences affect keypoint matching.
- Good keypoint matching ensures better alignment.
- Cropping and contour detection refine the final output.
