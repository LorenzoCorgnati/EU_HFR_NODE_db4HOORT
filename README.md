# EU_HFR_NODE_db4HOORT
Python3 scripts for feeding the European HFR Node (EU HFR Node) database for the HFR Online Outage Reporting Tool (HOORT). Tools to be run at the EU HFR Node.

These applications are written in Python3 language and are based on a MySQL database containing information about data and metadata. The applications are designed for High Frequency Radar (HFR) data management according to the European HFR node processing workflow, thus feeding the database with information about last available data and radial delay from each HFR system connected to the Node.
The radial delay is defined as the difference in hours between the run time rounded at o'clock hour (i.e. the registration date) and the datetime of the last radial data available from each HFR station.

The database is composed by the following tables:
- account_tb: it contains the general information about HFR providers and the HFR networks they manage.
- network_tb: it contains the general information about the HFR network producing the radial and total files. These information will be used for the metadata content of the netCDF files.
- station_tb: it contains the general information about the radar sites belonging to each HFR network producing the radial files. These information will be used for the metadata content of the netCDF files.
- radial_input_tb: it contains information about the radial files to be converted and combined into total files.
- radial_HFRnetCDF_tb: it contains information about the converted radial files.
- total_input_tb: it contains information about the total files to be converted.
- total_HFRnetCDF_tb: it contains information about the combined and converted total files.
- radial_delay_tb: it contains information about the last available data and radial delay from each HFR system.

These applications update the radial_delay_tb table of the database, that contains the following fields:
- registration_date: date and time (in UTC) of the programmed execution of the application. It is recommended to run the application on hourly basis at o'clock time.
- station_id: ID of the HFR station.
- last_data_available: date and time (in UTC) of the last available radial file received from each HFR station (ie. time of the last measurement).
- radial_delay: time interval (in hours) between registration_date and last_data_available.
- creation_date: date and time (in UTC) of the effective run of the script launched via the cron-hourly.

The application EU_HFR_NODE_NRTdb4HOORT.py has to be run on hourly basis at o'clock time and it is launched via the cron.hourly scheduler. When calling the application it is possible to specify the registration date for the retrieval of the last radial available time and for the evaluation of the radial delay. If no input is specified, the current time rounded at o'clock hour is used as
registration date. When programmed in the cron.hourly scheduler, the application fills the radial_delay_tb table based on the current time (i.e. no input is specified). 

The application EU_HFR_NODE_HISTdb4HOORT.py takes as input a starting registration date, creates a list of all o'clock hours from start registration date to the current date and runs the application EU_HFR_NODE_NRTdb4HOORT.py for all the listed registration dates.

These information are used by the API of the EU HFR NODE HF radar Online Outage Reporting Tool (HOORT).

General information for the tables network_tb and station_tb are loaded onto the database via a webform to be filled by the data providers. The webform is available at https://webform.hfrnode.eu

Usage: EU_HFR_NODE_NRTdb4HOORT.py [-r registration date formatted as yyyy-mm-ddTHH:00:00Z (ISO8601 UTC combined date-time representation, default to current time rounded at o'clock hour)]

Usage: EU_HFR_NODE_HISTdb4HOORT.py -s <start-registration date formatted as yyyy-mm-ddTHH:00:00Z (ISO8601 UTC combined date-time representation at o'clock hour)>

The required packages are:
- pandas
- sqlalchemy
- mysql-connector-python

The guidelines on how to synchronize the providers' HFR radial and total data towards the EU HFR Node are available at ​https://doi.org/10.25704/9XPF-76G7
How to cite:
- when using these guidelines, ​please use the following citation carefully and correctly​:
Reyes, E., Rotllán, P., Rubio, A., Corgnati, L., Mader, J., & Mantovani, C. (2019).
Guidelines on how to sync your High Frequency (HF) radar data with the European HF
Radar node (Version 1.1). Balearic Islands Coastal Observing and Forecasting System,
SOCIB . https://doi.org/10.25704/9XPF-76G7

Cite as:
Lorenzo Corgnati. (2022). EU_HFR_NODE_db4HOORT. Zenodo DOI to be assigned.


Author: Lorenzo Corgnati

Date: November 15, 2022

E-mail: lorenzo.corgnati@sp.ismar.cnr.it
