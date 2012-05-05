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
    
Includes built in support for CSV/TSV and DBF/SHP files. Uses OGR for other file types.


## Usage

Default, just get single sympol maps up (point or poly):

    python thematic.py --in_file=sample_data/ne_10m_admin_0_countries.shp --legend-type=single-symbol

Classify a polygon/polyline dataset in 5 steps:

    python thematic.py --in_file=sample_data/ne_10m_admin_0_countries.shp --indicator=POP_EST --legend-type=bins --classification-type=quantiles -n 5 --colors=YlGnBu

Separate color for each feature value:

    python thematic.py --in_file=sample_data/ne_10m_admin_0_countries.shp --indicator=MAP_COLOR --legend-type=bins --classification-type=unique-values --colors=YlGnBu

Will create 3 files:

`style.mml` - Cascadenik map markup layer file
`stylesheet.mss` - Cascadenik map style sheet file
`legend.html` - See the color breaks in a pretty HTML legend
    

## Requirements

- Python `>= 2.6`

- GDAL with OGR support `>= ?`


## Author

- Nathaniel V. KELSO (nvkelso)

### Contributors

- Michael Lawrence Evans (mlevans)
- Mike Migurski (migurski)


## Coda

Inspired by a fall 2011 workshop held at Stamen about future of Carto and Cascadenik CSS style map rendering in Mapnik & etc.