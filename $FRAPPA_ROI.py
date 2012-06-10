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
title_postfix = '_drawEventROIs'

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
im = iQImage(id, 'frap2.tif') # FIXME: Use GUI to allow user to choose image

"""
# Make a copy
new_title = im.title + title_postfix
if id.has_image(new_title): del id[new_title]
im2 = im.duplicate(new_title)
"""

# Generate ROI masks using PIL Image
mask = array(im.shape, dtype=bool)
x = im.getWidth()
y = im.getHeight()

for roi in im.targeted_ROIs():
    pil_im = Image.new('L', (x, y), 0)
    if roi['type'] == 'Rectangle':
        ImageDraw.Draw(pil_im).rectangle(roi['coordinates'],
                               # FIXME: outline > 1 does not increase thickness
                                         outline=line_width)
    # Convert mask to numpy array
    mask_2d = array(pil_im, dtype=bool)
    
    # TODO: append mask_2d into mask using roi['frame'] as Time dimension 
