# About

Python tools for querrying a data source and drawing thematic cartographic representations. Works with CSV, SHP, and other OGR based data files.

By **Nathaniel Vaughn Kelso** at [Stamen](http://stamen.com).

Stubs out MSS and MML files compatabile with [Mapnik](https://github.com/mapnik/mapnik) based on a dataset for:

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

Wonder what indicator to use? Use the "describe" mode to report OrgInfo style field listing:

    python thematic.py sample_data/ne_10m_admin_0_countries.shp --classification-type=describe


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

Describe:

    data source : ne_10m_admin_0_countries.shp
       full path: /Users/nvkelso/github/thematic-carto-tools/sample_data/ne_10m_admin_0_countries.shp
    ==== layer 0
      shape type: Polygon
      # features: 253
             srs: GEOGCS["GCS_WGS_1984",
        DATUM["WGS_1984",
            SPHEROID["WGS_1984",6378137.0,298.257223563]],
        PRIMEM["Greenwich",0.0],
        UNIT["Degree",0.0174532925199433]]
          extent: (-179.99978348919961, 180.0000000000001) - (-89.99982838943765, 83.63381093402974)
      # fields 31: NAME (first value)
                   ------------------
                   ne_10m_adm	(ABW)
                   ScaleRank	(3)
                   LabelRank	(6)
                   FeatureCla	(Adm-0 country)
                   OID_	(18)
                   SOVEREIGNT	(Netherlands)
                   SOV_A3	(NL1)
                   ADM0_DIF	(1.0)
                   LEVEL	(2.0)
                   TYPE	(Country)
                   ADMIN	(Aruba)
                   ADM0_A3	(ABW)
                   GEOU_DIF	(0.0)
                   GEOUNIT	(Aruba)
                   GU_A3	(ABW)
                   SU_DIF	(0.0)
                   SUBUNIT	(Aruba)
                   SU_A3	(ABW)
                   NAME	(Aruba)
                   ABBREV	(Aruba)
                   POSTAL	(AW)
                   NAME_FORMA	(None)
                   TERR_	(Neth.)
                   NAME_SORT	(Aruba)
                   MAP_COLOR	(9.0)
                   POP_EST	(103065.0)
                   GDP_MD_EST	(2258.0)
                   FIPS_10_	(0.0)
                   ISO_A2	(AW)
                   ISO_A3	(ABW)
                   ISO_N3	(533.0)

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