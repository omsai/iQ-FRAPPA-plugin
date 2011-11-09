#SHELL
'''
Extracts rectangular FRAPPA ROIs from image metadata, duplicates the original
image and draws bitmap ROIs on duplicate image for each FRAPPA event.

Input:
  Name of image in ImageList,
  Ordered list of frame numbers of event markers
Output:
  New image in ImageList

Written by Pariksheet Nanda <p.nanda@andor.com> Sep 2011
'''

DEMO_MODE = False # read metadata text file only; images not available
DEBUG = False

# Magic Numbers
ROI_LINE_THICKNESS = 2 # Thickness of 0 will fill the ROI completely
ROI_FILL_VALUE = 16000
FILE_FOR_ROIs = True
TIME_DIM = 0
CHANNEL_DIM = 1 # Wavelength is at position 1 in the ndarray for timelapse data
                # i.e. of the shape (time, wavelength, x, y)
# END: Magic Numbers

import re
import numpy as nd
import iqtools, imagedisk
import imp


def selectImage(imdsk):
  '''
  User input of dataset to process
  '''
  try:
    im = iqtools.dialogs.getDataset(imdsk)
  except ValueError:
    raise Exception, 'ImageDisk empty, nothing to export.'
  
  if im == None:
    print 'No image selected.'
    return None
  
  unsupported=[]
  for dim in im.dimNames:
    if dim.lower() not in ['time', 'wavelength', 'x', 'y']:
      unsupported.append(dim)
  
  if len(unsupported) > 0:
    for dim in unsupported:
      print 'ERROR: Cannot use selected image. Contains unsupported',
      print 'dimension %s' % dim
    return None
  
  return im


def getROIs(im4d,
             frames,
             file=None):
  '''
  Return FRAPPA ROIs from event markers in image metadata.
  
  Returns dictionary object of FRAPPA numeric coordinates:
    Key = frame number of event in the dataset
    Value for e.g. Rectangle = [x1, y1, x2, y2]

  - Events can have multiple ROIs and multiple types of ROIs (rectangle, 
    freehand, polygon, straight line, multipoint line, freehand line)
  - Presently only a single rectangle ROI is extracted
  '''
  print 'Extracting ROI metadata...'
  
  if file == None:
    # Get raw event marker string from image
    try:
      raw_event_markers = im4d.getDetails()[0]['Event Markers']
    except KeyError:
      print 'WARNING: No [Event Markers] found in image metadata'
      return {} # Empty dictionary
  else:
    f = open(file, 'r')
    metadata = f.readlines()
    try:
      start = metadata.index('[Event Markers]\n')
      end = metadata.index('[Event Markers End]\n')
      metadata = metadata[start+1:end]
      raw_event_markers = ''.join(string for string in metadata)
    except ValueError:
      print 'WARNING: No [Event Markers] found in file'
      return {}
  
  if DEBUG:
    print 'DEBUG: raw_event_markers:', raw_event_markers
  
  # Separate markers into list type
  separators = ['\n\n', '\n\r\n']
  for separator in separators:
    if separator in raw_event_markers:
      event_list = raw_event_markers.split(separator)
  
  print 'Events found:', len(event_list)
  
  coordinate_pattern= re.compile(r'''
  \:\D*       # colon precedes each coordinate match in event
  (\d{1,4})   # x1
  \D*         # non-digits
  (\d{1,4})   # y1
  \D*         # non-digits
  (\d{1,4})   # x2
  \D*         # non-digits
  (\d{1,4})   # y2
  ''', re.VERBOSE)
  
  values = []
  for event in event_list:
    if DEBUG:
      print 'DEBUG: Attempting Regex on event:', repr(event)
    
    lines = event.splitlines()
    roi_found = False
    roi_frame = event_list.index(event) + 1
    
    for line in lines:
      try:
        coordinate_set = coordinate_pattern.search(line)
      except:
        print 'ERROR: Regex failed'
        raise
      
      try:
        result = list(coordinate_set.groups())
        if DEBUG:
          print 'DEBUG: Regex groups() result: ', result
        if roi_found:
          values[-1] += [map(int, result)] # convert coordinates str to int
        else:
          values += [[map(int, result)]] # convert coordinates str to int
          roi_found = True
      except AttributeError:
        if DEBUG:
          print 'DEBUG: No regex result for line:', repr(line)
        
    print 'Event %d coordinates:' \
            % (roi_frame), values[-1]
  
  keys = frames
  
  print 'Number of event_list:', len(event_list)
  print 'Number of keys:', len(keys)
  print 'Number of values:', len(values)
  
  return dict(zip(keys, values))


def selectNumberWithRange(title, message):
  '''
  User input of FRAPPA frame numbers in the form 1,2,3-5
  '''
  frame_string = iqtools.dialogs.getInput('', message, title)
  
  # Make a list from the string
  print 'Frame string from user:', repr(frame_string)
  
  re.sub(frame_string, ' ', '')
  if DEBUG:
    print 'Stripped space characters:', repr(frame_string)
  
  frame_list = frame_string.split(',')
  if DEBUG:
    print 'Split into frames and ranges:', repr(frame_list)
  
  frames = []
  for frame_set in frame_list:
    try:
      if DEBUG:
        print 'DEBUG: Before hyphen split:', repr(frame_set)
      frame_set = frame_set.split('-')
      if DEBUG:
        print 'DEBUG: After hyphen split:', repr(frame_set)
      if len(frame_set) > 1:
        [begin, end] = frame_set
        begin = int(begin)
        end = int(end)
        frames += range(begin, end+1)
      else:
        frame_set = int(frame_set)
        frames += frame_set
    except ValueError:
      raise
  
  if DEBUG:
    print 'Parsed frames and ranges into numeric list:', frames
  
  return frames


def imDuplicate(im,
                  imdsk,
                  title_extension='_ROI_same_channel',
                  channel_label='ROI'):
  '''
  Duplicates image in ImageList creating a unique name in iQ's style of
  appending an integer increment to existing names
  '''
  base_name = im.title + title_extension
  name = base_name
  i = 1
  
  while imdsk.has_image(name):
    name = base_name + str(i)
    i += 1
  
  print 'Creating new image with additional ROI channel %s...' % name
  imroi = im.duplicate(name)
  
  return imroi


def drawROIs(im4d,
               roi_dictionary):
  '''
  Use ROI dictionary to fill rectangles into ROI channel of dataset
  '''
  shape = im4d.shape
  print 'Drawing FRAPPA ROIs:'
  
  for frame, rois in roi_dictionary.items():
    for [x1, y1, x2, y2] in rois:
    # Process frames one at a time
      print '- Frame %d with rectangle (%d,%d) (%d,%d)' % \
             (frame, x1, y1, x2, y2)
      orig = im4d[frame, 0,
                  x1+ROI_LINE_THICKNESS:x2-ROI_LINE_THICKNESS,
                  y1+ROI_LINE_THICKNESS:y2-ROI_LINE_THICKNESS]
      im4d[frame, shape[CHANNEL_DIM]-1, x1:x2, y1:y2] = ROI_FILL_VALUE
      if ROI_LINE_THICKNESS > 0:
        im4d[frame, 0,
             x1+ROI_LINE_THICKNESS:x2-ROI_LINE_THICKNESS,
             y1+ROI_LINE_THICKNESS:y2-ROI_LINE_THICKNESS] = orig


if __name__ == '__main__':
  
  if not DEMO_MODE:
    id = imagedisk.iQImageDisk()
    im = selectImage(id) # Select FRAPPA dataset
    print 'Image:', im
  else:
    print 'WARNING: Demo mode enabled.'
    print '         Only text file of metadata will be read.'
    print '         No image set will be read or created.'
    im = None
  
  if im is not None or DEMO_MODE is True:
    EVENT_FRAMES = selectNumberWithRange('Event numbers',
                                         'Type frame numbers of FRAPPA events\n'+
                                         'eg: 1-5,9-11,15,17'
                                        )
    print '%d event frames specified by user' % len(EVENT_FRAMES)
    if DEBUG:
      print 'DEBUG: EVENT_FRAMES:', EVENT_FRAMES
    file = None
    
    if FILE_FOR_ROIs:
      file = iqtools.dialogs.getFile('Choose iQ metadata file or click '+\
                                      'Cancel to use image metadata',
                                     'iQ Metadata (*.txt)|*.txt')
    if file == u'': # You get this if you click cancel to the dialogue
      file = None
    
    if file is None and DEMO_MODE is True:
      print 'ERROR: No file selected.  Exiting demo mode.'
    else:
      print 'ROI file selection: ', repr(file)
      rois = getROIs(im, EVENT_FRAMES, file)
      print '%d ROIs found in metadata' % len(rois)
      if DEBUG:
        print 'ROIs:', rois
      if len(rois) < len(EVENT_FRAMES):
        print 'WARNING: Fewer ROIs found than expected EVENT_FRAMES'
      if not DEMO_MODE:
        im2 = imDuplicate(im, id) # Duplicate image with safe name
        drawROIs(im2, rois)
  
  print 'Finished script'
  
  # Kludge: selectImage only can be run once in a Python IDE session
  if not DEMO_MODE:
    iqtools.dialogs.msg('Close the main IDE window if you want to '+\
                         're-run this script',
                         'Finished script')
