import numpy as np

def calculate_cyl_deadlength(d_bore):
    """Calculate total length of cylinder.
    based on rule of thumb calculation by BHO ('template cylinder sizing.xlsx')

    :param stroke: [m] Stroke of cylinder
    :param diameter: [m] Diameter of cylinder
    :return: [m] Dead length of cylinder
    """
    deadlength = 3.5 * d_bore + 200e-3
    return deadlength

def buckling_check(Fz, d_rod, buckling_length, E=210000e6):
    """Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx')

    :param Fz: [N] Axial force
    :param bore: [m] Bore of cylinder
    :param rod: [m] Rod of cylinder
    :param buckling_length: [m] Length of cylinder rod
    :param E: [Pa] Young's modulus of cylinder
    :return: [bool] True if buckling occurs
    """
    I = np.pi * (d_rod * 1e3) ** 4 / 64  # mm^4, moment of inertia
    v = 3  # safety factor for buckling
    lambda_ = 4 * buckling_length / d_rod  # slenderness ratio, [-]
    lambda_0 = 89
    if lambda_ > lambda_0:
        # Euler
        Fbuckling = np.pi**2 * E * I / (v * (buckling_length * 1e3) ** 2)
    else:
        # Tetmajer
        Fbuckling = np.pi * (d_rod * 1e3) ** 2 * (335 - 0.62 * lambda_) / (4 * v)
    return Fz / Fbuckling

# def buckling_check_dnv(Fz, d_rod, buckling_length, E = 210000):
#     """Check for buckling of the cylinder rod. (acc. DNVGL-ST-0378)

#     :param Fz: [N] Axial force
#     :param bore: [m] Bore of cylinder
#     :param rod: [m] Rod of cylinder
#     :param buckling_length: [m] Length of cylinder rod
#     :param E: [Pa] Young's modulus of cylinder
#     :return: [bool] True if buckling occurs
#     """
#     I = np.pi * (d_rod*1e3)**4 / 64 # mm^4, moment of inertia
#     v = 3 # safety factor for buckling
#     lambda_ = 4*buckling_length/d_rod # slenderness ratio, [-]
#     lambda_0 = 89
#     if lambda_ > lambda_0:
#         # Euler
#         Fbuckling = np.pi**2*E*I/(v*(buckling_length*1e3)**2)
#     else:
#         # Tetmajer
#         Fbuckling = np.pi*(d_rod*1e3)**2*(335-0.62*lambda_)/(4*v)
#     return Fz / Fbuckling

def get_min_rod_diameter(Fz, buckling_length, E=210000):
    """Check for buckling of the cylinder rod. (acc. BHO 'template cylinder sizing.xlsx')

    :param Fz: [N] Axial force
    :param bore: [m] Bore of cylinder
    :param rod: [m] Rod of cylinder
    :param buckling_length: [m] Length of cylinder rod
    :param E: [N/mm^2] Young's modulus of cylinder
    :return: [bool] True if buckling occurs
    """
    v = 3  # safety factor for buckling
    L = buckling_length * 1e3  # mm, length of cylinder rod
    d_rod_euler = np.power(Fz * 64 * v * L**2 / (np.pi**3 * E), 1 / 4) * 1e-3
    tetmajer = np.array(
        [np.pi / (4 * v) * 335, -np.pi / (4 * v) * 0.62 * 4 * L, -Fz]
    )  # coefficients for tetmajer equation
    d_rod_tetmajer = np.roots(tetmajer) * 1e-3
    d_rod_tetmajer = d_rod_tetmajer[d_rod_tetmajer > 0][0].item()

    lambda_e = 4 * buckling_length / d_rod_euler  # slenderness ratio, [-]
    lambda_t = 4 * buckling_length / d_rod_tetmajer  # slenderness ratio, [-]
    lambda_0 = 89
    if lambda_e > lambda_0:
        return d_rod_euler
    if lambda_t < lambda_0:
        return d_rod_tetmajer
    raise ValueError("No valid rod diameter found")
