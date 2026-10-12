PyBM.marine.tools.read_res
==========================

.. py:module:: PyBM.marine.tools.read_res

.. autoapi-nested-parse::

   This file reads .res output files from aNySIM and returns a dictionary with all the data



Functions
---------

.. autoapisummary::

   PyBM.marine.tools.read_res.__file_len
   PyBM.marine.tools.read_res.resample
   PyBM.marine.tools.read_res.__read_file
   PyBM.marine.tools.read_res.read_res
   PyBM.marine.tools.read_res.write_pickle
   PyBM.marine.tools.read_res.write_res


Module Contents
---------------

.. py:function:: __file_len(fname)

.. py:function:: resample(data, new_dt, data_dt)

.. py:function:: __read_file(filename, read_invalid=True)

.. py:function:: read_res(filename, dt=0, read_invalid=True)

   Read a text .res file with time traces.

   :param filename: name of file without extension
   :param dt: [s] sample time, if 0 the original sample time is used
   :param read_invalid: [bool] If false, invalid files are moved to Invalid folder
   :return: Dictionary of time_vectors.


.. py:function:: write_pickle(filename, data_dict)

.. py:function:: write_res(filename, data_dict)

   Write a data dictionary to a .res text file.

   :param filename: name of file (without extension)
   :param data_dict: dictionary of key / time_vector pairs


