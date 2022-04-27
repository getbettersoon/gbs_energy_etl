## 1. Defining the scope of the project and gathering data

At the start of the process I have deliberated on what domain of data I would be interested to engage in. After few potential ideas came to mind I spent time thinking of what kind of answers and insights could be drawn from using this data. I had to ensure it would be valuable to data analysts. Next, knowing what kind of data I need and that I can add value, I had to ensure I can obtain good amount and quality of it. I used Google Dataset Search and Kaggle to explore available datasets.

The data I was looking for was:</br>
- energy production and consumption</br>
- greenhouse emissions</br>
- temperature</br></br>

With all this data I wanted to create analytics tables to be able to answer questions like these:</br>
- what countries are at the forefront of decreasing fossil fuel use and increasing renewable energy production?</br>
- what are the effects of temperature on energy consumption?</br>
- is there a correlation between GDP and amount of clean energy produced?</br>
- in countries with least emissions per capita, what is a primary energy source?</br>
- are there any poor countries which are among countries driving transformation to clean energy?</br></br>

#### I have found three datasets

### "GlobalLandTemperaturesByCountry"

This temperature data comes from Berkeley Earth which is an independent U.S. non-profit organisation focused on environmental data science. Data range covered is between 1743-2013.</br>
![temperature dataset sample](/img/temp.png) 
<font  size=2>source: https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data</font></br>
<font  size=2>licence: https://creativecommons.org/licenses/by-nc-sa/4.0/</font></br></br>

### "CW_HistoricalEmissions"

Climate Watch is an online platform designed to provide open climate data. It is managed by World Resources Institute. Data contains historical greenhouse gas emissions per country, per year, per gas and covers years from 1850 to 2018.</br>

![emissions dataset sample](/img/emissions.png) 
<font  size=2>source: https://www.climatewatchdata.org/data-explorer/historical-emissions</font></br>
<font  size=2>licence: https://www.climatewatchdata.org/about/permissions</font></br>
<font  size=2>more info: https://zenodo.org/record/4479172#.Yg0yei-l06V</font></br></br>

### "OWID-energy-data"

Our World In Data is a non-profit organization providing data to tackle variety of issues. Dataset contains information about amounts of energy consumption and production by type, by country, by year. Data range covered is between 1900-2021.</br>

![energy dataset sample](/img/energy.png)
<font  size=2>source: https://github.com/owid/energy-data</font></br>
<font  size=2>licence: https://creativecommons.org/licenses/by/4.0/</font></br></br>

## 2. Explore and assess the data

### Choosing Pandas for the job

At this stage I inspected these datasets for data quality issues. I used pandas for that purpose as it is a suitable tool for data exploration and it also has a great support for the file formats I am working with.</br></br>

Quality checks included:
- column issues - unwanted columns, unsuitable naming
- type constraints - looking for possible data type issues, i.e. numeric values presented as objects
- range constraints - checking if data is within expected range
- missing values
- uniqueness constraints, duplicate rows</br>

### Quality check and data exploration results

#### Climate Change: Earth Surface Temperature Data

- Columns:
	- names in PascalCase, converted to snake_case</br>
	- drop column 'average temperature uncertainty'</br>

- Type constraints:
	- datetime (dt) imported as 'object', it will have to be converted to numeric later</br>
	- temperature data imported as 'float64'</br>

- Range constraints:
	- datetime (dt) column: year and month within range, day is always '1'</br>
	- AverageTemperature in expected range</br>
	
- Missing values:
	- ~32k values are missing in Average Temperature that is about 5.6% of total row count</br></br>

- Uniqueness constraints:</br>
	- no duplicate rows</br>

- Other:
	- some country names did not match ISO 3166, they were corrected</br></br>

- Units:
	- figures in Celsius</br></br>


#### Climate Watch - Historical Emissions

- Columns:
	- drop 'source' column</br>
	- using snake_c</br>

- Type constraints:
	- almost all columns were imported as 'object', and only few numerical columns were correctly interpreted as 'float64'. Since I expected all numerical columns to be imported as 'float' I investigated further. </br>
	
	- What I have found is very few rows had across majority of their columns '#NUM!' value which was causing Pandas to import those columns as 'object'. To fix it I removed these rows.</br>

- Range constraints:
	- for every combination of sector and gas, no value is higher than that for the entire world. Also no value is lower than 0.</br>

- Missing values:
	- as mentioned in 'type constraints' above there were 5 rows, out of 4717 total rows, that had over 150 columns of data missing each, out of 174 total columns. Because all the missing data was concentrated in so few rows, I replaced all the values with np.nan and then removed those rows altogether.</br>
	
- Uniqueness constraints:</br>
	- no duplicate rows</br>

- Units:
	- "Unit is either Gg or GgCO2eq (CO2-equivalent according to the global warming potential used)." </br>
	source: https://zenodo.org/record/4479172#.YitNqy-l1qu</br></br>


#### OWID - Energy Data

- Columns:
	- few column names had naming inconsistencies:</br>
		- 'other_renewable_exc_biofuel_electricity' here 'exc_biofuel' appendix was put in the middle of 'other_renewable_electricity' where in other cases was at the end. That will be renamed to 'other_renewable_electricity_exc_biofuel'</br>
		- 'other_renewable_consumption' column contained 'renewable' in singular form, where most others were in plural. This will be renamed to 'other_renewables_consumption'</br>
		- same as above for 'other_renewable_electricity', this will be renamed to 'other_renewables_electricity'</br>
	- using snake_case</br>


- Type constraints:
	- three columns: country, iso_code and data imported as objects</br>
	- 'data' column contains list of JSON objects. I used Pandas to flatten it and now it's in 1NF.</br>
	- after flattening all columns containing numerical values were converted to float</br>
	
- Range constraints:
	- checked subset of columns per year per gas to see if any max value for rest of the world is higher than value for the whole world</br>
	- checked if there are any value below 0</br>

	
- Missing values:
	- some records represented regions, rather than countries ('western_africa', 'Other Caribbean' etc.) and did not have an iso_code, those were dropped, as they are vague as to what countries they represent</br>
	- there are missing values all over the dataset which seem to be MNAR - Missing Not At Random. There is a strong pattern that indicates that data is missing in long stretches of time because:</br>
		- energy source was likely not used</br>
		- the technology did not exist at the time</br>
		- the data was not reported</br>
	- there were two Infinite values in a column representing energy consumption change in percent. That was caused by energy production in a previous year being 0 and next year going positive. Both 'inf' values were changed to 'nan'.
	</br>
		
- Uniqueness constraints:
	- no duplicate rows</br>

- Other:
	- some country names did not match ISO 3166, they were corrected</br>


- Units:
	- production and consumption figures in terawatt-hours</br>


## 3. Define the data model

### Conceptual data model

### Considering the right data model

At this stage I have considered suitable data model. Its purpose was to provide answers to analytical queries from data analysts. Data itself wasn't expected to change or be added more often than once a year. Therefore it wouldn't be used much to insert, update or delete data; it would be used to handle reads.</br></br> 
Total volume of data would be considered small. The model was expected to handle structured numeric and text data. And simple and easy to understand schema would be appreciated by end users.</br></br> 
In this case I decided that a suitable model for that task would be a dimensional model, which is appropriate for analytic queries, it embraces denormalization which helps with performance, supports relations between tables in a star schema which is easy to understand and it can handle null values in fact tables.</br></br>

### Choosing Amazon Redshift and Amazon S3

Redshift is a data warehouse running modified Postgres under the hood and uses SQL to query data. It's great for OLAP workloads, thanks to column-oriented approach it uses. On top of that, massive parallel processing allows it to divide big jobs into smaller ones, distribute it among a cluster of processors and apply them to process a query in a parallel manner.</br></br> 
Amazon Redshift is also scalable and available in regions all over the world, which is good news for scalability and data governance. It offers vast choice of hardware configuration, suitable for many kinds of applications. It has great web UI, that allows to accomplish many tasks by point-and-click and it also offers AWS CLI where users can securely connect and deploy infrastructure as code, and then manage and monitor it.</br></br> 
It also integrates well with other AWS products, like S3. Amazon S3 allowed me to easily store my datasets there and then copy into Redshift thanks to their integration. Another consideration for this project was its limited budget. Again, AWS was a great choice here as they offered 30day free trial for Redshift and 5GB free S3 storage.</br></br>

### Steps necessary to pipeline the data into the chosen data model

1. Upload raw datasets to S3.</br>
2. Clean datasets in Pandas using insights gained in data exploration stage.</br>
3. Upload clean datasets to Amazon S3.</br>
4. Configure and run AWS Redshift cluster</br>
	1. Create IAM Role for Redshift to access S3</br>
	2. Add inbound traffic rules for associated security group</br>
	3. Attach IAM Role to cluster</br>
5. Test connection to Redshift from VS Code</br>
6. Create a file that will contain SQL statements</br>
	1. Table creation, copy from S3 to Redshift staging, inserts into final tables</br>
7. Create ETL script that will, create all tables, copy from S3 to Redshift, transform data and insert into final tables
8. Create tests</br></br>

## 4. Run ETL to model the data

### Data dictionary </br> 

![data dict 1](/img/data_dict1.png)</br>
										![data dict 2](/img/data_dict2.png)</br>
										![data dict 3](/img/data_dict3.png)</br>