import numpy as np
import cv2
from PIL import Image
import streamlit as st


@st.cache_data()
def thresholding(img, strength=0):
    if strength == 0:
        return img.convert("RGBA")
    # define k
    ls_k = [3, 5, 7, 9, 11, 17, 31, 55, 75, 99][::-1]
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
    mask_rgb = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    mask_alpha = Image.fromarray(mask).convert("L")
    # apply mask to original image
    imgseg = np.where(mask_rgb == 255, imgnp, 0)
    # turn numpy array back to PIL Image
    imgseg_pil = Image.fromarray(imgseg).convert("RGBA")
    imgseg_pil.putalpha(mask_alpha)
    return imgseg_pil
