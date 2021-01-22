###########################################################
## This file is part of the BrainGenix Simulation System ##
###########################################################

import threading
import time

'''
Name: ZKCLI
Description: This file runs the actual CLI used by BG.
Date-Created: 2021-01-19
'''

class ConnectionInstance(): # This class is instantiated every time a user connects to the CLI #

    '''
    This class handles CLI connection instances.
    It's called by ZKCLI class and handles one specific instance of a connection.

    We'll need to add end-to-end encryption support later, but for now everything is done in plain text.
    Also adding ACL so the client can only interact with the zNode for it's own connection would be a good idea.
    '''

    def __init__(self, Logger:object, ZKInstance:object, zNodeLocation:str, LeaderPluginRegistry:dict, ModuleRegistry:dict):

        '''
        This function creates a local copy of pointers needed later on in the class, such as the logger.
        *Please don't use this unless you know what you're doing!*
        '''

        # Create Local Pointers #
        self.Logger = Logger
        self.ZK = ZKInstance
        self.zNodePath = zNodeLocation
        self.LeaderPluginRegistry = LeaderPluginRegistry
        self.ModuleRegistry = ModuleRegistry

        # Start Main Loop #
        self.MainThread()
        


    def MainThread(self, PollingInterval=0.05): # Main Thread That Runs The Connection #

        '''
        This function contains a loop which is used for every connection.
        First, it handles authentication, and will check this with the user database.
        Next, it goes into interactive mode, which is just a loop containing the actual commands.
        If the user fails an authentication check, the connection is dropped.
        *Please don't use this unless you know what you're doing!*
        '''

        # Authenticate #

        while self.ZK.ZookeeperConnection.get(self.zNodePath)[0] == b'':
            pass

        AuthInfo = self.ZK.ZookeeperConnection.get(self.zNodePath)[0]
        Username, Password = AuthInfo.decode().split('\n')

        if ((Username == 'tliao') and (Password == '123456')):
            self.Logger.Log(f'Authentication Completed For User {Username}')
            pass
        else:
            self.Logger.Log(f'Client Failed Authentication With Uname {Username}')
            return

        while True:
            pass


class ZKCLI(): # This class handles creating/destroying Connection Instances based on connections #

    '''
    This class handles the creation and destruction of connection instances.
    It's passed the location of the CLI zNode and it checks for new children underneath it.
    These children are connection instances.
    If a new connection is established, this class will create a new thread with a connection instance to handle it.
    If this node is demoted to follower mode from leader mode, it'll stop all the threads which handle connection instances.
    This is to avoid any issues with two systems handling the CLI at the same time.
    '''


    def __init__(self, Logger:object, ZKInstance:object, LeaderPluginRegistry:dict, ModuleRegistry:dict, zNodeRoot:str='/BrainGenix/CLI'):

        '''
        This function initializes the zkcli handler.
        It creates local copies of the pointers needed by the rest of this class.
        *Please don't use this unless you know what you're doing!*
        '''

        # Create Local Pointers #
        self.Logger = Logger
        self.ZK = ZKInstance
        self.zNodeRoot = zNodeRoot
        self.LeaderPluginRegistry = LeaderPluginRegistry
        self.ModuleRegistry = ModuleRegistry        

        # Create Local Vars #
        self.HandledConnections = []
        self.ConnectionInstances = []

        self.Logger.Log('ZKCLI Init Completed')


    def StartPollingThread(self): # Starts a thread that checks if new connections have been established #

        '''
        This function starts the polling thread.
        It creates a threading.Thread, and then calls thread.start()
        *Please don't use this unless you know what you're doing!*
        '''

        # Spawn Thread #
        self.PollerThread = threading.Thread(target=self.PollingFunction, name='CLI Polling Thread').start()

        self.Logger.Log('Started ZKCLI Polling Thread')


    def PollingFunction(self, PollingFrequency:int=1): # Polls the ZK CLI Root for any connections, and spawns new instances to handle it #

        '''
        This function contains the polling function, and is the target of the thread starting function.
        This function should not be called because it contains a loop which will never return.
        *Please don't use this unless you know what you're doing!*
        '''

        while True:

            if self.ZK.ZookeeperMode == 'Leader':            

                # Grab A List Of Connection Instances #
                ConnectionList = self.ZK.ZookeeperConnection.get_children(self.zNodeRoot)

                # Check If It's Already Handled #
                for Connection in ConnectionList:
                    
                    if Connection not in self.HandledConnections:
                        self.SpawnConnectionInstance(Connection)
                        self.Logger.Log(f'ZKCLI Started Connection Handler For Session {Connection}')

            # Delay For The Polling Time #
            time.sleep(PollingFrequency)


    def SpawnConnectionInstance(self, ConnectionName): # Creates A New Connection Instance #

        '''
        This function is used by the polling function to instantiate a new thread each time a new connection is detected.
        *Please don't use this unless you know what you're doing!*
        '''

        # Spawn Thread #
        ConnectionLocation = self.zNodeRoot + '/' + ConnectionName
        NewInstance = threading.Thread(target=ConnectionInstance, args=(self.Logger, self.ZK, ConnectionLocation, self.LeaderPluginRegistry, self.ModuleRegistry, ), name=f'ZK CLI Connection Handler On Connection {ConnectionName}')
        NewInstance.start()
        self.ConnectionInstances.append(NewInstance)
        self.HandledConnections.append(ConnectionName)