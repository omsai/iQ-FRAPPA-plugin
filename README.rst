iQ FRAPPA Plugin
================
Draws the FRAPPA region on iQ images.  This is especially useful for activation or 
stimulation experiments to see the targeted region.  A copy of the image is 
created in the ImageList in which the FRAPPA ROI outline is drawn destructively 
onto the image by setting the pixel intensity to a high value.

.. figure:: http://i.imgur.com/wmzO3.gif
   :alt: photo stimulation

.. figure:: http://i.imgur.com/xd9mm.gif
   :alt: bleaching

Installation
------------
#. `Download a release <https://github.com/omsai/iQ-FRAPPA-plugin/tags>`_
   and unzip in the plugins directory.  Developers may instead want to clone this
   Git respository into the plugins directory.

#. Plugins directory for iQ 2.5.0 and above:
   ``C:/Program Files/Andor Bioimaging/PythonEngine/Plugins/``

   For iQ 2.4.4 and earlier:
   ``C:/Program Files/Andor Bioimaging/Plugins/``

#. Now when you restart / start the Python IDE you will always see this 
   program in the plugins menu.