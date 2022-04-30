from PIL import Image, ImageDraw
from typing import Tuple

def to_circle(image: Image.Image, size: Tuple[int, int]):
  pfp = image.resize(size, Image.ANTIALIAS)
  mask = Image.new('L', pfp.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0, 0) + pfp.size, 255) #  (0, 0) + pfp.size = (0, 0, 285, 286)
  pfp.putalpha(mask)
  return pfp