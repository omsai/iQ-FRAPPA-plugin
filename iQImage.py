"""
Extends iQImage with `getEventROIs` to extract event ROIs from metadata.
Only works with rectangular ROIs.
"""

import re
from imagedisk import iQImage


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
