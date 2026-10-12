"""
Date: 06-05-2024
Author: CVE
Check: XXX

Refs:
    [1] TWD-NL-2021-501-C-010-REV-2 - LCD
    [2] TWD-NL-2021-501-R-00-REV-1 - BoD
    [3] TBB_280_6KN_Opt_T1T2_acc
    [4] BM-PR305-EN-2002 LCO Operational BM Standard feeder
    [5] TWD-NL-2021-397-C-110, Standard feeder cylinder limits
    [6] M:\Engineering\R&D Projects\043 PyBM\Engineering\SF Tower Check Operational Accelerations\MM400_Op_Accelerations_Rev0.py
"""

import numpy as np

from ...constants import *
from ...marine.machines.T700 import T700
from ...utils.mass_items import Tower, VerticalStack, massItem

# These are calculated by using T3 from Vinayard

design_loads = np.array([9810319])

Hs_design_transit = 2.5

Hs_design_operational = 2.0

t700 = T700([0] * 3, 90)

t700_cyl_push_max = t700.cylinder.Maxforce

t700_cyl_pull_max = t700.cylinder.max_pulling_force()

t700_cyl_pass_max = t700.cylinder.max_passive_force()

t700_cyl_pull_max_act = 1431e3  # [4]

t700_cyl_push_max_act = 1431e3  # [4]

# print(
#     f"t700_cyl_push_max: {t700_cyl_push_max}\n t700_cyl_pull_max: {t700_cyl_pull_max} \n t700_cyl_pass_max: {t700_cyl_pass_max} "
# )

def unity_checks_tower(
    tower: massItem,
    tbic: massItem = None,
    lifting_tool: massItem = None,
    Hs_transit: float = None,
    Hs_operational: float = None,
    debug=False,
) -> np.array:
    raise ValueError("This function is not yet implemented")
    """Calculate unity checks of a different tower w.r.t. the standard feeder design conditions.

    :param tower: Tower properties
    :type tower: massItem
    :param tbic: TBIC properties, by default the vinyard TBIC will be used.
    :type tbic: massItem
    :param lifting_tool: Lifting tool properties, by default the vinyard tool will be used.
    :type lifting_tool: massItem
    :param Hs: [m] Significant Waave height used for acceleration scaling, defaults to 2.5m (transit)
    :type Hs: float
    :return: list of unity checks [Fz_max@TLS(transit), F_zc_max@cyl(comp), F_zc_min@cyl(comp), F_zc_max@cyl(off_lead), F_zc_min@cyl(off_lead)]
    :rtype: np.array
    """
    # Factors
    alfa_cog = 1.05  # [-] cog contigency factor
    gamma_bP = 1.0  # [-] load factor permanent
    gamma_bE = 1.3  # [-] load factor environmental
    if Hs_transit:
        hs_factor_transit = Hs_transit / Hs_design_transit
    else:
        hs_factor_transit = 1
    if Hs_operational:
        hs_factor_operational = Hs_operational / Hs_design_operational
    else:
        hs_factor_operational = 1

    # Standard feeder [1] 3.2.2
    standard_feeder = massItem(h=3.083, m=126e3, h_cog=0)
    standard_feeder.h_p_hcr = 0.750  # [m] height of platform to horizontal constraining rod

    # Compensated items
    if tbic is None:
        h = 1.26 + 0.685  # [m] height of TBIC above TPL [1] 3.2.3
        h_cog = h - 0.45  # [m] height of cog above TPL [1] 3.2.3
        tbic = massItem(h=h, m=21.01e3, h_cog=h_cog)  # [1] 3.2.3
    if lifting_tool is None:
        lifting_tool = massItem(h=3, m=33e3, h_cog=1.5)  # [1] 3.2.2

    items = [tbic, tower, lifting_tool]
    combined_items = VerticalStack(items, alfa_cog)
    combined_mass = np.array(
        [combined_items.m] * 3
        + [combined_items.I_shifted(combined_items.y_cog)]
        + [combined_items.I_shifted(combined_items.x_cog)]
        + [0]
    )

    # Platform mass defintion
    I_plat_X = standard_feeder.m * t700.h**2 / 36  # [kgm^2] Inertia of the platform
    I_plat_Y = standard_feeder.m * t700.cd**2 / 48  # [kgm^2] Inertia of the platform
    I_plat_Z = standard_feeder.m * (t700.cd**2 + t700.h) / 12  # [kgm^2] Assumed rectangular plate

    platform_mass = np.concatenate([[standard_feeder.m] * 3, [I_plat_X], [I_plat_Y], [I_plat_Z]])

    # Barge
    barge_h = 6.01  # [m] height
    barge_draft = 2.5  # [m] draft
    barge_fb = barge_h - barge_draft  # [m] freeboard
    barge_heel = 1 * np.pi / 180  # [rad] heel angle

    # Crane wire offset angle
    crane_offset = np.deg2rad(1)  # [rad] crane wire angle

    # Motions
    h_CoG_ma = 31.3  # [m] height of cog above baseline ref [1] 3.2.4
    nd = (barge_fb + standard_feeder.h + combined_items.h_cog) / (
        h_CoG_ma - barge_draft
    )  # scaling factor for change in CoG Height
    acc_scaling = np.array([nd] * 3 + [1] * 3)
    # compensating for roll, pitch, 10% residual motions.
    acc_scaling_comp = np.array([1, 1, 1, 0.1, 0.1, 1])

    # Accelerations
    deg_2_rad = np.array([1] * 3 + [np.pi / 180] * 3)  # convert acceletions to rad/s2

    # [2] Table 7.2
    acc_SP = np.array([1.15, 2.31, 1.15, 2.04, 1.68, 0.53]) * deg_2_rad * acc_scaling * hs_factor_transit
    acc_SR = np.array([0.85, 4.80, 1.45, 5.08, 1.26, 0.43]) * deg_2_rad * acc_scaling * hs_factor_transit
    acc_H = np.array([0.91, 4.45, 1.51, 4.38, 1.37, 0.54]) * deg_2_rad * acc_scaling * hs_factor_transit

    # [6] Operational accelerations
    acc_op_SP = (
        np.array([0.51487444, 0.74028488, 0.56138126, 1.57753921, 0.98918306, 0.50796321])
        * deg_2_rad
        * acc_scaling
        * hs_factor_operational
    )
    acc_op_SR = (
        np.array([0.49491255, 1.01060966, 0.74668371, 1.64471827, 0.95432135, 0.41811959])
        * deg_2_rad
        * acc_scaling
        * hs_factor_operational
    )
    acc_op_H = (
        np.array([0.47750771, 0.91693239, 0.78096528, 1.56467609, 1.00787201, 0.44262981])
        * deg_2_rad
        * acc_scaling
        * hs_factor_operational
    )

    # LC2 Static Weight
    F_LC2 = combined_items.m * g * gamma_bP
    Fz_platf = standard_feeder.m * g

    F_pas = combined_items.m * g * 0.5 + standard_feeder.m * g

    # Passive cylinder force
    F_zc_pass = np.amin([t700_cyl_pass_max, F_pas / 3])

    # Calculations from [4] define min and max forces in cylinders
    # F_cyl_min = F_zc_pass - t700_cyl_pull_max_act
    # F_cyl_max = t700_cyl_push_max_act + F_zc_pass

    # Transit loads, max forces Fz Mx My at TLS points
    def tls_loads(acc):
        loads = acc * combined_mass * gamma_bE
        Mx = loads[1] * (combined_items.h_cog + standard_feeder.h_p_hcr) + (F_LC2 + loads[2]) * combined_items.y_cog
        My = loads[0] * (combined_items.h_cog + standard_feeder.h_p_hcr) + (F_LC2 + loads[2]) * combined_items.x_cog
        M_heel = np.sin(barge_heel) * (F_LC2 + loads[2]) * (combined_items.h_cog + standard_feeder.h_p_hcr)
        Mx_tot = Mx + M_heel + loads[3]
        My_tot = My + loads[4]
        Fz = F_LC2 + loads[2]
        # points of contact between tower and feeder
        d1 = [0, tower.D / 2]
        d2 = [np.sqrt(3) * tower.D / 4, -tower.D / 4]
        d3 = [-np.sqrt(3) * tower.D / 4, -tower.D / 4]
        a = np.array([[1, 1, 1], [d1[1], d2[1], d3[1]], [d1[0], d2[0], d3[0]]])
        b = np.array([Fz, Mx_tot, My_tot])
        assert all(b >= 0), "Negative forces or moments"
        F_zc_a = np.abs(np.linalg.solve(a, b))
        # Max vertical force at contact point due to tower
        F_zc = np.amax(np.abs(F_zc_a))
        return np.array([F_zc])

    # [4] OLC-4b
    # compesansation. 100% variable load. accelerations equal, 0 residual acc R&P
    def comp_loads(acc):
        loads = acc * (combined_mass + platform_mass) * gamma_bE * acc_scaling_comp
        Mx = loads[1] * (combined_items.h_cog + standard_feeder.h_p_hcr) + (F_LC2 + loads[2]) * combined_items.y_cog
        My = loads[0] * (combined_items.h_cog + standard_feeder.h_p_hcr) + (F_LC2 + loads[2]) * combined_items.x_cog
        Mx_tot = Mx + loads[3]
        My_tot = My + loads[4]
        Fz = F_LC2 + loads[2] + Fz_platf
        assert all(np.array([Fz, Mx_tot, My_tot]) >= 0), "Negative forces or moments"
        # cylinder locations
        F_zc_a = t700.compute_cylinder_forces(Fz, Mx_tot, My_tot)
        # assert all(F_zc_a >= 0), "Negative forces at cylinder points"
        # Max/min vertical forces in cylinders
        F_zc_max = np.amax(F_zc_a)
        F_zc_min = np.amin(F_zc_a)
        # F_zc_pass = np.amin([t700_cyl_pass_max,(F_zc_max-F_zc_min)/2])
        return np.array([F_zc_max, F_zc_min])

    # [4] OLC-4d
    # Loads during operation, compensation. 10% load due to pretension in crane. assume 1deg horizontal pull of crane wire.
    def tpull_loads(acc):
        loads = acc * (combined_mass + platform_mass) * gamma_bE * acc_scaling_comp
        Mx = loads[1] * (combined_items.h_cog + standard_feeder.h_p_hcr) + (F_LC2 + loads[2]) * combined_items.y_cog
        My = loads[0] * (combined_items.h_cog + standard_feeder.h_p_hcr) + (F_LC2 + loads[2]) * combined_items.x_cog
        # Moment due to horizontal pull of crane
        M_crane = np.sin(crane_offset) * (0.9 * F_LC2) * (combined_items.h + standard_feeder.h_p_hcr) / gamma_bP
        Mx_tot = Mx + M_crane + loads[3]
        My_tot = My + loads[4]
        Fz = loads[2] + Fz_platf
        assert all(np.array([Fz, Mx_tot, My_tot]) >= 0), "Negative forces or moments"
        # points of contact between tower and feeder
        F_zc_a = t700.compute_cylinder_forces(Fz, Mx_tot, My_tot)
        # assert all(F_zc_a >= 0), "Negative forces at cylinder points"
        # Max/min vertical forces in cylinders
        F_zc_max = np.amax(F_zc_a)
        F_zc_min = np.amin(F_zc_a)
        # F_zc_pass = np.amin([t700_cyl_pass_max,(F_zc_max+F_zc_min)/2])
        return np.array([F_zc_max, F_zc_min])

    # print(f"Passive force per cylinder: {F_zc_pass:0.2f} [N]")
    cb_load = np.array([0])
    # active cylinder forces for operational accelerations, max and min. Min can never be positive, hence starts at 0.
    op1_load = np.array([-1e15, 0])
    op2_load = np.array([-1e15, 0])

    for acc in [acc_SP, acc_SR, acc_H]:
        # calculate the loads at the TLS points. maximum of the loads is taken
        cb_load = np.maximum(tls_loads(acc), cb_load)
    for acc in [acc_op_SP, acc_op_SR, acc_op_H]:
        # calculate the active cylinder forces for OLC-4b
        op1_loads_acc = comp_loads(acc) - F_zc_pass
        # indexed op1_load because the first element is the max and the second is the min
        op1_load = [
            np.amax(np.concatenate([op1_loads_acc, [op1_load[0]]])),
            np.amin(np.concatenate([op1_loads_acc, [op1_load[1]]])),
        ]
        # calculate the active cylinder forces for OLC-4d
        op2_loads_acc = tpull_loads(acc) - F_zc_pass
        op2_load = [
            np.amax(np.concatenate([op2_loads_acc, [op2_load[0]]])),
            np.amin(np.concatenate([op2_loads_acc, [op2_load[1]]])),
        ]
    if debug:
        return F_zc_pass, op1_load, op2_load, t700_cyl_push_max_act, -t700_cyl_pull_max_act
    # op1_load = [
    #     np.amax(np.concatenate([[op1_load[0]]])),
    #     np.amin(np.concatenate([[op1_load[1]], [0]])),
    # ]
    # op2_load = [
    #     np.amax(np.concatenate([[op2_load[0]]])),
    #     np.amin(np.concatenate([[op2_load[1]], [0]])),
    # ]
    cyl_limits = np.array([t700_cyl_push_max_act, -t700_cyl_pull_max_act])
    unity_checks = cb_load / design_loads
    unity_checks_cylforce1 = op1_load / cyl_limits
    unity_checks_cylforce2 = op2_load / cyl_limits
    return np.round(np.concatenate([unity_checks, unity_checks_cylforce1, unity_checks_cylforce2]), 2)
