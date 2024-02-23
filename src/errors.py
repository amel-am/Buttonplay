from disnake.ext import commands


class Error(commands.Cog):

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # For not printing commands not found in the terminal.
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Some arguments are missing")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Your Arguments were bad")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("Only the owner of this bot can use this command.")
        else:
            print(f"Error is: {error}")
