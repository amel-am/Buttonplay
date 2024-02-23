from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from src.buttons import SwitchButtons
from src.yaml import connect, url
from src.helper_funcs import create_embed


class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.slash_command(name="buttonplayswitch", description="Buttonplay", dm_permission=True)
    async def button_play(self, interaction: ApplicationCommandInteraction):
        switch_buttons = SwitchButtons()
        embed = await create_embed()
        if url:
            await interaction.response.send_message(content=f"***Battery: {await connect.receive('charge')}%***\n***Button that has been clicked: None***\n {url}", view=switch_buttons)
        else:
            await interaction.response.send_message(embed=embed, view=switch_buttons)

    @commands.is_owner()
    @commands.slash_command()
    async def quit(self, interaction: ApplicationCommandInteraction):
        await connect.send("detachController")
        await interaction.response.send_message("until next time!")
        await self.bot.close()
