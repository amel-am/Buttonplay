import disnake
import asyncio
from io import BytesIO
from src.yaml import connect, url


async def edit_embed(button: disnake.ui.Button, interaction: disnake.MessageInteraction,  view: disnake.ui.View, followup: bool = False):
    if url:
        content = f"***Battery: {await connect.receive('charge')}%***\n***Button that was clicked previously: {button.label}***\n{url}"
        embed = None
    else:
        content = None
        embed = await create_embed(button)

    if followup:
        await interaction.edit_original_message(content=content, embed=embed, view=view)
    else:
        await interaction.response.edit_message(content=content, embed=embed, view=view)


async def create_embed(button: disnake.ui.Button = None):
    await connect.send("configure printDebugResultCodes 1")
    if button:
        embed = disnake.Embed(title=f"General info about your switch",
                              description=f"Button that was clicked previously: {button.label}", colour=disnake.Colour.random())

    else:
        embed = disnake.Embed(title=f"General info about your switch",
                              description="Button that was clicked previously: None", colour=disnake.Colour.random())
    pixelpeek = await connect.receive("pixelPeek")
    charge = await connect.receive("charge")
    screen_file = disnake.File(
        BytesIO(bytes.fromhex(pixelpeek)), filename="switch.jpg")
    embed.add_field(name="General info about your switch",
                    value=f"Battery:{charge}%\nNote: Information like battery gets updated once you click a button!")
    embed.set_image(file=screen_file)
    return embed
