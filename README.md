# Basic Data Preparation: Automated Clip and Project (Version 2) 

## Purpose
**Basic Data Preparation tool automates the basic data preparation of clipping and projecting large batches of geospatial data.** This script tool clips batches of vector and raster data to the boundaries of a focus area, which can be selected from a feature class within the tool. The tool also projects the datasets into a common projected coordinate system.

Before beginning to work in GIS, it is best practice to ensure all the data being used for that project uses the same spatial reference to prevent errors. Additionally, reducing large datasets to the boundaries of a given focus area reduces processing time. When there are many datasets to prepare, projecting and clipping the data becomes both repetitive and time-consuming. By automating this step, more time can be spent vetting the data for errors and working on the actual geoprocessing.

Anyone working with large batches of geospatial data will benefit from a streamlined data preparation process. This tool can be used for any geoprocessing project that uses multiple datasets.



## Data Inputs
### Input Folder: Datasets to be Prepared

This is the group of datasets that will be processed.

**Selection:** Through the file explorer menu in the tool.

**Data Type:** A folder containing any number and combination of point, polyline, or polygon feature classes and/or raster data OR a geodatabase containing point, polyline, or polygon feature classes

**Data Format:** A folder containing .shp, .tif, or other raster formats supported by arcpy OR a .gdb

**Field Name or Attribute Requirements:** None

**Note:** A geodatabase or secondary file within the input file will not be processed. Process geodatabases using the tool directly.


### Clip By: Boundaries to Clip To

This is the boundary that the datasets will be clipped to.

**Selection:** Through the file explorer menu in the tool or by selecting an active layer. A dialouge box can optionally be used to create a sql expression that selects features from a feature class.

**Data Type:** A polygon feature class

**Data Format:** A .shp or a .gdb

**Field Name or Attribute Requirements:** Optional. Any fields of the feature class can be used to select features within the feature class

**Note:** Selecting features to clip by using the sql expression dialouge box is optional. An example sql expression is provided:

<img width="596" height="146" alt="SQL_Example_Image" src="https://github.com/user-attachments/assets/1b465d17-3e32-4e7e-b586-1825141d339f" />




### Project To: Projected Coordinate System

This is the coordinate system that the datasets will be projected to.

**Selection:** Through the XY coordinate system menu in the tool, by selecting current map or an active layer, or by entering a WKID or spatial reference name

**Data Type:** A projected coordinate system

**Data Format:** A .prj

**Field Name or Attribute Requirements:** None



## Outputs
### Output Folder: Processed Datasets

The tool creates a folder containing a processed file that corresponds to each of the datasets within the input folder.

**Folder Selection/Creation:** A folder can be selected through the file explorer menu in the tool for the output, or a new folder can be created by naming it in the tool and selecting the folder destination in the file explorer menu.

**Files Created:** For each feature class or raster in the input folder, there will be a clipped and projected feature class or raster in the output folder. Note that the output files will have the same name as they did in the input folder.

**Tool Confirmation:** A completion message will display after the tool has run. Check the folder location for the processed datasets to confirm tool has run. No layers will be output to a map by the tool.

**Note:** The output folder will be overwritten every time the tool is run. Do not select a folder containing data that is separate from what is not being currently processed as the destination, because the tool will overwrite it.


## Other Details

**Tool Import:** Connect the folder containing BasicDataPrep_Script.py and BasicDataPrep.atbx to an ArcGIS Pro project. Do not seperate the script and toolbox files.

**Required Python Libraries:** arcpy and os

**Required ArcGIS Extensions:** ArcGIS Spatial Analyst

**Troubleshooting:**

* A geodatabase or secondary file within the input file will not be processed. Process geodatabases using the tool directly.
* Selecting features to clip by using the sql expression dialouge box is optional.
* The clip by feature class should not be in the input folder, which will be prepped.
* The output folder will be overwritten everytime the tool is run. Do not select a folder containing data that is seperate from what is not being currently processed as the destination, because the tool will overwrite it.
* Datasets, especially rasters won't correctly overwrite if their layers are left in the map. If you leave the layers active and rerun the tool, the tool will run but the raster data will be lost. Delete the layers and the output files and rerun to correct this. If the output file already exists but doesn't have data open (like in a layer), the tool can be rerun and have the data overwrite

## Updates

Additional inputs have been added to allow increased control over raster processing and orthogonality.

### Resampling Technique: Raster Processing

This is the resampling technique used to process raster data when re-projecting, or snapping.

**Selection:** The drop down menu allows selection of the supported resampling techniques.

**Note:** Selecting a resampling technique is optional but recommended whenever processing raster data. If no resampling technique is specified, the NEAREST neighbor technique will be used by default.


### Cell Size: Specifying Resolution

This is the resolution that raster datasets will have when being output.

**Selection:** Type the desired lenght of one side of the output cell without units.

**Note:** Specifying a cell size is optional. If not used, the original resolution of the dataset will be maintained. The unit of the cell size is specified by the projection.


### Snap To: Aligning Multiple Rasters

This shifts the grids raster datasets so that the lower left corner of the dataset's extent aligns with a cell corner of a specified dataset. This is used to align the cells of rasters and ensure orthagonality.

**Selection:** A raster dataset can be selected through the file explorer menu in the tool.

**Note:** Selecting a raster to snap to is optional.
