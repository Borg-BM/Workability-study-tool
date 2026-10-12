PyBM.marine.workability.workability_limits
==========================================

.. py:module:: PyBM.marine.workability.workability_limits


Attributes
----------

.. autoapisummary::

   PyBM.marine.workability.workability_limits.cmap


Classes
-------

.. autoapisummary::

   PyBM.marine.workability.workability_limits.workability_accessor


Functions
---------

.. autoapisummary::

   PyBM.marine.workability.workability_limits.directional_workability
   PyBM.marine.workability.workability_limits.directional_workability_timetrace
   PyBM.marine.workability.workability_limits._polar_plotter
   PyBM.marine.workability.workability_limits.multicolored_line
   PyBM.marine.workability.workability_limits.multiple_lines
   PyBM.marine.workability.workability_limits.set_polar_plot_params
   PyBM.marine.workability.workability_limits.plot_ship
   PyBM.marine.workability.workability_limits._make_legend_proxies


Module Contents
---------------

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

