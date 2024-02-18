import math
import random

from PIL import Image


class SeededImageGenerator:
    def __init__(self, seed):
        self.seed = seed
        self.image = None

    @staticmethod
    def get_image_filename(fingerprint):
        return f"{fingerprint}.png"

    def generate(self, width, height):
        heatmap = self.generate_random_heatmap(self.seed)
        return self.generate_multipoint_gradient(width, height, heatmap)

    def gaussian(self, x, a, b, c, d=0):
        return a * math.exp(-(x - b) ** 2 / (2 * c ** 2)) + d

    def pixel(self, x, width, pixel_map, spread=1):
        width = float(width)
        r = sum([self.gaussian(x, p[1][0], p[0] * width, width / (spread * len(pixel_map))) for p in pixel_map])
        g = sum([self.gaussian(x, p[1][1], p[0] * width, width / (spread * len(pixel_map))) for p in pixel_map])
        b = sum([self.gaussian(x, p[1][2], p[0] * width, width / (spread * len(pixel_map))) for p in pixel_map])
        return min(1.0, r), min(1.0, g), min(1.0, b)

    def get_random_color(self):
        return random.random(), random.random(), random.random()

    def generate_random_heatmap(self, seed):
        # heatmap = [
        #     [0.0, (0, 0, 0)],
        #     [0.20, (0, 0, .5)],
        #     [0.40, (0, .5, 0)],
        #     [0.60, (.5, 0, 0)],
        #     [0.80, (.75, .75, 0)],
        #     [0.90, (1.0, .75, 0)],
        #     [1.00, (1.0, 1.0, 1.0)],
        # ]
        random.seed(seed)
        number_of_points = random.randint(5, 10)
        heatmap = [[0.0, self.get_random_color()]]
        for i in range(number_of_points):
            heatmap.append([random.uniform(0.0, 1.0), self.get_random_color()])
        heatmap.append([1.0, self.get_random_color()])
        return heatmap

    # I took the code from here and modified it to use the heatmap
    # https://stackoverflow.com/a/31125282/7374799
    def generate_multipoint_gradient(self, width, height, heatmap):
        im = Image.new('RGB', (width, height))
        ld = im.load()
        for x in range(im.size[0]):
            r, g, b = self.pixel(x, width=im.size[0], pixel_map=heatmap)
            r, g, b = [int(256 * v) for v in (r, g, b)]
            for y in range(im.size[1]):
                ld[x, y] = r, g, b
        return im

if __name__ == "__main__":
    sg = SeededImageGenerator(random.randint(0, 1000000))
    image = sg.generate(512, 550)
    image.show()
