#import modules
import arcpy
import os

#define variables
in_folder = arcpy.GetParameterAsText(0) #folder that contains all files to be prepped directly
out_folder = arcpy.GetParameterAsText(1) #folder to be created to hold the prepped data

clip_by = arcpy.GetParameterAsText(2) #the feature layer that the data will be clipped by
clip_where_clause = arcpy.GetParameterAsText(3) #sql expression linked to the clip_by input

project_to = arcpy.GetParameter(4) #the srs to be projected to
resampling_method = arcpy.GetParameterAsText(5)#the method that rasters will be resampled by (must be "NEAREST", "BILINEAR", "CUBIC" or "MAJORITY")
resolution = arcpy.GetParameter(6) #the desired cell size of the rasters
snap_to = arcpy.GetParameterAsText(7) # the point that all the will be snapped to to make sure all rasters align

#create output folder
#use try/except to deal with error
try:
    os.mkdir(out_folder)
    print('folder created')
except FileExistsError:
    print('folder already exists')

#Select features to clip by
#create a feature layer to select off of
select_layer = arcpy.management.MakeFeatureLayer(in_features=clip_by, out_layer=f'{clip_by}_layer')
#select the features from the feature layer
select_layer = arcpy.management.SelectLayerByAttribute(
    in_layer_or_view=select_layer, 
    selection_type='NEW_SELECTION', 
    where_clause= clip_where_clause)

#set environment to in_folder and set overwrite
arcpy.env.workspace = in_folder
arcpy.env.overwriteOutput = True

arcpy.env.snapRaster = snap_to #set the environment to snap all rasters to this point

#sort feature classes from rasters (requires evironment to be set)
vector_data = arcpy.ListFeatureClasses()
raster_data = arcpy.ListRasters()

#work with the feature classes
for file in vector_data: #for all the feature classes
    arcpy.AddMessage("Working on feature class {}".format(file)) #progress message as the tool runs
    #project all of the feature classes
    projected = os.path.join(out_folder, "temp_{}".format(file)) #create a temporary file to hold the projected feature class
    arcpy.management.Project(in_dataset = file, out_dataset = projected, out_coor_system = project_to) #project the feature class and store it in the temporary file
    #clip all of the feature classes
    filename = os.path.join(out_folder, file) #create output
    arcpy.analysis.Clip(in_features = projected, clip_features = select_layer, out_feature_class = filename) #clip the feature classes
    arcpy.Delete_management(projected) #delete the temporary file

#work with the raster files
for file in raster_data: #for all the raster files
    arcpy.AddMessage("Working on raster {}".format(file)) #progress message as the tool runs
    #project all of the raster files
    projected_rast = os.path.join(out_folder, "temprast_{}".format(file)) #create a temporary file to hold the projected raster
    arcpy.management.ProjectRaster(
        in_raster = file,
        out_raster = projected_rast,
        out_coor_system = project_to,
        resampling_type = resampling_method,
        cell_size = resolution)#project the raster and store it as the temporary file
    #clip all of the raster files
    filename = os.path.join(out_folder, file) #create output
    rast_clip = arcpy.sa.ExtractByMask(in_raster = projected_rast, in_mask_data = select_layer) #clip the rasters
    rast_clip.save(filename)#save the raster
    arcpy.Delete_management(projected_rast) #delete the temprorary file

#unset the environment to not cause problems outside of the tool
arcpy.env.workspace = None

#signal that the tool is finished running
arcpy.AddMessage('Done')

