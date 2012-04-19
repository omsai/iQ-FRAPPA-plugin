iQ Plugins
==========

FRAPPA ROI display
------------------
Draws the FRAPPA region on iQ images.  This is especially useful for activation or 
stimulation experiments to see the targeted region.  A copy of the image is 
created in the ImageList in which the FRAPPA ROI outline is drawn destructively 
onto the image by setting the pixel intensity to a high value.

.. figure:: http://i.imgur.com/wmzO3.gif
   :alt: photo stimulation

.. figure:: http://i.imgur.com/xd9mm.gif
   :alt: bleaching

Installation
============

The Python IDE searches a specific `Plugins directory`_ to make programs visible in its 
plugins menu.

#. Developers can clone the Git respository into that directory.

   Users can download the release zip file by clicking on "Tags" on the top right, and 
   unpacking in that directory.

#. Now when you restart / start the Python IDE you will always see this 
   program in the plugins menu.

Plugins directory
=================
``C:/Program Files/Andor Bioimaging/PythonEngine/Plugins/``

It was different in iQ 2.4.4 and earlier:

``C:/Program Files/Andor Bioimaging/Plugins/``