from typing import Self
from PIL import Image
import numpy as np
from src.interfaces.image_converter import IImageConverter

class StripeToBlockConverter(IImageConverter):
    def __init__(self, strip_width: int = 10, blocks_count: int = 2):
        self.__strip_width = strip_width
        self.__blocks_count = blocks_count


    def convert(self, source: str | bytes, destination_path: str) -> Self:
        img = Image.open(source)
        img = img.convert("RGB")

        first_image = self._process_image(np.array(img), 1)
        rotated_image = np.rot90(first_image)
        second_image = self._process_image(rotated_image, 0)
        rotated_image = np.rot90(second_image, k=-1)

        Image.fromarray(rotated_image).save(destination_path)
        return self


    def _process_image(self, np_array: np.ndarray, glue_axis: int = 1) -> np.ndarray:
        width = np_array.shape[1]
        if glue_axis == 0:
            unit = self.__strip_width * self.__blocks_count
            width = width // unit * unit

        col_indexes = np.arange(width)
        mask = (col_indexes // self.__strip_width) % self.__blocks_count
        images: list[np.ndarray] = [np_array[:, :width, :][:, mask == i, :] for i in range(self.__blocks_count)]
        return np.concatenate(images, axis=glue_axis)
