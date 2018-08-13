import os
import imageio
from PIL import Image
png_dir = '..path/to/png/'
images = []
Image.MAX_IMAGE_PIXELS = None
for file_name in os.listdir(png_dir):
    file_path = os.path.join(png_dir, file_name)
    # print(file_name)
    images.append(imageio.imread(file_path))
imageio.mimsave('..path/to/movie.gif', images)
