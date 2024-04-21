import disnake
import asyncio
from io import BytesIO
from src.yaml import connect, delay, owner_id
from src.helper_funcs import edit_embed


class SwitchButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self._amount = 1

    async def interaction_check(self, interaction):
        if interaction.author.id != int(owner_id):
            await interaction.response.send_message("You are not the owner of the bot, thus not allowing you to control the owner's switch!")
            return False
        else:
            return True

    async def _amount_clicks(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        for _ in range(self._amount):
            if self._amount > 3:
                await asyncio.sleep(0.5)
            await connect.send(f"click {interaction.component.label}")
        await edit_embed(button, interaction, self, followup=True)

    @disnake.ui.button(custom_id="1", emoji="📷", label="CAPTURE", style=disnake.ButtonStyle.primary, row=0)
    async def button_capture(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="2", emoji="🏠", label="HOME", style=disnake.ButtonStyle.primary, row=0)
    async def button_home(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="3", label="+", style=disnake.ButtonStyle.primary, row=0)
    async def button_plus(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="4", label="-", style=disnake.ButtonStyle.primary, row=0)
    async def button_minus(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="5", label="screenoff", style=disnake.ButtonStyle.danger, row=0)
    async def button_screen(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if button.label == "screenoff":
            await connect.send("screenOff")
            button.label = "screenon"
            button.style = disnake.ButtonStyle.success
            return await edit_embed(button, interaction, view=self)
        await connect.send("screenOn")
        button.label = "screenoff"
        button.style = disnake.ButtonStyle.danger
        await edit_embed(button, interaction, view=self)

    # DPAD Control
    @disnake.ui.button(custom_id="6", emoji="⬆", label="DUP", style=disnake.ButtonStyle.primary, row=1)
    async def button_dup(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="7", emoji="⬇", label="DDOWN", style=disnake.ButtonStyle.primary, row=1)
    async def button_ddown(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="8", emoji="⬅", label="DLEFT", style=disnake.ButtonStyle.primary, row=1)
    async def button_dleft(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="9", emoji="➡", label="DRIGHT", style=disnake.ButtonStyle.primary, row=1)
    async def button_dright(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    # Button Control

    @disnake.ui.button(custom_id="11", label="X", style=disnake.ButtonStyle.primary, row=2)
    async def button_x(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="12", label="Y", style=disnake.ButtonStyle.primary, row=2)
    async def button_y(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="13", label="B", style=disnake.ButtonStyle.primary, row=2)
    async def button_b(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="14", label="A", style=disnake.ButtonStyle.primary, row=2)
    async def button_a(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)
    # Shoulder buttons

    @disnake.ui.button(custom_id="15", label="ZL", style=disnake.ButtonStyle.primary, row=3)
    async def button_zl(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="16", label="L", style=disnake.ButtonStyle.primary, row=3)
    async def button_l(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="17", label="ZR", style=disnake.ButtonStyle.primary, row=3)
    async def button_zr(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="18", label="R", style=disnake.ButtonStyle.primary, row=3)
    async def button_r(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self._amount_clicks(button, interaction)

    @disnake.ui.button(custom_id="19", emoji="🎮", label="game info", style=disnake.ButtonStyle.primary, row=4)
    async def button_game(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author.id != int(owner_id):
            return
        await edit_embed(button, interaction, view=self)
        try:
            embed = disnake.Embed(
                title="Information of the game you are in", type="rich", color=disnake.Color.random())
            game_commands = [
                ("name", "game name", "Game name"),
                ("author", "game author", "Made by"),
                ("version", "game version", "Game version"),
                ("rating", "game rating", "Game rating"),
                ("icon", "game icon", None),
                ("title_id", "getTitleID", "Game id")
            ]
            game_info = {}
            game_description = []
            for key, command, description in game_commands:
                info = await connect.receive(command)
                game_info[key] = info
                if description:
                    game_description.append(f'{description}:{info}')
            embed.add_field(name="info", value='\n'.join(game_description))
            embed.set_image(file=disnake.File(
                BytesIO(bytes.fromhex(game_info['icon'])), filename="game.jpg"))
            await interaction.followup.send(embed=embed)
        except ValueError:
            await interaction.followup.send(f" {game_info['name']} Check if you are in a game otherwise it's not going to work!")

    @disnake.ui.button(custom_id="20", label="🕹️ Stick Control Panel", style=disnake.ButtonStyle.blurple, row=4)
    async def button_stick_panel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await edit_embed(button, interaction, view=SwitchSticks())

    @disnake.ui.button(custom_id="21", label="amount of clicks: 1", style=disnake.ButtonStyle.blurple, row=4)
    async def button_add_clicks(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self._amount += 1
        button.label = f"amount of clicks: {self._amount}"
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="22", label="clear click amount", style=disnake.ButtonStyle.red, row=4)
    async def button_clear_clicks(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self._amount = 1
        self.button_add_clicks.label = f"amount of clicks: {self._amount}"
        await edit_embed(button, interaction, view=self)


class SwitchSticks(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self._direction = "LEFT"
        self._seconds = 1

    async def interaction_check(self, interaction):
        if interaction.author.id != int(owner_id):
            await interaction.response.send_message("You are not the owner of the bot, thus not allowing you to control the owner's switch!")
            return False
        else:
            return True

    @disnake.ui.button(custom_id="1", emoji="🕹️", label="Buttons Control Panel", style=disnake.ButtonStyle.blurple, row=1)
    async def button_stick_panel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await edit_embed(button, interaction, view=SwitchButtons())

    @disnake.ui.button(custom_id="2", emoji="🕹️", label="Set stick left", style=disnake.ButtonStyle.green, row=1)
    async def button_set_left(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self._direction = "LEFT"
        button.style = disnake.ButtonStyle.green
        self.button_set_right.style = disnake.ButtonStyle.blurple
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="3", emoji="🕹️", label="Set stick right", style=disnake.ButtonStyle.blurple, row=1)
    async def button_set_right(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self._direction = "RIGHT"
        button.style = disnake.ButtonStyle.green
        self.button_set_left.style = disnake.ButtonStyle.blurple
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="4", emoji="⬆️", label="Move forward forever until stop", style=disnake.ButtonStyle.blurple, row=2)
    async def button_stick_forward(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await connect.send(f"setStick {self._direction} 0 0x7FFF")
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="5", emoji="⬇️", label="Move down forever until stop", style=disnake.ButtonStyle.blurple, row=2)
    async def button_stick_down(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await connect.send(f"setStick {self._direction} 0 -0x8000")
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="6", emoji="⬅️", label="Move left forever until stop", style=disnake.ButtonStyle.blurple, row=2)
    async def button_stick_left(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await connect.send(f"setStick {self._direction} -0x8000 0")
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="7", emoji="➡️", label="Move right forever until stop", style=disnake.ButtonStyle.blurple, row=2)
    async def button_stick_right(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await connect.send(f"setStick {self._direction} 0x7FFF 0")
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="8", label="stop moving", style=disnake.ButtonStyle.danger, row=2)
    async def button_stick_stop(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await connect.send(f"setStick {self._direction} 0 0")
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="9", emoji="⬆️", label=f"Move forward for {delay} seconds", style=disnake.ButtonStyle.blurple, row=3)
    async def button_stick_forward_seconds(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await connect.send(f"setStick {self._direction} 0 0x7FFF")
        await asyncio.sleep(delay)
        await connect.send(f"setStick {self._direction} 0 0")
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="10", emoji="⬇️", label=f"Move down for {delay} seconds", style=disnake.ButtonStyle.blurple, row=3)
    async def button_stick_down_seconds(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await connect.send(f"setStick {self._direction} 0 -0x8000")
        await asyncio.sleep(delay)
        await connect.send(f"setStick {self._direction} 0 0")
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="11", emoji="⬅️", label=f"Move down for {delay} seconds", style=disnake.ButtonStyle.blurple, row=3)
    async def button_stick_left_seconds(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await connect.send(f"setStick {self._direction} -0x8000 0")
        await asyncio.sleep(delay)
        await connect.send(f"setStick {self._direction} 0 0")
        await edit_embed(button, interaction, view=self)

    @disnake.ui.button(custom_id="12", emoji="➡️", label=f"Move down for {delay} seconds", style=disnake.ButtonStyle.blurple, row=3)
    async def button_stick_right_seconds(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await connect.send(f"setStick {self._direction} 0x7FFF 0")
        await asyncio.sleep(delay)
        await connect.send(f"setStick {self._direction} 0 0")
        await edit_embed(button, interaction, view=self)
