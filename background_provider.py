import glob
import random

import cv2
import numpy as np


class MaxRetriesToLoadImageException(Exception):
    """Raised when failed to load image with limited retries"""
    pass


class BackgroundProvider:
    def __init__(self, images_dir: str, grayscale: bool = False):
        paths = glob.glob(f'{images_dir}/**', recursive=True)

        self._image_paths = [path for path in paths if self.is_image_path(path)]
        self._grayscale = grayscale

    @staticmethod
    def is_image_path(path: str) -> bool:
        image_exts = ['.jpg', '.png', '.bmp']
        return path[-4:].lower() in image_exts

    def get_random_image(self) -> np.ndarray:
        max_retries = 100
        for i in range(max_retries):
            image_path = random.choice(self._image_paths)
            load_flags = cv2.IMREAD_GRAYSCALE if self._grayscale else None
            image = cv2.imread(image_path, flags=load_flags)
            if image is not None:
                return image

        raise MaxRetriesToLoadImageException(
            'Max retries reached while trying to load image, probably some image files are corrupted')

    def get_random_crop(self, width: int, height: int) -> np.ndarray:
        image = self.get_random_image()
        image_h = image.shape[0]
        image_w = image.shape[1]

        min_crop_size = 10
        x1 = random.randint(0, image_w - min_crop_size)
        x2 = x1 + min_crop_size + random.randint(0, image_w - x1 - min_crop_size)
        y1 = random.randint(0, image_h - min_crop_size)
        y2 = y1 + min_crop_size + random.randint(0, image_h - y1 - min_crop_size)

        crop = image[y1:y2, x1:x2]

        inter = random.choice([cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_AREA, cv2.INTER_LANCZOS4, cv2.INTER_BITS])
        resized = cv2.resize(crop, (width, height), interpolation=inter)
        return resized


if __name__ == "__main__":
    path = '/media/mes/Speedy/datasets/indoor/'
    provider = BackgroundProvider(path)

    for i in range(10):
        image = provider.get_random_image()
        cv2.imwrite(f'image_{i}.jpg', image)
        crop = provider.get_random_crop(128, 256)
        cv2.imwrite(f'crop_{i}.jpg', crop)
