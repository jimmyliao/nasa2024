## TEAM

https://www.spaceappschallenge.org/nasa-space-apps-2024/find-a-team/404-not-found1/?tab=details

## Competition question

https://www.spaceappschallenge.org/nasa-space-apps-2024/challenges/

https://www.spaceappschallenge.org/nasa-space-apps-2024/challenges/tell-us-a-climate-story/?tab=details

---


## Project division of labor

Kay: Responsible for capturing data sets and processing data sets + processing chart data

Jimmy Liao: LLM deployment must be addressed in the near future (this part will require rewriting the story function due to changes in our page structure), and the deployment website will be online

Noflag: Integrate the entire architecture (add all current functions) + handle LLM function integration

Muhammad Shaharyar Sarwar: Responsible for program efficiency

Yuijuhn Ting: Responsible for page design and integrating all functions into the map screen display

----

### How to run

`streamlit run app.py`

-----
<h2 align='center'>dataset</h2>

### Other Dataset

+ https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions
+ http://data.un.org/Data.aspx?d=PopDiv&f=variableID%3a12
+ https://ourworldindata.org/grapher/population-density
+ https://www.worldometers.info/geography/flags-of-the-world
+ https://www.worldometers.info/world-population/population-by-country
+ https://developers.google.com/public-data/docs/canonical/countries_csv
+ https://ucdp.uu.se/downloads/index.html#ged_global
+ https://ucdp.uu.se/downloads/
+ https://gwis.jrc.ec.europa.eu/apps/country.profile/downloads
+ https://gwis.jrc.ec.europa.eu/apps/country.profile/downloads  


+ **GeoJson:** For the map, we used Leaflet and geoJson files for the boundaries of each country. You can find the full geoJson file here https://opendata.arcgis.com/datasets/2b93b06dc0dc4e809d3c8db5cb96ba69_0.geojson. 

** Kaggle:** 
  + https://www.kaggle.com/code/andrewmahandrew/temperature-map/notebook
  + https://www.kaggle.com/code/voraseth/climate-change-indicators-eda-010/input
  + https://www.kaggle.com/datasets/danielvalyano/country-coord
  + https://www.kaggle.com/sevgisarac/temperature-change?select=Environment_Temperature_change_E_All_Data_NOFLAG.csv
    
** Github:**
  + https://github.com/alanjones2/st-choropleth/tree/main/data
  + https://github.com/sudikshanavik/CS661A_Big_Data/tree/main/dataset
  + https://github.com/datasets/population/blob/main/data/population.csv
  + https://gwis.jrc.ec.europa.eu/apps/country.profile/downloads 
  + https://ourworldindata.org/grapher/annual-co2-emissions-per-country


### NASA Dataset

https://github.com/IvyQwinn/GlobalTemperatureAnalysis/tree/main

https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv 

> GLOBAL Land-Ocean Temperature Index in 0.01 degrees Celsius   base period: 1951-1980

https://data.giss.nasa.gov/gistemp/tabledata_v3/NH.Ts+dSST.csv

> The GISS Surface Temperature Analysis (GISTEMP) is an estimate of global surface temperature change

https://data.giss.nasa.gov/gistemp/tabledata_v3/SH.Ts+dSST.csv

> The GISS Surface Temperature Analysis (GISTEMP) is an estimate of global surface temperature change.

https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv 

> GLOBAL Land-Ocean Temperature Index in 0.01 degrees Celsius   base period: 1951-1980

https://data.giss.nasa.gov/gistemp/tabledata_v3/NH.Ts+dSST.csv

> The GISS Surface Temperature Analysis (GISTEMP) is an estimate of global surface temperature change

https://data.giss.nasa.gov/gistemp/tabledata_v3/SH.Ts+dSST.csv

> The GISS Surface Temperature Analysis (GISTEMP) is an estimate of global surface temperature change.

https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt

> CO2 data

https://climate.nasa.gov/vital-signs/global-temperature/?intent=121

> Global temperature data

+ NASA Data API
  + https://earth.gov/ghgcenter/api/stac
  + https://earth.gov/ghgcenter/api/raster

### LLM

+ Gemini API
  + Generate Stories
  + Please be sure to get your api key here. If the number of requests per minute is small, no money will be deducted, and no card binding is required!!
  > https://aistudio.google.com/app/apikey

---------------

The data sets used in this project are all placed here. Please download and place them in the final folder. The folder name is data. The data sets can only be captured when the program is running.

+ https://drive.google.com/drive/folders/1IVYH1StwpeC9c-vi9j-c8_LSxlnf4jSI?usp=sharing

### Please be sure to add a new folder in this directory with the name `.streamlit` , and add a new file in this folder with the name `config.toml`, and write the following content

```
[theme]
base="dark"
primaryColor="#fff200"
font="monospace"

```

### Demo



https://github.com/user-attachments/assets/3da99464-3228-41a5-a161-6ab51be12dc6

