# By Nathaniel Vaughn KELSO
#
# OGR based Python tools for querrying a data source (SHP, etc) and drawing 
# thematic cartographic representations.
#
# More specifically, stubs out MSS and MML files based on a dataset for:
#
#   * quick data exploration of what's in a dataset 
#   * refined cartographic presentations
#
# Inspired by a fall 2011 workshop held at Stamen about future of Carto and
# Cascadenik CSS style map rendering in Mapnik.

import os, sys
import math, stat
from optparse import OptionParser
try:
  from osgeo import gdal, ogr  
except ImportError:
  import gdal
  import ogr
#from import Thematic.ogrinfo import Ogrinfo
from Thematic.quantile import Quantile
from Thematic.classify import Classify


optparser = OptionParser(usage="""%prog [options]

OGR based Python tools for querrying a data source (SHP, etc) and drawing 
# thematic cartographic representations.""")

optparser.add_option('-s', '--data_file', dest='infilename',
                  help='Give me your huddled masses of geodata.')
optparser.add_option('-o', '--out_file', dest='outfilename', default='stylesheet',
                  help='Style name for resulting MSS and MML files.')                  
optparser.add_option('-i', '--indicator', dest='fieldname', 
                  help='Data is in which column.')
optparser.add_option('-l', '--legend-type', dest='legend_type', 
                  help='Valid types are: single-symbol, unique-value, continuous-color, and graduated-symbol.')
optparser.add_option('-c', '--classification-type', dest='class_type', 
                  help='Valid types are: quantiles, tk tk tk.')
optparser.add_option('-n', '--number-breaks', dest='num_breaks', default=5, type='int',
                  help='Number of data breaks. single-symbol=1 by default.')
optparser.add_option('-r', '--colors', dest='colors', default='YlGnBu',
                  help='From ColorBrewer.org')

if __name__ == "__main__":

    (options, args) = optparser.parse_args()

    if not options.infilename:
        print 'Requires input file'
        sys.exit(1)
    
    # Input geodata
    in_dir = os.path.dirname( os.path.abspath( options.infilename ) )
    in_file = os.path.basename( os.path.abspath( options.infilename ) )
    in_file_fullpath = os.path.abspath( options.infilename )
    
    # Output MSS and MML files
    out_dir = os.path.dirname( os.path.abspath( options.outfilename ) )
    out_mss = options.outfilename + '.mss'
    out_mml = options.outfilename + '.mml'
    
    # Store the options
    fieldname = options.fieldname
    legend_type = options.legend_type
    
    # If the output directory doesn't exist, make it so we don't error later on file open()
    if not os.path.exists(out_dir):
        print 'making dir...'
        os.makedirs(out_dir)
    
    mss_file = open(out_mss,"w")
    mml_file = open(out_mml,"w")
    
    # Set the working directory
    os.chdir(in_dir)
    #os.chdir(r'C:\Data\Conferences\UGIC2009\data')
    
    # Get the shapefile driver
    driver = ogr.GetDriverByName('ESRI Shapefile')
    
    # Open the data source
    datasource = driver.Open(in_file, 0)
    if datasource is None:
      print 'Could not open ' + in_file
      sys.exit(1)
    
    # Get the data layer
    layer = datasource.GetLayer()
    
    # If no legend type was provided, print info about the file, and make a single-symbol map
    if not legend_type:
        print 'Looking for stats on your file? Printing those (one moment)... Then drawing simple single-simple map styles...'
        
        # TODO: print out the (field names) and (field types).
        #ogrinfo(in_file_fullpath)
        
        # Proceed and just dump out the data
        legend_type = 'single-symbol'
    
    # Stub out the MSS (styles)
    mss_header = ['/* MSS header tk tk tk */']
    mss_footer = ['']
    
    # Stub out the MML (layers)
    mml_header = ['<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE Map[\n\t<!ENTITY epsg4326 "+proj=longlat +datum=WGS84">\n\t<!ENTITY epsg900913 "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over">\n\t<!ENTITY epsg900913_extent "-20037508,-20037508,20037508,20037508">\n]>\n\n<Map srs="&epsg900913;">\n\n\t<Stylesheet src="stylesheet.mss"/>']
    mml_footer = ['\n</Map>']
    
    
    # Write out the headers to the text files
    mss_file.writelines(mss_header)
    mml_file.writelines(mml_header)
    
    mml_layer = ['\n\n\t<Layer class="' + in_file + '" id="'+ in_file + '" srs="&epsg4326;">\n\t\t<Datasource>\n\t\t\t<Parameter name="type">shape</Parameter>\n\t\t\t<Parameter name="file">' + in_file_fullpath + '</Parameter>\n\t\t</Datasource>\n\t</Layer>\n']
    
    mml_file.writelines(mml_layer)
    
    
    # What type of map are we making?
    if legend_type == 'single-symbol':
        #points
        #lines
        #polygons
        pass
    elif legend_type == 'unique-value':
        # If no fieldname was provided, error
        if not fieldname:
            print 'Bad fieldname, exiting.'
            sys.exit(1)
        
        stats = gather_stats( layer, fieldname, 10000)
        
        # TODO: loop thru the stats.values and make an MSS layer for each entry in Dict
        
        #for i in stats.values:
        print stats
        
        #points
        #lines
        #polygons
        
        #mss_layer = ['#water-bodies[zoom=8][area>50000000] { polygon-fill: #000; }',
        #'#water-bodies[zoom=9][area>10000000] { polygon-fill: #000; }',
        #'#water-bodies[zoom=10][area>2500000] { polygon-fill: #000; }']

    elif legend_type == 'continuous-color':
        # If no fieldname was provided, error
        if not fieldname:
            print 'Bad fieldname, exiting.'
            sys.exit(1)
        
        stats = gather_stats( layer, fieldname, 10000)
        
        # TODO: Then quantiles
                       
        # Let's look at the first value in the Dict and see if it's a String
        # TODO
        # val = 1st element in Dict's name
        if isinstance(val, str):
            print 'Can only make quantiles for numbers fields, exiting...'
            sys.exit(1)
            
        # TODO: Cast the dict to a list ignoring the counts
     
        for qtype in range(1,10):
            print qtype, Quantile(x, 0.35, qtype)
            
        # TODO: make the MSS
                        
    elif legend_type == 'graduated-symbol':
         # TODO: et al
        pass
    else:
        print 'Bad legend type, exiting.'
        sys.exit(1)
        
        
        
    # Close the data source
    datasource.Destroy()
    
    # Write out the footers to the text files
    mss_file.writelines(mss_footer)
    mml_file.writelines(mml_footer)
    
    # Close the MSS and MML files
    mss_file.close()
    mml_file.close()


def gather_stats(layer, fieldname, num_features=10000):
    statistics = {'values':{}, 'min':{}, 'max':{}, 'type':'', 'count':0, 'count_not_null':0}
    # Loop through the features in the layer
    feature = layer.GetNextFeature()

    if type( feature.GetField(fieldname) ) is str:
        statistics['type'] = 'String'
    else:
        statistics['type'] = 'Number'
    
    # Gather values
    while feature:        
        # get the attributes
        key = feature.GetField(fieldname)
        
        # Add key to dictonary, and track with value counter for total values (histogram)
        if key in statistics['values']:
            statistics['values'][ key ] += 1
        else:
            statistics['values'][ key ] = 1
        
        # Increment the statistics counter
        statistics['count'] += 1
        if key:
            statistics['count_not_null'] += 1
               
        # Destroy the feature and get a new one
        feature.Destroy()
        feature = layer.GetNextFeature()
    
    # Calculate min/max for the data ranges
    
    field_values = []
    field_values_counts = []
    for k, v in statistics['values'].iteritems():
        field_values.append(k)
        field_values_counts.append(v)
    
    #print min(field_values)
    #print max(field_values)
    #print min(field_values_counts)
    #print max(field_values_counts)
    
    statistics['min'] = min(field_values)
    statistics['max'] = max(field_values)
        
    # TODO: sort the dict and take the last and first
    
    # Return the results
    return statistics