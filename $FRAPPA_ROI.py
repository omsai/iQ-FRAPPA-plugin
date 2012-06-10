#SHELL
"""
Draws bitmap ROIs from each event onto duplicated image.
"""
from imagedisk import iQImageDisk
from iQImage import *
from PIL import Image, ImageDraw
from numpy import array

# User editable variables
intensity = 16000
line_width = 2

# iQImage.shape seems to be the only way to get image width and height
# attributes.  Monkey patch with explicit width and height properties, inspired
# by ImageJ getWidth and getHeight
def _get_width(self):
    return self.shape[-2]

def _get_height(self):
    return self.shape[-1]

iQImage.getWidth = _get_width
iQImage.getHeight = _get_height

# Get image from user
from imagedisk import iQImageDisk
id = iQImageDisk()
# FIXME: Use GUI to allow user to choose image
im = iQImage(id, 'frap2.tif')

# Assemble ROIs using PIL Image
for roi in im.targeted_ROIs():
    x = im.getWidth()
    y = im.getHeight()
    pil_im = Image.new('L', (x, y), 0)
    if roi['type'] == 'Rectangle':
        ImageDraw.Draw(pil_im).rectangle(roi['coordinates'],
                               # FIXME: outline > 1 does not increase thickness
                                         outline=line_width)
    from iqtools.mplot import imshow
    imshow(pil_im)

##im2 = im.duplicate(im.title + '_drawEventROIs')
