import os
import re
from pathlib import Path
from PIL import Image


class ImageManager:
    DEFAULT_IMAGE_EXPRESSION = "[\d]+.(png|jpg|jpeg|gif)"

    def __init__(self, image_path, max_objects=200, file_expression=DEFAULT_IMAGE_EXPRESSION):
        self.image_path = Path(image_path)
        if not self.image_path.exists() or not self.image_path.is_dir() or not os.access(image_path, os.W_OK):
            raise Exception(f"Cannot find or use {image_path} as temporary images storage")
        self.max_objects = int(max_objects)
        self.file_expression = re.compile(file_expression)
        self.usage = {}

    def file_exists(self, image_name):
        return (self.image_path / image_name).exists()

    def get_image(self, image_name):
        if not self.file_exists(self.image_path / image_name):
            return None

        if image_name in self.usage:
            self.usage[image_name] += 1
        else:
            self.usage[image_name] = 1

        return Image.open(self.image_path / image_name)

    def save_image(self, image, image_name):
        if self.has_maximum_objects(self.usage, self.max_objects):
            self.cleanup_images()
        image.save(self.image_path / image_name)

    def has_maximum_objects(self, usage, max_objects):
        return len(usage.keys()) >= max_objects

    # Delete the oldest images if we have too many
    def cleanup_images(self):
        flipped_usage = {v: k for k, v in self.usage.items()}
        sorted_usage = sorted(flipped_usage)
        for i in range(len(sorted_usage) - self.max_objects):
            image_name = flipped_usage[sorted_usage[i]]
            try:
                self.image_path / image_name.unlink()
            except FileNotFoundError:
                pass
            del self.usage[image_name]
