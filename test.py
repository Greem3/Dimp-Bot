import discord
from discord.ext import commands
from discord import Embed as DiscordEmbed
from discord import Interaction
from NewSimpleSQL import Database, generate_id
from src.discord_funcs.embed_funcs import create_embed
from src.Exception_Classes.custom_exceptions import *
import sqlite3, marshal

#region BOT INFO

prefixes = 'd!'
TOKEN = "MTI3NDUyNjM0NzczNzMwMTEyNA.Gz6OQZ.5XUeH-Omd0qef-20OMSdJkDjO1-Hf17sTNL7Tc"

intents: discord.Intents = discord.Intents(messages=True, guilds=True)
intents.presences = True
intents.message_content = True
intents.webhooks = True
intents.bans = True
intents.members = True

bot: commands.Bot = commands.Bot(command_prefix=prefixes, intents=intents)

db: Database = Database(sqlite3.connect("Dimp_Data.db"))

#region EVENTS

@bot.event
async def on_command_error(ctx: discord.ApplicationContext, error: commands.CommandError):
    
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("This command does not exist, type d!help to know all the available commands")
        return
    
    if isinstance(error, OnlyUsers):
        await ctx.send("Other bots can't use this bot!")

#region HELP COMMAND

class CustomHelpCommand(commands.HelpCommand):
    
    def __init__(self):
        super().__init__()
        
    async def send_bot_help(self, mapping):
        return await super().send_bot_help(mapping)
    
    async def send_command_help(self, command):
        return await super().send_command_help(command)
    
    async def send_group_help(self, group):
        return await super().send_group_help(group)
    
    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

#region USER COG

class User(commands.Cog, name="User Commands"):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="save-user", help="Save your user data")
    async def save_user_Command(self, ctx: discord.ApplicationContext):
        
        if ctx.author.bot:
            raise OnlyUsers()
        
        db.simple_insert_data("Users", (
            ctx.author.name,
            ctx.author.id,
            "Hello! I'm a new user.",
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ))
        
        await ctx.send("Your data has been saved! You can now use all the bot's commands")
        
    @commands.command(name="info", help="View your info or another user's info")
    async def info_Command(self, ctx: discord.ApplicationContext, user: discord.Member|None = None):
        
        if user.bot:
            raise OnlyUsers()
        
        user: discord.Member = ctx.author if user == None else user
        
        user_info: tuple|None = db.simple_select_data("Users", "*", f'WHERE id = {user.id}', True)
        
        if user_info != None:
            message = create_embed(
                user.name,
                user_info[2],
                discord.Colour.blue(),
                None,
                (f"User Id: {user.id}", None),
                [
                    (
                        "Points",
                        user_info[7],
                        False
                    ),
                    (
                        "Verified Problems Published",
                        user_info[3],
                        True
                    ),
                    (
                        "Unverified Problems Published",
                        user_info[4],
                        True
                    ),
                    (
                        "Verified Problems Resolved",
                        user_info[5],
                        False
                    ),
                    (
                        "Unverified Problems Resolved",
                        user_info[6],
                        True
                    )
                ],
                thumbnail=user.avatar
            )
            
            await ctx.send(embed=message)
            return
        
        await ctx.send("You haven't saved your information in the bot! Save it so you can see your stats, data, and use more commands" if user.id == ctx.author.id else "This user has not created their account in the bot")
    
    @commands.command(name="set-description", help="Allows you to change your user description")
    async def set_description_Command(self, ctx: discord.ApplicationContext, *, description: str):
        
        if len(description) > 4096:
            ctx.send("Your description is too long! Put a shorter one")
            return
        
        try:
            db.simple_update_data("Users", f'description = "{description}"', f"WHERE id = {ctx.author.id}")
            await ctx.send("Your description has been changed!")
        except:
            await ctx.send(f"You haven't created your bot account yet! \n \nUse the d!save-user command to be able to use this command.")

#region ON READY

@bot.event
async def on_ready():
    print(f"Conectado como: {bot.user}")
    
    bot.add_cog(User(bot))
    
    await bot.change_presence(activity=discord.Game("Use d!help for more info!"))
    
@bot.event
async def on_connect():
    print(f"Totalmente conectado a discord")

bot.run(TOKEN)