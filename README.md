# About

OGR based Python tools for querrying a data source (SHP, etc) and drawing thematic cartographic representations.

By Nathaniel Vaughn Kelso at Stamen.

Stubs out MSS and MML files based on a dataset for:

* quick data exploration of what's in a dataset
* refined cartographic presentations

# Usage

Default, just get single sympol maps up (point or poly):

`thematic.py datafile outstylefile`

Classify a polygon/polyline dataset in 5 steps:

`thematic.py datafile outstylefile -f fieldname --legend-type continuous-color -c quantiles -n 5 -r YlGnBu`

Separate color for each feature value:

`thematic.py datafile outstylefile -f fieldname --legend-type unique-value -r YlGnBu`

# Coda

Inspired by a fall 2011 workshop held at Stamen about future of Carto and Cascadenik CSS style map rendering in Mapnik & etc.