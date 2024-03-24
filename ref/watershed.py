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


def watershed(img, thresh_fg=0.3, iter_bg=1):
    if img.mode != "RGB":
        img = img.convert("RGB")
    imgnp = np.array(img)
    gray = cv2.cvtColor(imgnp, cv2.COLOR_RGB2GRAY)

    # background
    ret, thresh = cv2.threshold(
        src=gray,
        thresh=0,
        maxval=255,
        type=cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )
    kernel = np.ones((3, 3), np.uint8)
    sure_bg = cv2.dilate(
        src=thresh,
        kernel=kernel,
        iterations=iter_bg,
    )

    # foreground
    dist_transform = cv2.distanceTransform(
        src=thresh,
        distanceType=cv2.DIST_L2,
        maskSize=5,
    )
    ret, sure_fg = cv2.threshold(
        src=dist_transform,
        thresh=thresh_fg * dist_transform.max(),
        maxval=255,
        type=0,
    )

    # unknown
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    cv2.watershed(imgnp, markers)
    return markers


# img = load_image(path_img).crop((260, 350, 550, 400))
img = load_image(path_img).crop((260, 250, 450, 400))
img
markers = watershed(img, thresh_fg=0.6, iter_bg=5)
plt.imshow(markers)
print(np.unique(markers))


# show unique values
all_cat = np.unique(markers)
all_cat = all_cat[all_cat != -1]
combins = [
    all_cat[i:j] for i in range(len(all_cat)) for j in range(i + 1, len(all_cat) + 1)
]
imgsegs = []
for i in range(len(combins)):
    print(f"Combination {i}: {combins[i]}")
    markers_s = np.where(np.isin(markers, combins[i]), 255, 0).astype(np.uint8)
    mask_alpha = Image.fromarray(markers_s).convert("L")
    imgseg = img.convert("RGBA")
    imgseg.putalpha(mask_alpha)
    imgsegs += [imgseg]
imgsegs[5]

plt.imshow(markers)
# Convert back to RGB to display using matplotlib
final_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()

plt.imshow(markers)
