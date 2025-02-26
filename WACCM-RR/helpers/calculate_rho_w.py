def converta_omega_to_w(omega,T,pressure): # Convert Pa/s to m/s (take care with units!)
    """_summary_

    omega - vertical velocity in Pa/s
    T - temperature in Kelvin
    pressure - atmospheric pressure in hPa (take care with units!)
    
    returns vertical velocity data array in m/s
    """

    
    # Calculate mass density: kg m^-3
    # Conversion constants
    R = 287.058 # J/ kg^-1 K^-1 => m^2 s^-2 K^-1
    to_Pa = 100 # convert from hPa to Pa. Pa => kg m^-1 s^-2
    rho = pressure*to_Pa/(R*T) # Units: kg m^-1 s^-2 * m^-2 s^2 K * K^-1 => kg m^-3

    g = 9.80665 # m s^-2
    w = -omega/(rho*g) # Units: kg m^-1 s^-2 * s^-1 * kg^-1 m^3 * m^-1 s^2 => m s^-1

    return w



# # ds = xr dataset containing 'lev' and 'T'

# ### Calculate mass density: kg m^-3 (take care with units!)
# # Conversion constants
# R = 287.058 # J/ kg^-1 K^-1 => m^2 s^-2 K^-1
# to_Pa = 100 # convert from hPa to Pa. Pa => kg m^-1 s^-2
# rho = ds['lev']*to_Pa/(R*ds['T']) # Units: kg m^-1 s^-2 * m^-2 s^2 K * K^-1 => kg m^-3

# # ds = xr dataset containing 'lev' and 'T'

# ### Calculate number density: particles cm^-3 (take care with units!)
# # Conversion constants
# k = 1.380649e-23 # Boltzmann constant J K^-1 =  kg m^2 s^-2 K^-1
# to_cm3 = 1e6 # convertion from m^3 to cm^3
# to_Pa = 100 # convert from hPa to Pa. Pa = kg m^-1 s^-2
# n = ds['lev']*to_Pa/(to_cm3*k*ds['T']) # Units: kg m^-1 s^-2 * kg^-1 m^-2 s^2 K * K^-1 = m^-3 | m^-3 * 1e-6 = cm^-3

