#!/usr/bin/python

# Program to use Google Maps API to extract 
# Location Coordinates from a list of
# Location Addresses.
# @author - Sarthak Sharma <sarthakgatech@gmail.com>
# Date of last modification - 04/02/2018

# [TODO]: 
#   Implement the getLocationAttributes method
#   Shorten extractCoords method
#   Implement better data structures
#   Implement a method for local caching

import urllib2
import json
import urllib
import sys

class LocationExtractor:
    def __init__(self, apiKey):
        self.addresses = []
        self.geoCodeUrl = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false"
        self.apiKey = "&key="+apiKey
        self.locations = []
        # self.locationAttributes = []
        print "PollingLocationExtractor created!"

    def readAddressesFromFile(self,filename):
        # The file should have lines like: 
        # 98056,B21, Ground Floor, Gandhi Park Lane,Hauz Rani
        # 134098,C-174,Madhuban enclave,Preet Vihar,
        # 307045,House no 35 block i sector 41 noida,
        with open(filename, 'r') as fIn:
            for line in fIn:
                address = str(line).replace('"','').replace('\n','')
                self.addresses.append(address)

    def extractCoords(self):
        for address in self.addresses:
            urlCompatibleAddress = self._getUrlCompatibleAddress(address)
            requestUrl = str(self.geoCodeUrl + self.apiKey) % urlCompatibleAddress
            request = self._makeRequest(requestUrl)
            jsonResponse = self._readJsonResponse(request)
            (latCoords,longCoords, formattedAddress, classifiers) = self._parseJsonResponse(jsonResponse)
            self.locations.append((address, latCoords, longCoords, formattedAddress, classifiers))
            print address
            #self.responses.append(str(jsonResponse))

    def printOutLocations(self):
        for location in self.locations:
            print location
            print "\n"

    def writeLocationsToFile(self, filename):
        with open(filename,'w') as fOut:
            for location in self.locations:
                outputLine = "\t".join(str(attr) for attr in location)
                fOut.write(outputLine)
                fOut.write("\n")

    def writeResponsesToFile(self,filename):
        with open(filename, 'w') as fOut:
            for response in self.responses:
                fOut.write(response)
                fOut.write("\n\n")

    def readResponsesFromFile(self, filename):
        with open(filename, 'r') as fIn:
            lines = fIn.readlines()
        for line in lines:
            if (self.isResponse(line)):
                response = line.replace("\n","")
                print dict(response)
            #(latCoords, longCoords) = self._parseDictResponse(dict(response))
            #print (latCoords, longCoords)
            #self.responses.append(

    def isResponse(self,line):
        if len(line) < 10:
            return False
        else:
            return True

    def _getUrlCompatibleAddress(self, address):
        urlCompatibleAddress = urllib2.quote(address)
        return urlCompatibleAddress

    def _makeRequest(self, url):
        request = urllib2.urlopen(url)
        return request

    def _readJsonResponse(self, request):
        jsonResponse = json.loads(request.read())
        return jsonResponse

    def _parseJsonResponse(self, jsonResponse):
        try:
            latCoords = jsonResponse[u'results'][0][u'geometry'][u'location'][u'lat']
            longCoords = jsonResponse[u'results'][0][u'geometry'][u'location'][u'lng']
            formattedAddress = jsonResponse[u'results'][0][u'formatted_address']
            classifiers = jsonResponse[u'results'][0][u'types']
        except IndexError:
            print "IndexError found!"
            print jsonResponse
        return (latCoords, longCoords, formattedAddress, classifiers)

    def _parseDictResponse(self, dictResponse):
        latCoords = dictResponse[u'results'][0][u'geometry'][u'location'][u'lat']
        longCoords = dictResponse[u'results'][0][u'geometry'][u'location'][u'lng']
        return (latCoords, longCoords)

    #def getLocationAttributes(self,*args):
    # [TODO]:Implement this function which will take in
    # the attributes of a location as arguments
    # These attributes will be used in to extract more details 
    # other than latitudes and longitudes
    #    self.locationAttributes.extend(args)

def main():
    if len(sys.argv) < 2:
        print "Usage: python " + sys.argv[0] + " <AddressesFile>"
        quit()
    filename = str(sys.argv[1])
    locationExtractor = LocationExtractor("YOUR_API_KEY")
    locationExtractor.readAddressesFromFile(filename)
    locationExtractor.extractCoords()
    locationExtractor.writeLocationsToFile("FultonPollingLocationAttrs.tsv")
    # locationExtractor.readResponsesFromFile("test.txt")
    # locationExtractor.getLocationAttributes("bounds")
    # locationExtractor.printOutLocations()
    # locationExtractor.writeResponsesToFile("responses.txt")

if __name__ == '__main__':
	main()
