import nextcord
from nextcord.ext import commands, tasks

import socket

from ....utils.enums.IntervalUnits import IntervalUnits

from ..._tasks.Task import Task

from ....utils.enums.ChannelTypes import ChannelTypes

from ....database.models.srvm_tables.Server import Server
from ....database.models.srvm_tables.DistantServer import DistantServer
from ....database.models.srvm_tables.Channel import Channel

class CheckDistantServerActivity(Task):
    """ # CheckDistantServerActivity task class
    
    Description :
    ---
        Manage the CheckDistantServerActivity task discord task
        
    Access :
    ---
        src.bots.server_manager.srvm_tasks.CheckDistantServerActivity.py\n
        CheckDistantServerActivity
    
    inheritance :
    ---
        - task : :class:`task` => Parent class of all tasks
    """
    def __init__(self, guild: nextcord.Guild):
        """ # CheckDistantServerActivity constructor
        
        Description :
        ---
            Construct a CheckDistantServerActivity object
        
        Access :
        ---
            src.bots.server_manager.srvm_tasks.CheckDistantServerActivity.py\n
            CheckDistantServerActivity.__init__()
        
        Returns :
        ---
            :class:`None`
        """
        self.guild = guild
        self.embed = nextcord.Embed(title="Servers Activity")
        self.distant_servers = {}
        super().__init__()

    def start(self):
        """ # CheckDistantServerActivity task start method
        
        Description :
        ---
            Start the CheckDistantServerActivity task
        
        Access :
        ---
            src.bots.server_manager.srvm_tasks.CheckDistantServerActivity.py\n
            CheckDistantServerActivity.start()
            
        Returns :
        ---
            :class:`None`
        """
        self.execute.start()

    def stop(self):
        """ # CheckDistantServerActivity task stop method
        
        Description :
        ---
            Stop the CheckDistantServerActivity task
        
        Access :
        ---
            src.bots.server_manager.srvm_tasks.CheckDistantServerActivity.py\n
            CheckDistantServerActivity.stop()
            
        Returns :
        ---
            :class:`None`
        """
        self.execute.cancel()

    def change_interval(self, interval_unit: IntervalUnits, interval_time: int):
        """ # CheckDistantServerActivity task change_interval method
        
        Description :
        ---
            Change the interval of the CheckDistantServerActivity task
        
        Access :
        ---
            src.bots.server_manager.srvm_tasks.CheckDistantServerActivity.py\n
            CheckDistantServerActivity.change_interval()
            
        Parameters :
        ---
            minutes : :class:`int` => The new interval in minutes
            
        Returns :
        ---
            :class:`None`
        """
        match interval_unit:
            case IntervalUnits.SECONDS.value:
                self.execute.change_interval(seconds=interval_time)
            case IntervalUnits.MINUTES.value:
                self.execute.change_interval(minutes=interval_time)
            case IntervalUnits.HOURS.value:
                self.execute.change_interval(hours=interval_time)
    
    @tasks.loop(minutes=1)
    async def execute(self):
        """ # CheckDistantServerActivity task execute method
        
        Description :
        ---
            Execute the CheckDistantServerActivity task
            
        Access :
        ---
            src.bots.server_manager.srvm_tasks.CheckDistantServerActivity.py\n
            CheckDistantServerActivity.execute()
            
        Returns :
        ---
            :class:`None`
        """
        # Get the server id
        server_id_result = await Server.get_server_id_by_guild_id(self.guild.id)
        print("test")
        # Check if the server exists
        if not server_id_result.get("value") or not server_id_result.get("passed"):
            return 
        
        # Get the server special channel
        special_channel_result = await Channel.get_channel_by_guild_id_and_type_id(self.guild.id, ChannelTypes.SERVER.value)

        # Check if the special channel exists
        if not special_channel_result.get("object") or not special_channel_result.get("passed"):
            return
        
        # Get the distant servers
        distant_servers_result = await DistantServer.get_distant_servers_by_server_id(server_id_result.get("value"))

        # Check if the distant servers exists
        if not distant_servers_result.get("objects") or not distant_servers_result.get("passed"):
            return
        
        def isOpen(adress: str, port: int = 8080):
            """ # isOpen function
            
            Description :
            ---
                Check if the distant server is open
                
            Access :
            ---
                src.bots.server_manager.srvm_tasks.CheckDistantServerActivity.py\n
                CheckDistantServerActivity.execute() -> isOpen()

            Parameters :
            ---
                adress : :class:`str` => The adress of the distant server
                port : :class:`int` => The port of the distant server
                
            Returns :
            ---
                :class:`bool`
            """
            # Create a socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Try to connect to the distant server
            try:
                s.connect((adress, int(port)))
                s.shutdown(2)
                return True
            except:
                return False

        # Reset the list of distant servers
        distant_servers_changes = {}
        self.embed.clear_fields()

        # Loop through the distant servers
        for distant_server in distant_servers_result.get("objects"):
            # Get the distant server full name
            distant_server_full_name = f"{distant_server.adress}:{str(distant_server.port)}"

            # Check if the distant server is open
            if isOpen(distant_server.adress, distant_server.port):
                distant_servers_changes[distant_server_full_name] = True
                self.embed.add_field(name=distant_server_full_name, value="Online", inline=False)
            else:
                distant_servers_changes[distant_server_full_name] = False
                self.embed.add_field(name=distant_server_full_name, value="Offline", inline=False)

        # Check if the distant servers have changed
        if self.distant_servers != distant_servers_changes:
            self.distant_servers = distant_servers_changes
            await self.guild.get_channel(special_channel_result.get("object").channelID).send(embed=self.embed)

            


