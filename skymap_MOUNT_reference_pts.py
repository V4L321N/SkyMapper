import matplotlib.pyplot as plt
import numpy as np

# Step 1: Define a list of the reference points where the azimuth and elevation are given in ten degree increments
# written into a single array of tuples

azimuths = np.arange(0, 360, 45)  # Azimuths in 45 degree increments
elevations = np.arange(15, 91, 15)  # Elevation angles in 15 degree increments
reference_points = [(az, el) for az in azimuths for el in elevations]
print(reference_points)


# plot reference points in a polar scatter plot
def plot_reference_points(reference_points):
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

plot_reference_points(reference_points)


# Generate an array of the same size as the reference points array with zero values to store the calculated offset values

offset_values = np.zeros_like(reference_points)
print(type(offset_values))
print(type(reference_points))



