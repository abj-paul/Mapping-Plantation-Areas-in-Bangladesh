import rasterio
import numpy as np
import matplotlib.pyplot as plt

def visualize_ndvi(ndvi_path, output_image_path):
    """
    Visualize NDVI values using a green color map and save the image.
    :param ndvi_path: Path to the NDVI raster file (TIF)
    :param output_image_path: Path to save the output visualization image
    """
    # Open the NDVI raster file
    with rasterio.open(ndvi_path) as src:
        ndvi = src.read(1, masked=True)  # Read NDVI values

    # Set up the figure
    plt.figure(figsize=(10, 10))

    # Define the colormap (green)
    cmap = plt.cm.gist_earth

    # Plot NDVI values
    plt.imshow(ndvi, cmap=cmap, vmin=-1, vmax=1)

    # Add color bar
    cbar = plt.colorbar(label='NDVI')
    cbar.set_ticks([-1, -0.5, 0, 0.5, 1])

    # Save the visualization image
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def calculate_ndvi(red_band_path, nir_band_path, output_ndvi_path):
    """
    Calculate Normalized Difference Vegetation Index (NDVI) and save to a new raster file.
    :param red_band_path: Path to the red band image (TIF)
    :param nir_band_path: Path to the near-infrared band image (TIF)
    :param output_ndvi_path: Path to save the NDVI raster file
    :return: Percentage of total 
area with vegetation
    """
    with rasterio.open(red_band_path) as red_src:
        red_band = red_src.read(1).astype(np.float32)
        profile = red_src.profile  # Get metadata from the red band

    with rasterio.open(nir_band_path) as nir_src:
        nir_band = nir_src.read(1).astype(np.float32)

    # Handle possible division by zero by setting a value where both bands are zero
    np.seterr(divide='ignore', invalid='ignore')
    
    # Calculate NDVI
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    
    # Reset the error settings to their original values
    np.seterr(divide='warn', invalid='warn')

    # Save NDVI to a new raster file
    with rasterio.open(output_ndvi_path, 'w', **profile) as dst:
        dst.write(ndvi*255, 1)

    # Calculate the percentage of total area with vegetation
    vegetation_pixels = np.count_nonzero(ndvi > 0.37036)  # Count pixels with NDVI > 0
    total_pixels = ndvi.size
    percentage_vegetation = (vegetation_pixels / total_pixels) * 100

    return percentage_vegetation

# Paths to the red and near-infrared bands
red_band_path = "../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B4.TIF"
nir_band_path = "../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B5.TIF"
output_ndvi_path = "output/shanir_akhra_ndvi_v0.TIF"

# Calculate NDVI and save to a new raster file
percentage_vegetation = calculate_ndvi(red_band_path, nir_band_path, output_ndvi_path)
print(f"Percentage of total area with vegetation: {percentage_vegetation:.2f}%")



# Path to save the output visualization image
output_image_path = "output/shanir_akhra_ndvi_v0.png"

# Visualize NDVI values and save the image
visualize_ndvi(output_ndvi_path, output_image_path)
