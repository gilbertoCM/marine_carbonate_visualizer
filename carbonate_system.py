"""
Marine Carbonate System Calculator

Core calculations for TA-DIC-pH relationships using PyCO2SYS.
"""

import PyCO2SYS as pyco2


def calc_system(alk=None, dic=None, pH=None, pCO2=None, salinity=35, temperature=25):
    """
    Calculate carbonate system from any two parameters.

    At least two of TA, DIC, pH, pCO2 must be provided.

    Parameters:
    -----------
    alk : float, optional
        Total Alkalinity (μmol/kg)
    dic : float, optional
        Dissolved Inorganic Carbon (μmol/kg)
    pH : float, optional
        pH (total scale)
    pCO2 : float, optional
        Partial pressure of CO2 (μatm)
    salinity : float, default 35
        Salinity (PSU)
    temperature : float, default 25
        Temperature (°C)

    Returns:
    --------
    dict with keys: pH, pCO2, HCO3, CO3, DIC, TA, omega, salinity, temperature
    """

    params_provided = sum([x is not None for x in [alk, dic, pH, pCO2]])
    if params_provided < 2:
        raise ValueError("At least 2 of (alk, dic, pH, pCO2) must be provided")

    # Map parameters to PyCO2SYS format
    # par1_type: 1=TA, 2=DIC, 3=pH, 4=pCO2
    param_map = {1: alk, 2: dic, 3: pH, 4: pCO2}
    available_types = [k for k, v in param_map.items() if v is not None]

    par1_type, par1 = available_types[0], param_map[available_types[0]]
    par2_type, par2 = available_types[1], param_map[available_types[1]]

    results = pyco2.sys(
        par1=par1, par2=par2,
        par1_type=par1_type, par2_type=par2_type,
        salinity=salinity, temperature=temperature, pressure=0,
        opt_pH_scale=1, opt_k_carbonic=10
    )

    return {
        'pH': float(results['pH_total']),
        'pCO2': float(results['pCO2']),
        'HCO3': float(results['bicarbonate']),
        'CO3': float(results['carbonate']),
        'CO2': float(results['CO2']),
        'DIC': float(results['dic']),
        'TA': float(results['alkalinity']),
        'omega': float(results['saturation_aragonite']),
        'salinity': salinity,
        'temperature': temperature
    }


def validate_carbonate_system(result, tolerance=0.01):
    """
    Validate physical and chemical consistency of carbonate system.

    Checks:
    - All values are positive
    - DIC = CO2 + HCO3 + CO3 (within tolerance)
    - pH is in reasonable range (4-11)
    - pCO2 is positive

    Parameters:
    -----------
    result : dict
        Result from calc_system()
    tolerance : float, default 0.01
        Tolerance for DIC check (as fraction)

    Returns:
    --------
    dict with 'valid' (bool) and 'errors' (list)
    """
    errors = []

    # Check positivity
    for key in ['pH', 'DIC', 'HCO3', 'CO3', 'CO2', 'TA', 'pCO2']:
        if result[key] < 0:
            errors.append(f"{key} is negative: {result[key]}")

    # Check pH range
    if not (4 <= result['pH'] <= 11):
        errors.append(f"pH {result['pH']} out of range (4-11)")

    # Check DIC conservation: DIC ≈ CO2 + HCO3 + CO3
    dic_sum = result['CO2'] + result['HCO3'] + result['CO3']
    dic_error = abs(dic_sum - result['DIC']) / result['DIC']
    if dic_error > tolerance:
        errors.append(f"DIC conservation failed: {dic_sum:.1f} vs {result['DIC']:.1f} (error: {dic_error*100:.2f}%)")

    # Check pCO2 > 0
    if result['pCO2'] <= 0:
        errors.append(f"pCO2 is not positive: {result['pCO2']}")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'dic_conservation_error': dic_error if 'dic_error' in locals() else None
    }


def check_oceanic_ranges(result):
    """
    Check if result is within typical oceanic ranges.

    Reference ranges:
    - pH: 7.8-8.3 (modern ocean)
    - TA: 2250-2350 μmol/kg (typical seawater)
    - DIC: 1900-2250 μmol/kg (typical seawater)
    - HCO3: 1800-2100 μmol/kg (dominant species)
    - CO3: 80-250 μmol/kg
    - Omega: 0.5-4.5 (sustainable range)

    Returns:
    --------
    dict with warnings for out-of-range values
    """
    warnings = []

    ranges = {
        'pH': (7.8, 8.3),
        'TA': (2250, 2350),
        'DIC': (1900, 2250),
        'HCO3': (1800, 2100),
        'CO3': (80, 250),
        'omega': (0.5, 4.5)
    }

    for key, (min_val, max_val) in ranges.items():
        if key in result:
            val = result[key]
            if not (min_val <= val <= max_val):
                warnings.append(f"{key}: {val:.2f} outside typical range ({min_val}-{max_val})")

    return {'warnings': warnings}
