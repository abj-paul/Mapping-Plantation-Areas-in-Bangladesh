import rasterio
import numpy as np

def calculate_ndvi(red_band_path, nir_band_path, output_ndvi_path):
    """
    Calculate Normalized Difference Vegetation Index (NDVI) and save to a new raster file.
    :param red_band_path: Path to the red band image (TIF)
    :param nir_band_path: Path to the near-infrared band image (TIF)
    :param output_ndvi_path: Path to save the NDVI raster file
    :return: Percentage of total area with vegetation
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
        dst.write(ndvi, 1)

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
