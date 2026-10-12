"""
Time domain tools

References:
    [1]: Ship Motion Control, Tristan Perez
"""

import copy
import os
import re
import sys
from pathlib import Path

import numpy as np
import xarray as xr
from dask.diagnostics import ProgressBar
from numpy.random import default_rng
from scipy.io import loadmat, savemat

from PyBM.marine.motion_analysis.MotionRAO import MotionRAO
from PyBM.marine.wave_spectrum import WaveSpectrum
from PyBM.utils import isFileLocked

@xr.register_dataarray_accessor("timedomain")
@xr.register_dataset_accessor("timedomain")

class TimeDomainTools:
    """Tools for time domain traces in xarray.DataArray type"""

    def __init__(self, xarray_obj):
        # if not "Frequency" in xarray_obj.coords:
        #     raise AttributeError("DataArray must have Frequency coordinate for Spectral tools to work.")

        self._obj = xarray_obj

    def translate_trace(self, offset: np.array):
        """
        Translates the trace in 6 DOF. Does not use small angle approx..

        :param offset: offset in [x,y,z]
        :type offset: np.array
        """
        cosroll = np.cos(np.deg2rad(self._obj.loc[dict(DOF="Rx")]))
        sinroll = np.sin(np.deg2rad(self._obj.loc[dict(DOF="Rx")]))
        cospitch = np.cos(np.deg2rad(self._obj.loc[dict(DOF="Ry")]))
        sinpitch = np.sin(np.deg2rad(self._obj.loc[dict(DOF="Ry")]))
        cosyaw = np.cos(np.deg2rad(self._obj.loc[dict(DOF="Rz")]))
        sinyaw = np.sin(np.deg2rad(self._obj.loc[dict(DOF="Rz")]))

        Trace = self._obj.copy(deep=True)
        Trace.loc[dict(DOF="X")] += offset[0] * cospitch * cosyaw - offset[1] * cospitch * sinyaw + offset[2] * sinpitch
        Trace.loc[dict(DOF="Y")] += (
            offset[0] * (sinpitch * sinroll * cosyaw + cosroll * sinyaw)
            + offset[1] * (-sinpitch * sinroll * sinyaw + cosyaw * cosroll)
            - offset[2] * sinroll * cospitch
        )
        Trace.loc[dict(DOF="Z")] += (
            offset[0] * (-sinpitch * cosroll * cosyaw + sinroll * sinyaw)
            + offset[1] * (sinpitch * cosroll * sinyaw + sinroll * cosyaw)
            + offset[2] * cosroll * cospitch
        )
        return Trace

    def translate_trace_smallangle(self, offset: np.array):
        """
        Translates the trace in 6 DOF. Uses small angle approx

        :param offset: offset in [x,y,z]
        :type offset: np.array
        """
        if len(offset) != 3:
            raise ValueError("Offset should be vector of length 3: [x,y,z]")
        Trace = self._obj.copy(deep=True)

        roll = np.deg2rad(Trace.loc[dict(DOF="Rx")])
        pitch = np.deg2rad(Trace.loc[dict(DOF="Ry")])
        yaw = np.deg2rad(Trace.loc[dict(DOF="Rz")])

        Trace.loc[dict(DOF="X")] += offset[0] - offset[1] * yaw + offset[2] * pitch
        Trace.loc[dict(DOF="Y")] += offset[0] * yaw + offset[1] - offset[2] * roll
        Trace.loc[dict(DOF="Z")] += -offset[0] * pitch + offset[1] * roll + offset[2]
        return Trace

class TimeDomain:
    def __init__(self, wave: WaveSpectrum, rao: MotionRAO, vesselCoG) -> None:
        """Time Domain tools to create and load time traces of vessel motions.

        :param wave: Wave defintion
        :type wave: WaveSpectrum
        :param rao: Vessel RAO
        :type rao: MotionRAO
        :param vesselCoG: [x,y,z] CoG position of the Vessel [m]
        """

        self.rao = rao

        self.vesselCoG = vesselCoG

        self.wave = copy.deepcopy(wave)

    @staticmethod

    def time_vector(dt, duration):
        """Create labelled time vector

        :param dt: [s] Time step
        :param duration: [s] Duration of time trace
        """
        time = np.arange(0, duration + dt, dt)
        return xr.DataArray(time, coords=[time], dims="Time")

    def generate_mat_time_traces(self, folder: str, dt, duration, wave):
        """Generate .mat time traces to be used in the matlab workability tools.

        :param folder: Folder to save the files
        :param dt: [s] Time step
        :param duration: [s] Duration of time trace
        :param wave: [s] Wave to generate time traces for. Parameters may be vectorized.
        :param directions: [deg] Wave directions
        """
        time = self.time_vector(dt, duration)
        trace = self.time_trace_from_rao_and_wave(time, wave, self.rao)
        filenames = self.save_mat_file(folder, trace)
        return filenames

    def generate_time_traces(self, folder: str, dt, duration, wave):
        """Generate .mat time traces to be used in the matlab workability tools.

        :param folder: Folder to save the files
        :param dt: [s] Time step
        :param duration: [s] Duration of time trace
        :param wave: [s] Wave to generate time traces for. Parameters may be vectorized.
        :param directions: [deg] Wave directions
        """
        if isFileLocked(os.path.join(folder, self.nc_file_name())):
            raise IOError(
                f"file: {os.path.join(folder, self.nc_file_name())} is locked! \n please close the file or check permissions, and start trace generation again."
            )
        time = self.time_vector(dt, duration)
        trace = self.time_trace_from_rao_and_wave(time, wave, self.rao)
        filenames = self.save_nc_file(folder, trace)
        return filenames

    def save_mat_file(self, folder, trace):
        """
        Vectorized saving function
        """
        print("Computing trace...", end="\r")
        trace = trace.compute()
        print("\033[K Saving traces now")

        def save_single(time, trace, filename):
            filename = os.path.join(folder, filename)
            output = {
                "Vessel_CoG": self.vesselCoG,
                "dt": time[1] - time[0],
                "t": time,
                "surge": trace[0].squeeze(),
                "sway": trace[1].squeeze(),
                "heave": trace[2].squeeze(),
                "roll": trace[3].squeeze(),
                "pitch": trace[4].squeeze(),
                "yaw": trace[5].squeeze(),
            }
            if not os.path.exists(folder):
                os.makedirs(folder)
            savemat(filename, output, oned_as="column")
            return filename

        return xr.apply_ufunc(
            save_single,
            trace.Time,
            trace,
            self.mat_file_name(),
            input_core_dims=[["Time"], ["DOF", "Time"], []],
            vectorize=True,
        )

    def save_nc_file(self, folder, trace):
        return self._save_nc_file(folder, trace, self.rao.VesselName, self.vesselCoG)

    @staticmethod

    def _save_nc_file(folder, traces: xr.DataArray, VesselName, vesselCoG):
        """
        Save traces as a single nc file. will append nc with extra coordinates, if already there.
        :param folder: folder name
        :type folder: string
        :param traces: traces to save.
        :type traces: xarray.DataArray
        """

        print("Computing trace...", end="\r")
        with ProgressBar():
            traces = traces.compute()
        print("\033[K Saving traces now")

        filename = os.path.join(folder, TimeDomain._nc_file_name(VesselName))
        if not os.path.exists(folder):
            os.makedirs(folder)
        traces = traces.assign_attrs({"origin": vesselCoG})
        if os.path.exists(filename):
            print("file already exists. loading and merging so file can be saved again.")
            extrace = xr.load_dataarray(filename)
            if xr.zeros_like(traces).equals(xr.zeros_like(extrace)):
                print(f".NC file already exists with all the same dimensions! Overriding trace...")
            else:
                traces = xr.combine_by_coords(
                    [extrace, traces],
                    compat="override",
                    data_vars="all",
                    coords="all",
                    combine_attrs="override",
                )
        while True:
            if isFileLocked(filename):
                input(
                    "I got the above exception. The file is probably open somewhere. Please close the file, press enter to try again... press CTRL+C to cancel."
                )
            else:
                try:
                    traces.to_netcdf(filename, "w")
                except IOError as e:
                    print(e)
                    input(
                        "I got the above exception. The file is probably open somewhere. Please close the file, press enter to try again... press CTRL+C to cancel."
                    )
                else:
                    return filename

    @staticmethod

    def default_trace_path(VesselName, revision=0):
        dir = Path(
            f"O:/Engineering/Database/Vessel Motions/Vessel RAOs and time traces/{VesselName}/Processed data/Time traces Rev{revision}"
        )
        return dir

    def load_time_trace(self, folder):
        """
        Loads time traces. Tries to open nc files first, if non existent, opens mat files.
        :param folder: folder name
        :type folder: str
        """
        # First check if folder exists
        if not os.path.exists(folder):
            raise ReferenceError(f"Path {folder} does not exist or can not be accessed")
        # Check if .nc file exists
        ncfn = os.path.join(folder, self.nc_file_name())
        if os.path.isfile(ncfn):
            print(f"{ncfn} exists. loading nc traces")
            return self.load_nc_time_trace(folder)
        print("{ncfn} does not exist. Checking for .mat time traces")
        matre = r"([^\.\n]+)_Tp(\d\d\d)_Hs(\d\d\d)_Hdg(\d\d\d)\.mat"
        mattraces = [
            dict(zip(("VesselName", "Tp", "Hs", "Hdg"), re.search(matre, file).groups()))
            for file in os.listdir(folder)
            if re.match(matre, file)
        ]
        if any(mattraces):
            print(".mat file(s) exist in the folder. Loading .mat time traces")
            traces = self.load_mat_time_trace(folder)
            print("Loaded mat files. saving as .nc files now.")
            self.save_nc_file(folder, traces)
            return traces
        raise ReferenceError(
            f"No traces exist in folder:\n{folder}. \nEither a wrong folder has been given, or no traces have been generated yet for this Vessel and revision!"
        )

    @staticmethod

    def load_all_default_time_traces(VesselName, rev=0):
        """
        Load the time traces of the given vessel and revision in the default engineering library folder.
        :param VesselName: vessel name
        :type VesselName: str
        :param rev: revision number
        :type rev: int
        """
        folder = TimeDomain.default_trace_path(VesselName, revision=rev)
        return TimeDomain.load_all_time_traces(folder, VesselName)

    @staticmethod

    def load_all_time_traces(folder, VesselName):
        """
        Static version of load_time_trace. Loads all time traces present in given folder. do not need to supply any sort of dimensioning for Tp, Hs or direction.
        If using default trace path, you can also use the function TimeDomain.load_default_time_trace().
        :param folder: folder to load time traces from.
        :type folder: str
        :param VesselName: name of the vessel to be loaded.
        :type VesselName: str
        """
        # First check if folder exists
        if not os.path.exists(folder):
            raise ReferenceError(f"Path {folder} does not exist or can not be accessed")
        # Check if .nc file exists
        ncfn = os.path.join(folder, TimeDomain._nc_file_name(VesselName))
        if os.path.isfile(ncfn):
            print(f"{ncfn} exists. loading nc traces")
            return TimeDomain._load_nc_time_trace(folder, VesselName)
        print("{ncfn} does not exist. Checking for .mat time traces")
        matre = r"([^\.\n]+)_Tp(\d\d\d)_Hs(\d\d\d)_Hdg(\d\d\d)\.mat"
        mattraces = [
            dict(zip(("VesselName", "Tp", "Hs", "Hdg"), re.search(matre, file).groups()))
            for file in os.listdir(folder)
            if re.match(matre, file)
        ]
        print("Found the following traces in .mat files, loading:\n", "\n".join([str(mt) for mt in mattraces]))
        Tps = list(set([float(mt["Tp"]) / 10 for mt in mattraces]))
        Tps.sort()
        Tps = xr.DataArray(Tps, dict(Tp=Tps))
        Hs = list(set([float(mt["Hs"]) / 100 for mt in mattraces]))
        Hs.sort()
        Hs = xr.DataArray(Hs, dict(Hs=Hs))
        Hdg = list(set([float(mt["Hdg"]) for mt in mattraces]))
        Hdg.sort()
        Hdg = xr.DataArray(Hdg, dict(WaveDirection=Hdg))

        if any(mattraces):
            traces = TimeDomain._load_mat_time_trace(folder, VesselName, Tps, Hs, Hdg)
            print("Loaded mat traces, now saving as .nc...")
            TimeDomain._save_nc_file(folder, traces, VesselName, traces.origin)
            return traces

    def load_mat_time_trace(self, folder):
        """Load a MAT time trace(s) as DataArray. Uses objects' properties for selecting which traces to load.

        :param folder: path of folder
        :type folder: str
        """
        return TimeDomain._load_mat_time_trace(
            folder, self.rao.VesselName, self.wave.Tp, self.wave.Hs, self.wave.main_direction
        )

    @staticmethod

    def _load_mat_time_trace(folder, VesselName, Tp, Hs, Direction):
        """
        Vectorized static function to load mat time traces according to given parameters.
        """
        fn = np.frompyfunc(
            lambda tp, hs, md: TimeDomain._load_single_mat_time_trace(folder, VesselName, tp, hs, md), 3, 1
        )
        traces = fn(Tp, Hs, Direction)
        # if all parameters were scalar, the result is already the finished trace.
        if "DOF" in traces.dims:
            return traces
        # if parameters included lists, the arrays must be combined first into one DataArray.
        return xr.combine_by_coords(list(np.array(traces.values).squeeze().flatten()), compat="no_conflicts")

    @staticmethod

    def _load_single_mat_time_trace(folder, VesselName, Tp, Hs, Direction):
        print(f"\033[K Loading .mat Time Trace: VesselName {VesselName}, Tp {Tp}, Hs {Hs}, Dir {Direction}", end="\r")
        filename = TimeDomain._mat_file_name(VesselName, Tp, Hs, Direction)
        m_dict = loadmat(os.path.join(folder, filename), squeeze_me=True)
        x = xr.DataArray(m_dict["surge"], coords=[("Time", m_dict["t"])]).expand_dims(
            WaveDirection=[Direction], DOF=["X"], Tp=[Tp], Hs=[Hs]
        )
        y = xr.DataArray(m_dict["sway"], coords=[("Time", m_dict["t"])]).expand_dims(
            WaveDirection=[Direction], DOF=["Y"], Tp=[Tp], Hs=[Hs]
        )
        z = xr.DataArray(m_dict["heave"], coords=[("Time", m_dict["t"])]).expand_dims(
            WaveDirection=[Direction], DOF=["Z"], Tp=[Tp], Hs=[Hs]
        )
        rx = xr.DataArray(m_dict["roll"], coords=[("Time", m_dict["t"])]).expand_dims(
            WaveDirection=[Direction], DOF=["Rx"], Tp=[Tp], Hs=[Hs]
        )
        ry = xr.DataArray(m_dict["pitch"], coords=[("Time", m_dict["t"])]).expand_dims(
            WaveDirection=[Direction], DOF=["Ry"], Tp=[Tp], Hs=[Hs]
        )
        rz = xr.DataArray(m_dict["yaw"], coords=[("Time", m_dict["t"])]).expand_dims(
            WaveDirection=[Direction], DOF=["Rz"], Tp=[Tp], Hs=[Hs]
        )
        da = xr.concat([x, y, z, rx, ry, rz], dim="DOF")
        da = da.assign_attrs({"origin": np.array(m_dict["Vessel_CoG"])})
        return da

    def load_nc_time_trace(self, folder):
        """Load NC stored time trace(s) as DataArray

        :param folder: path of folder
        """
        traces = self._load_nc_time_trace(folder, self.rao.VesselName)
        return traces

    @staticmethod

    def _load_nc_time_trace(folder, VesselName):
        """
        Loads nc file with traces.
        """
        filename = os.path.join(folder, TimeDomain._nc_file_name(VesselName))
        result = xr.load_dataarray(filename)
        return result

    def mat_file_name(self):
        return self._mat_file_name(self.rao.VesselName, self.wave.Tp, self.wave.Hs, self.wave.main_direction)

    @staticmethod

    def _mat_file_name(VesselName, Tp, Hs, Direction):
        """
        Returns mat file names for trace. Broadcasts arrays in case of multiple values for Tp,Hs,main_direction.
        """

        def func(tp, hs, dir):
            return f"{TimeDomain._file_name(VesselName,tp,hs,dir)}.mat"

        fnvect = np.frompyfunc(func, 3, 1)
        return fnvect(Tp, Hs, Direction)

    def nc_file_name(self):
        return self._nc_file_name(self.rao.VesselName)

    @staticmethod

    def _nc_file_name(VesselName):
        """
        Returns nc file name for trace. Since nc files include all directions it is not a vectorized function
        """

        return f"{VesselName}_trace.nc"

    @staticmethod

    def _file_name(VesselName, Tp, Hs, Direction):
        return f"{VesselName}_Tp{Tp*10:03.0f}_Hs{Hs*100:03.0f}_Hdg{Direction:03.0f}"

    @staticmethod

    def time_trace_from_rao_and_wave(time: xr.DataArray, wave: WaveSpectrum, rao: MotionRAO, Nfreqs=100, bounds=None):
        """Generate time trace based on RAO and Wave.

        :param time: [s] time vector
        :type time: xr.DataArray
        :param wave: [m2/(rad/s)] WaveSpectrum
        :type wave: WaveSpectrum
        :param rao: [m/m, deg/m] 6DOF Motion RAO
        :type rao: MotionRAO
        """
        if bounds is None:
            bounds = (rao.Frequency[0], rao.Frequency[-1])
        time = time.chunk({"Time": 30 * 60})
        if "POS" in rao:
            rao = rao.POS
        if wave.spreading <= 0:
            interp_rao = rao.interp(Direction=wave.main_direction)
            freqs = wave.equal_energy_frequencies(bounds, Nfreqs=Nfreqs)
            interp_rao = interp_rao.interp(Frequency=freqs)
            trace = TimeDomain.single_direction_time_trace(time, wave, interp_rao)
        else:
            trace = TimeDomain.multi_directional_time_trace(time, wave, rao, bounds=bounds)
        return trace

    def multi_directional_time_trace(time: xr.DataArray, wave: WaveSpectrum, rao: MotionRAO, bounds=None):
        """Create time trace including wave spreading.

        :param time: [s] time vector
        :type time: xr.DataArray
        :param rao: [m/m, deg/m] 6DOF Motion RAO
        :type rao: MotionRAO
        :param wave: [m2/(rad/s)] WaveSpectrum
        :type wave: WaveSpectrum
        """
        Nfreqs = 200
        wave_dirs = wave.abs_directions(wave.equal_energy_directions())
        random = default_rng()
        if bounds is None:
            bounds = (rao.Frequency[0], rao.Frequency[-1])
        # https://www.orcina.com/webhelp/OrcaFlex/Content/html/Wavetheory.htm#SpectrumDiscretisationTheory
        allfreqs = wave.equal_energy_frequencies(Nfreqs=Nfreqs * wave.Ndirs, bounds=bounds)

        # Randomize frequencies for each direction
        dir_idx = np.tile(random.permutation(wave.Ndirs), Nfreqs)
        allfreqs = allfreqs.assign_coords(dir_idx=("Frequency", dir_idx))

        trace = None
        for lbl, grp in allfreqs.groupby("dir_idx"):
            interp_rao = rao.interp(Frequency=grp, Direction=wave_dirs[lbl])
            # Ref [1] eq (4.32)
            single_dir_trace = TimeDomain.single_direction_time_trace(time, wave, interp_rao) / np.sqrt(wave.Ndirs)
            if trace is None:
                trace = single_dir_trace
            else:
                trace = trace + single_dir_trace
        return trace.reset_coords(drop=True)

    def single_direction_time_trace(time: xr.DataArray, wave: WaveSpectrum, rao: MotionRAO):
        """Create time trace for a single wave direction

        :param time: [s] time vector
        :type time: xr.DataArray
        :param rao: [m/m, deg/m] 6DOF Motion RAO. Must have interpolated frequencies according to equal area method
        :type rao: MotionRAO
        :param wave: [m2/(rad/s)] WaveSpectrum
        :type wave: WaveSpectrum
        """
        random = default_rng()
        rao.chunk({"Frequency": 100})
        amplitudes = np.abs(rao) * wave.Hs * np.sqrt(2 / rao.sizes["Frequency"]) / 4  # Ref [1] eq (4.32)
        random_phases = random.uniform(0, 2 * np.pi, size=np.shape(rao.Frequency))
        random_phases = rao.Frequency.copy(data=random_phases)
        phases = xr.apply_ufunc(np.angle, rao, dask="allowed") + random_phases
        components = amplitudes * np.cos(2 * np.pi * rao.Frequency * time + phases)
        trace = components.sum(dim="Frequency")
        return trace

    @staticmethod

    def compute_deltas(coordinates, dim):
        """Create bins centered a coordinate points.

        :param coordinates: Coordinates to create bins around.
        :param dim: Dimension name
        """
        coordinates = coordinates.sortby(coordinates)
        mean = coordinates.rolling({dim: 2}).mean().values
        bins = mean[1:] - mean[:-1]
        bins[0] = mean[1] - coordinates[0]
        bins = np.append(bins, coordinates[-1] - mean[-1])
        return xr.DataArray(bins, coords=[coordinates[dim]])

    @staticmethod

    def zero_crossing_period(trace):
        """Compute average zero-crossing period of a time trace.

        return: [s] average zero-crossing period.
        """
        crossings = np.sign(trace).diff(dim="Time")
        N_crossings = crossings.where(crossings > 0).sum(dim="Time") / 2
        return (trace.Time[-1] - trace.Time[0]) / N_crossings
