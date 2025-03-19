# Import necessary libraries
from skyfield.api import Topos, load, EarthSatellite, utc
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time  # For epoch time conversion

# Step 1: Load the TLE data manually (using EarthSatellite)
def load_tle(tle_lines):
    ts = load.timescale()
    satellite = EarthSatellite(tle_lines[1], tle_lines[2], tle_lines[0], ts)
    return satellite, ts

# Step 2: Define the observer's location
def observer_location(latitude, longitude):
    return Topos(latitude_degrees=latitude, longitude_degrees=longitude)

# Step 3: Convert datetime to epoch time
def datetime_to_epoch(dt):
    return int(time.mktime(dt.timetuple()))

# Step 4: Calculate satellite position for a given time in epoch format
def satellite_position(satellite, observer, ts, specific_time, duration=60):
    # Generate times over the specified duration (in minutes)
    times = [specific_time + timedelta(minutes=i) for i in range(duration)]
    
    # Convert the times to epoch
    epoch_times = [datetime_to_epoch(t) for t in times]
    
    # Calculate the satellite's position relative to the observer for each time
    altitudes = []
    azimuths = []
    for t in times:
        observer_pos = satellite - observer
        alt, az, _ = observer_pos.at(ts.utc(t)).altaz()  # Altitude and Azimuth for each time step
        altitudes.append(alt.degrees)
        azimuths.append(az.degrees)

    return epoch_times, altitudes, azimuths

# Step 5: Plotting the satellite's path on a polar plot
def plot_sky_path(azimuths, altitudes):
    # Convert azimuths to radians for polar plot
    azimuths_rad = np.radians(azimuths)

    # Create polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    
    # In polar coordinates, the azimuth (theta) is the angular component
    # and the altitude (r) is the radial component
    ax.plot(azimuths_rad, altitudes)

    # Set labels and formatting for the plot
    ax.set_theta_direction(-1)  # To have azimuths go clockwise
    ax.set_theta_offset(np.pi / 2)  # Set North (0 degrees) at the top
    ax.set_rlim(90, 0)  # Set the altitude range: 90 (zenith) at the center, 0 at the edge

    ax.set_title('Satellite Sky Path (Azimuth vs Altitude)', va='bottom')
    ax.set_xlabel('Azimuth (Degrees)')
    ax.set_ylabel('Altitude (Degrees)')

    # Show the plot
    plt.show()

# Example TLE data and observer location
tle_lines = [
    "ISS (ZARYA)",
    "1 25544U 98067A   20029.54791667  .00016717  00000-0  10270-3 0  9002",
    "2 25544  51.6433 356.2590 0007410  32.1057 328.3274 15.50165878212082"
]
observer_latitude = 37.7749  # Example: San Francisco
observer_longitude = -122.4194

# Load satellite and observer details
satellite, ts = load_tle(tle_lines)
observer = observer_location(observer_latitude, observer_longitude)

# Define a specific UTC time in the past (this is the datetime to be converted to epoch time)
specific_time = datetime(2022, 10, 1, 15, 0, 0, tzinfo=utc)  # October 1, 2022 at 15:00:00 UTC

# Calculate satellite position for a 60-minute window starting from the specific past time
epoch_times, altitudes, azimuths = satellite_position(satellite, observer, ts, specific_time)

# Print out the epoch times along with altitudes and azimuths
for epoch_time, altitude, azimuth in zip(epoch_times, altitudes, azimuths):
    print(f"Epoch time: {epoch_time}, Altitude: {altitude:.2f}, Azimuth: {azimuth:.2f}")

# Plot the satellite's sky path
plot_sky_path(azimuths, altitudes)
