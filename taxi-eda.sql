/*
# Exploratory Data Analysis using Synapse Serverless over a Lakehouse

Let's look at some basic EDA patterns using the NYC taxi dataset.  
We can enrich the data using external datasets. 

Business Problem:  
There are a few anomalies where ridership drops.  
Could we determine if the cause might be weather?


This is my standard EDA SQL template
*/

-------------------------------------------------------------------------------------------------------------
-------------------------Standard Template Setup-------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

--best to start with a new SQL SERVERLESS db
CREATE DATABASE taxiAnalytics
GO
USE taxiAnalytics
GO

--we need to set our db to utf-8 so parquet works properly
ALTER DATABASE taxiAnalytics 
    COLLATE Latin1_General_100_BIN2_UTF8;

--we need to setup some security and credentials
IF NOT EXISTS (SELECT * FROM sys.symmetric_keys) 
BEGIN
    CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Password01!!' ;
END;

--file format definitions
IF (EXISTS(SELECT * FROM sys.external_file_formats WHERE name = 'ParquetFF')) BEGIN
    DROP EXTERNAL FILE FORMAT ParquetFF
END
CREATE EXTERNAL FILE FORMAT [ParquetFF] WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);
IF (EXISTS(SELECT * FROM sys.external_file_formats WHERE name = 'DeltaFF')) BEGIN
    DROP EXTERNAL FILE FORMAT DeltaFF
END
CREATE EXTERNAL FILE FORMAT [DeltaFF] WITH (
    FORMAT_TYPE = DELTA
);
GO

--build a connection to our sandbox data lake (where we "write" data during development)
--I think the best practice is to use the Primary data lake associated with the workspace
IF EXISTS (SELECT * FROM sys.database_scoped_credentials WHERE name = 'WorkspaceIdentity')
   DROP DATABASE SCOPED CREDENTIAL [WorkspaceIdentity]
GO
CREATE DATABASE SCOPED CREDENTIAL WorkspaceIdentity WITH IDENTITY = 'Managed Identity'
GO
IF (EXISTS(SELECT * FROM sys.external_data_sources WHERE name = 'sandbox')) BEGIN
    DROP EXTERNAL DATA SOURCE sandbox;
END
GO
CREATE EXTERNAL DATA SOURCE sandbox
WITH (    LOCATION   = 'https://asadatalakedavew891.dfs.core.windows.net/sandbox',
          CREDENTIAL = WorkspaceIdentity
)


-------------------------------------------------------------------------------------------------------------
---------------------------Connection Info for external data lakes-------------------------------------------
-------------------------------------------------------------------------------------------------------------

/*
    I use SAS tokens to look at 3rd party data lakes.  
    We can also visually explore the data in a local data lake --OR-- using AzStorageExplorer

    https://davewdemodata.dfs.core.windows.net/lake/gold/nyctlc/

    Let's assume you want to query MY datalake as a third party data source
*/

--connect to the "remote" data lake
--this is a container-based "rle" SAS token
IF (EXISTS(SELECT * FROM sys.external_data_sources WHERE name = 'davewdemolake')) BEGIN
    DROP EXTERNAL DATA SOURCE davewdemolake;
END
GO
IF EXISTS
   (SELECT * FROM sys.database_scoped_credentials WHERE name = 'davewdemolakeCred')
   DROP DATABASE SCOPED CREDENTIAL [davewdemolakeCred];
GO
CREATE DATABASE SCOPED CREDENTIAL davewdemolakeCred
WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
--container level SAS with rle
SECRET = 'sp=rle&st=2021-02-15T20:57:11Z&se=2032-02-16T04:57:11Z&spr=https&sv=2020-08-04&sr=c&sig=1v3rK0g6uK3sGHNesqIQqWxPbr3s7Pe%2FD4tNYBmD2oQ%3D'
GO
CREATE EXTERNAL DATA SOURCE davewdemolake
WITH (    LOCATION   = 'https://davewdemodata.dfs.core.windows.net/lake',
          CREDENTIAL = davewdemolakeCred
)

--let's make sure we can connect
SELECT TOP 10 * FROM
    OPENROWSET(
        BULK 'gold/nyctlc-yellow/puYear=*/puMonth=*/*.parquet',
        FORMAT='PARQUET',
        DATA_SOURCE='davewdemolake'
    ) AS result


-------------------------------------------------------------------------------------------------------------
----------------------------Analytics------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

--let's look at one decade of data
--data summarized at the Year level
--this may take a minute to run
SELECT
    YEAR(tpepPickupDateTime) AS current_year,
    COUNT(*) AS rides_per_year
FROM
    OPENROWSET(
        BULK 'gold/nyctlc-yellow/puYear=*/puMonth=*/*.parquet',
        FORMAT='PARQUET',
        DATA_SOURCE='davewdemolake'
    ) AS [nyc]
WHERE nyc.filepath(1) >= '2010' AND nyc.filepath(1) <= '2019'
GROUP BY YEAR(tpepPickupDateTime)
ORDER BY 1 ASC

/*
    now switch to chart view to visualize the data
    the default should be Chart type=Line, Category=None

    note that yellow cab rides are precipitously dropping
    this should make sense given the popularity of Uber and Lyft
*/


/* 

## CETAS Pattern for EDA

These queries run pretty fast, considering they are against a remote data lake.  Sometimes 
the queries are _slow_ and it may make sense to _materialize_ data and queries that we know
we are going to do frequent analytics against.  

Let's assume the "decade data query" above is something we are going to do a lot of analytics against.
Let's materialize that data in our local datalake/sandbox using the CETAS pattern

*/ 
--drop external table with data isn't supported
CREATE EXTERNAL TABLE taxi_2010_decade
WITH (
    --adjust your pathing accordingly
    --this will write to YOUR sandbox datalake in Synapse
    DATA_SOURCE = sandbox,
    LOCATION = 'taxi_2010s_decade/',
    FILE_FORMAT = ParquetFF
) 
AS
--original query
SELECT
    * 
FROM
    OPENROWSET(
        BULK 'gold/nyctlc-yellow/puYear=*/puMonth=*/*.parquet',
        FORMAT='PARQUET',
        DATA_SOURCE='davewdemolake'
    ) AS [nyc]
WHERE nyc.filepath(1) >= '2010' AND nyc.filepath(1) <= '2019';

/*
## is there seasonality to the data? 

let's just look at a single year (2016) and aggregate by DAY
again, graph the data
    change it to a column chart, category=current_day

we can use our materialized data in our sandbox INSTEAD OF the remote data lake, 
which might make queries a little faster.  
*/

SELECT
    CAST([tpepPickupDateTime] AS DATE) AS [current_day],
    COUNT(*) as rides_per_day
--now I can simplify the syntax by using the EXTERNAL table on the
--FROM clause vs the OPENROWSET
FROM taxi_2010_decade
WHERE CAST([tpepPickupDateTime] AS DATE) BETWEEN '2016-01-01' AND '2017-01-01'
GROUP BY CAST([tpepPickupDateTime] AS DATE)
ORDER BY 1 ASC

/*
    We decide that last query for 2016 taxi rides is something we will use often, so,
    let's materialize that too
*/
--drop external table taxi_2016_by_day
CREATE EXTERNAL TABLE taxi_2016_by_day
WITH (
    --adjust your pathing accordingly
    --this will write to YOUR sandbox datalake in Synapse
    DATA_SOURCE = sandbox,
    LOCATION = 'taxi_2016_by_day/',
    FILE_FORMAT = ParquetFF
) 
AS
--same query, no changes
SELECT
    CAST([tpepPickupDateTime] AS DATE) AS [current_day],
    COUNT(*) as rides_per_day
FROM taxi_2010_decade
WHERE CAST([tpepPickupDateTime] AS DATE) BETWEEN '2016-01-01' AND '2017-01-01'
GROUP BY CAST([tpepPickupDateTime] AS DATE)
ORDER BY 1 ASC


SELECT * 
from taxi_2016_by_day
ORDER BY 1 ASC;
;

/*
Interpretation:
  * there are fewer rides in the summer
  * at a weekly level it looks like Saturday is the peak day (we should probably confirm that though)
  * there are some significant drops that don't fit a seasonality pattern.  Could this be holidays?  Let's check

  Holidays are available as a public dataset that you can connect to
*/
CREATE VIEW holidays
AS 
SELECT
    holidayName,
    date
FROM
    OPENROWSET(
        BULK 'https://azureopendatastorage.blob.core.windows.net/holidaydatacontainer/Processed/*.parquet',
        FORMAT='PARQUET'
    ) AS [holidays]
WHERE countryOrRegion = 'United States' AND YEAR(date) = 2016

--map the holidays to our dataset
SELECT  t.current_day, 
    t.rides_per_day, 
    h.holidayName,
    CASE WHEN h.holidayName IS NOT NULL THEN 1 ELSE 0 END AS IsHoliday
FROM taxi_2016_by_day t
LEFT JOIN holidays h 
    ON t.current_day = h.date
ORDER BY t.current_day ASC

/*
    if we chart this it kinda seems like the drop offs do roughy align to holidays.  
    we would want to confirm this better, but it's good enough for now.  

    What we do see is that Jan 23 has a HUGE drop off and it isn't a holiday.  
    Could it be weather?  

    Well, it turns out we can get weather data for free from another public dataset.
*/

SELECT
    AVG(windSpeed) AS avg_windspeed,
    MIN(windSpeed) AS min_windspeed,
    MAX(windSpeed) AS max_windspeed,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    AVG(precipDepth) AS avg_precipdepth,
    MIN(precipDepth) AS min_precipdepth,
    MAX(precipDepth) AS max_precipdepth,
    AVG(snowDepth) AS avg_snowdepth,
    MIN(snowDepth) AS min_snowdepth,
    MAX(snowDepth) AS max_snowdepth
    --select top 10 * 
FROM
    OPENROWSET(
        BULK 'https://azureopendatastorage.blob.core.windows.net/isdweatherdatacontainer/ISDWeather/year=*/month=*/*.parquet',
        FORMAT='PARQUET'
    ) AS [weather]
WHERE countryOrRegion = 'US' 
AND year = 2016
AND CAST([datetime] AS DATE) = '2016-01-23' 
--let's find the nearest weatherstation to NYC
AND stationName = 'JOHN F KENNEDY INTERNATIONAL AIRPORT'


/*

Interpretation:

Taxi rides probaby dropped on 1/23/2016 due to:

* heavy snow (29 cm)
* cold (-1C)

*/

