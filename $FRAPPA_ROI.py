#SHELL
"""
Draws bitmap ROIs from each event onto duplicated image.
"""
from imagedisk import iQImageDisk
from iQImage import *
from PIL import Image, ImageDraw
from numpy import array, zeros

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

# Make a copy of that image
new_title = im.title + title_postfix
if id.has_image(new_title): del id[new_title]
im2 = im[:]

# Generate ROI masks using PIL Image
mask = zeros(im.shape, dtype=bool)
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
    # Get dimensions except x and y, so that x and y can be overwritten
    dimensions = len(im.shape[:-2])
    # Create index defaulting to zero
    index = [0] * dimensions
    # use roi['frame'] as Time dimension 
    index[im.dimPosition('Time')] = roi['frame']
    # write mask_2d into mask
    mask[index] = mask_2d

im2[mask] = intensity
im3 = id.newImage(new_title, im2, im.getDimNames())
