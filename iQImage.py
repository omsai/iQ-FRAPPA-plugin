"""
Monkey patches iQImage with `targeted_ROIs` generator to extract FRAPPA event
ROI metadata.

>>> id = iQImageDisk()
>>> im = iQImage(id, 'frap2.tif')
>>> print im.targeted_ROIs()
<generator object _targeted_ROIs at 0x01578FD0>
>>> for roi in im.targeted_ROIs():
... print roi
{'frame': 5, 'type': 'Rectangle', 'coordinates': [189, 66, 244, 94]}
{'frame': 4, 'type': 'Rectangle', 'coordinates': [167, 295, 222, 323]}
{'frame': 3, 'type': 'Rectangle', 'coordinates': [181, 293, 236, 321]}
{'frame': 2, 'type': 'Rectangle', 'coordinates': [237, 191, 292, 219]}
"""

from imagedisk import iQImage
import re

def _targeted_ROIs(self):
    """
    ROI metadata from FRAPPA event markers.
    @rtype: dictionary of frame number, ROI type and coordinates
    """
    try:
        event_markers = self.getDetails()[0]['Event Markers']
    except KeyError: # No [Event Markers] found in image metadata
        yield []
    event_lines = event_markers.splitlines()
    
    # Traverse list backwards since location line comes after ROI coordinates
    event_lines.reverse()
    ROI_types = ['Rectangle']
    frame = None
    
    for event_line in event_lines:
        # match number preceded by `Time(`
        match = re.search(r'(?<=Time[(])\d+', event_line)
        if match is not None:
            frame = int(match.group())
            continue
        elif frame == None:
            continue
        
        # match all x, y number pairs in the form `( x, y)`
        pattern = re.compile(r'(?<=[(] )\d+(?![)])|(?<=[,] )\d+(?=[)])')
        """
        pattern explanation:
            (?<=[(] )\d+    # match a number preceded with `( ` ...
            (?![)])         # ... as long as it does not have a `)` after
            |               # or
            (?<=[,] )\d+    # match a number preceded with `, ` ...
            (?=[)])         # ... as long as it has a `)` after
        could not use re.VERBOSE as it doesn't seem to work with the
        (?...) extension notation
        """
        coordinate_string_list = re.findall(pattern, event_line)
        if coordinate_string_list == []:
            continue
        coordinates = map(int, coordinate_string_list)

        type = 'Unknown'
        for ROI_type in ROI_types:
            if re.search(ROI_type, event_line):
                type = ROI_type
                break

        yield dict(
            frame = frame,
            type = type,
            coordinates = coordinates
            )

iQImage.targeted_ROIs = _targeted_ROIs


if __name__ == '__main__':
    from imagedisk import iQImageDisk
    id = iQImageDisk()
    im = iQImage(id, 'frap2.tif')
    print im.targeted_ROIs()
    
    for roi in im.targeted_ROIs():
        print roi
