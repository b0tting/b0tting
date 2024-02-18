import asyncio
import collections
from io import StringIO, BytesIO

import tornado
from dotenv import dotenv_values

from dynamic_fingerprint_generator.lib.seeded_image_generator import SeededImageGenerator
from dynamic_fingerprint_generator.lib.image_manager import ImageManager
from dynamic_fingerprint_generator.lib.object_hasher import ObjectHasher

config = dotenv_values(".env")

image_manager = ImageManager(config["IMAGES_PATH"], max_objects=config["MAX_OBJECTS"])


class MainHandler(tornado.web.RequestHandler):
    def send_image(self, image):
        self.set_header('Content-Type', 'image/png')
        self.set_header('Cache-Control', 'no-cache')
        temp_image = BytesIO()
        image.save(temp_image, format="png")  # jpeg encoder isn't available in my install...
        self.write(temp_image.getvalue())

    def get(self):
        # Oh right, order matters when generating the string
        ordered_headers = collections.OrderedDict(self.request.headers.items())
        fingerprint = ObjectHasher.hash_objects(headers=ordered_headers, remote_ip=self.request.remote_ip)
        my_fingerprint = int(config["MY_FINGERPRINT"])
        fingerprint += my_fingerprint
        image_file = SeededImageGenerator.get_image_filename(fingerprint)
        image = image_manager.get_image(image_file)
        if not image:
            seeded_image_generator = SeededImageGenerator(fingerprint)
            image = seeded_image_generator.generate(512, 64)
            image_manager.save_image(image, image_file)

        self.send_image(image)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


async def main():
    app = make_app()
    app.listen(config["WEBSERVER_PORT"])
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()


if __name__ == "__main__":
    print(f"Running webserver on port {config.get('WEBSERVER_PORT')}")
    asyncio.run(main())
