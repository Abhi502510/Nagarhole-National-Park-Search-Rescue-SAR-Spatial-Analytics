import os
import numpy as np
import rioxarray
import xarray as xr


class NagarholeSpatialProcessor:

    def __init__(self, data_dir="data_payload"):
        self.data_dir = data_dir
        print("🌲 Spatial Processor Engine initialized.")

    def compute_ndvi(self, scene_id, output_name="Nagarhole_NDVI_April2026.tif"):
        """Loads Red (B04) and NIR (B08) rasters to safely calculate NDVI."""
        red_path = os.path.join(self.data_dir, f"{scene_id}_B04.tif")
        nir_path = os.path.join(self.data_dir, f"{scene_id}_B08.tif")

        print(f"📖 Loading spectral bands for scene {scene_id}...")
        red = rioxarray.open_rasterio(red_path, masked=True).squeeze()
        nir = rioxarray.open_rasterio(nir_path, masked=True).squeeze()

        print("🧮 Calculating NDVI matrix layer...")
        denominator = nir + red
        ndvi = xr.where(denominator == 0, 0, (nir - red) / denominator)

        output_path = os.path.join(self.data_dir, output_name)
        print(f"💾 Writing calculated NDVI raster to: {output_path}")
        ndvi.name = "NDVI"
        ndvi.rio.to_raster(output_path)
        print("✨ NDVI processing complete.")
        return output_path

    def compute_slope(self, dem_name="Nagarhole_DEM.tif", output_name="Nagarhole_Slope.tif"):
        """Calculates terrain slope in degrees using 2D spatial gradients."""
        dem_path = os.path.join(self.data_dir, dem_name)
        print(f"📖 Loading Elevation Layer: {dem_path}")
        
        # Open DEM raster
        dem = rioxarray.open_rasterio(dem_path).squeeze()
        
        # Extract pixel spacing (resolution) natively from geospatial metadata
        # Sentinel-2 / Copernicus assets are typically in meters or degrees depending on CRS
        dx, dy = dem.rio.resolution()
        dx = abs(dx)
        dy = abs(dy)

        print("🧮 Computing directional spatial gradients...")
        # Calculate gradients along axes using standard numpy central differences
        gradient_y, gradient_x = np.gradient(dem.values, dy, dx)

        # Calculate slope rise/run rise magnitude
        rise_run = np.sqrt(gradient_x**2 + gradient_y**2)
        
        # Convert radian values to degree slopes natively
        slope_degrees = np.degrees(np.arctan(rise_run))

        # Build output xarray structure preserving spatial attributes and projections
        slope_xr = xr.DataArray(
            slope_degrees,
            coords=dem.coords,
            dims=dem.dims,
            attrs=dem.attrs
        )
        
        output_path = os.path.join(self.data_dir, output_name)
        print(f"💾 Writing calculated Slope raster to: {output_path}")
        slope_xr.rio.to_raster(output_path)
        print("✨ Slope extraction complete.")
        return output_path


# Verification Execution Block
if __name__ == "__main__":
    processor = NagarholeSpatialProcessor()
    
    # Run slope calculation engine
    processor.compute_slope(dem_name="Nagarhole_DEM.tif", output_name="Nagarhole_Slope.tif")