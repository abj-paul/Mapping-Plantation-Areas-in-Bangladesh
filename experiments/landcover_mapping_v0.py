import rasterio
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the bands
with rasterio.open('../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B2.TIF') as src:
    blue = src.read(1)
with rasterio.open('../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B3.TIF') as src:
    green = src.read(1)
with rasterio.open('../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B4.TIF') as src:
    red = src.read(1)
with rasterio.open('../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B5.TIF') as src:
    nir = src.read(1)
with rasterio.open('../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B6.TIF') as src:
    swir1 = src.read(1)
with rasterio.open('../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B7.TIF') as src:
    swir2 = src.read(1)

# Stack the bands
stacked_bands = np.stack([blue, green, red, nir, swir1, swir2], axis=-1)

# Reshape the stacked bands to 2D array (pixels as rows and bands as columns)
X = stacked_bands.reshape((-1, stacked_bands.shape[-1]))

# Perform k-means clustering
n_clusters = 5  # Number of clusters (you can adjust this as needed)
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
labels = kmeans.fit_predict(X)

# Reshape the labels back to the original image dimensions
labels_image = labels.reshape(blue.shape)

# Plot the clustered image
plt.figure(figsize=(10, 10))
plt.imshow(labels_image, cmap='viridis')  # You can choose any colormap you prefer
plt.colorbar(label='Cluster')
plt.title('Unsupervised Classification (k-means)')
plt.show()
