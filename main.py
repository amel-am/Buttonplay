import disnake
from colorama import Fore
from loguru import logger
from disnake.ext import commands
from src.commands import Control
from src.errors import Error
from src.yaml import prefix, token, status, guild, connect

bot = commands.Bot(command_sync_flags=commands.CommandSyncFlags.default(), test_guilds=guild,
                   command_prefix=prefix, help_command=None, activity=disnake.Game(status), intents=disnake.Intents.all())


@bot.event
async def on_ready():
    await connect.send("screenOn")
    channel_count = 0
    member_count = 0
    for guild in bot.guilds:
        channel_count += len(guild.channels)
        member_count += len(guild.members)
    print(f"Logged into {bot.user}")
    print(f'''{Fore.GREEN}

         88888888ba                                                                 88                                                     88                   88           
         88      "8b               ,d      ,d                                       88                                                     ""   ,d              88           
         88      ,8P               88      88                                       88                                                          88              88           
         88aaaaaa8P' 88       88 MM88MMM MM88MMM ,adPPYba,  8b,dPPYba,  8b,dPPYba,  88 ,adPPYYba, 8b       d8 ,adPPYba, 8b      db      d8 88 MM88MMM ,adPPYba, 88,dPPYba,   
         88""""""8b, 88       88   88      88   a8"     "8a 88P'   `"8a 88P'    "8a 88 ""     `Y8 `8b     d8' I8[    "" `8b    d88b    d8' 88   88   a8"     "" 88P'    "8a  
         88      `8b 88       88   88      88   8b       d8 88       88 88       d8 88 ,adPPPPP88  `8b   d8'   `"Y8ba,   `8b  d8'`8b  d8'  88   88   8b         88       88  
         88      a8P "8a,   ,a88   88,     88,  "8a,   ,a8" 88       88 88b,   ,a8" 88 88,    ,88   `8b,d8'   aa    ]8I   `8bd8'  `8bd8'   88   88,  "8a,   ,aa 88       88  
         88888888P"   `"YbbdP'Y8   "Y888   "Y888 `"YbbdP"'  88       88 88`YbbdP"'  88 `"8bbdP"Y8     Y88'    `"YbbdP"'     YP      YP     88   "Y888 `"Ybbd8"' 88       88  
                                                                        88                            d8'                                                                    
                                                                        88                           d8'                                                                     
        {Fore.WHITE}-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                    {Fore.LIGHTYELLOW_EX}Bot Owner: {Fore.LIGHTYELLOW_EX}{bot.owner}                         
                                    {Fore.LIGHTYELLOW_EX}Connected as: {Fore.LIGHTYELLOW_EX}{bot.user}
                                    {Fore.LIGHTYELLOW_EX}Guild Count: {Fore.LIGHTYELLOW_EX}{len(bot.guilds)}
                                    {Fore.LIGHTYELLOW_EX}Channel Count: {Fore.LIGHTYELLOW_EX}{channel_count}
                                    {Fore.LIGHTYELLOW_EX}Member Count: {Fore.LIGHTYELLOW_EX}{member_count}
                                    {Fore.LIGHTYELLOW_EX}Prefix: {Fore.LIGHTYELLOW_EX}{(bot.command_prefix)}
        {Fore.WHITE}-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

''')

if __name__ == "__main__":
    try:
        bot.add_cog(Control(bot))
        bot.add_cog(Error())
        logger.success("All cogs have been added successfully")
    except Exception as e:
        logger.error(f"An error occured: {e}")
    bot.run(token)
