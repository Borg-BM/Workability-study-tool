RAO Import Tool
=================

The RAO Import Tool is a Python-based web application for importing, visualizing, checking, and uploading Response Amplitude Operators (RAOs) from various file types.
This is a user-friendly interface for managing vessel RAO data and storing it in a MongoDB database. PyBM also contains an integration to easily import RAOs from this database.

.. image:: ../images/rao_workflow.png
    :alt: rao_workflow
    :align: center

|

For more information on how the application is built, please refer to the `RAO Import Tool GitHub repository <https://github.com/Barge-Master/rao-import-tool>`_.

**Key features**

- Import RAOs from multiple file formats (Excel, CSV, TXT, LIS, Octopus)
- Visualize amplitude and phase plots
- Comprehensive RAO quality checks and validation
- Data convention management
- Dual mode operation: Upload mode and Check mode
- MongoDB integration to upload RAOs for easy access in PyBM (no more storing in the local Vessel Motions Library folder)

Usage
######

Creating the folder
------------------------------

The folder for the RAOs should be located in *O:\\Engineering\\Database\\Vessel Motions\\Vessel RAOs and time traces*.
Copy the *_DEFAULT FOLDER* and change name to the vessel name. Note that the following characters should be avoided:
``<space>#%&{}\`<>*?/$!'":@+|-``

| The folder will have the following structure:
| ├───Original data
| │   ├───RAO Rev0
| │   └───Time traces Rev0
| └───Processed data
|     ├───PyBM Rev0
|     ├───RAO Rev0
|     └───Time traces Rev0

Place the RAOs as received from the client in *Original data\\RAO Rev0\\*
The structured RAO data (e.g., reformatted Excel file) will be placed in *Processed data\\RAO Rev0\\*
This is for archiving, and to store the original data as received.

Accessing the RAO Import Tool
------------------------------

The RAO Import Tool can be accessed via the main BM Apps landing page: `https://apps.barge-master.com/ <https://apps.barge-master.com/>`_, and by clicking on **RAO Import Tool**.
Alternatively, you can directly access the tool via: `https://rao-importer.app.barge-master.com/ <https://rao-importer.app.barge-master.com/>`_. In either case, you will be asked to log in with your BM credentials. Do so by selecting the Microsoft logo option.

.. image:: ../images/login_rao_import_tool.png
    :alt: login_rao_import_tool
    :align: center

|

Upload mode
------------

This mode concerns the addition of **new** RAOs to the database. The main workflow is as follows:

1. Select **"Upload"** mode in the toggle option (selected by default when the app is initially launched). 

2. Click the **“Plus”** icon in the *Import File* area to select a file containing RAO data.

3. Navigate to the RAO file, click **Open**, and upload it by clicking the **"Cloud"** icon after.

4. You will be prompted to select the appropriate file type from the dropdown menu. You can read more about file formats and examples of each in the section :ref:`sec-file-formats`. For Excel, CSV, and TXT files, you will also need to specify subsequently if you want the mirroring option or not. Choose mirroring if there's only data for one of the sides of the vessel (e.g. 0 to 180 degrees).

5. Enter the **Vessel Name** and **Loading Condition** in the respective fields. Names should not contain spaces or special characters. Press *Enter* after each input or click the **Confirm** button, otherwise the input is not saved! You can verify this in the title, as the title will become "Importing RAOs for {Vessel Name} @ {Loading Condition}".

6. Configure DOF conventions (Surge, Sway, Heave, Roll, Pitch, Yaw), wave origin, phase, and rotation unit. These should match the RAO data being imported and are crucial for ensuring that the RAO data aligns with PyBM conventions.

7. Specify RAO origin coordinates (X, Y, Z) relative to the vessel's reference point (APP, Centerline, Keel). Press *Enter* after each input or click the **Confirm** button, otherwise the input is not saved!

8. Click **Run Analysis** to generate RAO amplitude and phase plots for each DOF.

9. Click **Run RAO Quality Checks** to validate the data. *Please note that these checks are just general guidelines. They do not guarantee 100% correctness, and similarly, the RAO could still be correct even if some checks fail. For extra information on these checks, please see* `Orcaflex website <https://www.orcina.com/webhelp/OrcaFlex/Content/html/Vesseltheory,RAOqualitychecks.htm>`_.

10. If you are not happy with the outcome, feel free to change the conventions and then click **Rerun Analysis (and RAO checks)**. You can do this as many times as you want until you are satisfied with the results.

11. Hopefully with all checks passed, you can enter your name acronym (XXX) and click **Upload Results** to store the RAO in the MongoDB database. *If some RAO quality checks have failed, you will be prompted to choose an R&D member to be contacted via e-mail to check the RAO.*

.. image:: ../images/rao_email.png
    :alt: rao_email
    :align: center

|

12. Upon successful upload, you will be notified on the screen, and you can safely close the app after. 

Check mode
-----------

This mode is intended to review and revise the RAOs that have already been imported to the database. The main workflow is as follows:

1. Select **"Check"** mode in the toggle option.

2. Click **Load From MongoDB**.

3. In the popup window, select the **Vessel Name** and **Loading Condition** from the dropdown menus. This will load the RAO with the saved conventions and origin.

4. Click **Run Analysis** to generate RAO amplitude and phase plots for each DOF.

5. Click **Run RAO Quality Checks**.

6. Review results. Two scenarios are possible:

   - If all checks pass and everything looks correct, you don't have to do anything, the RAO is already in the database.

   - If some checks fail, you can modify the conventions and origin as appropriate and click **Rerun Analysis (and RAO checks)** to regenerate plots and re-evaluate the RAO quality checks with the updated conventions.

        1. If you are satisfied with the updated conventions and all RAO quality checks pass, enter your name acronym (XXX), click **Upload Results** and choose **Overwrite** to correct the RAO on the database.

**Note:** No new revisions of the same loading condition are allowed, as the RAO of a loading condition is either correct or not. If there is "another correct" RAO, please create a new loading condition for it.

.. _sec-file-formats:

RAO File Formats
##################

The RAO Import Tool (and PyBM) supports the following file formats for importing RAO data:

Excel (.xls, .xlsx)
--------------------

This is the most commonly used format. The RAO data should be structured in a specific way for successful import. You can use this file as a template structure: :download:`Excel RAO <../../../templates/rao/RAO_combined.xlsx>`.

Crucial things to note about this file are the following:

- All data must be combined on the first sheet. The RAO can be defined per heading direction, given in degrees.
- The data arrays must have the columns in following order:

    1. Wave Frequency (rad/s)
    2. Surge amplitude (m/m)
    3. Surge Phase (deg)
    4. Sway amplitude (m/m)
    5. Sway Phase (deg)
    6. Heave amplitude (m/m)
    7. Heave Phase (deg)
    8. Roll amplitude
    9. Roll Phase (deg)
    10. Pitch amplitude
    11. Pitch Phase (deg)
    12. Yaw amplitude
    13. Yaw Phase (deg)

This means that if a RAO is delivered in a different way (for example, each DoF (surge, sway, ...) in a different sheet), it must be manually sorted into the above structure.

CSV (.csv)
------------

In this file format, the RAO data should be structured as the following file example: :download:`CSV RAO <../../../templates/rao/rao_csv.csv>`.

.. image:: ../images/rao_csv_example.png
    :alt: rao_csv_example
    :align: center

|

TXT (.txt)
------------

This .txt file type should include the same format as the one Orcaflex uses to `import hydrodynamic data <https://www.orcina.com/webhelp/OrcaFlex/Content/html/Importinghydrodynamicdata,Generictextfiles.htm#>`_. 
You can see an example of the required format here: :download:`TXT RAO <../../../templates/rao/rao_txt.txt>`.

.. image:: ../images/rao_txt_example.png
    :alt: rao_txt_example
    :align: center

|

LIS (.lis)
-------------

This file type is an output typically from AQWA software. An example of the format can be found here: :download:`LIS RAO <../../../templates/rao/rao_lis.LIS>`.

Octopus
---------------

This file is also supported, but since it is less common, no example file is available at the moment.

Importing RAO to PyBM
#######################

After uploading the RAO to the MongoDB database using the RAO Import Tool, you can easily import it into your PyBM scripts using the following method:

.. code-block:: python
    :linenos:

    from PyBM.marine.motion_analysis import MotionRAO

    rao = MotionRAO.from_api(
        vessel_name="Vessel_Name", 
        loading_condition="Loading_Condition"
    )

In the attributes of the RAO instance, you can find additional information, including the conventions used, author, date of upload, etc.