#!/usr/bin/python3


# Created on Sun Nov 6 15:32:31 2022

# @author: Lorenzo Corgnati
# e-mail: lorenzo.corgnati@sp.ismar.cnr.it


# This application retrieves the last radial available file and evaluates the 
# radial delay for all the HFR systems connected to the NRT processing of the 
# EU HFR NODE and inserts them in the radial_delay_tb of the EU HFR NODE database.

# These information are used by the API of the EU HFR NODE HF radar Online Outage
# Reporting Tool (HOORT).

# When calling the application it is possible to specify the registration date for 
# the retrieval of the last radial available file and for the evaluation of the 
# radial delay.
# If no input is specified, the current time rounded at o'clock hour is used as
# registration date.

import sys
import getopt
import logging
import datetime as dt
import pandas as pd
import sqlalchemy

####################
# MAIN DEFINITION
####################

def main(argv):
    
#####
# Setup
#####
       
    # Set the argument structure
    try:
        opts, args = getopt.getopt(argv,"r:h",["registration-date=","help"])
    except getopt.GetoptError:
        print("Usage: EU_HFR_NODE_NRTdb4HOORT.py -r <registration date formatted as yyyy-mm-ddTHH:00:00Z (ISO8601 UTC combined date-time representation, default to current time rounded at o'clock hour)>")
        sys.exit(2)
        
    if not argv:
        regDate = dt.datetime.now().strftime("%Y-%m-%d %H:00:00")
            
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: EU_HFR_NODE_NRTdb4HOORT.py -r <registration date formatted as yyyy-mm-ddTHH:00:00Z (ISO8601 UTC combined date-time representation, default to current time rounded at o'clock hour)>")
            sys.exit()
        elif opt in ("-r", "--registration-date"):
            # Check date format and round to o'clock hour if needed
            try:
                dateCheck = dt.datetime.strptime(arg, '%Y-%m-%dT%H:%M:%SZ')
                regDate = dt.datetime.strftime(dateCheck, "%Y-%m-%d %H:00:00")
            except ValueError:
                print("Incorrect date format, should be yyyy-mm-ddTHH:00:00Z (i.e. ISO8601 UTC combined date-time representation at o'clock hour')")
                sys.exit(2)
                
    # Set execution date
    execDate = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          
    # Create logger
    logger = logging.getLogger('EU_HFR_NODE_NRT_db4HOORT')
    logger.setLevel(logging.INFO)
    # Create console handler and set level to DEBUG
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # Create logfile handler
    lfh = logging.FileHandler('/var/log/EU_HFR_NODE_NRT/EU_HFR_NODE_NRT_db4HOORT.log')
    lfh.setLevel(logging.INFO)
    # Create formatter
    formatter = logging.Formatter('[%(asctime)s] -- %(levelname)s -- %(module)s - %(message)s', datefmt = '%d-%m-%Y %H:%M:%S')
    # Add formatter to lfh and ch
    lfh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # Add lfh and ch to logger
    logger.addHandler(lfh)
    logger.addHandler(ch)
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!TO BE COMMENTED FOR OPERATIONS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Set parameter for Mysql database connection
    sqlConfig = {
      'user': 'HFRuserCP',
      'password': '!_kRIVAHYH2RLpmQxz_!',
      'host': '150.145.136.108',
      'database': 'HFR_node_db',
    }
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!TO BE UNCOMMENTED FOR OPERATIONS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # sqlConfig = {
    #   'user': 'HFRuserHOORT',
    #   'password': '!_Wga4JNtb8tCGyX]9_!',
    #   'host': 'localhost',
    #   'database': 'HFR_node_db',
    # }
    
    # Initialize error flag
    EHNerr = False
    
    logger.info('Processing started.')
    
#####
# last_data_available and radial_delay retrieval
#####
    
    # Create SQLAlchemy engine for connecting to database
    eng = sqlalchemy.create_engine('mysql+mysqlconnector://' + sqlConfig['user'] + ':' + \
                                   sqlConfig['password'] + '@' + sqlConfig['host'] + '/' + \
                                   sqlConfig['database'])
    
    try:
        # Set and execute the query for retrieving sttion_id, last_data_available and radial_delay
        radialInputSelectQuery = "SELECT station_id, MAX(datetime) as last_data_available, " \
                                 "TIMESTAMPDIFF(HOUR, '" + regDate + "', MAX(datetime)) AS " \
                                 "radial_delay FROM radial_input_tb WHERE datetime <= '" \
                                 + regDate + "' GROUP BY station_id"                   
        delayData = pd.read_sql(radialInputSelectQuery, con=eng)
        # Add registration_date and creation_date to the dataframe
        if not delayData.empty:
            delayData.loc[:,'registration_date'] = regDate
            delayData.loc[:,'creation_date'] = execDate
            
            # Write the dataframe to the radial_delay_tb table
            delayData.to_sql('radial_delay_tb', con=eng, if_exists='append', index=False, index_label=delayData.columns)
                    
            logger.info('radial_delay_tb table succesfully updated for registration date ' + regDate)
        
    except sqlalchemy.exc.DBAPIError as err:        
        EHNerr = True
        logger.error('MySQL error ' + err._message())
        logger.info('Exited with errors.')
        sys.exit()
    
####################
    
    if(not EHNerr):
        logger.info('Successfully executed.')
    else:
        logger.info('Exited with errors.')
            
####################


#####################################
# SCRIPT LAUNCHER
#####################################    
    
if __name__ == '__main__':
    main(sys.argv[1:])
    
    