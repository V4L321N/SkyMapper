import numpy as np
from datetime import datetime, timedelta, timezone
import os

def generate_reference_point_tracking_file(lat, lon, alt, az, el, start_time=None):
    """
    Generate a dummy tracking file with static Az/El, 5-minute intervals, and Az/El in filename.
    
    Args:
        lat, lon, alt (float): Observer's geodetic coordinates (deg, deg, m).
        az, el (float): Static azimuth/elevation (deg).
        start_time (datetime): Optional start time (default: current UTC).
    Returns:
        str: Generated filename (e.g., "RPT045030.txt" for Az=45°, El=30°).
    """
    # Default to current UTC if no start_time provided
    start_time = datetime.now(timezone.utc) - timedelta(hours=1)
    
    folder_path = "C:/Users/vstok/OneDrive/Desktop/SLR Thesis/pyCODE_AdaptiveOptics/SkyMapper/ref_pnt_data"

    # Header metadata (placeholders for satellite-specific fields)
    day_of_year = start_time.timetuple().tm_yday
    hour_min_sec = start_time.strftime("%H%M%S")
    year = start_time.year
    

    # Generate filename (e.g., "RPT4530.GRZ")
    filename = f"X{number}{day_of_year}{start_time.hour:02d}"
    file_path = os.path.join(folder_path, filename)
    
    # Generate header
    header = (
        f"X{number}{day_of_year:03d}{start_time.hour:02d} " # e.g., RPT11613 (RPT + DOY + hour)
        f"R_PNT     "                             # 10-char name
        f"RP_TEST "         # CPF-like placeholder
        f"1808 "                               # SAT number
        f"0000000 "                               # COSPAR placeholder
        f"{az:4.0f} " 
        f"{el:2.1f} "                   # Az/El at closest approach
        f"{year} "                             # Year
        f"{day_of_year:03d} "                   # Day-of-year
        f"{hour_min_sec} "                        # Start time (HHMMSS)
        f"300 "                               # Time interval (5 min = 300 sec)
        f"100 "                                 # Number of lines
        f"  0   0 "                               # Polar motion placeholders
        f"1     -1\n"                              # Visibility flags
    )
    
    # Generate data lines (100 entries, 5-minute intervals)
    data_lines = []
    current_time = start_time
    distance_km = 1000.0  # Fixed distance (1,000 km)
    
    for _ in range(100):
        time_str = current_time.strftime("%H%M%S")
        
        # Compute ECEF coordinates (using your function)
        X, Y, Z = az_el_to_ecef(lat, lon, alt, az, el, distance_km * 1000)
        
        # Format line
        line = (
                f"{time_str:<6} "
                f"{az:9.4f} " 
                f"{el:8.4f}   "
                f"{distance_km:10.4f}   "
                f"{X:12.4f}   "
                f"{Y:12.4f}   "
                f"{Z:12.4f}\n"
            )
        data_lines.append(line)
        current_time += timedelta(seconds=300)  # 5-minute step
    
    # Write to file
    with open(file_path, "w") as f:
        f.write(header)
        f.writelines(data_lines)
    
    return filename

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

if __name__ == "__main__":
    # Observer location (Graz, Austria)
    lat = 47.0671
    lon = 15.4933
    alt = 539.4  # Station altitude in meters

    # Generate files for all Az/El pairs
    az_values = np.arange(0, 360, 45)  # [0°, 45°, ..., 315°]
    el_values = np.arange(15, 105, 15)  # [15°, 30°, ..., 90°]

    number=10

    for az in az_values:
        for el in el_values:
            # Get the current time for each iteration
            start_time = datetime.now(timezone.utc)
            day_of_year = start_time.timetuple().tm_yday  # Calculate day_of_year inside the loop

            # Generate the filename
            filename = f"X{number:02d}{day_of_year:03d}{start_time.hour:02d}"  # Format with leading zeros
            generate_reference_point_tracking_file(lat, lon, alt, az, el, start_time=start_time)
            print(f"Generated: {filename} (Az={az}°, El={el}°)")

            number += 1  # Increment the counter

    # for az in az_values:
    #     for el in el_values:
    #         filename = generate_reference_point_tracking_file(lat, lon, alt, az, el)
    #         filename = f"X{number:02d}{day_of_year}{start_time.hour:02d}"  # Format with leading zeros
    #         print(f"Generated: {filename} (Az={az}°, El={el}°)")