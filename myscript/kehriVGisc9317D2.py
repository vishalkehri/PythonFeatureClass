#Name:      Vishal Kehri
#Course:    GISC9317 Advanced Programming in GIS
#Date:      14 March, 2019
#Purpose:   To create point feature class from XY table



#Import modules of arcpy, operating system and shutil
import arcpy, os, shutil

#Define base path and input and output path
basePath = 'C:\\temp'
inPath = os.path.join(basePath, 'd2RawData')
outPath = os.path.join(basePath, 'kehriVD2ProcData')


#Delete the output folder if exists
if os.path.exists:
    shutil.rmtree(outPath, ignore_errors = True)


#Set workspace
arcpy.env.workspace = outPath
#Overwrite output
arcpy.env.overwriteOutput = True
#Set spatial reference
sr = arcpy.SpatialReference(26917)
#Create output folder if does not exists
if not os.path.exists(outPath):
    os.makedirs(outPath)

#List text files
fileList = arcpy.ListFiles('*.txt')
x = 'EastingM'
y = 'NorthingM'

#Create event layer from xy and converting to shapefile
for filename in os.listdir(inPath):
    if filename.endswith('.txt'):
        fc = filename[:-4]
        arcpy.MakeXYEventLayer_management(inPath + '/' + filename, x, y, fc, sr)
        shp = os.path.join(outPath, fc)
        arcpy.CopyFeatures_management(fc, shp)

arcpy.env.workspace = outPath
arcpy.env.overwriteOutput = True

#Merge shapefiles
mergeFile = arcpy.ListFeatureClasses('*.shp')
mergePath = outPath + '\\npFarms.shp'
arcpy.Merge_management(mergeFile, mergePath)

#List the number od farms in a given extent

extent = x + '> 610000 and ' + y + '> 4760000 and ' + x + '< 660000 and ' + y + '< 4780000' 
cursor = arcpy.da.SearchCursor(mergePath, [x,y], extent)
count = 0
for row in cursor:
    count +=1
print 'The total number of farms in the given coordinates = ' + str(count)

del cursor