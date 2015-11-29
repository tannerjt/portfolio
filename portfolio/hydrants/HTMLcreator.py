#Name: HTMLcreator.py
#Purpose: Creates an HTML page that will
#         outline the shortest path for
#         a fire incident.  The page will
#         also display information about the
#         closest fire hydrant and images.
#Author: Joshua Tanner
#Date: 11/10/2012
import os, arcpy

class HTML:
    '''Class for creating html'''
    def __init__(self, html_in):
        self.html = open(html_in, 'r')
        self.outF = self.html.read()
        self.html.close()

    def addShortestPath(self, coords):
        '''Adds shortest path to output html'''
        self.outF = self.outF.replace('"PATH_COORDS"', '"' + str(coords) +  '"')
        
    def addHydrantImage(self, hydrant, baseURL):
        '''Adds hydrant image to HTML'''
        sc = arcpy.SearchCursor(hydrant)
        for row in sc:
            self.hydrantImage = row.photos.split(";")[0]
            break
        self.outF = self.outF.replace("HYDRANT_IMAGE", baseURL + \
                                      '/images/' + self.hydrantImage)

    def writeHTML(self, outHTML):
        '''Writes final HTML file and opens it'''
        self.outFile = open(outHTML, 'w')
        self.outFile.write(self.outF)
        self.outFile.close()
        os.startfile(outHTML)
    
    