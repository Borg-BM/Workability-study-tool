# DNV-RP-C205 (2014-04) Appendix B/C: the "GWS" 104-zone nautic grid used for long-term wave
# statistics, and Table C-1's Weibull/lognormal parameters for the significant wave height and
# zero-crossing period in each zone.
#
# Table C-1 gives, per zone: alpha_s, beta_s (3-parameter Weibull scale/shape for Hs, with the
# location parameter gamma_s = 0 fixed for every zone), and a1, a2, b1, b2 -- the zone-dependent
# terms of the conditional lognormal distribution of Tz given Hs:
#   mu    = a0 + a1 * Hs^a2   (a0 = 0.70, fixed for every zone)
#   sigma = b0 + b1 * exp(b2 * Hs)   (b0 = 0.07, fixed for every zone)
# This lines up exactly with DNVLoader's (alpha_s, beta_s, a1, a2, b1, b2, a0, b0, gamma_s).
#
# ZONE_BBOX gives the lat/long rectangle per zone for the map picker, matching the boundaries
# in the DNV-RP-C205 Appendix B map.

WEIBULL_PARAM_KEYS = ("alpha_s", "beta_s", "a1", "a2", "b1", "b2", "a0", "b0", "gamma_s")

_A0 = 0.70
_B0 = 0.07

# Table C-1: zone -> (alpha_s, beta_s, a1, a2, b1, b2)
_ZONE_PARAMS: dict[int, tuple[float, float, float, float, float, float]] = {
    1: (2.33, 1.33, 0.974, 0.205, 0.1263, -0.0201),
    2: (1.96, 1.34, 0.994, 0.175, 0.1414, -0.0238),
    3: (2.74, 1.35, 1.127, 0.160, 0.1255, -0.0912),
    4: (2.84, 1.53, 1.125, 0.150, 0.0978, -0.0074),
    5: (1.76, 1.59, 0.828, 0.167, 0.3449, -0.2073),
    6: (2.76, 1.45, 1.128, 0.154, 0.0964, -0.0066),
    7: (3.39, 1.75, 1.256, 0.118, 0.0809, -0.0069),
    8: (3.47, 1.57, 1.272, 0.114, 0.0728, -0.0015),
    9: (3.56, 1.61, 1.260, 0.119, 0.0755, -0.0054),
    10: (2.45, 1.37, 1.036, 0.181, 0.1166, -0.0137),
    11: (2.19, 1.26, 0.935, 0.222, 0.1386, -0.0208),
    12: (3.31, 1.56, 1.150, 0.150, 0.0934, -0.0409),
    13: (3.18, 1.64, 1.257, 0.111, 0.0850, -0.0032),
    14: (2.62, 1.46, 1.215, 0.115, 0.0976, -0.0111),
    15: (3.09, 1.50, 1.207, 0.134, 0.0855, -0.0124),
    16: (3.42, 1.56, 1.243, 0.126, 0.0898, -0.0528),
    17: (2.77, 1.41, 1.197, 0.135, 0.0954, -0.0083),
    18: (1.66, 1.14, 1.310, 0.121, 0.4006, -0.2123),
    19: (2.48, 1.35, 1.085, 0.166, 0.1071, -0.0096),
    20: (3.15, 1.48, 1.196, 0.139, 0.0914, -0.0248),
    21: (2.97, 1.69, 1.249, 0.111, 0.1044, -0.0452),
    22: (2.29, 1.72, 1.139, 0.117, 0.1160, -0.0177),
    23: (2.23, 1.39, 1.039, 0.167, 0.1248, -0.0131),
    24: (2.95, 1.48, 1.211, 0.131, 0.0859, -0.0059),
    25: (2.90, 1.61, 1.268, 0.096, 0.1055, -0.0521),
    26: (1.81, 1.30, 0.858, 0.232, 0.1955, -0.0497),
    27: (1.76, 1.30, 0.880, 0.218, 0.1879, -0.0419),
    28: (1.81, 1.28, 0.841, 0.241, 0.1977, -0.0498),
    29: (2.31, 1.38, 0.976, 0.197, 0.1288, -0.0184),
    30: (3.14, 1.56, 1.243, 0.118, 0.0861, -0.0122),
    31: (2.62, 1.79, 1.219, 0.126, 0.1022, -0.0116),
    32: (1.81, 1.47, 0.950, 0.158, 0.1685, -0.0312),
    33: (2.17, 1.66, 1.111, 0.135, 0.1191, -0.0147),
    34: (2.46, 1.70, 1.189, 0.141, 0.1059, -0.0055),
    35: (2.74, 2.05, 1.219, 0.128, 0.1097, -0.0101),
    36: (2.32, 1.82, 1.111, 0.143, 0.1165, -0.0189),
    37: (1.66, 1.53, 0.815, 0.199, 0.2754, -0.1051),
    38: (1.23, 1.24, 0.616, 0.332, 0.3204, -0.0054),
    39: (1.74, 1.37, 0.798, 0.239, 0.2571, -0.0908),
    40: (2.36, 1.42, 0.975, 0.195, 0.1288, -0.0214),
    41: (2.47, 1.50, 1.044, 0.161, 0.1166, -0.0158),
    42: (2.32, 1.41, 1.121, 0.128, 0.1159, -0.0118),
    43: (2.78, 1.78, 1.222, 0.124, 0.1029, -0.0078),
    44: (2.83, 2.17, 1.181, 0.149, 0.1005, -0.0124),
    45: (2.60, 2.07, 1.177, 0.173, 0.1017, -0.0258),
    46: (1.76, 1.44, 1.070, 0.139, 0.1365, -0.0306),
    47: (2.30, 1.78, 1.058, 0.149, 0.1301, -0.0250),
    48: (2.55, 2.20, 1.160, 0.172, 0.1048, -0.0233),
    49: (2.50, 2.13, 1.141, 0.149, 0.1223, -0.0123),
    50: (2.05, 1.28, 0.879, 0.237, 0.1651, -0.0344),
    51: (1.78, 1.44, 0.952, 0.159, 0.1763, -0.0544),
    52: (2.14, 1.50, 1.072, 0.133, 0.1271, -0.0245),
    53: (2.56, 1.93, 1.188, 0.129, 0.1041, -0.0091),
    54: (2.45, 2.19, 1.176, 0.168, 0.1097, -0.0091),
    55: (1.83, 1.96, 1.046, 0.143, 0.1542, -0.0191),
    56: (2.40, 2.18, 1.157, 0.157, 0.1067, -0.0169),
    57: (2.17, 2.19, 1.083, 0.214, 0.1202, -0.0173),
    58: (1.85, 2.08, 1.013, 0.165, 0.1578, -0.0248),
    59: (2.02, 1.76, 1.025, 0.159, 0.1432, -0.0254),
    60: (1.93, 1.39, 1.057, 0.145, 0.1349, -0.0215),
    61: (2.10, 1.82, 1.080, 0.132, 0.1300, -0.0261),
    62: (1.73, 1.39, 0.871, 0.214, 0.1941, -0.0266),
    63: (1.88, 1.70, 1.026, 0.155, 0.1477, -0.0224),
    64: (2.34, 2.16, 1.138, 0.186, 0.1134, -0.0062),
    65: (2.02, 1.90, 1.132, 0.169, 0.1187, -0.0125),
    66: (2.33, 2.15, 1.115, 0.183, 0.1192, -0.0203),
    67: (2.43, 2.21, 1.159, 0.155, 0.1056, -0.0194),
    68: (2.42, 2.16, 1.121, 0.155, 0.1243, -0.0151),
    69: (2.23, 1.89, 1.177, 0.124, 0.1176, -0.0101),
    70: (2.32, 1.84, 1.170, 0.167, 0.1659, -0.2086),
    71: (1.79, 1.69, 1.005, 0.147, 0.1602, -0.0309),
    72: (2.44, 1.93, 1.158, 0.187, 0.1068, -0.0110),
    73: (2.80, 2.26, 1.174, 0.182, 0.1050, -0.0493),
    74: (2.23, 1.69, 1.143, 0.148, 0.1148, -0.0087),
    75: (2.69, 1.67, 1.216, 0.118, 0.0991, -0.0103),
    76: (2.86, 1.77, 1.218, 0.143, 0.1016, -0.0251),
    77: (3.04, 1.83, 1.213, 0.152, 0.0844, 0.0),
    78: (2.60, 1.70, 1.244, 0.073, 0.1060, -0.0059),
    79: (2.18, 1.53, 1.069, 0.131, 0.1286, -0.0173),
    80: (2.54, 1.70, 1.201, 0.131, 0.1019, -0.0101),
    81: (2.83, 1.71, 1.218, 0.144, 0.1017, -0.0258),
    82: (2.84, 1.94, 1.209, 0.146, 0.0911, 0.0),
    83: (2.60, 1.83, 1.214, 0.132, 0.1076, -0.0080),
    84: (2.92, 2.10, 1.190, 0.170, 0.1018, -0.0972),
    85: (3.32, 1.94, 1.226, 0.145, 0.0947, -0.0505),
    86: (2.91, 1.54, 1.261, 0.111, 0.0865, -0.0031),
    87: (2.43, 1.40, 1.203, 0.129, 0.1009, -0.0072),
    88: (3.35, 1.75, 1.248, 0.128, 0.0842, -0.0194),
    89: (3.02, 1.45, 1.249, 0.124, 0.0938, -0.0444),
    90: (3.35, 1.59, 1.266, 0.116, 0.0766, -0.0051),
    91: (3.54, 1.68, 1.281, 0.110, 0.0829, -0.0400),
    92: (3.42, 1.71, 1.283, 0.105, 0.0831, -0.0230),
    93: (2.66, 1.45, 1.233, 0.119, 0.1011, -0.0198),
    94: (3.89, 1.69, 1.296, 0.112, 0.0632, 0.0),
    95: (3.71, 1.93, 1.256, 0.131, 0.0726, -0.0022),
    96: (2.65, 1.47, 1.200, 0.110, 0.0986, -0.0103),
    97: (3.61, 1.63, 1.279, 0.114, 0.0733, -0.0029),
    98: (3.53, 1.70, 1.248, 0.135, 0.0744, -0.0025),
    99: (4.07, 1.77, 1.305, 0.106, 0.0614, -0.0011),
    100: (3.76, 1.54, 1.279, 0.120, 0.0636, -0.0006),
    101: (3.21, 1.57, 1.261, 0.116, 0.0934, -0.0049),
    102: (3.08, 1.60, 1.243, 0.130, 0.0833, -0.0046),
    103: (3.52, 1.58, 1.253, 0.122, 0.0758, -0.0056),
    104: (2.97, 1.57, 1.267, 0.108, 0.0847, -0.0049),
}

# zone -> (lat_min, lat_max, lon_min, lon_max, short region hint)
_ZONE_BBOX: dict[int, tuple[float, float, float, float, str]] = {
    1: (65.0, 75.0, 10.0, 30.0, "Svalbard / Barents Sea"),
    2: (60.0, 70.0, -60.0, -45.0, "Davis Strait / Labrador Sea"),
    3: (60.0, 70.0, -45.0, -15.0, "North Atlantic / South Greenland"),
    4: (60.0, 70.0, -15.0, 10.0, "Norwegian Sea / Iceland"),
    5: (50.0, 65.0, 12.0, 30.0, "Baltic / North Europe"),
    6: (55.0, 60.0, -160.0, -130.0, "Bering Sea / Gulf of Alaska"),
    7: (50.0, 55.0, -170.0, -135.0, "Aleutians / Gulf of Alaska"),
    8: (50.0, 60.0, -60.0, -30.0, "NW Atlantic / Labrador"),
    9: (50.0, 60.0, -30.0, -11.0, "NE Atlantic Ocean"),
    10: (50.0, 55.0, -11.0, -2.0, "Celtic Sea / UK"),
    11: (51.0, 60.0, -2.0, 8.0, "North Sea"),
    12: (50.0, 55.0, 160.0, 190.0, "North Pacific Ocean"),
    13: (40.0, 50.0, -170.0, -130.0, "NE Pacific Ocean"),
    14: (40.0, 48.0, -130.0, -122.0, "US Pacific NW Coast"),
    15: (40.0, 50.0, -70.0, -40.0, "NW Atlantic / Grand Banks"),
    16: (40.0, 50.0, -40.0, -8.0, "Central North Atlantic"),
    17: (42.0, 50.0, -8.0, 0.0, "Bay of Biscay / West Europe"),
    18: (35.0, 50.0, 130.0, 140.0, "Yellow Sea / Sea of Japan"),
    19: (40.0, 50.0, 142.0, 150.0, "Japan / Sea of Okhotsk"),
    20: (40.0, 50.0, 150.0, 190.0, "NW Pacific Ocean"),
    21: (30.0, 40.0, -170.0, -130.0, "North Central Pacific"),
    22: (20.0, 40.0, -130.0, -105.0, "Off Baja California"),
    23: (30.0, 42.0, -80.0, -70.0, "US East Coast / Bermuda"),
    24: (30.0, 40.0, -70.0, -40.0, "Mid-North Atlantic"),
    25: (30.0, 40.0, -40.0, -10.0, "East Atlantic / Azores"),
    26: (30.0, 45.0, 0.0, 13.0, "West Mediterranean"),
    27: (30.0, 40.0, 13.0, 37.0, "East Mediterranean / Black Sea"),
    28: (30.0, 40.0, 120.0, 130.0, "East China Sea"),
    29: (30.0, 35.0, 130.0, 145.0, "South of Japan"),
    30: (30.0, 40.0, 145.0, 190.0, "West Pacific Subtropical"),
    31: (20.0, 30.0, -170.0, -130.0, "Central North Pacific"),
    32: (20.0, 30.0, -100.0, -80.0, "Gulf of Mexico"),
    33: (20.0, 30.0, -80.0, -60.0, "Sargasso Sea / Bahamas"),
    34: (20.0, 30.0, -60.0, -40.0, "Central Atlantic Ocean"),
    35: (20.0, 30.0, -40.0, -20.0, "East Atlantic / Canaries"),
    36: (10.0, 30.0, -20.0, -10.0, "Off West Africa"),
    37: (10.0, 30.0, 33.0, 46.0, "Red Sea / Gulf of Aden"),
    38: (24.0, 31.0, 46.0, 56.0, "Persian Gulf"),
    39: (20.0, 30.0, 56.0, 75.0, "Arabian Sea"),
    40: (10.0, 30.0, 105.0, 121.0, "South China Sea"),
    41: (20.0, 30.0, 121.0, 130.0, "Philippine Sea West"),
    42: (20.0, 30.0, 130.0, 150.0, "Philippine Sea East"),
    43: (20.0, 30.0, 150.0, 190.0, "Tropical West Pacific"),
    44: (10.0, 20.0, -180.0, -140.0, "Tropical North Pacific"),
    45: (10.0, 20.0, -140.0, -110.0, "NE Tropical Pacific"),
    46: (10.0, 20.0, -110.0, -90.0, "Off Central America"),
    47: (10.0, 20.0, -85.0, -55.0, "Caribbean Sea"),
    48: (10.0, 20.0, -55.0, -40.0, "Tropical NW Atlantic"),
    49: (10.0, 20.0, -40.0, -20.0, "Tropical Mid-Atlantic"),
    50: (10.0, 20.0, 46.0, 75.0, "North Indian Ocean"),
    51: (10.0, 22.0, 80.0, 100.0, "Bay of Bengal"),
    52: (10.0, 20.0, 121.0, 150.0, "West Pacific Equatorial"),
    53: (10.0, 20.0, 150.0, 180.0, "Western Equatorial Pacific"),
    54: (-10.0, 10.0, -175.0, -135.0, "Central Equatorial Pacific"),
    55: (0.0, 10.0, -90.0, -80.0, "Panama Basin / Galapagos"),
    56: (0.0, 10.0, -60.0, -40.0, "Off Amazon River Mouth"),
    57: (0.0, 10.0, -40.0, -15.0, "Equatorial Atlantic"),
    58: (0.0, 10.0, -15.0, 10.0, "Gulf of Guinea"),
    59: (-10.0, 10.0, 40.0, 50.0, "East Africa Coast / Somali"),
    60: (0.0, 10.0, 50.0, 80.0, "Equatorial Indian Ocean"),
    61: (0.0, 10.0, 80.0, 100.0, "East Equatorial Indian Ocean"),
    62: (0.0, 10.0, 100.0, 115.0, "Indonesian Seas"),
    63: (0.0, 10.0, 130.0, 160.0, "Coral Sea North / Solomon"),
    64: (-10.0, 0.0, -110.0, -85.0, "SE Tropical Pacific"),
    65: (-20.0, 0.0, -85.0, -70.0, "Peru Current / Coast"),
    66: (-10.0, 0.0, -50.0, -30.0, "Off NE Brazil"),
    67: (-20.0, 0.0, -30.0, -10.0, "Tropical South Atlantic"),
    68: (-20.0, 0.0, -10.0, 10.0, "SE Atlantic / Angola Basin"),
    69: (-10.0, 0.0, 50.0, 80.0, "South Tropical Indian Ocean"),
    70: (-10.0, 0.0, 80.0, 105.0, "Mid South Indian Ocean"),
    71: (-10.0, 0.0, 150.0, 190.0, "South Pacific Ocean"),
    72: (-20.0, -10.0, -180.0, -130.0, "South Central Pacific"),
    73: (-20.0, -10.0, -130.0, -85.0, "South East Central Pacific"),
    74: (-30.0, -10.0, -50.0, -30.0, "Off Brazil Coast"),
    75: (-30.0, -10.0, 30.0, 50.0, "Mozambique Channel"),
    76: (-30.0, -10.0, 50.0, 90.0, "Subtropical South Indian"),
    77: (-30.0, -10.0, 90.0, 110.0, "East South Indian Ocean"),
    78: (-30.0, -10.0, 110.0, 130.0, "Off West Australia"),
    79: (-30.0, -10.0, 140.0, 160.0, "Coral Sea South / Coast"),
    80: (-30.0, -10.0, 160.0, 180.0, "South Pacific Subtropical"),
    81: (-30.0, -20.0, -180.0, -140.0, "South Pacific Basin"),
    82: (-30.0, -20.0, -140.0, -110.0, "South Pacific Mid-East"),
    83: (-40.0, -20.0, -85.0, -70.0, "Off Chile Coast"),
    84: (-30.0, -20.0, -30.0, 10.0, "South Atlantic Basin"),
    85: (-40.0, -20.0, 10.0, 20.0, "Off South Africa / Agulhas"),
    86: (-40.0, -30.0, -185.0, -120.0, "South Pacific Temperate"),
    87: (-40.0, -30.0, -65.0, -40.0, "Argentine Basin / Coast"),
    88: (-40.0, -30.0, -40.0, -15.0, "SW Atlantic Ocean"),
    89: (-40.0, -30.0, -15.0, 10.0, "Mid South Atlantic"),
    90: (-40.0, -30.0, 20.0, 40.0, "Agulhas Retroflection"),
    91: (-40.0, -30.0, 40.0, 110.0, "Southern Indian Ocean"),
    92: (-40.0, -30.0, 110.0, 145.0, "Great Australian Bight"),
    93: (-40.0, -30.0, 145.0, 175.0, "Tasman Sea"),
    94: (-50.0, -40.0, -150.0, -120.0, "South Pacific Deep"),
    95: (-50.0, -40.0, -90.0, -70.0, "SE Pacific / Chile Rise"),
    96: (-50.0, -40.0, -70.0, -50.0, "Falkland Islands / Patagonia"),
    97: (-50.0, -40.0, -50.0, -10.0, "South Atlantic Subpolar"),
    98: (-50.0, -40.0, -10.0, 40.0, "SE Atlantic Subpolar"),
    99: (-50.0, -40.0, 40.0, 90.0, "SW Indian Subpolar"),
    100: (-50.0, -40.0, 90.0, 140.0, "SE Indian Subpolar"),
    101: (-50.0, -40.0, 140.0, 170.0, "South of Australia / NZ"),
    102: (-50.0, -40.0, -190.0, -150.0, "South Pacific Boundary"),
    103: (-60.0, -50.0, -80.0, -60.0, "Drake Passage"),
    104: (-55.0, -50.0, -60.0, -30.0, "Scotia Sea / Scotia Arc"),
}


def _build_locations() -> dict[str, dict]:
    """Joins _ZONE_PARAMS (the Table C-1 Weibull numbers) with _ZONE_BBOX (the map
    boundaries) into one flat dict keyed by "gws_zone_<n>" id -- the shape both
    resolve_weibull_params() below and the /api/locations route expect. A zone missing
    from either dict would KeyError here at import time (fail fast, not at request time)."""
    locations: dict[str, dict] = {}
    for zone, (alpha_s, beta_s, a1, a2, b1, b2) in _ZONE_PARAMS.items():
        lat_min, lat_max, lon_min, lon_max, region = _ZONE_BBOX[zone]
        locations[f"gws_zone_{zone}"] = {
            "label": f"GWS Zone {zone} — {region}",
            "zone": zone,
            "region": region,
            "alpha_s": alpha_s,
            "beta_s": beta_s,
            "a1": a1,
            "a2": a2,
            "b1": b1,
            "b2": b2,
            "a0": _A0,
            "b0": _B0,
            "gamma_s": 0.0,
            "bbox": {"lat_min": lat_min, "lat_max": lat_max, "lon_min": lon_min, "lon_max": lon_max},
        }
    return locations


# DNV-RP-C205 Table C-1: 104 nautic zones ("GWS ocean areas") with their Weibull/lognormal
# parameters for Hs and Tz, and their Appendix B boundaries.
LOCATIONS: dict[str, dict] = _build_locations()


def resolve_weibull_params(location_id: str | None) -> tuple[dict, str]:
    """Return (params, label) for one of the 104 built-in DNV-RP-C205 zones -- the one
    entry point pybm_service.py's _build_hindcast() uses for scatter_source ==
    "weibull_builtin". Raises ValueError -- turned into a 422 by the router -- on an
    unknown location_id, rather than silently falling back to a default zone."""
    if location_id not in LOCATIONS:
        raise ValueError(f"Unknown location '{location_id}'. Available: {', '.join(LOCATIONS)}")

    entry = LOCATIONS[location_id]
    return {k: entry[k] for k in WEIBULL_PARAM_KEYS}, entry["label"]
