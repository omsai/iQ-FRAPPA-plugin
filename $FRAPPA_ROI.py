#SHELL
"""
Draws bitmap ROIs from each event onto duplicated image.
"""

from imagedisk import iQImageDisk
from iQImage import *
from gui import *


def drawEventROIs(im, intensity=16000, line_width=2, channel_dim=1):
    """
    Inject ROI outline into images

    @param im: pixel intensity of ROI outline
    @type im: iQImage
    @param intensity: pixel intensity of ROI outline
    @type intensity: int
    @param line_width: width of ROI outline
    @type line_width: int
    @param channel_dim: wavelength dimension position in ndarray
    @type channel_dim: int
    @rtype: None
    """
    if line_width <= 0:
        return

    for index, rois in im.getEventROIs():
        # TODO: Draw other ROI shapes besides rectangle
        for [x1, y1, x2, y2] in rois:
            # Copy original data before filling
            orig = im[index, 0,
                x1 + line_width:x2 - line_width,
                y1 + line_width:y2 - line_width]
            # Fill rectangle
            im[index, int(im.shape[channel_dim] - 1),
               x1:x2, y1:y2] = intensity
            # Fill in with original data
            im[index, 0,
               x1 + line_width:x2 - line_width,
               y1 + line_width:y2 - line_width] = orig


if __name__ == "__main__":
    app.QApplication(sys.argv)
    imageList = ImageList()
    imageList.show()
    im = iQImage(iQImageDisk(), app.exec_())

    im2 = im.duplicate(im.title + '_drawEventROIs')
