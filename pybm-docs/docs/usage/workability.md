<!-- Source: https://docs.app.barge-master.com/usage/workability.html -->

# PyBM Workability Training

Workability calculations follow the diagram:

\[image: workability_diagram — not available, stored as Git LFS pointer on the server\]

The most important steps are in correctly defining the parameters according to the [conventions](../conventions.md#conventions). The parameters can be split in three major parts:

- **Response Amplitude Operators or RAOs**. These can be imported from the BM database using `PyBM.marine.motion_analysis.MotionRAO.from_api()`. If a new RAO is still to be imported into the BM database, please follow the procedure to [import RAOs](importing_rao_tool.md#rao-import-tool).

- **Sea state or Wave Spectrums**. All the parameters for the Sea state, including Significant Wave Height (*Hs*), Mean Wave Period (*Tp*), Wave Direction (*main_direction*), spreading, etc, can be defined using arrays. The parameters will automatically be broadcasted, this way multiple variants of the same workability can be calculated simultaneously. More details on wave spectra and how to choose its parameters can be found in the [theory section](../theory.md#wave-spectra).

- **Machine**. The machine defines the workability limits that are taken into account. It is important to define the position of the machine correctly, with the correct conventions.
