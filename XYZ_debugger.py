import numpy as np

# def geodetic_to_ecef(lat, lon, alt):
#     a = 6378137.0
#     f = 1 / 298.257223563
#     e2 = 2 * f - f**2
#     lat_rad = np.radians(lat)
#     lon_rad = np.radians(lon)
#     N = a / np.sqrt(1 - e2 * np.sin(lat_rad)**2)
#     X = (N + alt) * np.cos(lat_rad) * np.cos(lon_rad)
#     Y = (N + alt) * np.cos(lat_rad) * np.sin(lon_rad)
#     Z = (N * (1 - e2) + alt) * np.sin(lat_rad)
#     return X, Y, Z

# def az_el_to_local_tangential(az, el, distance):
#     az_rad = np.radians(az)
#     el_rad = np.radians(el)
#     x_prime = distance * np.cos(el_rad) * np.sin(az_rad)
#     y_prime = distance * np.cos(el_rad) * np.cos(az_rad)
#     z_prime = distance * np.sin(el_rad)
#     return x_prime, y_prime, z_prime

# def local_tangential_to_ecef(lat, lon, x_prime, y_prime, z_prime):
#     lat_rad = np.radians(lat)
#     lon_rad = np.radians(lon)
#     rotation_matrix = np.array([
#         [-np.sin(lon_rad), np.cos(lon_rad), 0],
#         [-np.sin(lat_rad) * np.cos(lon_rad), -np.sin(lat_rad) * np.sin(lon_rad), np.cos(lat_rad)],
#         [np.cos(lat_rad) * np.cos(lon_rad), np.cos(lat_rad) * np.sin(lon_rad), np.sin(lat_rad)]
#     ])
#     ecef_coords = np.dot(rotation_matrix, np.array([x_prime, y_prime, z_prime]))
#     return ecef_coords

# def az_el_to_ecef(lat, lon, alt, az, el, distance):
#     X0, Y0, Z0 = geodetic_to_ecef(lat, lon, alt)
#     x_prime, y_prime, z_prime = az_el_to_local_tangential(az, el, distance)
#     ecef_coords = local_tangential_to_ecef(lat, lon, x_prime, y_prime, z_prime)
#     return X0 + ecef_coords[0], Y0 + ecef_coords[1], Z0 + ecef_coords[2]

def az_el_ra_to_xyz(sat_az, sat_el, sat_rang, site_lat, site_long):
    """
    Convert satellite Azimuth, Elevation, and Range to ECEF coordinates.

    Args:
        sat_az (float): Satellite azimuth in degrees.
        sat_el (float): Satellite elevation in degrees.
        sat_rang (float): Satellite range in kilometers.
        site_lat (float): Observer's latitude in radians.
        site_long (float): Observer's longitude in radians.
        

    Returns:
        tuple: Satellite ECEF coordinates (sat_x, sat_y, sat_z) in meters.
    """

    # Observer's ECEF XYZ coordinates in meters.
    site_xx = 4194426.1 
    site_yy = 1162694.5
    site_zz = 4647246.9

    # Convert inputs to radians and meters
    sat_az = np.radians(sat_az)  # Convert azimuth from degrees to radians
    sat_el = np.radians(sat_el)  # Convert elevation from degrees to radians
    sat_rang = sat_rang * 1000  # Convert range from kilometers to meters

    # Calculate local tangential coordinates
    south = -sat_rang * np.cos(sat_el) * np.cos(sat_az)
    east = sat_rang * np.cos(sat_el) * np.sin(sat_az)
    zenith = sat_rang * np.sin(sat_el)

    # Precompute trigonometric values for site latitude and longitude
    site_lat_sin = np.sin(site_lat)
    site_lat_cos = np.cos(site_lat)
    site_long_sin = np.sin(site_long)
    site_long_cos = np.cos(site_long)

    # Calculate ECEF coordinates
    sat_x = (site_lat_sin * site_long_cos * south) + (-site_long_sin * east) + (site_lat_cos * site_long_cos * zenith) + site_xx
    sat_y = (site_lat_sin * site_long_sin * south) + (site_long_cos * east) + (site_lat_cos * site_long_sin * zenith) + site_yy
    sat_z = (-site_lat_cos * south) + (site_lat_sin * zenith) + site_zz

    return sat_x, sat_y, sat_z

lat_graz = 47.0671
lon_graz = 15.4933
alt_graz = 539.4

az_test = 318.9604
el_test = 5.3959
dist_test = 2842.4619

# print(az_el_to_ecef(lat_graz, lon_graz, alt_graz, az_test, el_test, dist_test))
print(az_el_ra_to_xyz(az_test, el_test, dist_test, np.radians(lat_graz), np.radians(lon_graz)))