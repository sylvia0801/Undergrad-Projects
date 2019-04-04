# CS 591 Spring17 Project

### Group Members: [Xiaotong Niu](https://github.com/sylvia0801), [Po-Yu,Tseng](https://github.com/cybersoftintern)

## Datasets we use

From City of Boston Data Portal:

Property Assessment 2014: https://data.cityofboston.gov/dataset/Property-Assessment-2014/qz7u-kb7x

Property Assessment 2015: https://data.cityofboston.gov/Permitting/Property-Assessment-2015/yv8c-t43q

Crime Incident Reports: https://data.cityofboston.gov/Public-Safety/Crime-Incident-Reports-July-2012-August-2015-Sourc/7cdf-6fgx


From BostonMaps Open Data: 

Police Districts: http://bostonopendata-boston.opendata.arcgis.com/datasets/9a3a8c427add450eaf45a470245680fc_5?uiTab=table


From MassData:

FLD Complaints: https://data.mass.gov/dataset/FLD-Complaints/c5kv-hee8

## The Impact of Crime on Property Values

### Introduction
For most people nowadays, the most pressing demand is to improve their living standards. In a crowded city like Boston, one of the main factors that influence people’s decision on choosing residential properties is the amount of crime incidents that had happened in their respective area. For this project, we attempt to analyze the relationship between property prices in 2015 and the number of crime incidents that had happened in 2015 in the Boston area.
We use Relational Paradigm to extract certain data from City of Boston Data Portal: Property Assessment 2015 and Crime Incident Reports. First, we assume higher property price will lead to lower number of crime incidents. To test our assumption, we use statistical analysis to find if the correlation value between the two is negative, and how strongly they are correlated; we also look at the p-value to check the accuracy of our correlation value. Secondly, we use k-means technique to find the most optimized point where the property is the safest, which indicates that the frequency of crime incidents happened around that point is the smallest.
Overall, we implement two techniques: statistical analysis and optimization(k-means) to study the relationship between the 2015 property price and the number of crime incidents in Boston area.

#### Algorithms and Relational Paradigms Overview
![relation_paradigm](https://github.com/sylvia0801/course-2017-spr-proj/blob/master/pt0713_silnuext/proj3/images/relation_paradigm.jpeg)

### Statistical Analysis
As for the statistical analysis, we want to find the correlation between property price and number of crime incidents; we expected that the higher property price will lead to lower number of crime incidents. We first use the definition of r-tree and polygon to correspond “property15_price_coordination_float” to “zip_to_coor,” compute the number of properties and the average price of properties in each zip code, and the result shows all the zip codes along with its corresponding average property price in Boston area. 
Second, we also use the same definition we mentioned earlier to correspond “crime_15coordination” to “zip_to_coor,” compute how many crime incidents happened within each zip code, and the result will show all the zip codes along with its corresponding number of crime incidents. Finally, we find the correlation between the average price of properties and the amount of crime incidents. The number we got is: -0.246.

#### Visualization of Statistical Analysis
##### Scatter Plot Graph of Crime Numbers and Average Property Values of the City of Boston
![scatter_plot](https://github.com/sylvia0801/course-2017-spr-proj/blob/master/pt0713_silnuext/proj3/images/scatter_plot.png)


### Optimization
For the k-means section, we want to find the most optimized point where the property is the safest (farthest from crime incidents). To do so, we input “crime_15coordination” to our k-means function and find the most optimized coordinate. Then we correspond the coordinate back to polygon and claim the zip code we get is the area where people can obtain property that is the safest. The zip code we obtained is “02119”.

#### Visualization of Optimization
##### Map of Crime Points Happened in the City of Boston
![crime_points](https://github.com/sylvia0801/course-2017-spr-proj/blob/master/pt0713_silnuext/proj3/images/crime_points.png)
##### Map of the Safest Point we got by K-Means Algorithm in the City of Boston
![opt_point](https://github.com/sylvia0801/course-2017-spr-proj/blob/master/pt0713_silnuext/proj3/images/opt_point.png)

### Conclusion and Future Works
In conclusion, the correlation value, -0.246 shows that property value and crime incident are indeed negatively related (an inverse relationship) which matches our assumption. However, | (-0.246) | also shows that they are weakly related, and the p- value we obtained is very high. Moving forward with this project, we should consider factors such as population density, school districts and police districts more thoroughly since they are also contributors to crime rates. Further, due to time constraint, we were only able to run the small portion of our crime data, which might outcome the unideal correlation and p value. Thus, we assume by running more data in the future, we will be able to obtain a better correlation and p value.

## Usage
To run index.html file, just open the file directory and drag it into the browser.

## Reference
K-Means Clustering Algorithm. **"Data Mechanics"**. [http://cs-people.bu.edu/lapets/591/s.php#2.2](http://cs-people.bu.edu/lapets/591/s.php#2.2)<br>
Correlation Value and P-Value Calculator. **"Data Mechanics"**. [http://cs-people.bu.edu/lapets/591/s.php#4.4](http://cs-people.bu.edu/lapets/591/s.php#4.4)<br>

## Installation
To set up MongoDB, follow the procedure in [Data-Mechanics/course-2017-spr-proj](https://github.com/Data-Mechanics/course-2017-spr-proj).

To install all dependencies:
```
python3 -m pip install --upgrade --no-cache-dir -r requirements.txt
```
To execute the script:
```
python3 execute.py pt0713_silnuext
```
To execute the script in trial mode:
```
python3 execute.py pt0713_silnuext --trial
```


