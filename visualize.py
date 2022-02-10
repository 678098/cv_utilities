from typing import List

import cv2
import numpy as np


def collage(images: List[np.ndarray], margin_pix: int = 5) -> np.ndarray:
    assert len(images) > 0

    def is_grayscale(image: np.ndarray) -> bool:
        return len(image.shape) == 2 or image.shape[-1] == 1

    gray = [is_grayscale(image) for image in images]
    bgr_needed = sum(gray) < len(gray)

    dy = max(image.shape[0] for image in images) + margin_pix
    dx = max(image.shape[1] for image in images) + margin_pix

    square_width = int(pow(len(images) - 0.1, 0.5)) + 1
    square_height = int((len(images) - 0.1) // square_width) + 1

    collage_shape = (square_height * dy + margin_pix, square_width * dx + margin_pix, 3 if bgr_needed else 1)

    clg = np.ones(collage_shape, dtype='uint8') * 255

    for i, image in enumerate(images):
        ycoord = i // square_width
        xcoord = i - ycoord * square_width
        ypos = margin_pix + ycoord * dy
        xpos = margin_pix + xcoord * dx

        if bgr_needed and is_grayscale(image):
            to_draw = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            if len(image.shape) == 2:
                to_draw = image.reshape(image.shape + (1,))
            else:
                to_draw = image

        clg[ypos:ypos + to_draw.shape[0], xpos:xpos + to_draw.shape[1], :] = to_draw

    return clg


if __name__ == "__main__":
    import glob
    import random

    fpaths = glob.glob('/media/mes/Speedy/OCR/gen/*.png')[:44]
    images = [cv2.imread(path, random.choice([cv2.IMREAD_GRAYSCALE, cv2.IMREAD_COLOR])) for path in fpaths]

    clg = collage(images, margin_pix=10)
    cv2.imwrite('res.png', clg)
