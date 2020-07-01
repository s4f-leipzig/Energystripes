# ENERGYSTRIPES

Energystripes show the share of energy production in Germany from renewable sources (wind, solar, water and biomass) and from conventional sources (lignite, hard coal, gas, oil and nuclear power).
Days with more than 50% of energy produced from renewable sources are marked in green while days on which more than 50% of the produced energy is derived from conventional sources are colored in black.

## Data and Download
The data is derived from the webpage https://www.energy-charts.de/energy_de.htm?source=all-sources&period=daily&year=2019, which is maintained by the Fraunhofer ISE Institute.
As there is no direct download, it can be downloaded as .json-file using the Firefox web developer tool:
1. go to the year you want to download.
2. open web developer tool
3. choose tab 'network'
4. choose sub-tab 'xhr'
5. reload page and click on .json file that appears
6. save .json file
7. repeat for every year 

## Prerequisits
The code is written in Python-2.7 

## Required Python Packages
numpy  
matplotlib  
pandas    

## Authors
Scientists for Future Leipzig
