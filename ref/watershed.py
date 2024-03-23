import re
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

path_img = "/Users/niche/Pictures/cow.jpeg"


def load_image(img, tgt_width=640):
    pil_in = Image.open(img)
    w, h = pil_in.size
    ratio = h / w
    height = int(tgt_width * ratio)
    pil_out = pil_in.resize((tgt_width, height))
    return pil_out


img = load_image(path_img).crop((260, 350, 550, 400))
img
img

kernel = np.ones((5, 5), np.uint8)
sure_bg = cv2.dilate(thresh, kernel, iterations=3)
plt.imshow(sure_bg)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
plt.imshow(sure_fg)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)


# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers + 1

# Now, mark the region of unknown with zero
markers[unknown == 255] = 0


cv2.watershed(img, markers)
img[markers == -1] = [255, 0, 0]

# Convert back to RGB to display using matplotlib
final_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()

plt.imshow(markers)


def segmentaion(img, strength=50):
    # define k
    ls_k = [(2 * i - 1) for i in range(2, 52)][::-1]
    k = ls_k[strength - 1]

    # process img (PIL.Image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    imgnp = np.array(img)
    gray = cv2.cvtColor(imgnp, cv2.COLOR_RGB2GRAY)

    # binarize the image
    blur = cv2.GaussianBlur(
        src=gray,
        ksize=(k, k),
        sigmaX=10,
        sigmaY=10,
    )
    ret, thresh = cv2.threshold(
        src=blur,
        thresh=0,
        maxval=255,
        type=cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    # find contours
    contours, hierarchy = cv2.findContours(
        image=thresh,
        mode=cv2.RETR_TREE,
        method=cv2.CHAIN_APPROX_NONE,
    )
    largest_contour = max(contours, key=cv2.contourArea)

    # Create a mask for the largest contour
    mask = np.zeros(thresh.shape, np.uint8)
    cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
    mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)


zimg_seg = np.where(mask == 255, imgnp, 0)
plt.imshow(img_seg)


img_seg
