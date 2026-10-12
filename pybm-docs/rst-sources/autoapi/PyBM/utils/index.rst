PyBM.utils
==========

.. py:module:: PyBM.utils


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/utils/data_classes/index
   /autoapi/PyBM/utils/helper_functions/index
   /autoapi/PyBM/utils/mass_items/index
   /autoapi/PyBM/utils/plot_template/index
   /autoapi/PyBM/utils/windows_helpers/index


Classes
-------

.. autoapisummary::

   PyBM.utils.POI
   PyBM.utils.VesselDimensions
   PyBM.utils.massItem
   PyBM.utils.Tower
   PyBM.utils.Stack
   PyBM.utils.VerticalStack
   PyBM.utils.HorizontalStack


Functions
---------

.. autoapisummary::

   PyBM.utils.unwrap_angle
   PyBM.utils.amp_phase_to_complex
   PyBM.utils.disc_area
   PyBM.utils.complex_max
   PyBM.utils.delta
   PyBM.utils.component_absolute
   PyBM.utils.absolute_sum
   PyBM.utils.differentiate
   PyBM.utils.isFileLocked


Package Contents
----------------

.. py:class:: POI

   .. py:attribute:: x
      :type:  float
      :value: 0.0


      [m] x postion (length) 



   .. py:attribute:: y
      :type:  float
      :value: 0.0


      [m] y postion (width) 



   .. py:attribute:: z
      :type:  float
      :value: 0.0


      [m] z postion (height) 



.. py:class:: VesselDimensions

   .. py:attribute:: Length
      :type:  float
      :value: 90.0


      [m] length of vessel, from APP



   .. py:attribute:: Depth
      :type:  float
      :value: 13.0


      [m] depth of vessel, keel to deck



   .. py:attribute:: Draft
      :type:  float
      :value: 7.0


      [m] draft of vessel



   .. py:attribute:: Breadth
      :type:  float
      :value: 20.0


      [m] Breadth of vessel



.. py:function:: unwrap_angle(angle)

   Make sure angle is between 0 and 360.

   :param angle: [deg] angle


.. py:function:: amp_phase_to_complex(amp, phase)

   Convert amplitude / phase representation to complex number

   :param amp: Amplitude
   :param phase: [deg] Phase
   :rtype: Complex


.. py:function:: disc_area(diameter)

   Return area from diameter.

   :param diameter: Diamter of disc
   :return: Area of disc


.. py:function:: complex_max(data: xarray.Dataset, dim)

.. py:function:: delta(steps: numpy.ndarray) -> numpy.ndarray

   Return array of differences, the first value will be 0 to conserve the length.

   :param steps: Array of values
   :type steps: np.ndarray
   :return: Array off diferences
   :rtype: np.ndarray


.. py:function:: component_absolute(x)

   Take the absolute value of the real and imaginary part separatly.

   :param x: Complex number


.. py:function:: absolute_sum(a, b)

   Sum complex numbers as absolute values (to include phase information), for example to get flow from 2 complex velocity signals.
   WARNING: only resulting amplitude is meaningfull.

   :param a: Complex component
   :param b: Complex component
   :return: Magnitude of sum of absolute values. Equivalent to time based: max(abs(signal_a) + abs(signal_b)))


.. py:function:: differentiate(rao, freqs)

   Take the derivate of RAO data

   :param rao: Motion RAO
   :param freqs: [Hz] Frequencies corresponding to the data points
   :return: Time derivative of the data


.. py:class:: massItem

   Represents a mass item with height, mass, and center of gravity properties.


   .. py:attribute:: h
      :type:  float

      [m] height



   .. py:attribute:: m
      :type:  float

      [kg] mass



   .. py:attribute:: h_cog
      :type:  float
      :value: 0


      [m] Height of CoG



   .. py:attribute:: x_cog
      :type:  float
      :value: 0


      [m] Longitudinal offset of CoG



   .. py:attribute:: y_cog
      :type:  float
      :value: 0


      [m] transverse offset of CoG



   .. py:attribute:: I
      :type:  float
      :value: 0


      Inertia around CoG [kg.m2]



   .. py:method:: get_I() -> float

      [kg.m2] Get the inertia around the center of gravity.



   .. py:method:: set_I(value: float)

      [kg.m2] Set the inertia around the center of gravity.



   .. py:method:: I_shifted(offset)

      Get the inertia around an offset point.

      :param offset: [m] distance from stack CoG
      :return: Inertia around offset point [kg.m2]



.. py:class:: Tower

   Bases: :py:obj:`massItem`


   Represents a tower mass item.


   .. py:attribute:: D
      :type:  float
      :value: 0


      [m] Diameter of Tower



   .. py:property:: I

      Get the inertia around the center of gravity of the tower.



.. py:class:: Stack(items)

   Bases: :py:obj:`abc.ABC`


   Abstract base class for a stack of mass items.


   .. py:attribute:: items


   .. py:property:: m

      Get the total mass of the stack.

      :return: The total mass of the stack in units of meters [kg].
      :rtype: float



   .. py:method:: h()
      :abstractmethod:


      [m] Abstract method to get the height of the stack.



   .. py:property:: h_cog

      [m] Get the height of the center of gravity of the stack.



   .. py:property:: x_cog

      [m] Get the longitudinal offset of the center of gravity of the stack.



   .. py:property:: y_cog

      [m] Get the transverse offset of the center of gravity of the stack.



   .. py:property:: I

      Get the inertia around the center of gravity of the stack.

      :return: Inertia around the center of gravity [kg.m2]



   .. py:method:: I_shifted(offset)

      Get the inertia around an offset point.

      :param offset: [m] distance from stack CoG
      :return: Inertia around offset point [kg.m2]



   .. py:method:: __str__() -> str

      Get a string representation of the stack.



.. py:class:: VerticalStack(items, cog_factor=1.0)

   Bases: :py:obj:`Stack`


   Represents a vertical stack of mass items.


   .. py:property:: h

      [m] Get the height of the vertical stack.



.. py:class:: HorizontalStack(items, spacing, cog_factor=1.0)

   Bases: :py:obj:`Stack`


   Represents a horizontal stack of mass items.


   .. py:property:: h

      [m] Get the height of the horizontal stack.



   .. py:method:: __str__() -> str

      Get a string representation of the horizontal stack.



.. py:function:: isFileLocked(filePath)

   Source: https://stackoverflow.com/questions/13371444/python-check-file-is-locked
   Checks to see if a file is locked. Performs three checks
       1. Checks if the file even exists
       2. Attempts to open the file for reading. This will determine if the file has a write lock.
           Write locks occur when the file is being edited or copied to, e.g. a file copy destination
       3. Attempts to rename the file. If this fails the file is open by some other process for reading. The
           file can be read, but not written to or deleted.
   :param filePath: path of file to check


