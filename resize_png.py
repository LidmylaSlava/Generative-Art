import os
from PIL import Image

png_dir = '..path/to/png/'
png_dir_new = '..path/to/new_png/'
Image.MAX_IMAGE_PIXELS = None
for file_name in os.listdir(png_dir):
    file_path = os.path.join(png_dir, file_name)
    foo = Image.open(file_path)
    foo = foo.resize((1000, 1000), Image.ANTIALIAS) # set size
    file_path_new = os.path.join(png_dir_new, file_name)
    foo.save(file_path_new, optimize=True, quality=95)
