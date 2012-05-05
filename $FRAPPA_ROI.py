#SHELL
'''
Extracts rectangular FRAPPA ROIs from image metadata, duplicates the original
image and draws bitmap ROIs on duplicate image for each FRAPPA event.
'''

import re
import numpy as nd
import iqtools, imagedisk
import imp



class iQImage(iQImage):
	
	def __init__(self):
		super(iQImage, self).__init__()
	
	
	def getEventROIs(self):
		'''
		Return ROIs from event markers in image metadata.
		
		Note:
		- Events can have multiple ROIs and multiple types of ROIs (rectangle, 
		  freehand, polygon, straight line, multipoint line, freehand line)
		- Presently only a single rectangle coordinates are extracted in the
		  form: [x1, y1, x2, y2]
		
		@rtype: dictionary of frame number and coordinate list
		'''
		
		try:
			raw_event_markers = self.getDetails()[0]['Event Markers']
		except KeyError: # No [Event Markers] found in image metadata
			return {} # Empty dictionary
		
		# Separate markers into list type
		separators = ['\n\n', '\n\r\n']
		for separator in separators:
			if separator in raw_event_markers:
				event_list = raw_event_markers.split(separator)
		
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
			lines = event.splitlines()
			roi_found = False
			roi_frame = event_list.index(event) + 1
			
			for line in lines:
				try:
					coordinate_set = coordinate_pattern.search(line)
				except:
					raise ValueError('Regex failed on %s' % line)
			
				try:
					result = list(coordinate_set.groups())
					if roi_found:
						values[-1] += [map(int, result)] # convert coordinates str to int
					else:
						values += [[map(int, result)]] # convert coordinates str to int
						roi_found = True
				except AttributeError:
					pass # No regex result
				
			print 'Event %d coordinates:' \
					% (roi_frame), values[-1]
	
		keys = frames
	
		return dict(zip(keys, values))


	def drawEventROIs(self, value=16000, line_width=2, channel_dim=1):
		'''
		Inject ROI outline into imageset
		
		@param value: pixel intensity of ROI outline
		@type value: int
		@param line_width: width of ROI outline
		@param line_width: int
		@param channel_dim: wavelength dimension in ndarray
		@type channel_dim: int
		@rtype: None
		'''
		
		if line_width <= 0:
			return
	
		for index, rois in self.getEventROIs():
			for [x1, y1, x2, y2] in rois:
				
				orig =	self.__getitem__(
							index,
							0,
							x1+line_width:x2-line_width,
							y1+line_width:y2-line_width
						)
				
				self.__setitem__(
					index,
					int(shape[channel_dim]-1),
					x1:x2,
					y1:y2) = value
				
				self.__setitem__(
					frame,
					0,
					x1+line_width:x2-line_width,
					y1+line_width:y2-line_width
				) = orig



if __name__ == "__main__":
	
	id = imagedisk.iQImageDisk()
	
	# Run Qt GUI here to select image
	
	im.duplicate(im2)
	im2.drawEventROIs()
