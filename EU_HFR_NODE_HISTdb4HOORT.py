#!/usr/bin/python3


# Created on Tue Nov 8 12:32:57 2022

# @author: Lorenzo Corgnati
# e-mail: lorenzo.corgnati@sp.ismar.cnr.it


# This application runs the EU_HFR_NODE_NRTprocessor_NRTdb4HOORT.py application
# for all the registration dates from the input one to present for populating
# the radial_delay_tb table of the EU HFR NODE database with historical information.

# These information are used by the API of the EU HFR NODE HF radar Online Outage
# Reporting Tool (HOORT) for gathering the history of "last_data_available" and 
# "radial_ delay" values for all radial sites and running the delay KPPI.

# When calling the application, the first registration date from which starting
#the evluation must be specified.

import sys
import getopt
import logging
import datetime as dt
import math
import EU_HFR_NODE_NRTdb4HOORT

####################
# MAIN DEFINITION
####################

def main(argv):
    
#####
# Setup
#####
       
    # Set the argument structure
    try:
        opts, args = getopt.getopt(argv,"s:h",["start-registration-date=","help"])
    except getopt.GetoptError:
        print("Usage: EU_HFR_NODE_HISTdb4HOORT.py -s <start-registration date formatted as yyyy-mm-ddTHH:00:00Z (ISO8601 UTC combined date-time representation at o'clock hour)>")
        sys.exit(2)
        
    if not argv:
        print("No start registration date specified. Please type 'EU_HFR_NODE_HISTdb4HOORT.py -h' for help.")
        sys.exit(2)
            
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: EU_HFR_NODE_HISTdb4HOORT.py -s <start-registration date formatted as yyyy-mm-ddTHH:00:00Z (ISO8601 UTC combined date-time representation at o'clock hour)>")
            sys.exit()
        elif opt in ("-s", "--start-registration-date"):
            # Check date format and round to o'clock hour if needed
            try:
                dateCheck = dt.datetime.strptime(arg, '%Y-%m-%dT%H:%M:%SZ')
                startRegDate = dt.datetime.strftime(dateCheck, "%Y-%m-%d %H:00:00")
            except ValueError:
                print("Incorrect date format, should be yyyy-mm-ddTHH:00:00Z (i.e. ISO8601 UTC combined date-time representation at o'clock hour')")
                sys.exit(2)
                
    # Create logger
    logger = logging.getLogger('EU_HFR_NODE_HIST_db4HOORT')
    logger.setLevel(logging.INFO)
    # Create console handler and set level to DEBUG
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # Create logfile handler
    lfh = logging.FileHandler('/var/log/EU_HFR_NODE_NRT/EU_HFR_NODE_HIST_db4HOORT.log')
    lfh.setLevel(logging.INFO)
    # Create formatter
    formatter = logging.Formatter('[%(asctime)s] -- %(levelname)s -- %(module)s - %(message)s', datefmt = '%d-%m-%Y %H:%M:%S')
    # Add formatter to lfh and ch
    lfh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # Add lfh and ch to logger
    logger.addHandler(lfh)
    logger.addHandler(ch)
    
    # Initialize error flag
    EHNerr = False
    
    logger.info('Processing started.')
    
#####
# Create list of all o'clock hours from start registration date to end registration date
#####

    # Convert start registration date string to datetime object
    startRegDatetime = dt.datetime.strptime(startRegDate, '%Y-%m-%d %H:%M:%S')
    
    # Get interval between start registration date and current time as timedelta object
    timeDiff = dt.datetime.now() - startRegDatetime
    # Convert interval to hours
    timeDiffHours = math.floor(timeDiff.total_seconds() / 3600)
    
    # Create the list of registration dates as strings
    allDatetimes = [startRegDatetime+dt.timedelta(hours=hh) for hh in range(timeDiffHours)]
    allDates = [date_obj.strftime('%Y-%m-%dT%H:00:00Z') for date_obj in allDatetimes]
    
#####
# Run the application EU_HFR_NODE_NRTdb4HOORT.py for all the listed registration dates
#####

    for rd in allDates:
        logger.info('Processing registration date ' + rd)
        EU_HFR_NODE_NRTdb4HOORT.main(['-r', rd])
    
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
    
    