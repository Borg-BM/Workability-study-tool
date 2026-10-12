PyBM.marine.workability
=======================

.. py:module:: PyBM.marine.workability


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/marine/workability/workability_limits/index


Attributes
----------

.. autoapisummary::

   PyBM.marine.workability.cmap


Classes
-------

.. autoapisummary::

   PyBM.marine.workability.Machine_Linear
   PyBM.marine.workability.Machine_Nonlinear
   PyBM.marine.workability.workability_accessor


Functions
---------

.. autoapisummary::

   PyBM.marine.workability.directional_workability
   PyBM.marine.workability.directional_workability_timetrace
   PyBM.marine.workability._polar_plotter
   PyBM.marine.workability.multicolored_line
   PyBM.marine.workability.multiple_lines
   PyBM.marine.workability.set_polar_plot_params
   PyBM.marine.workability.plot_ship
   PyBM.marine.workability._make_legend_proxies


Package Contents
----------------

.. py:class:: Machine_Linear(position, orientation)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: pos


   .. py:attribute:: orient


   .. py:attribute:: rotation


   .. py:method:: apply_transform(point: numpy.array) -> numpy.array

      Apply rotation then translation to 3D point

      :param point: 3D vector [x,y,z]
      :type point: np.array
      :return: Transformed position
      :rtype: np.array



   .. py:method:: get_rao_at_poi(rao) -> PyBM.marine.motion_analysis.MotionRAO.MotionRAO

      Get the Motion RAOs at the POI



   .. py:method:: get_POI() -> dict
      :abstractmethod:



   .. py:method:: apply_machine_dofs(rao) -> PyBM.marine.motion_analysis.MotionRAO.MotionRAO


   .. py:method:: get_workability_limit(motion_at_poi, **kwargs)


   .. py:method:: __str__() -> str


.. py:class:: Machine_Nonlinear(position, orientation)

   Bases: :py:obj:`abc.ABC`


   Helper class that provides a standard way to create an ABC using
   inheritance.


   .. py:attribute:: pos


   .. py:attribute:: orient


   .. py:attribute:: rotation


   .. py:method:: apply_transform(point: numpy.array) -> numpy.array

      Apply rotation then translation to 3D point

      :param point: 3D vector [x,y,z]
      :type point: np.array
      :return: Transformed position
      :rtype: np.array



   .. py:method:: get_POI() -> dict
      :abstractmethod:



.. py:data:: cmap

.. py:class:: workability_accessor(obj)

   .. py:attribute:: _obj


   .. py:method:: table(Hs, Hsrange)


   .. py:method:: byscatter(scatter)


   .. py:method:: plot_detailed_workability(max_hs=None, fig=None)

      Plot workability for each system limit.

      :param workability_result: _description_
      :type workability_result: xr.DataArray
      :param max_hs: _description_, defaults to None
      :type max_hs: _type_, optional
      :param fig: _description_, defaults to None
      :type fig: _type_, optional



   .. py:method:: plot_combined_workability(max_hs=None, fig=None)

      Plot the result of the workability in polar plots

      :param workability_result: [m] Array of limiting Hs for each wave peak period, direction and machine limit.
      :param max_hs: [m] maximum Hs on the polar plot, defaults to None
      :param fig: figure to plot on, defaults to None



.. py:function:: directional_workability(rao: PyBM.marine.MotionRAO, wave: PyBM.marine.WaveSpectrum, machine: PyBM.marine.machines.Machine_Linear, **kwargs) -> xarray.DataArray

   Compute the workability of the machine for the given wave directions.

   :return: [m] Array of limiting Hs for each wave peak period, direction and machine limit.


.. py:function:: directional_workability_timetrace(trace: xarray.DataArray, machine: PyBM.marine.machines.MCG30.MCG30_Nonlinear, **kwargs) -> xarray.DataArray

   Compute the workability of the machine using the time trace supplied (MCG)

   :return: [m] Array of limiting Hs for each wave peak period, direction and machine limit.


.. py:function:: _polar_plotter(plot_method, workability_result: xarray.DataArray, max_hs=None, fig: matplotlib.figure.Figure = None)

.. py:function:: multicolored_line(ax: matplotlib.pyplot.Axes, Tp_result)

.. py:function:: multiple_lines(ax: matplotlib.pyplot.Axes, Tp_result)

.. py:function:: set_polar_plot_params(ax: matplotlib.pyplot.Axes, max_y, Tp)

.. py:function:: plot_ship(ax: matplotlib.pyplot.Axes, plot_diameter=1.0)

   Plot a ship contour on the given axis.

   :param axs: Axes to plot on.
   :param plot_diameter: diameter of vessel contour, defaults to 1.0


.. py:function:: _make_legend_proxies(cmap, **kwargs)

