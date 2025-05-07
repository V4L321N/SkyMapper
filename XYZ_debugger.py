import numpy as np

def geodetic_to_ecef(lat, lon, alt):
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = 2 * f - f**2
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    N = a / np.sqrt(1 - e2 * np.sin(lat_rad)**2)
    X = (N + alt) * np.cos(lat_rad) * np.cos(lon_rad)
    Y = (N + alt) * np.cos(lat_rad) * np.sin(lon_rad)
    Z = (N * (1 - e2) + alt) * np.sin(lat_rad)
    return X, Y, Z

def az_el_to_local_tangential(az, el, distance):
    az_rad = np.radians(az)
    el_rad = np.radians(el)
    x_prime = distance * np.cos(el_rad) * np.sin(az_rad)
    y_prime = distance * np.cos(el_rad) * np.cos(az_rad)
    z_prime = distance * np.sin(el_rad)
    return x_prime, y_prime, z_prime

def local_tangential_to_ecef(lat, lon, x_prime, y_prime, z_prime):
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    rotation_matrix = np.array([
        [-np.sin(lon_rad), np.cos(lon_rad), 0],
        [-np.sin(lat_rad) * np.cos(lon_rad), -np.sin(lat_rad) * np.sin(lon_rad), np.cos(lat_rad)],
        [np.cos(lat_rad) * np.cos(lon_rad), np.cos(lat_rad) * np.sin(lon_rad), np.sin(lat_rad)]
    ])
    ecef_coords = np.dot(rotation_matrix, np.array([x_prime, y_prime, z_prime]))
    return ecef_coords

def az_el_to_ecef(lat, lon, alt, az, el, distance):
    X0, Y0, Z0 = geodetic_to_ecef(lat, lon, alt)
    x_prime, y_prime, z_prime = az_el_to_local_tangential(az, el, distance)
    ecef_coords = local_tangential_to_ecef(lat, lon, x_prime, y_prime, z_prime)
    return X0 + ecef_coords[0], Y0 + ecef_coords[1], Z0 + ecef_coords[2]

lat_graz = 47.0671
lon_graz = 15.4933
alt_graz = 539.4

az_test = 318.9604
el_test = 5.3959
dist_test = 2842.4619

print(az_el_to_ecef(lat_graz, lon_graz, alt_graz, az_test, el_test, dist_test))