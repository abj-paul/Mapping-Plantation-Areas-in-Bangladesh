import rasterio
import numpy as np

def calculate_ndvi(red_band_path, nir_band_path):
    """
    Calculate Normalized Difference Vegetation Index (NDVI).
    :param red_band_path: Path to the red band image (TIF)
    :param nir_band_path: Path to the near-infrared band image (TIF)
    :return: NDVI array
    """
    with rasterio.open(red_band_path) as red_src:
        red_band = red_src.read(1).astype(np.float32)

    with rasterio.open(nir_band_path) as nir_src:
        nir_band = nir_src.read(1).astype(np.float32)

    # Handle possible division by zero by setting a value where both bands are zero
    np.seterr(divide='ignore', invalid='ignore')
    
    # Calculate NDVI
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    
    # Reset the error settings to their original values
    np.seterr(divide='warn', invalid='warn')

    return ndvi

# Paths to the red and near-infrared bands
red_band_path = "../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B4.TIF"
nir_band_path = "../data/LC09_L2SP_137043_20240402_20240403_02_T1_SR_B5.TIF"

# Calculate NDVI
ndvi = calculate_ndvi(red_band_path, nir_band_path)

# Now you can use the 'ndvi' array for further analysis or visualization.
