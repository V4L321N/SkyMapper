import numpy as np
from datetime import datetime, timedelta, timezone
import os

def generate_reference_point_tracking_file(az, el, lat, lon, start_time=None):
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
        
        # Compute ECEF coordinates
        X, Y, Z = az_el_ra_to_xyz(az, el, distance_km, np.radians(lat), np.radians(lon))
        
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
            generate_reference_point_tracking_file(az, el, lat, lon, start_time=start_time)
            print(f"Generated: {filename} (Az={az}°, El={el}°)")

            number += 1  # Increment the counter
