import matplotlib.pyplot as plt
import numpy as np

# Define a list of the reference points where the well spaced azimuth and elevation are written into a single array of tuples

azimuths = np.arange(0, 360, 45)  # Azimuths in 45 degree increments
elevations = np.arange(15, 91, 15)  # Elevation angles in 15 degree increments
reference_points = [(az, el) for az in azimuths for el in elevations]
offset_values = [(0, 0) for _ in reference_points]  # Initialize offset values

# plot reference points in a polar scatter plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10,10))
ax.grid(True)
for az, el in reference_points:
    az_rad = np.radians(az)
    ax.scatter(az_rad, el, color='b', s=28)
ax.set_rlabel_position(0)  # Move radial labels to 0 degrees
ax.set_theta_direction(-1)  # To have azimuths go clockwise
ax.set_theta_offset(2*3*np.pi/4)  
ax.set_rlim(90, 0)  # Set radial limits from 0 to 90 degrees
ax.set_yticks([15,30,45,60,75,90], [' 15°',' 30°',' 45°',' 60°',' 75°',' 90°'], fontsize=11)
ax.set_xticks(np.radians(np.arange(0, 360, 45)), ['0°/ N','45°','90°/ E    ','135°','180°/ S','225°','       270°/ W','315°'], fontsize=12)
plt.show()


# transform Az/El coordinated to x,y,z coordinates in the earth centered, earth fixed coordinate system
'''def az_el_to_xyz(az, el):
    # Convert azimuth and elevation to radians
    az_rad = np.radians(az)
    el_rad = np.radians(el)

    # Calculate x, y, z coordinates
    x = np.cos(el_rad) * np.sin(az_rad)
    y = np.cos(el_rad) * np.cos(az_rad)
    z = np.sin(el_rad)

    return x, y, z

for az, el in reference_points:
    x, y, z = az_el_to_xyz(az, el)
    print(f"Azimuth: {az}°, Elevation: {el}° -> X: {x:.3f}, Y: {y:.3f}, Z: {z:.3f}")'''