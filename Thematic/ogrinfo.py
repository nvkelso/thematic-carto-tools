"""
From GeoDjango (and old copy)...

This module includes some utility functions for inspecting the layout
of a GDAL data source -- the functionality is analogous to the output
produced by the `ogrinfo` utility.
"""

from osgeo.gdal import Dataset
from osgeo.gdal.geometries import GEO_CLASSES

class Ogrinfo:
    
    def ogrinfo(data_source, num_features=10000):
        """
        Walks the available layers in the supplied `data_source`, displaying
        the fields for the first `num_features` features.
        """
    
        # Checking the parameters.
        if isinstance(data_source, str):
            data_source = Dataset(data_source)
        elif isinstance(data_source, DataSource):
            pass
        else:
            raise Exception('Data source parameter must be a string or a DataSource object.')
    
        for i, layer in enumerate(data_source):
            print "data source : %s" % data_source.name
            print "==== layer %s" % i
            print "  shape type: %s" % GEO_CLASSES[layer.geom_type.num].__name__
            print "  # features: %s" % len(layer)
            print "         srs: %s" % layer.srs
            extent_tup = layer.extent.tuple
            print "      extent: %s - %s" % (extent_tup[0:2], extent_tup[2:4])
            print "Displaying the first %s features ====" % num_features
    
            width = max(*map(len,layer.fields))
            fmt = " %%%ss: %%s" % width
            for j, feature in enumerate(layer[:num_features]):
                print "=== Feature %s" % j
                for fld_name in layer.fields:
                    type_name = feature[fld_name].type_name
                    output = fmt % (fld_name, type_name)
                    val = feature.get(fld_name)
                    if val:
                        if isinstance(val, str):
                            val_fmt = ' ("%s")'
                        else:
                            val_fmt = ' (%s)'
                        output += val_fmt % val
                    else:
                        output += ' (None)'
                    print output
                
                    gather_ogr_stats( layer, fld_name, 100000 )

                    
    # TODO: This isn't tested yet
    def gather_ogr_stats( layer, indicator_field, num_features=10000 ):
        statistics = {'values':{}, 'min':{}, 'max':{}, 'type':'', 'count':0, 'count_not_null':0}
        # Loop through the features in the layer
        feature = layer.GetNextFeature()
    
        if type( feature.GetField(indicator_field) ) is str:
            statistics['type'] = 'String'
        else:
            statistics['type'] = 'Number'
        
        # Gather values
        while feature:        
            # get the attributes
            key = feature.GetField(indicator_field)
            
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