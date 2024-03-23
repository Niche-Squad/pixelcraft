import streamlit as st
from PIL import Image
import cv2
import numpy as np


def load_image(img, tgt_width=640):
    pil_in = Image.open(img)
    w, h = pil_in.size
    ratio = h / w
    height = int(tgt_width * ratio)
    pil_out = pil_in.resize((tgt_width, height))
    return pil_out


def caching_images():
    text_bar = "Caching images..."
    bar = st.progress(0, text=text_bar)
    n_imgs = st.session_state.n_imgs
    file_imgs = st.session_state.file_imgs
    pil_imgs = st.session_state.pil_imgs
    portion = int(100 / n_imgs)
    # showing progress bar of caching images
    for i in range(n_imgs):
        pil = pil_imgs[i]
        if pil is None:
            pil = load_image(file_imgs[i])
            st.session_state.pil_imgs[i] = pil
        bar.progress((i + 1) * portion, text=text_bar)
    bar.empty()


def segmentaion(img, strength=0):
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


def avg_rgb(img_pil):
    """
    Assuming the img_pil is in mode "RGBA"
    """
    # turn 4-channel 2d array to 1d array
    rgbvec = np.array(img_pil)[:, :, :3].reshape(-1, 3)
    a_vec = np.array(img_pil)[:, :, 3].reshape(-1)
    # get average value of each channel
    return np.mean(rgbvec[a_vec > 0], axis=0)
