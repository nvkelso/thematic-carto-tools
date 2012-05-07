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
from optparse import OptionParser
import csv
import math, stat

try:
  from osgeo import gdal, ogr  
except ImportError:
  import gdal
  import ogr
  
from Thematic.classify import Classify
from Thematic.ogrinfo import describe as Describe


optparser = OptionParser(usage="""%prog [options]

THEMATIC CARTO TOOLS

Is a CSV, SHP, and OGR based Python tools for querrying a data source and drawing 
thematic cartographic representations.""")

optparser.add_option('-s', '--in_file','--data_file', dest='infilename',
                      help='Give me your huddled masses of geodata!')

optparser.add_option('-o', '--out_files', dest='outfiles', action='append', nargs=3, default=('stylesheet.mss', 'style.mml', 'legend.html'),
                      help='Style name for resulting MSS, MML, and HTML files.')

optparser.add_option('-i', '--indicator', '--field-name', dest='field_name', 
                      help='Data is in which column.')

optparser.add_option('-m', '--measurement', dest='measurement', default='quantitative',
                      help='quantitative or qualitative.')

optparser.add_option('--name-field', dest='name_field', default='name',
                      help='Optional name of column for labels to name themselves. Default value is "name".')

optparser.add_option('--filter-field', dest='filter_field', action='append', nargs=2,
                      help='Field to use for limiting selection by theme and the value to limit by. Default is no filter. Useful if more than one enumeration unit type is present in master data file (eg: mixed ZIPs and Counties).')

optparser.add_option('-c', '--classification-type', dest='class_type', default='quantile',
                      help='Valid types are: quantile, single-symbol, unique-value, equal-interval, standard-deviation, minimum-variance, jenks, manual, ratio, continuous-color, graduated-symbol, describe')

optparser.add_option('-n', '--number-breaks', dest='num_breaks', default=5, type='int',
                      help='Number of data breaks. single-symbol=1 by default.')

optparser.add_option('-r', '--colors', dest='colors', default='YlGnBu',
                      help='Named color series from ColorBrewer.org or other --color-space. Note yet implemented: comma-separated-values for specific #aabbcc; hex values')

optparser.add_option('--color-space', dest='color-space', default='ColorBrewer',
                      help='ColorBrewer. Not yet implemented: Hex, Kuler')


if __name__ == "__main__":

    (options, args) = optparser.parse_args()
    
    #print 'len(args): ', len(args)
    indicator_field = None
    
    if len(args) > 0:
        filename = str(args[:1][0])
        other_files = args[1:] # this list might be empty, if no other output files were provided

        parse_indicator = ''
        parse_mss = ''
        parse_mml = ''
        parse_html = ''
        
        if not other_files:
            other_files = options.outfiles
        else:
            for item in other_files:
                if item.find('.mss') != -1:
                    parse_mss = item
                elif item.find('.mml') != -1:
                    parse_mml = item
                elif item.find('.html') != -1:
                    parse_html = item
                else:
                    parse_indicator = item
            
            if parse_mss == '' and parse_mml == '' and parse_html == '':
                other_files = options.outfiles
            else:            
                other_files = ( parse_mss, parse_mml, parse_html )
                        
            if parse_indicator != '':
                indicator_field = parse_indicator
            else:
                indicator_field = options.field_name
    else:
        filename = options.infilename
        other_files = options.outfiles
        indicator_field = options.field_name    
   
    #filename, columnname = args[:2] # this will fail if there are any fewer than two args
    #other_files = args[2:] # this list might be empty, if no other output files were provided

    if not filename:
        print 'Requires input file'
        sys.exit(1)
        
    options.infilename
    
    # Input geodata
    in_dir = os.path.dirname( os.path.abspath( filename ) )
    in_file, in_file_extension = os.path.splitext( os.path.abspath( filename ) )
    in_file_name_part, in_file_ext_part = os.path.basename( os.path.abspath( filename ) ).split('.')
    in_file_fullpath = os.path.abspath( filename )
            
    # Output MSS, MML, and HTML files
    out_dir = os.path.dirname( os.path.abspath( other_files[0] ) )
    out_mss = other_files[0]
    out_mml = other_files[1]
    out_html = other_files[2]
        
    # Store the options
    if indicator_field == None:
        indicator_field = options.field_name
    if options.measurement == 'quantitative': 
        quantitative = True
    else: 
        quantitative = False
    feature_name_field = options.name_field
    classification_type = options.class_type
    filter_field = options.filter_field
    
    # User just wants to know what's in their data file
    if classification_type == 'describe':
        Describe( in_file_fullpath )        
        sys.exit(1)    
    
    if indicator_field == None:
        print 'ALERT: no --indicator field name provided so defaulting back to single-symbol'
        classification_type = 'single-symbol'
        
        
    # init the cleaned data holder
    data_clean = []
    
    # gather the data...
    # what file type are we working with?
    
    if classification_type != 'single-symbol':
        if in_file_extension == '.csv' :
            try:
                f = open( in_file_fullpath, 'rt' )
            except IOError as (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
                sys.exit(1)
            
            data_raw = []
            try:
                reader = csv.DictReader( f )
                for row in reader:
                    #print row
                    #print type( row )
                    data_raw.append( row )
            finally:
                f.close()
                    
            for row in data_raw:
                try:
                    # if the value of the indicator in this row DOESN'T match the filter value, skip this feature
                    if filter_field:
                        if row[ options.filter_field[0][0] ] != options.filter_field[0][1] :
                            continue
    
                    if quantitative and (classification_type != 'unique-value' and classification_type != 'unique-values'):
                        indicator = float( row[ indicator_field ] )
                    else:
                        indicator = row[ indicator_field ]
                    name = row[ feature_name_field ]
                    data_clean.append( {'name': name, indicator_field: indicator } )
                except Exception, e:
                    print "The following exception occurred : ", e
            
        elif in_file_extension == '.shp' :
            
            # Get the shapefile driver
            driver = ogr.GetDriverByName('ESRI Shapefile')
            
            # Open the data source
            data_raw = driver.Open(in_file_fullpath, 0)
            
            if data_raw is None:
              print 'Could not open ' + in_file_fullpath
              sys.exit(1)
            
            # Get the data layer
            layer = data_raw.GetLayer()
            
            #http://www.gdal.org/ogr/ogr__core_8h.html#a800236a0d460ef66e687b7b65610f12a
            # wkbPoint or wkbMultiPoint or wkbPoint25D or wkbMultiPoint25D
            # wkbLineString or wkbMultiLineString or wkbLineString25D or wkbMultiLineString25D
            # wkbPolygon or wkbMultiPolygon or wkbPolygon25D or wkbMultiPolygon25D
            #geometry_type = layer
            
            # Get the row
            feature = layer.GetNextFeature()
            
            # counter if there is no name field
            i = 0
    
            # Gather values
            while feature:
                # if the value of the indicator in this row DOESN'T match the filter value, skip this feature
                if filter_field:
                    if feature.GetField( options.filter_field[0][0] ) != options.filter_field[0][1] :
                        continue
            
                # get the attributes
                indicator = feature.GetField(indicator_field)
                try:
                    name = feature.GetField( feature_name_field )
                except:
                    name = i
                    
                data_clean.append( {'name': name, indicator_field: indicator } )
                       
                # Destroy the feature and get a new one
                feature.Destroy()
                feature = layer.GetNextFeature()
            
            # Close the data source
            data_raw.Destroy()
    else:
        classification_type = 'single-symbol'
        indicator_field = 'indicator'
        data_clean.append( {'name': '', indicator_field: 1 } )
        data_clean.append( {'name': '', indicator_field: 1 } )

   
    #print 'data_clean: ', data_clean

        
    # If the output directory doesn't exist, make it so we don't error later on file open()
    if not os.path.exists(out_dir):
        print 'making dir...'
        os.makedirs(out_dir)
    
    # prepare output files
    if other_files[0] != '':
        mss_file = open(out_mss,"w")
    if other_files[1] != '':
        mml_file = open(out_mml,"w")
    if other_files[2] != '':
        html_file = open(out_html,"w")
    
    # Set the working directory (important for the SHP OGR bits?)
    os.chdir(in_dir)        
    
    # Stub out the MSS (styles)
    mss_header = ['/* MSS Stylesheet */\n\n']
    mss_footer = ['']
    
    # Stub out the MML (layers)
    mml_header = ['<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE Map[\n\t<!ENTITY epsg4326 "+proj=longlat +datum=WGS84">\n\t<!ENTITY epsg900913 "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over">\n\t<!ENTITY epsg900913_extent "-20037508,-20037508,20037508,20037508">\n]>\n\n<Map srs="&epsg900913;">\n\n\t<Stylesheet src="' + other_files[0] + '"/>']
    mml_layer = ['\n\n\t<Layer class="' + in_file_name_part + '" id="'+ in_file_name_part + '" srs="&epsg4326;">\n\t\t<Datasource>\n\t\t\t<Parameter name="type">shape</Parameter>\n\t\t\t<Parameter name="file">' + in_file + '</Parameter>\n\t\t</Datasource>\n\t</Layer>\n']
    mml_footer = ['\n</Map>']
    
    # Stub out the HTML (legend)
    html_header = ['<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<title>Map legend</title>\n</head>\n<body >']
    html_footer = ['</body></html>']
            
    # Write out the headers to the text files
    if other_files[0] != '':
        mss_file.writelines(mss_header)
    if other_files[1] != '':
        mml_file.writelines(mml_header)
    if other_files[2] != '':
        html_file.writelines(html_header)    
    
    #print 'classification_type: ', classification_type
    #print 'indicator: ', indicator_field
    
    # What type of map are we making?
    if classification_type == 'single-symbol':
        data_classed = Classify( data_clean, False, indicator_field, 5, 'Universal', [], indicator_field, 2, 'None', [], 'YlGn', in_file_name_part  )
    elif classification_type == 'unique-value' or classification_type == 'unique-values':
        data_classed = Classify( data_clean, False, indicator_field, 5, 'Unique value', [], indicator_field, 2, 'None', [], 'YlGn', in_file_name_part  )
    elif classification_type == 'quantile' or classification_type == 'quantiles':
        if not quantitative:
            print 'Can only make Quantiles for numbers fields, exiting...'
            sys.exit(1)
        data_classed = Classify( data_clean, False, indicator_field , 5, 'Quantiles', [], indicator_field, 2, 'None', [], 'YlGn', in_file_name_part  )
    elif classification_type == 'equal-interval':
        if not quantitative:
            print 'Can only make Equal Interval for numbers fields, exiting...'
            sys.exit(1)
        data_classed = Classify( data_clean, False, indicator_field , 4, 'Equal Interval', [], indicator_field, 2, 'None', [], 'YlGn', in_file_name_part  )
    elif classification_type == 'standard-deviation':
        if not quantitative:
            print 'Can only make Standard Deviation for numbers fields, exiting...'
            sys.exit(1)
        data_classed = Classify( data_clean, False, indicator_field , 4, 'Standard Deviation', [], indicator_field, 2, 'None', [], 'YlGn', in_file_name_part  )
    elif classification_type == 'minimum-variance' or classification_type == 'jenks' or classification_type == 'jenks-optimal':
        if not quantitative:
            print 'Can only make Minimum Variance for numbers fields, exiting...'
            sys.exit(1)
        data_classed = Classify( data_clean, False, indicator_field , 4, 'Minimum Variance', [], indicator_field, 2, 'None', [], 'YlGn', in_file_name_part  )
    elif classification_type == 'manual':
        data_classed = Classify( data_clean, False, indicator_field , 4, 'Manual', [], indicator_field, 2, 'None', [], 'YlGn', in_file_name_part  )
    elif classification_type == 'continuous-color' or classification_type == 'ratio':
        data_classed = Classify( data_clean, False, indicator_field , 4, 'Ratio', [], indicator_field, 2, 'None', [], 'YlGn', in_file_name_part  )
    elif classification_type == 'graduated-symbol':
        pass
    else:
        print 'Bad legend or classification type, exiting.'
        sys.exit(1)
    
    #self.classInit( dataTest, False, dataAttrName, 4, 'Equal Interval', testBreaks, dataAttrName, 2, 'None', testNominalBreaks, 'YlGn'  )
    #self.classInit( dataTest, False, dataAttrName, 5, 'Quantiles', testBreaks, dataAttrName, 2, 'None', testNominalBreaks, 'YlGn'  )
    #self.classInit( dataTest, False, dataAttrName, 3, 'Quantiles', testBreaks, dataAttrName, 2, 'None', testNominalBreaks, 'YlGn'  )
    #self.classInit( dataTest, False, dataAttrName, 3, 'Standard Deviation', testBreaks, dataAttrName, 2, 'None', testNominalBreaks, 'YlGn'  )
    
    #TODO: fix
    #self.classInit( dataTest, False, dataAttrName, 3, 'Minimum Variance', testBreaks, dataAttrName, 2, 'Ratio', testNominalBreaks, 'YlGn'  )
    #self.classInit( dataTest, False, dataAttrName, 3, 'Manual', testBreaks, dataAttrName, 2, 'Ratio', testNominalBreaks, 'YlGn' )
    
    #self.classInit( dataTest, False, dataAttrName, 3, 'Ratio', testBreaks, 'pumpType', 2, 'Nominal', testNominalBreaks, 'YlGn' )
    #self.classInit( dataTest, False, dataAttrName, 3, 'Ratio', testBreaks, 'pumpType', 4, 'None', testNominalBreaks, 'YlGn' )
    #self.classInit( dataTest, False, dataAttrName, 4, 'Equal Interval', testBreaks, 'pumpType', 2, 'Nominal', testNominalBreaks, 'YlGn'  )

    mss_layers = data_classed.get_mss()
    if indicator_field:
        legend_layers = indicator_field + '<br/>' + data_classed.get_legend()
    else:
        legend_layers = data_classed.get_legend()
    
    # Write out the layer content to the text files
    if other_files[0] != '':
        mss_file.writelines(mss_layers)
    if other_files[1] != '':
        mml_file.writelines(mml_layer)    
    if other_files[2] != '':
        html_file.writelines(legend_layers)
    
    # Write out the footers to the text files
    if other_files[0] != '':
        mss_file.writelines(mss_footer)
    if other_files[1] != '':
        mml_file.writelines(mml_footer)
    if other_files[2] != '':
        html_file.writelines(html_footer)
    
    # Close the MSS and MML files
    if other_files[0] != '':
        mss_file.close()
    if other_files[1] != '':
        mml_file.close()
    if other_files[2] != '':
        html_file.close()