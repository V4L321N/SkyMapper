# Import necessary libraries
from skyfield.api import Topos, load, EarthSatellite, utc
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Step 1: Load the TLE data manually (using EarthSatellite)
def load_tle(tle_lines):
    ts = load.timescale()
    satellite = EarthSatellite(tle_lines[1], tle_lines[2], tle_lines[0], ts)
    return satellite, ts

# Step 2: Define the observer's location
def observer_location(latitude, longitude):
    return Topos(latitude_degrees=latitude, longitude_degrees=longitude)

# Step 3: Calculate satellite position for a given time
def satellite_position(satellite, observer, ts, duration=60):
    # Generate times over the specified duration (in minutes)
    current_time = datetime.utcnow().replace(tzinfo=utc)  # Set timezone to UTC
    times = [ts.utc(current_time + timedelta(minutes=i)) for i in range(duration)]
    
    # Calculate the satellite's position relative to the observer for each time
    altitudes = []
    azimuths = []
    for time in times:
        observer_pos = satellite - observer
        alt, az, _ = observer_pos.at(time).altaz()  # Altitude and Azimuth for each time step
        altitudes.append(alt.degrees)
        azimuths.append(az.degrees)

    return times, altitudes, azimuths

# Step 4: Plotting the satellite's path on a polar plot
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
    ax.set_yticks([0,15,30,45,60,75,90], ['0°','15°','30°','45°','60°','75°','90°'], fontsize=7)
    #ax.set_title('Satellite Sky Path (Azimuth vs Altitude)', va='bottom')
    #ax.set_xlabel('Azimuth (Degrees)')
    #ax.set_ylabel('Altitude (Degrees)')

    # Show the plot
    plt.show()

# Example TLE data and observer location
# tle_lines = [
#     "STE 241 18",
#     "1 22824U 93061B   24241.58041946 -.00000005  00000-0  16585-4 0  9992",
#     "2 22824  98.8724 288.9714 0006249 358.4185 132.6559 14.27431834610951"
# ]

tle_lines = [
    "LA1 296 12",
    "1  8820U 76039A   24296.50940701  .00000002  00000-0  00000+0 0  9993",
    "2  8820 109.8559 332.9143 0043992  71.1657 282.8431  6.38664967875054"
]





observer_latitude = 47.067155  # Example: Graz
observer_longitude = 15.493364

# Load satellite and observer details
satellite, ts = load_tle(tle_lines)
observer = observer_location(observer_latitude, observer_longitude)

# Calculate satellite position for a 60-minute window
times, altitudes, azimuths = satellite_position(satellite, observer, ts)

# Plot the satellite's sky path
plot_sky_path(azimuths, altitudes)
