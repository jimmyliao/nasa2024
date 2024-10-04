## Project division of labor

Kay: Responsible for capturing data sets and processing data sets + processing chart data

Jimmy Liao: The data loading speed + LLM deployment must be addressed in the near future (this part will require rewriting the story function due to changes in our page structure), and the deployment website will be online

Noflag: Integrate the entire architecture (add all current functions) + handle LLM function integration

Muhammad Shaharyar Sarwar: Responsible for program efficiency

Yuijuhn Ting: Responsible for page design and integrating all functions into the map screen display

----

### How to run

`streamlit run app.py`

-----
<h2 align='center'>dataset</h2>

### Other Dataset

**1. Temperature changes:** Data set [here](https://www.kaggle.com/sevgisarac/temperature-change?select=Environment_Temperature_change_E_All_Data_NOFLAG.csv) shows the changes in temperature in each country from 1961 to 2019. The data is also split up into each month, so that you can compare January vs January, and by season. The changes go anywhere from 9&deg;C cooler to 11&deg;C warmer.<br/><br/> 

**2. CO2 Emissions:** Temperature fluctuations can be caused by many different events, one of which is CO2 emissions. Each country produces different amounts of CO2 dependent on their access to electricity, the total population, the urban population and other factors. We used the data from https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions and you can find the dataset [here](./static/data/CO2_emission.csv)

**3. Country demographics:** Since the CO2 emissions can be influenced by the demographics of the country, the dashboard includes current demographics, as of May 2021, so that as you are reviewing the charts, you can see how the demographics might play a role. The demographics were scraped from three different websites using Beautiful Soup. After scraping the websites, the data was pushed into the sqlite database as an additional table and also saved as a csv file.<br><br>

- a. __Flags__ - https://www.worldometers.info/geography/flags-of-the-world/<br>
- b. __Population__ - https://www.worldometers.info/world-population/population-by-country/<br>
- c. __Latitude and Longitude coordinates__ - https://developers.google.com/public-data/docs/canonical/countries_csv<br><br>

**4. GeoJson:** For the map, we used Leaflet and geoJson files for the boundaries of each country. You can find the full geoJson file here https://opendata.arcgis.com/datasets/2b93b06dc0dc4e809d3c8db5cb96ba69_0.geojson. 

**5. Kaggle:** https://www.kaggle.com/code/andrewmahandrew/temperature-map/notebook

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

https://github.com/user-attachments/assets/7b998976-9d6d-4ae6-bdee-26550d3fa4e1
