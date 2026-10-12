Installation
============


Automated Installation
----------------------

An installation script can be downloaded via the following link (right-click and "Save link as..."):

:download:`PyBM Installation Script <download/install_setup.ps1>`

Run the script by right-clicking it and selecting "Run with PowerShell".
Manual installation is described below.


Manual Installation
-------------------

Prerequisites
^^^^^^^^^^^^^

- Python is installed on your PC. `Download Python <https://www.python.org/downloads/>`_ (make sure to select the "add python to environment variables" option, see image below)
- An IDE is installed, such as Visual Studio Code: `Download & Install VSCode <https://code.visualstudio.com/download>`_
- Knowledge of Python


.. image:: images/python_install.png
    :alt: venv_activation
    :align: center

|

Registry Setup
^^^^^^^^^^^^^^

To install the PyBM package you need to add the package registry to your PIP configuration.

Create a file called `pip.ini` in the following location: ``C:\Users\<username>\pip\pip.ini``, where `<username>` is your windows username.

The file should contain the following:

.. code-block:: ini

    [global]
    index-url = https://pip:5jXpNnQe0l450buVYKt9uvEO5Vz5Hdnmm47f3unAmHTo9GlBnpF5a40qEIOL@pypi.app.barge-master.com/simple/

Creating a project
=========================

Virtual environments
--------------------

Please check :ref:`usage/venv:Virtual Environments` for a more extensive explanation on package usage and virtual environments.

For your project, create a *virtual environment* on your local machine (client) by following the steps:

    #. Go to the folder on your PC (not on the server) where you want to create your environment. For example: ``C:\Users\<username>\Documents\venvs\``
    #. Open a terminal: right click in the folder then "Open in Terminal"
    #. Run: ``python -m venv ./<name_of_environment>``, replace ``<name_of_environment>`` with the name of your environment (typically the project number), do not use spaces in the name.


Opening a project in Visual Studio Code
---------------------------------------

*(If using a different IDE than VS Code, this chapter will be different)*

    #. Create the project folder if it does not exist yet. The project folder is usually in one of the following locations, and includes the ``requirements.txt`` file:

        - ``C:\Users\<username>\Barge Master B.V\PRxxx\Documents\Engineering\``
        - ``C:\Users\<username>\Barge Master B.V\Commercial\Documents\Sales\Opportunities\xxxx\Sales engineering\``
        - ``C:\Users\<username>\Barge Master B.V\RDxxx\Documents\Engineering\``
        - ``C:\Users\<username>\Barge Master B.V\Design & Engineering\Documents\Quick R&D projects\xxx\``

    #. Do not open the files separately in VS Code, rather open the **project folder**:

        .. image:: images/open_folder_vscode.png
            :width: 300
            :alt: open_folder_vscode
            :align: center

    #. Now you can open the python file you will work on. If the file does not exist yet, you can find templates for your use case :ref:`here <templates:Templates>`.

    #. Activate the virtual environment (you must have a python file opened in VS Code):

        #. Use your editor and select the virtual environment in the bottom right corner (VS Code is recommended, see image below). In case you don't want to always browse for the environment, you can also make VS Code display automatically all the virtual environments available on your venvs folder (for example, ``C:\Users\<username>\Documents\venvs\``). To do so, open the command palette (ctrl + shift + P), then search for "Preferences: Open User Settings (JSON)", then add the following line to the curly brackets in the JSON file: 

            .. code-block:: json

                "python.venvPath": ["C:\\Users\\<username>\\Documents\\venvs"]

            .. image:: images/venv_activation.png
                :width: 500
                :alt: venv_activation
                :align: center

        #. To check what packages are installed in the environment run: ``pip list`` in the terminal (ctrl + ~ to open terminal). If the environment was just created, it should be empty.

Installing PyBM
---------------

If the project is new, install the newest version of PyBM using PIP, otherwise install the requirements.txt file (see :ref:`Loading dependencies <sec-loading-dependencies>` below).

.. code-block:: bash

    pip install PyBM

Or to install a specific version:

.. code-block:: bash

    pip install PyBM==4.0.0

PyBM versions will be released following the `semantic versioning scheme <https://semver.org/>`_.
This means that the version number will be in the format `MAJOR.MINOR.PATCH`. And a change in major version number indicates a breaking change.

To check if it was installed correctly in the environment, you can run ``pip list`` in the terminal. You should see PyBM in the list.


Versioning & dependencies
-------------------------

Saving dependencies
^^^^^^^^^^^^^^^^^^^

When using python packages installed from PIP, it is important to keep track of the versions of the packages used in your project. This is because new versions of packages can be released that would break existing code.
This can be done by creating a `requirements.txt` file in your project. This file contains a list of all the packages used in your project and their versions.

To create a `requirements.txt` file, run the following command after you have installed all the required packages:

.. code-block:: bash

    pip freeze > requirements.txt

.. _sec-loading-dependencies:

Loading dependencies
^^^^^^^^^^^^^^^^^^^^

When opening a project that has a `requirements.txt` file, you can install all the required packages by running the following command:

.. code-block:: bash

    pip install -r requirements.txt

This will install all the packages listed in the `requirements.txt` file.
