###########################################################
## This file is part of the BrainGenix Simulation System ##
###########################################################

import datetime
import time
import pymysql
import threading

## @package LogDeletionSystem
# Name: LogAutoDeletionSystem
# Description: The LogAutodeletionSystem automatically purges logs that are older than the defined retention period (see config.yaml).
# Date-Created: 2021-07-15

# Create Class To Hold Log Auto Deletion System
class LogAutoDeletionSystem():

    ## Initialize The System
    #@param Logger Logger object
    #@param ControlQueue Control Queue object
    #@param SystemConfiguration System Configuration Dictionary
    #@param PollingInterval Polling Interval (default=5)
    def __init__(self, Logger:object, ControlQueue: object, SystemConfiguration:dict, PollingInterval:int=5): 

        ## Create Local Variables
        self.Logger = Logger
        self.ControlQueue = ControlQueue
        self.SystemConfiguration = SystemConfiguration
        self.PollingInterval = PollingInterval

        ## Log Init Start
        self.Logger.Log('Initializing Log AutoDeletion Thread', 3)

        ## Create Thread Object
        self.Logger.Log('Creating Log Auto Deletion System Daemon Thread', 2)
        self.UpdateThread = threading.Thread(
            target=self.DeleteLogThread,
            args=(),
            name='Log Auto Deletion System'
        )
        self.Logger.Log('Created Log Auto Deletion System Daemon Thread', 1)

        self.Logger.Log('Starting Log Auto Deletion System Daemon Thread', 2)
        self.UpdateThread.start()
        self.Logger.Log('Started Log Auto Deletion System Daemon Thread', 1)

    ## Thread Target That Deletes Old Logs
    def DeleteLogThread(self):

        ## Log Initialization
        self.Logger.Log('Log Deletion Thread Created')

        ## Get Seconds To Keep Logs
        self.SecondsToKeepLogs = self.SystemConfiguration['SecondsToKeepLogs']

        ## Connect To MySQL Server
        self.Logger.Log('Reading Log Auto Deletion System AutoDeletion Configuration Parameters From Local Configuration File', 2)
        DBUsername = str(self.SystemConfiguration.get('DatabaseUsername'))
        DBPassword = str(self.SystemConfiguration.get('DatabasePassword'))
        DBHost = str(self.SystemConfiguration.get('DatabaseHost'))
        DBDatabaseName = str(self.SystemConfiguration.get('DatabaseName'))
        self.Logger.Log('Read Log Auto Deletion System Configuration Parameters', 1)


        ## Connect To DB Server
        self.Logger.Log('Creating Log Auto Deletion System PymySQL Instance, Connecting To Database Server', 2)
        self.DatabaseConnection = pymysql.connect(
            host = DBHost,
            user = DBUsername,
            password = DBPassword,
            db = DBDatabaseName
        )
        self.Logger.Log('Created Log Auto Deletion System PymySQL Instance', 1)

        ## Create Database Cursor
        self.Logger.Log('Creating Log Auto Deletion System Daemon Cursor', 2)
        self.LoggerCursor = self.DatabaseConnection.cursor()
        self.Logger.Log('Created Log Auto Deletion System Cursor', 1)

        ## Enter Polling Loop
        while self.ControlQueue.empty():


            ## Calculate Old Date (Current Date Minus KeepSeconds)
            DeleteDateRaw = datetime.datetime.now() - datetime.timedelta(seconds=self.SecondsToKeepLogs)
            DeleteDate = DeleteDateRaw.strftime('%Y-%m-%d %H:%M:%S')
            DeleteDate = DeleteDate

            ## Delete Old Logs
            # DeleteStatement= ("DELETE FROM log WHERE LogDatetime < %s" % str(DeleteDate))
            # self.LoggerCursor.execute(DeleteStatement) ## FIXME, SQL SYNTAX ERROR


            ## Delay For Set Polling Interval 
            time.sleep(self.PollingInterval)


        ## Shutdown Thread
        self.Logger.Log('Shutting Down Log Auto Deletion System Daemon', 4)

        self.Logger.Log('Committing Outstanding Cursor Queries', 2)
        self.DatabaseConnection.commit()
        self.Logger.Log('Committed Oustanding Queries', 1)

        self.Logger.Log('Closing Log AutoDeletion System MySQL Instance', 2)
        self.DatabaseConnection.close()
        self.Logger.Log('Closed Log AutoDeletion System Connection', 1)

        self.Logger.Log('Log AutoDeletion System UnInit Completed', 3)
