PyBM.marine.tools.api
=====================

.. py:module:: PyBM.marine.tools.api


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/PyBM/marine/tools/api/api_calls/index
   /autoapi/PyBM/marine/tools/api/oauth_session/index


Attributes
----------

.. autoapisummary::

   PyBM.marine.tools.api.API_BASE_URL


Classes
-------

.. autoapisummary::

   PyBM.marine.tools.api.MotionRAO
   PyBM.marine.tools.api.SurgeDir
   PyBM.marine.tools.api.SwayDir
   PyBM.marine.tools.api.HeaveDir
   PyBM.marine.tools.api.RollDir
   PyBM.marine.tools.api.PitchDir
   PyBM.marine.tools.api.YawDir
   PyBM.marine.tools.api.WaveOrigin
   PyBM.marine.tools.api.RotationUnit


Functions
---------

.. autoapisummary::

   PyBM.marine.tools.api.get_authenticated_session
   PyBM.marine.tools.api.get_raos
   PyBM.marine.tools.api.get_rao_loadcases
   PyBM.marine.tools.api.get_rao_loadcase


Package Contents
----------------

.. py:class:: MotionRAO(data_vars: xarray.core.types.DataVars | None = None, coords: collections.abc.Mapping[Any, Any] | None = None, attrs: collections.abc.Mapping[Any, Any] | None = None)

   Bases: :py:obj:`PyBM.marine.motion_analysis.RAO.RAO`


   This is the parent class for motion and force RAOs


   .. py:attribute:: __slots__
      :value: ()



   .. py:method:: translate_rao(offset)

      Translates the RAO to a point of interest. Ref[1] eq (4.27)

      :param offset: [m] (x,y,z) offset of the point of interest
      :return: Full vessel motion RAOs around POI



.. py:class:: SurgeDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Surge direction


   .. py:attribute:: FWD
      :value: 1



   .. py:attribute:: AFT
      :value: -1



.. py:class:: SwayDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Sway direction


   .. py:attribute:: PORT
      :value: 1



   .. py:attribute:: STARBOARD
      :value: -1



.. py:class:: HeaveDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Heave direction


   .. py:attribute:: UP
      :value: 1



   .. py:attribute:: DOWN
      :value: -1



.. py:class:: RollDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Roll direction


   .. py:attribute:: PORT_UP
      :value: 1



   .. py:attribute:: PORT_DOWN
      :value: -1



.. py:class:: PitchDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Pitch direction


   .. py:attribute:: BOW_DOWN
      :value: 1



   .. py:attribute:: BOW_UP
      :value: -1



.. py:class:: YawDir(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Yaw direction


   .. py:attribute:: BOW_PORT
      :value: 1



   .. py:attribute:: BOW_STARBOARD
      :value: -1



.. py:class:: WaveOrigin(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Wave direction


   .. py:attribute:: STERN
      :value: 0



   .. py:attribute:: STARBOARD
      :value: 90



   .. py:attribute:: BOW
      :value: 180



   .. py:attribute:: PORT
      :value: 270



.. py:class:: RotationUnit(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Enum for Rotation unit


   .. py:attribute:: DEG_PER_M
      :value: 1



   .. py:attribute:: RAD_PER_M


   .. py:attribute:: DEG_PER_FT
      :value: 3.28084



   .. py:attribute:: DEG_PER_DEG
      :value: 0



   .. py:attribute:: RAD_PER_RAD


.. py:function:: get_authenticated_session()

   Get authenticated session using OAuth2 (browser-based, tokens cached locally)


.. py:data:: API_BASE_URL
   :value: 'https://api.app.barge-master.com'


.. py:function:: get_raos(session=None)

   Get RAOs from API (auto-authenticates if needed)


.. py:function:: get_rao_loadcases(VesselName: str, session=None)

   Get loadcases for a specific RAO from API (auto-authenticates if needed)


.. py:function:: get_rao_loadcase(VesselName: str, Vessel_LC: str, session=None)

   Get specific loadcase details for a RAO from API (auto-authenticates if needed)


