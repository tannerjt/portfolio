#Name: ResponseFeatures.py
#Purpose: Object that stores all related data for
#         fire hydrants, fire stations, and path
#         from station to an incident
#Author: Joshua Tanner
#Date: 11/10/2012
import arcpy,os

class Hydrant:
    '''Class for storing fire Hydrants'''
    def __init__(self, id, location, scratch_location):
        self.id = id
        self.location = location
        self.scratch = scratch_location
        self.selectHydrant()
        
    def selectHydrant(self):
        '''Selects and extracts current hydrant'''
        query = "OBJECTID = " + str(self.id) 
        self.feature = arcpy.Select_analysis(self.location, \
                                             self.scratch + "/hydrant",
                                             query)
        #Retrieve images of hydrant and store
        self.storeImages()
        
    def setDistance(self, distance):
        '''Stores the distance from the hydrant to an address'''
        self.distance = distance
        
    def storeImages(self):
        '''Stores any images associated with the hydrant'''
        sc = arcpy.SearchCursor(self.feature)
        hydrant = sc.next()
        self.images = []
        for image in hydrant.photos.split(", "):
            self.images.append(image)
            

class Path:
    '''Class for storing shortest path'''
    def __init__(self, origin, destination, cost_surface, output):
        self.origin = origin
        self.destination = destination
        self.cost_surface = cost_surface
        self.outputGDB = output
        self.findShortest()
        
    def findShortest(self):
        '''Finds the shortest path and stores it'''
        #First must compute cost distance
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.workspace = self.outputGDB
        arcpy.env.overwriteOutput = 1
        cost_dist = arcpy.sa.CostDistance(self.origin, self.cost_surface, \
                                          "", self.outputGDB + "/Backlink")
        cost_dist.save(self.outputGDB + "/cost_dist")
        #Find shortest path
        cost_path = arcpy.sa.CostPath(self.destination, cost_dist, \
                                      self.outputGDB + "/Backlink")
        cost_path.save(self.outputGDB + "/path_rast")
        #Convert raster path to polyline
        self.path = arcpy.RasterToPolyline_conversion(self.outputGDB + "/path_rast", \
                                                 self.outputGDB + "/ShortestPath")
                                      
    def pathTokml(self, output):
        '''Converts the raster path to a kml'''
        #Set Environment
        arcpy.env.workspace = output
        arcpy.env.overwriteOutput = True
        
        #Remove shapefile is it already exists
        if(os.path.exists(output + "ShortestPath.shp")):
           arcpy.Delete_management(output + "ShortestPath.shp")

        #Export to a shapefile
        shapefile = arcpy.FeatureClassToShapefile_conversion(self.path, \
                                                             output)
        #Create a layer file
        layer = arcpy.MakeFeatureLayer_management("ShortestPath.shp", \
                                                  "PathLayer")
        #Convert to KMZ
        self.kmz = arcpy.LayerToKML_conversion(layer, "path.kmz")
        return self.kmz
        
    
class Station:
    '''Class for storing the fire respose station'''
    def __init__(self, input, output, station):
        self.input = input
        self.output = output
        self.station = station
        self.select()
        
    def select(self):
        '''Selects and extracts the station'''
        query = "STATION_ID = " + str(self.station)
        self.feature = arcpy.Select_analysis(self.input, \
                                             self.output, \
                                             query)
        