.. OUT OF USE, REPLACED BY IMPORTING_RAO_TOOL.RST

.. Importing RAOs into the Vessel Motions Library
.. ----------------------------------------------

.. Creating the folder
.. *******************

.. The folder for the RAOs should be located in *O:\\Engineering\\Database\\Vessel Motions\\Vessel RAOs and time traces*.
.. Copy the *_DEFAULT FOLDER* and change name to the vessel name. Note that the following characters should be avoided:
.. ``<space>#%&{}\`<>*?/$!'":@+|-``

.. | The folder will have the following structure:
.. | ├───Original data
.. | │   ├───RAO Rev0
.. | │   └───Time traces Rev0
.. | └───Processed data
.. |     ├───PyBM Rev0
.. |     ├───RAO Rev0
.. |     └───Time traces Rev0

.. Place the RAOs as received from the client in *Original data\\RAO Rev0\\*
.. The structured RAO data will be placed in *Processed data\\RAO Rev0\\*
.. The code to import the data to Xarray format used by PyBM (stored as .nc file), as well as the .nc file itself, will be in *Processed data\\PyBM Rev0\\*.

.. Importing the RAO
.. *********************************

.. The next step is to structure the RAO into a format that we can easily import using the import tools that PyBM has.
.. Herein we have two options:

.. 1. LIS file importer (:meth:`PyBM.marine.tools.LIS_to_Xarray`)
.. 2. XLS file importer (:meth:`PyBM.marine.tools.XLS_to_Xarray`)

.. Structuring XLS file for import
.. ===============================

.. An example of a correctly structured XLS file for import is

.. *O:\\Engineering\\Database\\Vessel Motions\\Vessel RAOs and time traces\\Example Vessel\\Processed Data\\RAOs Rev0\\RAO_combined.xls*

.. Important things to note about this file:

.. - Note that the file must be in XLS format, instead of XLSX. This is the older, 93-2003 Excel workbook format.
.. - All data must be combined on the first sheet. The RAO can be defined per heading direction, given in degrees.
.. - The data arrays must have the columns in the following order:

..     1. Wave Frequency (rad/s)
..     2. Surge amplitude (m/m)
..     3. Surge Phase (deg)
..     4. Sway amplitude (m/m)
..     5. Sway Phase (deg)
..     6. Heave amplitude (m/m)
..     7. Heave Phase (deg)
..     8. Roll amplitude (deg/m)
..     9. Roll Phase (deg)
..     10. Pitch amplitude (deg/m)
..     11. Pitch Phase (deg)
..     12. Yaw amplitude (deg/m)
..     13. Yaw Phase (deg)

.. This means that if a RAO is delivered in a different way (for example, each DoF (surge, sway, ...) in a different sheet), it must be manually sorted into the above structure.

.. Importing XLS file
.. ==================

.. After sorting the data into the correct structured XLS file, the python import file can be prepared. See the example file below:

.. .. code-block:: python
..     :linenos:

..     from PyBM.marine.tools import XLS_to_RAO
..     from PyBM.marine import *
..     from pathlib import Path

..     dir_path = Path(__file__).parent
..     original_rao = dir_path.parents[1] / "Original data" / "RAO Rev0" / "SARTOR_RAO_APRIL2023.xlsx"
..     VesselName = "Sartor"
..     loading_condition = "Sartor/Draft_4.35/KG_6.30"
..     CoG = [35.192, 0, 6.3] # Wr.t. APP, Centerline, Keel

..     if __name__ == '__main__':
..         rao = XLS_to_RAO(original_rao, VesselName, loading_condition, CoG, mirror=False)
..         rao.modify_conventions(SurgeDir.AFT, SwayDir.STARBOARD, HeaveDir.UP, RollDir.PORT_DOWN, PitchDir.BOW_UP, YawDir.BOW_PORT)
..         rao.save_rao(os.path.join(dir_path, f"{VesselName}.nc"))
..         print("done")

.. Note that the conventions must be defined correctly as seen in line 15 of the above example code. PyBM will consequently correctly transform the RAO to the :ref:`conventions <conventions:Conventions>` as used in PyBM.


.. Importing LIS file
.. ==================

.. .. code-block:: python
..     :linenos:

..     from PyBM.marine.tools import LIS_to_RAO
..     from PyBM.marine import *
..     from pathlib import Path

..     Revision = 0

..     dir_path = Path(__file__).parent
..     filename_RAO = dir_path.parents[1] / "Original data\RAO Rev0\ALLC_0_DP3_BARGE_400FT_FOU.LIS"
..     VesselName = "Marmac400"

..     if __name__ == '__main__':
..         rao = LIS_to_RAO(filename_RAO, VesselName)
..         save_location = rao.default_rao_path(VesselName, Revision)
..         rao.save_rao(save_location)
..         print("done")
