<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/utils/windows_helpers/index.html -->

# PyBM.utils.windows_helpers

## Functions

|                                                                                                                |                                                                                                                                                              |
|----------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`isFileLocked`](#PyBM.utils.windows_helpers.isFileLocked "PyBM.utils.windows_helpers.isFileLocked")(filePath) | Source: [https://stackoverflow.com/questions/13371444/python-check-file-is-locked](https://stackoverflow.com/questions/13371444/python-check-file-is-locked) |

## Module Contents

PyBM.utils.windows_helpers.isFileLocked(*filePath*)[](../../../../../source-code/PyBM/utils/windows_helpers.py)  
Source: [https://stackoverflow.com/questions/13371444/python-check-file-is-locked](https://stackoverflow.com/questions/13371444/python-check-file-is-locked) Checks to see if a file is locked. Performs three checks

> 1.  Checks if the file even exists
>
> 2.  Attempts to open the file for reading. This will determine if the file has a write lock.  
>     Write locks occur when the file is being edited or copied to, e.g. a file copy destination
>
> 3.  Attempts to rename the file. If this fails the file is open by some other process for reading. The  
>     file can be read, but not written to or deleted.

Parameters:  
**filePath** – path of file to check
