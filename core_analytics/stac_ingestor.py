import os
import requests
import pystac_client
import planetary_computer


class PlanetarySTACIngestor:

    def __init__(self):
        """Initializes the STAC API Client targeting Planetary Computer."""
        self.catalog = pystac_client.Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace,
        )
        print("🛰️  Multi-Sensor STAC Client initialized and signed securely.")

    def query_assets(self, collection, bbox, datetime_range, extra_query=None):
        """Queries the STAC catalog for specific collections (Sentinel-1 or Sentinel-2)."""
        print(f"🔍 Searching {collection} catalog for area: {bbox}...")
        
        search_params = {
            "collections": [collection],
            "bbox": bbox,
            "datetime": datetime_range
        }
        if extra_query:
            search_params["query"] = extra_query

        search = self.catalog.search(**search_params)
        items = search.item_collection()
        print(f"✅ Found {len(items)} matching scene(s) in {collection}.")
        return items

    def download_bands(self, item, bands, output_dir="data_payload"):
        """Downloads specific assets (bands or polarizations) for a given STAC item."""
        os.makedirs(output_dir, exist_ok=True)
        scene_id = item.id
        print(f"📥 Extracting assets for scene: {scene_id}")

        for band in bands:
            if band in item.assets:
                asset_url = item.assets[band].href
                # Determine suffix (.tif for data bands, sometimes raw paths differ)
                output_filename = os.path.join(output_dir, f"{scene_id}_{band}.tif")
                
                print(f" └── Downloading {band}...", end="", flush=True)
                response = requests.get(asset_url, stream=True)
                if response.status_code == 200:
                    with open(output_filename, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(" Done! ✨")
                else:
                    print(f" Failed (HTTP {response.status_code})")
            else:
                print(f" ⚠️  Asset {band} not available in this scene catalog.")


# Verification Execution Block
if __name__ == "__main__":
    NAGARHOLE_BBOX = [76.10, 11.90, 76.40, 12.15]
    APRIL_2026 = "2026-04-01/2026-04-30"

    ingestor = PlanetarySTACIngestor()

    # Query and fetch Sentinel-1 SAR GRD Data (VV and VH polarizations)
    # SAR instruments aren't limited by clouds, so we drop cloud queries
    sar_scenes = ingestor.query_assets(
        collection="sentinel-1-grd", 
        bbox=NAGARHOLE_BBOX, 
        datetime_range=APRIL_2026,
        extra_query={"sar:instrument_mode": {"eq": "IW"}} # Interferometric Wide Swath
    )

    if len(sar_scenes) > 0:
        # Download the main VV backscatter band from the first scene
        target_sar = sar_scenes[0]
        ingestor.download_bands(item=target_sar, bands=["vv"])