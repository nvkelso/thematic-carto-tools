# About

CSV, SHP, and OGR based Python tools for querrying a data source and drawing thematic cartographic representations.

By **Nathaniel Vaughn Kelso** at [Stamen](http://stamen.com).

Stubs out MSS and MML files based on a dataset for:

* Quick data exploration of what's in a dataset
* Refined cartographic presentations

Bonus: Will also build a legend in HTML format displaying the colors and bin labels.

Looking for vector thematic maps in the browser instead? Try IndieMaps [OpenLayers-Symbology](https://github.com/sourcepole/qgis-openlayers-plugin).

## Installation

Git checkout (requires git)

    git clone git://github.com/nvkelso/thematic-carto-tools.git
    cd thematic-carto-tools
    
Includes built in support for CSV/TSV and DBF/SHP files. Uses OGR for other file types.


## Usage

Just a single sympol:

    python thematic.py sample_data/ne_10m_admin_0_countries.shp

Classify a polygon/polyline dataset in 5 steps using the POP_EST indicator field (default is: --classification-type=quantile -n 5):

    python thematic.py sample_data/ne_10m_admin_0_countries.shp POP_EST

Separate color for each feature value:

    python thematic.py sample_data/ne_10m_admin_0_countries.shp MAP_COLOR --classification-type=unique-value

Will create 3 files:

1. `style.mml` - Cascadenik map markup layer file
2. `stylesheet.mss` - Cascadenik map style sheet file
3. `legend.html` - See the color breaks in a pretty HTML legend

These files are writen local to where you ran the script. Use the "--out_files" option to specify different names OR...

NOTE: If you only want to generate the .mss file, try this:
    
    python thematic.py sample_data/ne_10m_admin_0_countries.shp POP_EST stylesheet.mss

### Sample output

Legend HTML:

![legend](https://github.com/nvkelso/thematic-carto-tools/raw/master/sample_data/images/legend.png)

Styling MSS:

    .ne_10m_admin_0_countries[zoom>=0][POP_EST>=-99.0]{ polygon-fill: #ffffcc; }
    .ne_10m_admin_0_countries[zoom>=0][POP_EST>=72660.0]{ polygon-fill: #c2e699; }
    .ne_10m_admin_0_countries[zoom>=0][POP_EST>=1533964.0]{ polygon-fill: #78c679; }
    .ne_10m_admin_0_countries[zoom>=0][POP_EST>=6995655.0]{ polygon-fill: #31a354; }
    .ne_10m_admin_0_countries[zoom>=0][POP_EST>=22215421.0]{ polygon-fill: #006837; }

Layers MML:

    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE Map[
        <!ENTITY epsg4326 "+proj=longlat +datum=WGS84">
	    <!ENTITY epsg900913 "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over">
	    <!ENTITY epsg900913_extent "-20037508,-20037508,20037508,20037508">
    ]>
    
    <Map srs="&epsg900913;">
    
	    <Stylesheet src="stylesheet.mss"/>

	    <Layer class="ne_10m_admin_0_countries" id="ne_10m_admin_0_countries" srs="&epsg4326;">
		    <Datasource>
			    <Parameter name="type">shape</Parameter>
			    <Parameter name="file">/Users/nvkelso/github/thematic-carto-tools/sample_data/ne_10m_admin_0_countries</Parameter>
		    </Datasource>
	    </Layer>
    
    </Map>


## Requirements

- Python `>= 2.6`

- GDAL with OGR support `>= 1.8.1`


## Author

- Nathaniel V. KELSO (nvkelso)

### Contributors

- Michael Lawrence Evans (mlevans)
- Mike Migurski (migurski)


## Coda

Inspired by a fall 2011 workshop held at Stamen about future of Carto and Cascadenik CSS style map rendering in Mapnik & etc.