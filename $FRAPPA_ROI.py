#SHELL
"""
Draws bitmap ROIs from each event onto duplicated image.

Extends iQImage with `getEventROIs` to extract event ROIs from metadata.
Only works with rectangular ROIs.
"""

import re
from imagedisk import iQImage, iQImageDisk


class iQImage(iQImage):
    def __init__(self, iQImageDisk, title):
        super(iQImage, self).__init__(iQImageDisk, title)


    def getEventROIs(self):
        """
          Generate ROIs from event markers in image metadata.

          Note:
          - Events can have multiple ROIs and multiple types of ROIs (rectangle,
            freehand, polygon, straight line, multipoint line, freehand line)
          - Presently only a single rectangle coordinates are extracted in the
            form: [x1, y1, x2, y2]

          @rtype: dictionary of frame number and coordinate list
          """

        try:
            event_markers = self.getDetails()[0]['Event Markers']
        except KeyError: # No [Event Markers] found in image metadata
            return

        # regex pattern to extract ROI coordinates and event frame
        pattern = re.compile(r'''
		\:\D*       # colon precedes each coordinate match in event
		(\d{1,4})   # x1
		\D*         # non-digits
		(\d{1,4})   # y1
		\D*         # non-digits
		(\d{1,4})   # x2
		\D*         # non-digits
		(\d{1,4})   # y2
		''', re.VERBOSE)

        # TODO: Extract multiple coordinates per event
        for match in re.finditer(pattern, event_markers):
            yield [map(int, match)] # convert coordinates str to int


def drawEventROIs(im, intensity=16000, line_width=2, channel_dim=1):
    """
     Inject ROI outline into images

     @param im: pixel intensity of ROI outline
     @type im: iQImage
     @param intensity: pixel intensity of ROI outline
     @type intensity: int
     @param line_width: width of ROI outline
     @param line_width: int
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
    id = iQImageDisk()

    # TODO: Run Qt GUI here to select image
    im = id['test image']

    im2 = im.duplicate(im.title + '_drawEventROIs')
    drawEventROIs(im2)
