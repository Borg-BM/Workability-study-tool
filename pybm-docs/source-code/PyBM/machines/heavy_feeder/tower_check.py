"""
Date: 20-03-2023
Date checked: 12-06-2025
Author: CBR
Check: AKO

Refs:
    [1] TWD-NL-2021-512-C-010-REV-6 Heavy feeder re-design LCD
    [2] TBB_280_6KN_Opt_T1T2_acc
"""

import numpy as np

from ...constants import *
from ...utils.mass_items import Tower, VerticalStack, massItem

design_loads = np.array([3.49e7, 3.06e8, 8.65e7])

Hs_design = 2.5

def unity_checks_tower(
    tower: massItem, tbic: massItem = None, lifting_tool: massItem = None, Hs: float = None
) -> np.array:
    """Calculate unity checks of a different tower w.r.t. the heavy feeder design conditions.

    :param tower: Tower properties
    :type tower: massItem
    :param tbic: TBIC properties, by default the vinyard TBIC will be used.
    :type tbic: massItem
    :param lifting_tool: Lifting tool properties, by default the vinyard tool will be used.
    :type lifting_tool: massItem
    :param Hs: [m] Significant Waave height used for acceleration scaling, defaults to 2.5m
    :type Hs: float
    :return: list of unity checks [Fz, Mx, My]
    :rtype: np.array
    """
    # Factors
    alfa_cog = 1.05  # [-] cog contigency factor
    gamma_bP = 1.0  # [-] load factor permanent
    gamma_bE = 1.3  # [-] load factor environmental
    if Hs:
        hs_factor = Hs / Hs_design
    else:
        hs_factor = 1

    # Heavy feeder
    heavy_feeder = massItem(h=7.32, m=170e3, h_cog=5.73)
    heavy_feeder.hp_cb = 5.12  # [m] height platform to central bearing
    heavy_feeder.lp = 11.43  # [m] lenght of platform y-direction

    # Compensated items
    if not tbic:
        tbic = massItem(h=1.3, m=46.1e3, h_cog=0.958)
    if not lifting_tool:
        lifting_tool = massItem(h=5, m=45.8e3, h_cog=1.62)

    items = [tbic, tower, lifting_tool]
    combined_items = VerticalStack(items, alfa_cog)
    combined_mass = np.array(
        [combined_items.m] * 3
        + [combined_items.I_shifted(combined_items.y_cog)]
        + [combined_items.I_shifted(combined_items.x_cog)]
        + [0]
    )

    # Barge
    barge_h = 6.55  # [m] heught
    barge_draft = 2.9  # [m] draft
    barge_fb = barge_h - barge_draft  # [m] freeboard
    barge_heel = 1 * np.pi / 180  # [rad] heel angle

    # Motions
    h_CoG_ma = 44.3  # [m] height of cog above baseline
    nd = (barge_fb + heavy_feeder.h + combined_items.h_cog) / (
        h_CoG_ma - barge_draft
    )  # scaling factor for change in CoG Height
    acc_scaling = np.array([nd] * 3 + [1] * 3)

    # Accelerations
    deg_2_rad = np.array([1] * 3 + [np.pi / 180] * 3)  # convert acceletions to rad/s2
    acc_SP = np.array([1.58, 2.59, 1.35, 2.13, 1.86, 0.35]) * deg_2_rad * acc_scaling * hs_factor
    acc_SR = np.array([1.05, 5.81, 1.32, 5.08, 1.26, 0.43]) * deg_2_rad * acc_scaling * hs_factor
    acc_H = np.array([1.32, 4.35, 1.55, 3.66, 1.64, 0.50]) * deg_2_rad * acc_scaling * hs_factor

    # LC2 Static Weight
    F_LC2 = combined_items.m * g * gamma_bP

    def central_bearing_loads(acc):
        loads = acc * combined_mass * gamma_bE
        Mx = loads[1] * (combined_items.h_cog + heavy_feeder.hp_cb) + (F_LC2 + loads[2]) * combined_items.y_cog
        My = loads[0] * (combined_items.h_cog + heavy_feeder.hp_cb) + (F_LC2 + loads[2]) * combined_items.x_cog
        M_heel = np.sin(barge_heel) * (F_LC2 + loads[2]) * (combined_items.h_cog + heavy_feeder.hp_cb)
        Mx_tot = Mx + M_heel + loads[3]
        My_tot = My + loads[4]
        Fz = F_LC2 + Mx_tot / heavy_feeder.lp
        return np.array([Fz, Mx_tot, My_tot])

    cb_load = np.array([0, 0, 0])

    for acc in [acc_SP, acc_SR, acc_H]:
        cb_load = np.maximum(central_bearing_loads(acc), cb_load)

    unity_checks = cb_load / design_loads
    return np.round(unity_checks, 2)
