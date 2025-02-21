import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


image=cv2.imread('coin_image.jpg')

gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur=cv2.GaussianBlur(gray, (5, 5), 0)


output_dir="output_images"
os.makedirs(output_dir, exist_ok=True)


_, binary=cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel=np.ones((3, 3), np.uint8)
binary=cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

# Edge detection
edges = cv2.Canny(binary, 120, 250)
plt.imshow(edges, cmap='gray')
plt.axis("off")
plt.show()
cv2.imwrite(os.path.join(output_dir, "edge_detection_output.jpg"), edges)

# Segmentation
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
segmented = np.zeros_like(gray)
cv2.drawContours(segmented, contours, -1, 255, thickness=cv2.FILLED)

plt.imshow(segmented, cmap='gray')
plt.axis("off")
plt.show()
cv2.imwrite(os.path.join(output_dir, "segmentation_output.jpg"), segmented)

# Counting the coins
cnt, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
min_contour_area = 500  
filtered_cnt = [c for c in cnt if cv2.contourArea(c) > min_contour_area]

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.drawContours(rgb, filtered_cnt, -1, (0, 255, 0), thickness=2)

#contour output
plt.imshow(rgb)
plt.axis("off")
plt.show()
cv2.imwrite(os.path.join(output_dir, "contour_output.jpg"), rgb)

num_coins = len(filtered_cnt)
cv2.putText(rgb, f'Total Coins: {num_coins}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (255, 0, 0), 2, cv2.LINE_AA)

#count coins output
plt.imshow(rgb)
plt.axis("off")
plt.show()
cv2.imwrite(os.path.join(output_dir, "count_coint_output.jpg"), rgb)

print("Number of coins in the image:", num_coins)
