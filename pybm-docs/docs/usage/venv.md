<!-- Source: https://docs.app.barge-master.com/usage/venv.html -->

# Virtual Environments

For BM engineering projects, we use PyBM and other packages to run the code we create. Since PyBM keeps being updated, sometimes breaking changes take place.

**When is a change breaking?**

*PyBM uses semantic versioning, where the version number is stated as: major.minor.patch (i.e., breaking.feature.bug). Meaning: The update from 1.0.0 to 2.0.0 is a breaking change, so scripts written with the old version usually cannot be run in the newest version without changes. 1.0.0 to 1.1.0 is a feature release, meaning that a feature has been added. Code written in 1.1.0 might use features that are not present in 1.0.0. Finally, 1.0.0 to 1.0.1 is a bug fix release, usually only including some fixes.  
New version releases will be announced by e-mail to PyBM users, who should update their PyBM themselves after.*

  

By storing which packages and their versions are used for in a *requirements.txt* file, we can automatically install the required packages for that code on a later date. We do this to make sure the correct PyBM version is used for each (older) project that is ran.

**Example**

*A project PR123 is created in 2019, when the PyBM version is still 1.0.0. If this project is then ran in 2024, and the PyBM version has been updated to 5.0.0, there have been at least **4** breaking changes. This means that the code created in 2019 probably doesn't work with the newest version. Hence it shows the importance of storing the used packages and their versions, so the old code can still easily be run.*

  

Since you are probably working on multiple projects around the same timeframe, you will want to use virtual environments to run each project. This is because it allows you to create an isolated environment for your project, where you can install specific package versions without affecting other projects. By using virtual environments, one does not have to install the relevant packages every time.

**Example**

*You are handling two opportunities, OP123 and OP321. Each opportunity might use a different PyBM version, for example because OP123 was created in 2020. If you're switching between these projects without virtual environments for each, you would have to reinstall the packages every time, with running the command: `pip install -r requirements.txt`. If virtual environments are created for each opportunity, the IDE (Visual Studio Code) will automatically switch to the relevant virtual enviroment every time.*

  

Because virtual environments contain many large files, it is not allowed to store these on the server (SharePoint). Therefore, we store the virtual environments on the *client*, while the project itself stays on the *server*. See the figure below for a graphical representation of this.

[\[image: venv_relation — not available, stored as Git LFS pointer on the server\]](../_images/client_server_venvs.png)

## Creation of Virtual Environments

Virtual environments should be created in a local folder on your PC (not on the server), since they contain a lot of files.

> 1.  Create virtual environment:  
>     1.  Go to the folder on your PC (not on the server) where you want to create your environment. For example: `C:\Users\<username>\Documents\venvs\`
>
>     2.  Open a terminal: right click in the folder then “Open in Terminal”
>
>     3.  Run: `python -m venv ./<name_of_environment>`, replace `<name_of_environment>` with the name of your environment (typically the project number). Do not use spaces in the name.
>
> 2.  Activate the virtual environment:  
>     1.  Open VS Code, then open the folder of the project: File \> Open Folder.
>
>     2.  Use your editor and select the virtual environment in the bottom right corner (VS Code is recommended, see image below). You must have a python file opened in VS Code.
>
>     3.  You can verify that the correct environment is activated by opening a new terminal tab. The environment name should appear in green, between parentheses (see image at the end).
>
>     4.  To check which packages are installed in the environment, run `pip list` in the terminal (ctrl + ~ to open terminal).

\[image: venv_activation — not available, stored as Git LFS pointer on the server\] \[image: check_venv — not available, stored as Git LFS pointer on the server\]

  
