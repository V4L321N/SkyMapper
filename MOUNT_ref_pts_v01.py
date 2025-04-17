import numpy as np
import datetime as dt

def geodetic_to_ecef(lat, lon, alt):
    # WGS-84 ellipsoid constants
    a = 6378137.0  # semi-major axis
    f = 1 / 298.257223563  # flattening
    e2 = 2 * f - f**2  # square of eccentricity

    # Convert geodetic to ECEF
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

    local_coords = np.array([x_prime, y_prime, z_prime])
    ecef_coords = np.dot(rotation_matrix, local_coords)

    return ecef_coords

def az_el_to_ecef(lat, lon, alt, az, el, distance):
    # Observer's ECEF position
    a = 6378137.0
    e_sq = 6.69437999014e-3
    sin_lat = np.sin(np.radians(lat))
    cos_lat = np.cos(np.radians(lat))
    sin_lon = np.sin(np.radians(lon))
    cos_lon = np.cos(np.radians(lon))
    N = a / np.sqrt(1 - e_sq * sin_lat**2)
    X0 = (N + alt) * cos_lat * cos_lon
    Y0 = (N + alt) * cos_lat * sin_lon
    Z0 = (N * (1 - e_sq) + alt) * sin_lat

    # Az/El to ENU
    az_rad = np.radians(az)
    el_rad = np.radians(el)
    x_prime = distance * np.cos(el_rad) * np.sin(az_rad)  # East
    y_prime = distance * np.cos(el_rad) * np.cos(az_rad)  # North
    z_prime = distance * np.sin(el_rad)                   # Up

    # ENU-to-ECEF rotation (transposed basis vectors)
    e = [-sin_lon,          cos_lon,          0      ]
    n = [-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat]
    u = [ cos_lat * cos_lon,  cos_lat * sin_lon, sin_lat]
    rot = np.array([e, n, u]).T  # Stack as columns

    # Apply rotation and add observer's position
    dx, dy, dz = rot @ [x_prime, y_prime, z_prime]
    return X0 + dx, Y0 + dy, Z0 + dz


latitude = 47.0671  # Latitude of Graz, Austria
longitude = 15.4933 
altitude = 539.4  # Altitude in meters
azimuth = 0  # Azimuth in degrees of target
elevation = 0  # Elevation in degrees of target
distance = 0  # Distance in meters of target

X, Y, Z = az_el_to_ecef(latitude, longitude, altitude, azimuth, elevation, distance)
print(f"ECEF Coordinates of target at {distance} meters distance: X={X}, Y={Y}, Z={Z}")
