# Nagarhole Search and Rescue (SAR) Spatial Operations Framework

An advanced geospatial routing and terrain-masked grid framework designed to optimize tactical Search and Rescue (SAR) operations in the Nagarhole operational zone. This repository archives the complete spatial analysis workspace, vector grid indices, and deployment-ready dispatch map layouts.

---

## 📌 Project CHARLIE Overview

When executing SAR operations in dense or complex terrain, ground teams require systematic, easily identifiable geographic boundaries rather than ambiguous topographical landmarks. This project establishes a structured spatial deployment plan by:
1. Identifying operational thresholds based on slope, cliff barriers, and proximity rings from the Last Known Position (LKP).
2. Segmenting priority navigable transit corridors into discrete, indexed tactical sectors.
3. Overlaying a standardized 1-kilometer reference grid matrix matching universal coordinate systems for unified field communication.

---

## 🛠️ Tech Stack & GIS Architecture

*   **Platform:** QGIS Desktop
*   **Coordinate Reference System (CRS):** EPSG:32643 — WGS 84 / UTM zone 43N (Metric units for precise distance calculations)
*   **Data Formats:** OGC GeoPackage (.gpkg) vector layers, Classified Raster Mask matrices, and high-resolution layout prints.

---

## 🗂️ Repository Structure

```text
├── Nagarhole_SAR_Ops_v1.qgz       # Core QGIS project workspace containing styles, labels, and map layouts
├── Dispatch_map.png              # High-resolution, deployment-ready 1km gridded operational field printout
├── data/
│   ├── Search_Grid_1km.gpkg       # Standardized 1-kilometer reference matrix layer
│   ├── Tactical_Search_Sectors.gpkg # Vector tracks split into numbered tactical segments (e.g., Sector 1, Sector 2)
│   ├── Priority_Search_Corridors.gpkg # High-probability linear corridors classified by accessibility
│   └── Cliff_raster_mask.tif      # Terrain exclusion mask isolating hazardous slope thresholds
