"""
This file reads .res output files from aNySIM and returns a dictionary with all the data
"""

import os.path
import pickle
import shutil

import numpy as np

def __file_len(fname):
    with open(fname, "r") as f:
        for i, l in enumerate(f):
            pass
    return i

def resample(data, new_dt, data_dt):
    interval = new_dt / data_dt
    if np.abs(interval - int(interval)) < 1e-8:
        print("Selecting data")
        interval = int(interval)
        for key, val in data.items():
            data[key] = val[::interval]
    else:  # Interpolate data
        print("Interpolating data")
        new_time = np.arange(data["time"][0], data["time"][-1], new_dt)
        time = data["time"]
        for key, val in data.items():
            data[key] = np.interp(new_time, time, val)
    print("Resampled to dt={:3f}".format(data["time"][1] - data["time"][0]))
    return data

def __read_file(filename, read_invalid=True):
    move = False
    length = __file_len(filename + ".res")
    with open(filename + ".res", "r") as res:
        var_names = res.readline().strip().split("\t")
        data = np.zeros((length, len(var_names)))
        end = length
        for i, line in enumerate(res):
            line_var = line.strip().split("\t")
            try:
                line_var = list(map(float, line_var))
                data[i, :] = line_var
            except:
                print("WARNING: Invalid data encountered: " + filename)
                end = i
                if not read_invalid:
                    move = True
                break

    data_dict = {}
    if move:
        print("Moving invalid RES file")
        if not os.path.isdir("invalid"):
            os.mkdir("invalid")
        shutil.move(filename + ".res", "invalid")
    else:
        # Creating data dictionary
        for i, name in enumerate(var_names):
            data_dict[name] = data[0:end, i]
        # Saving binary file
        write_pickle(filename, data_dict)
        return data_dict

def read_res(filename, dt=0, read_invalid=True):
    """
    Read a text .res file with time traces.

    :param filename: name of file without extension
    :param dt: [s] sample time, if 0 the original sample time is used
    :param read_invalid: [bool] If false, invalid files are moved to Invalid folder
    :return: Dictionary of time_vectors.
    """
    # Initialize
    load_pkl = False
    res_exists = os.path.isfile(filename + ".res")
    pkl_exists = os.path.isfile("pkl\\" + filename + ".pkl")

    # Decide between pkl and res file
    if res_exists and pkl_exists:
        pkl_time = os.path.getmtime("pkl\\" + filename + ".pkl")
        res_time = os.path.getmtime(filename + ".res")
        if pkl_time > res_time:
            load_pkl = True
    elif pkl_exists:
        load_pkl = True

    # Loading file
    if load_pkl:
        print("loading from binary: {}.pkl".format(filename))
        with open("pkl\\" + filename + ".pkl", "rb") as f:
            data_dict = pickle.load(f)
    else:
        print("loading res file: {}.res".format(filename))
        data_dict = __read_file(filename, read_invalid=read_invalid)

    # Resampling data (if required)
    if dt > 0:
        data_dt = data_dict["time"][1] - data_dict["time"][0]
        if (dt - data_dt) > 1e-6:
            data_dict = resample(data_dict, dt, data_dt)
            # Saving new pkl
            with open("pkl\\" + filename + ".pkl", "wb") as f:
                pickle.dump(data_dict, f)
        else:
            print("Data time-step ({:.3f}s) is larger than given resample time-step ({:.3f}s)".format(data_dt, dt))
    return data_dict

def write_pickle(filename, data_dict):
    # Write pkl
    if not os.path.isdir("pkl"):
        os.mkdir("pkl")
    with open("pkl\\" + filename + ".pkl", "wb") as f:
        pickle.dump(data_dict, f)

def write_res(filename, data_dict):
    """
    Write a data dictionary to a .res text file.

    :param filename: name of file (without extension)
    :param data_dict: dictionary of key / time_vector pairs
    """
    write_pickle(filename, data_dict)

    # Write res
    with open(filename + ".res", "w") as res:
        # Write keys
        keys = ""
        for key in data_dict.keys():
            keys += key + "\t"
        keys = keys[0:-1]
        res.write(keys + "\n")

        # Write values
        for i in range(0, len(data_dict["time"]) - 1):
            val = ""
            for key in data_dict.keys():
                val += str(data_dict[key][i]) + "\t"
            val = val[0:-1]
            res.write(val + "\n")

        res.close()

    print("Res and pkl successfully created")
