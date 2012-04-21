# About

OGR based Python tools for querrying a data source (SHP, etc) and drawing thematic cartographic representations.

By Nathaniel Vaughn Kelso at Stamen.

Stubs out MSS and MML files based on a dataset for:

* Quick data exploration of what's in a dataset
* Refined cartographic presentations


## Installation

Git checkout (requires git)

    git clone git://github.com/nvkelso/thematic-carto-tools.git
    cd thematic-carto-tools


## Usage

Default, just get single sympol maps up (point or poly):

    thematic.py datafile outstylefile

Classify a polygon/polyline dataset in 5 steps:

    thematic.py datafile outstylefile -f fieldname --legend-type continuous-color -c quantiles -n 5 -r YlGnBu

Separate color for each feature value:

    thematic.py datafile outstylefile -f fieldname --legend-type unique-value -r YlGnBu


## Requirements

- Python `>= 2.6`

- GDAL with OGR support `>= ?`


## Authors

- Nathaniel V. KELSO (nvkelso)

- Michael Lawrence Evans (mlevans)


## Coda

Inspired by a fall 2011 workshop held at Stamen about future of Carto and Cascadenik CSS style map rendering in Mapnik & etc.