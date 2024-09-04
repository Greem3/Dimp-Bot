#   DISCORD
import discord
from discord import Embed as DiscordEmbed, Interaction, ui, File, SelectOption, SelectMenu, ChannelType, ApplicationContext, User as DUser
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord.ui import Button, View, Select, InputText, Modal
import docx.document
import scipy.constants
import scipy.constants._constants
import scipy.linalg
import scipy.special
from src.discord_funcs.embed_funcs import create_embed
from src.discord_funcs.view_funcs import create_view
#   ARCHIVOS
import io
from io import StringIO, BytesIO
#   FUNCIONES
from src.Exception_Classes.custom_exceptions import *
from src.Dictionarys.dict_funcs import *
#   TRADUCTOR
import translate
from translate import Translator
from translate.exceptions import TranslationError, InvalidProviderError
#   BASE DE DATOS
import sqlite3
from NewSimpleSQL.SimpleSQLite import generate_id, Database
from src.sql_scripts import db, SearchBy
#   SERIALIZACION DE OBJETOS
import marshal, pickle, json, yaml
#   EXPRESIONES REGULARES
import re
from re import Pattern, Match
#   MATEMATICAS
import math, decimal, scipy
from decimal import Decimal, getcontext, ROUND_HALF_UP
from scipy.constants._constants import c, G, g, alpha, h, k, m_p, m_n
#   THREADS
import threading
from threading import Thread
#   WEB
#! import page.start_page
#   EXTRA
import datetime, time, asyncio, string

#region BOT INFO

prefixes = 'd!'
TOKEN = "MTI3NDUyNjM0NzczNzMwMTEyNA.Gz6OQZ.5XUeH-Omd0qef-20OMSdJkDjO1-Hf17sTNL7Tc"

# intents: discord.Intents = discord.Intents(messages=True, guilds=True, )
# intents.presences = True
# intents.message_content = True
# intents.webhooks = True
# intents.bans = True
# intents.members = True

bot: commands.Bot = commands.Bot(command_prefix=prefixes, intents=discord.Intents.all())

#region GLOBAL VARS

creator: discord.User = 427319348831453186

#region EVENTS

@bot.event
async def on_command_error(ctx: discord.ApplicationContext, error: commands.CommandError):
    
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("This command does not exist, type d!help to know all the available commands")
        return
    
    if isinstance(error, commands.MissingRequiredArgument):
        command_info: commands.Command = ctx.command
        
        command_args: list = []
        
        for name, param in command_info.clean_params.items():
            command_args.append(f'<{name}>') if param.default == param.empty else command_args.append(f'[{name}]')
        
        await ctx.send(f"Use the command correctly by giving all the necessary arguments \n\nExample: `{prefixes}{command_info} {" ".join(command_args)}`")
        return
    
    if isinstance(error, CommandInvokeError):
        orierr = error.original
        
        if isinstance(orierr, ZeroDivisionError):
            await ctx.send("You can't divide by 0!")
            return
        
        if isinstance(orierr, OnlyInts):
            await ctx.send("You can't use decimals with factorials and square roots")
            return
        
        if isinstance(orierr, OverflowError):
            await ctx.send("This number is very long!")
            return
        
        if isinstance(orierr, discord.HTTPException):
            await ctx.send("The text is very long")
            return
        
        if isinstance(orierr, NotAdmin):
            await ctx.send("You are not an admin of this bot!")
            return
        
        if isinstance(orierr, NotIsAdmin):
            await ctx.send("This user not is admin of this bot!")
            return

        if isinstance(orierr, NotSuperAdmin):
            await ctx.send("You are not an super admin of this bot!")
            return
            
        if isinstance(orierr, NotIsSuperAdmin):
            await ctx.send("This user not is super admin of this bot!")

        if isinstance(orierr, AlreadyBanned):
            await ctx.send("This user is already banned!")
            return
        
        if isinstance(orierr, AlreadyAdmin):
            await ctx.send("This user is already an administrator")
            return
        
        if isinstance(orierr, NotRegistered):
            await ctx.send("You're not registered! use d!register to register")
            return
        
        if isinstance(orierr, BannedUser):
            await ctx.send("You are banned from this bot")
            return
        
        if isinstance(orierr, decimal.InvalidOperation|OnlyInts):
            await ctx.send("You can't use decimal with factorials, double factorials and roots")
            return
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("I don't have enough permissions to run this command")
        return
    
    if isinstance(error, OnlyUsers):
        await ctx.send("Other bots can't use this bot!")
        return
    
    error: str = error.args
    
    if error == "NaN":
        return

    await ctx.send(f"An error occurred during the command: \n\n {error}")

#region GLOBAL FUNCS

async def isbot(user_id: DUser|int):
    
    user: DUser = user_id if isinstance(user_id, DUser|discord.Member) else await bot.fetch_user(user_id)
    
    if user.bot:
        raise OnlyUsers()

    return user

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
    
#region ADMINISTRATORS COG

class Administrators(commands.Cog, name="Bot Administrator Commands"):
    
    def __init__(self, bot):
        self.bot: discord.Bot = bot
    
    @staticmethod
    def verify_admin(self, user_id: int, to_author: bool = True):
        
        answer: tuple[int|bool]|None = db.simple_select_data("administrators", "user_id, super_admin", f'WHERE user_id = {user_id}', True)
        
        if not bool(answer):
            raise NotAdmin() if to_author else NotIsAdmin()
        
        return answer
    
    def verify_super_admin(self, user_id: int, to_author: bool = True):
        
        if not bool(self.verify_admin(user_id)[1]):
            raise NotSuperAdmin() if to_author else NotIsSuperAdmin()
    
    @staticmethod
    def already_banned(self, user_id: int):
        if bool(db.simple_select_data("banned_users", 'user_id', f'WHERE user_id = {user_id}', True)):
            raise AlreadyBanned()
    
    @staticmethod
    def already_admin(self, user_id: int):
        if bool(db.simple_select_data("administrators", "user_id", f'WHERE user_id = {user_id}', True)):
            raise AlreadyAdmin()
    
    @commands.command(name="stop-bot", help="Stop the bot code")
    async def stop_bot_Command(self, ctx: discord.ApplicationContext):
        self.verify_super_admin(ctx.author.id)
        await ctx.send("Bot closed.")
        await bot.close()
        import sys
        sys.close(0)
    
    @commands.command(name="new-admin", help="Add a new admin in the bot!")
    async def new_admin_Command(self, ctx: discord.ApplicationContext, user_id_or_member: discord.Member|int, super_admin: str = "False"):
        
        
        self.verify_super_admin(ctx.author.id)
        user: DUser = await isbot(user_id_or_member)
        self.already_admin(user)
        
        positive: tuple = ("Y", "TRUE", "T")
        
        super_admin: bool = True if positive.count(super_admin.upper()) > 0 else False
        
        db.simple_insert_data("administrators", (
            user.id,
            super_admin
        ),
        (
            "user_id, super_admin"
        ))
        
        await ctx.send("New admin added")
        
    @commands.command(name='remove-admin', help="Remove a admin from the bot")
    async def remove_admin_Command(self, ctx: discord.ApplicationContext, user_id_or_member: discord.Member|int):
        
        
        self.verify_super_admin(ctx.author.id)
        user: DUser = await isbot(user_id_or_member)
        self.verify_admin(user.id, False)
        
        answer: bool = bool(db.simple_select_data("administrators", "super_admin", f'WHERE user_id = {user.id}', True)[0])
        
        if answer:
            await ctx.send("This user is an super admin!")
            return
        
        db.simple_delete_data("administrators", f'WHERE user_id = {user.id}')
        
        await ctx.send("Admin removed")
        
    @commands.command(name="ban-user", help="Ban a user of the bot")
    async def ban_user_Command(self, ctx: discord.ApplicationContext, user_id_or_member: discord.Member|int, unban_days: int = None):
        
        self.verify_admin(ctx.author.id)
        user: DUser = await isbot(user_id_or_member)
        self.already_banned(user.id)
        
        today_date: datetime.date = datetime.datetime.now().date()
        
        db.simple_insert_data("banned_users", (
            user.id,
            today_date,
            today_date + datetime.timedelta(days=unban_days) if unban_days is not None else None
        ))
        
        await ctx.send("User banned")
        
    @commands.command(name="verify-problem", help="Verify is a problem have an real solution")
    async def verify_problem_Command(self, ctx: discord.ApplicationContext, problem_id: int, *, difficulty: str):
         
        self.verify_admin(ctx.author.id)
    
    @commands.command(name="delete-problem", help="Delete an unopropiated problem")
    async def delete_problem_Command(self, ctx: discord.ApplicationContext, problem_id: int, *, reason: str):
        
        self.verify_admin(ctx.author.id)

#region USER COG

class User(commands.Cog, name="User Commands"):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="register", help="Save your user data")
    async def save_user_Command(self, ctx: discord.ApplicationContext):
        
        db.simple_insert_data("Users", (
            ctx.author.id,
            datetime.datetime.now().date()
        ), 
        "id, create_date")
        
        await ctx.send("Your data has been saved! You can now use all the bot's commands")
        
    @commands.command(name="info", help="View your info or another user's info")
    async def info_Command(self, ctx: discord.ApplicationContext, user: discord.Member|None|int = None, what_see: str = "profile"):
        
        see_options: tuple[str] = ("profile", "p", "problems", "pr", "solutions", "s", "clubs", "c")
        
        what_see = what_see.lower()
        if what_see not in see_options:
            what_see = "profile"
        
        user: discord.Member = ctx.author if user is None else user if isinstance(user, DUser|discord.Member) else await bot.fetch_user(user)
        
        await isbot(user)
        
        if what_see in ("profile", "p"):
            user_info: tuple|None = db.simple_select_data("Users", "*", f'WHERE id = {user.id}', True)
            
            if user_info is not None:
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
        
        if what_see in ("problems", "pr"):
            pass
        
        if what_see in ("solutions", "s"):
            pass
        
        if what_see in ("clubs", "c"):
            pass
        
        await ctx.send("You don't have registered your information in the bot! Save it so you can see your stats, data, and use more commands" if user.id == ctx.author.id else "This user has not created their account in the bot")
    
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

#region PROBLEMS COG

class Problems(commands.Cog, name="Problems Commands"):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="publish", help="Post a math problem")
    async def publish_Command(self, ctx: discord.ApplicationContext, name: str, type: str, *, description: str):
        
        if len(name) > 245:
            await ctx.send("The name of the problem is very long!")
        
        problems_types: tuple[str] = ("ALGEBRA", "COMBINATORICS", "COMBINATORIAL", "NUMBERS_THEORY", "TEO", "LOGIC", "GEOMETRY")
        
        if type.upper() not in problems_types:
            await ctx.send("That problem type doesn't exist!")
            return
        
        type = type.lower().capitalize()
        
        if "_" in type:
            type = type.replace("_", " ")
        
        name = name.replace("_", " ")
        
        db.simple_insert_data("Problems", (
            ctx.author.id,
            name,
            description,
            type,
            datetime.datetime.now().date()
        ),
        "author_id, name, description, type, publish_date"
        )
        
        await ctx.send("Your problem has publicated!")
        
    @commands.command(name="search", help="Search a problem")
    async def search_Command(self, ctx: discord.ApplicationContext, *, name_or_id: str|int|None = None):
        
        if name_or_id is None:
            
            all_problems: list[tuple] = db.simple_select_data("Problems", "name, id, publish_date", f'ORDER BY publish_date DESC')
            
            message: discord.Embed = create_embed(
                "Problems",
                "",
                discord.Colour.green(),
                footer=(f"Page 1: 1-{10 if len(all_problems) > 10 else len(all_problems)}", None)
            )
                
            for i in all_problems:
                message.add_field(name=i[0], value=f'ID: {i[1]}', inline=True)
                message.add_field(name="Publish Date:", value=i[2], inline=True)
                message.add_field(name="\u200B", value="", inline=False)
                
            message.remove_field(-1)
                
            await ctx.send(embed=message)
            return
        
        problem_data = SearchBy("Problems", "*", name_or_id)
        
        if problem_data is None:
            await ctx.send("This problem don't exist!")
            return
        
        author: discord.Member = await bot.fetch_user(problem_data[1])
        
        message = create_embed(
            problem_data[2],
            problem_data[3],
            discord.Colour.purple(),
            (author.name, author.avatar),
            (f'Problem ID: {problem_data[0]}', None),
            [
                (
                    "Problem Type:",
                    f'{problem_data[4]}',
                    True
                ),
                (
                    "Publish date:",
                    problem_data[5],
                    True
                ),
                (
                    "Difficulty:",
                    problem_data[7],
                    True
                ),
                (
                    "\u200B",
                    "\n",
                    False
                ),
                (
                    "Verified:",
                    bool(problem_data[9]),
                    True
                ),
                (
                    "Has Oficial Solution:",
                    True if problem_data[8] is not None else False,
                    True
                ),
                (
                    "Total Published Solutions:",
                    problem_data[6],
                    True
                )
            ]
        )
        
        await ctx.send(embed=message)

    @commands.command(name="edit", help="Edit a math problem")
    async def edit_Command(self, ctx: discord.ApplicationContext, problem_id: int, category: str, *, new_value: str):
        
        problem_data = db.simple_select_data("Problems", "*", f'WHERE id = {problem_id}', True)
        
        if problem_data is None:
            await ctx.send("This problem don't exist!")
            return
        
        if problem_data[4] != ctx.author.id:
            await ctx.send("You are not the creator of this problem!")
            return
        
        if category not in ("name", "type", "description", "solution"):
            await ctx.send("This category doesn't exists")
            return
        
        value_len = len(new_value)
        
        if (category == "name") & (value_len > 256):
            await ctx.send("The name is too large, try with less than 256 characters")
            return
        
        if category == "type":
            
            problems_types: tuple[str] = ("ALGEBRA", "COMBINATORICS", "COMBINATORIAL", "NUMBERS_THEORY", "TEO", "LOGIC", "GEOMETRY")
        
            if new_value.upper() not in problems_types:
                await ctx.send("That problem problem doesn't exist!")
                return
            
            if value_len > 1011:
                await ctx.send("The problem type is too large")
                return
        
        if value_len > 4096:
            await ctx.send("The description is too large")
            return
        
        db.simple_update_data("Problems", f'{category} = "{new_value}"', f'WHERE id = {problem_id}')
        
        await ctx.send("Your problem has changed")

#region SOLUTIONS COG

class Solutions(commands.Cog, name="Solutions Commands"):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="submit", help="Submit a solution to a problem")
    async def submit_Command(self, ctx: discord.ApplicationContext, problem_id: int, *, solution: str):
        
        if len(solution) > 4096:
            await ctx.send("The solution is too large")
            return
        
        problem: tuple[int]|None = db.simple_select_data("Problems", "total_solutions", f'WHERE id = {problem_id}', True)
        
        if not bool(problem):
            await ctx.send("This Problem Don't Exists!")
            return
        
        id_solution = generate_id()
        
        while bool(db.simple_select_data("Solutions", "id", f'WHERE problem_id = {problem_id} AND id = {id_solution}', True)):
            id_solution = generate_id()
        
        db.simple_insert_data("Solutions", (
            id_solution,
            problem_id,
            ctx.author.id,
            solution,
            datetime.datetime.now().date(),
            marshal.dumps({})
        ),
        "id, problem_id, author_id, description, publish_date, users_votes"
        )
        
        db.simple_update_data("Problems", f"total_solutions = total_solutions + 1", f'WHERE id = {problem_id}')
        
        await ctx.send("Your solution has been submitted!")
        
    @commands.command(name="see", help="See a solution of a user")
    async def see_Command(self, ctx: discord.ApplicationContext, problem_id: int, solution_id: int|None = None):
        
        problem = db.simple_select_data("Problems", "name, id", f'WHERE id = {problem_id}', True)
        
        if not bool(problem):
            await ctx.send("The problem does not exist!")
            return
        
        solution: tuple[str|int|dict]|None = db.simple_select_data("Solutions", "*", f'WHERE id = {solution_id} AND problem_id = {problem_id}', True) if bool(solution_id) else None
        
        if not bool(solution):
            all_solutions: list[tuple] = db.simple_select_data("Solutions", 
                '''author_id, id, positive_votes+negative_votes,
                CASE
                    WHEN (positive_votes - negative_votes) = 0 THEN 0
                    ELSE positive_votes / (positive_votes - negative_votes)
                END AS score''', 
                f'WHERE problem_id = {problem[1]} \n ORDER BY score'
            )
            
            if len(all_solutions) == 0:
                await ctx.send("This problem don't have solutions")
                return
            
            message: discord.Embed = create_embed(
                f"{problem[0]} : Solutions",
                "",
                discord.Colour.green(),
                footer=(f"Page 1: 1-{10 if len(all_solutions) > 10 else len(all_solutions)}", None) 
            )
                
            for i in all_solutions:
                message.add_field(name=f'Author: {(await bot.fetch_user(i[0])).name}', value=f'Solution ID: {i[1]}', inline=True)
                message.add_field(name='Votes:', value=i[2], inline=True)
                message.add_field(
                    name='Positive Votes Percentaje:', 
                    value=f'{i[3]}%', 
                    inline=True
                )
                message.add_field(name="\u200B", value="", inline=False)
                
            message.remove_field(-1)
                
            await ctx.send(embed=message)
            return
        
        creator: discord.Member = await bot.fetch_user(solution[2])
        
        message: discord.Embed = create_embed(
            f'{problem[0]} : Solution',
            solution[3],
            discord.Colour.dark_blue(),
            (creator.name, creator.avatar),
            (f'Solution ID: {solution[0]} \nProblem ID: {problem[1]}', None),
            [
                (
                    "\u200B",
                    "",
                    False
                ),
                (
                    "Votes:",
                    solution[6]+solution[7],
                    True
                ),
                (
                    "Positive Votes Percentaje:",
                    f'{(solution[6]/(solution[6]+solution[7]))*100}%' if solution[6]+solution[7] > 0 else "0%",
                    True
                ),
                (
                    "\u200B",
                    "",
                    False
                )
            ]
        )
        
        users_votes: dict = marshal.loads(solution[5])
        
        button_up: Button = Button(style=discord.ButtonStyle.green, emoji="✅", custom_id="more")
        button_down: Button = Button(style=discord.ButtonStyle.danger, emoji="✖", custom_id="less")
        button_reset: Button = Button(style=discord.ButtonStyle.secondary, emoji="🔄", custom_id="reset")
        
        async def Buttons_Callbacks(interaction: discord.Interaction):
            
            if not KeyIn(users_votes, interaction.user.id):
                
                if interaction.custom_id == "more":
                    users_votes[interaction.user.id] = "positive"
                    db.custom_execute("UPDATE Solutions SET positive_votes = positive_votes + 1, users_votes = ? WHERE id = ? AND problem_id = ?", marshal.dumps(users_votes), solution_id, problem_id)
                    
                if interaction.custom_id == "less":
                    users_votes[interaction.user.id] = "negative"
                    db.custom_execute("UPDATE Solutions SET negative_votes = negative_votes + 1, users_votes = ? WHERE id = ? AND problem_id = ?", marshal.dumps(users_votes), solution_id, problem_id)
                    
                new_values = db.simple_select_data("Solutions", f'positive_votes, negative_votes', f'WHERE id = {solution_id} AND problem_id = {problem_id}', True)
            
                message.set_field_at(1, name="Votes:", value=new_values[0]+new_values[1])
                message.set_field_at(2, name="Positive Votes Percentaje:", value=f'{(new_values[0]/(new_values[0] + new_values[1]))*100}%' if new_values[0]+new_values[1] > 0 else "0%")   
            else:
                
                if interaction.custom_id == "reset":
                    positive, negative = 0, 0
                    
                    if users_votes[interaction.user.id] == "positive":
                        positive += 1
                    else:
                        negative += 1
                        
                    users_votes.pop(interaction.user.id)
                    
                    db.custom_execute(f"UPDATE Solutions SET positive_votes = positive_votes - {positive}, negative_votes = negative_votes - {negative}, users_votes = ? WHERE id = ? AND problem_id = ?", marshal.dumps(users_votes), solution_id, problem_id)
                    
                    new_values = db.simple_select_data("Solutions", f'positive_votes, negative_votes', f'WHERE id = {solution_id} AND problem_id = {problem_id}', True)
                    
                    message.set_field_at(1, name="Votes:", value=new_values[0]+new_values[1])
                    message.set_field_at(2, name="Positive Votes Percentaje:", value=f'{(new_values[0]/(new_values[0] + new_values[1]))*100}%' if new_values[0]+new_values[1] > 0 else "0%")
            
            await interaction.response.edit_message(embed=message)
        
        buttons_list: list[Button] = [button_up, button_down, button_reset]

        for num in range(0, len(buttons_list)):
            buttons_list[num].callback = Buttons_Callbacks
            
        views: View = View(buttons_list[0], buttons_list[2], buttons_list[1], timeout=60, disable_on_timeout=True)
        
        answer: discord.Message = await ctx.send(embed=message, view=views)

#region CLUBS COG

class Clubs(commands.Cog, name="Clubs Commands"):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="create-club", help="Create a club")
    async def create_club_Command(self, ctx: discord.ApplicationContext, *, name: str):
        pass

#region CALCULATOR COG
class Calculator(commands.Cog, name="Calculator Commands"):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="calc", help="Does math calculations")
    async def calc_Command(self, ctx: discord.ApplicationContext, *, calculation: str):
        round_number: bool|int = False
        send_file: bool = False
        custom_command_parameters: Pattern = r'--([a-zA-Z]+):([\w\d]+)' # Parametros que tengan valores customizados
        custom_command_parameters_no_value: Pattern = r'--([a-zA-Z]+)' #! Parametros con valores fijos. SIN USAR AUN
        
        if calculation.find("∞") >= 0:
            await ctx.send("∞")
            return
        
        def change_parameters(match: Match):
            param = match.group(1).lower() # Nombre del parametro
            
            if len(match.groups()) >= 2:
                value = match.group(2) if match.group(2).isnumeric() else match.group(2).lower()
            
            params = ("length", "round", "file")
            
            if param not in params:
                return ""
            
            if param == "length":
                getcontext().prec = int(value)
                return ""
            
            if param == "round":
                nonlocal round_number
                round_number = int(value)
                return ""
            
            if param == "file":
                nonlocal send_file
                send_file = True
                return ""
            
            return ""
        
        calculation: str = calculation.lower()

        calculation: str = re.sub(custom_command_parameters, change_parameters, calculation)
        calculation: str = re.sub(custom_command_parameters_no_value, change_parameters, calculation)
        
        calculation: str = calculation.replace("mod", "%")
        calculation: str = calculation.replace("pi", str(math.pi))
        calculation: str = calculation.replace("e", str(math.e))
        calculation: str = calculation.replace("^", "**")
        calculation: str = calculation.replace("c", str(c))
        calculation: str = calculation.replace("gn", str(G))
        calculation: str = calculation.replace("g", str(g))
        calculation: str = calculation.replace("h", str(h))
        calculation: str = calculation.replace("a", str(alpha))
        calculation: str = calculation.replace("k", str(k))
        calculation: str = calculation.replace("pm", str(m_p))
        calculation: str = calculation.replace("nm", str(m_n))
        
        def calculate(num: str) -> str:
            
            parentesis_pattern: Pattern = r'\(([^()]*)\)'
            
            def give_parentesis(match: Match):
                return str(calculate(match.group(1)))
            
            while re.search(parentesis_pattern, num):
                num: str = re.sub(parentesis_pattern, give_parentesis, num)
                
            infinity_number_pattern: Pattern = r'(-?\d+\.?\d*)\.\.\.(?:\{(.*?)\})?'
            
            def give_infinity_number(match: Match):
                number = match.group(1)
                limit = int(calculate(match.group(2))) if bool(match.group(2)) else 10**3
                
                number = number + number[-1] * limit    
                
                return str(number)
            
            num: str = re.sub(infinity_number_pattern, give_infinity_number, num)
                
            reverse_absolute_pattern: Pattern = r'~(.*?)~'
            
            def give_reverse_absolute(match: Match):
                return str(-(abs(float(calculate(match.group(1))))))
            
            num: str = re.sub(reverse_absolute_pattern, give_reverse_absolute, num)
            
            absolute_pattern: Pattern = r'\|(.*?)\|'
            
            def give_absolute(match: Match):
                return str(abs(float(calculate(match.group(1)))))
            
            num: str = re.sub(absolute_pattern, give_absolute, num)
            
            custom_root_pattern: Pattern = r'(\d*\.?\d*)\[(.*?)\]'
            
            def custom_root(match: Match):
                indice: int = 2 if not bool(match.group(1)) else float(match.group(1)) # Si el tamaño del primer número es 0 entonces lo hara una raiz cuadrada
                number: int = float(calculate(match.group(2)))
                
                root = number ** (1 / indice)
                
                if root.is_integer():
                    root = int(root)
                    
                return str(root)
            
            num: str = re.sub(custom_root_pattern, custom_root, num)
            
            double_factorial_pattern = r'(\d+)!!'
            
            def give_double_factorial(match: Match):
                number = int(match.group(1))
                
                if number % 2 == 0:
                    answer: int = 2
                    
                    for i in range(4, number+1, 2):
                        answer *= i
                        
                    return str(answer)
                
                if number % 2 == 1:
                    answer: int = 1
                    
                    for i in range(3, number+1, 2):
                        answer *= i
                        
                    return str(answer)
                
                raise OnlyInts()
            
            num: str = re.sub(double_factorial_pattern, give_double_factorial, num)
            
            factorial_pattern = r'(\d+)!(?:\{(\d+)\})?'
            
            def give_factorial(match: Match):
                number = int(match.group(1))
                limit: int = int(match.group(2)) if bool(match.group(2)) else 0
                
                if bool(limit):
                    divisors = 1
                    
                    for i in range(2, limit):
                        divisors *= i
                    
                    return str(math.factorial(number)/divisors)
                
                return str(math.factorial(number))
            
            num = re.sub(factorial_pattern, give_factorial, num)
            
            join_pattern: Pattern = r'(\d+)&(\d+)'
            
            def join_numbers(match: Match):
                return str(calculate(match.group(1)) + calculate(match.group(2)))
            
            num = re.sub(join_pattern, join_numbers, num)
                
            return str(Decimal(eval(num)))
        
        def replace_functions(match: Match):
            func = match.group(1)
            value = float(match.group(2))
            
            if func == "w":
                return str(scipy.special.lambertw(value))
            
            if func == "log":
                return str()
            
            return ""
        
        calculation: str = re.sub(r'([a-zA-Z]{1,3})\((.*?)\)', replace_functions, calculation)
        
        if re.search(r'[a-zA-Z]', calculation) is not None:
            
            calculation = re.sub(r'[a-zA-Z]+', "", calculation)
        
        calculation: Decimal = Decimal(calculate(calculation))

        if round_number is not False:
            calculation: Decimal = calculation.quantize(Decimal('0.' + '0' * round_number), rounding=ROUND_HALF_UP)
            
        calculation = str(calculation)
        
        if (send_file) | (len(calculation) > 2000):
            
            if len(calculation) > 4300:
                await ctx.send("The number is too large!")
                return
            
            with StringIO() as file:
                file.write(calculation)
                file.seek(0)
                
                await ctx.send(file=discord.File(file, "number.txt"))
                
            return
        
        await ctx.send(calculation)

#region GAMES COG

class Games(commands.Cog, name="Games Commands"):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='games', help='See all games in the bot!')
    async def games_Command(self, ctx: discord.ApplicationContext):
        
        message: DiscordEmbed = create_embed(
            "Bot Games",
            "All games in the bot!",
            discord.Colour.purple(),
            tables=
            [
                (
                    "\u200B",
                    "",
                    False
                ),
                (
                    "Calculate Number",
                    "A roguelike game in which you have to get the number they ask you for with mathematical calculations with a calculator!",
                    False
                ),
                (
                    "\u200B",
                    "",
                    False
                ),
                (
                    "Twenty Four",
                    "A game of 1 or more players in which you have to look for 24 in a group of 4 cards from 1 to 13 or say that there are no 24.",
                    False
                )
            ],
            image="games.png"
        )
        
        file: File = File('images/png/test_image.png', filename='games.png')
        
        # VIEW
        games_select: Select = Select(
            discord.ComponentType.string_select, 
            placeholder="More information about a game",
            options=
            [
                SelectOption(
                    label="Calculate Number",
                    value="cn",
                    emoji="📱"
                ),
                SelectOption(
                    label="Twenty Four",
                    value="24",
                    emoji="🃏"
                )
            ]
        )
        
        view: View = View(disable_on_timeout=True)
        
        async def ShowInfo(interaction: Interaction):
            value = interaction.data['values'][0]
            
            if value == 'cn':
                await interaction.response.send_message("Test Message 1")
                return
            
            if value == '24':
                await interaction.response.send_message("Test Message 2")
                return
            
        games_select.callback = ShowInfo
        
        view.add_item(games_select)
        
        await ctx.send(embed=message, file=file, view=view)
    
    @commands.command(name="cn-register", help="Register your account for Calculate Number")
    async def cn_create_Command(self, ctx: discord.ApplicationContext):
        pass
    
class General(commands.Cog, name="General Commands"):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="translate", help="Translate a text or a problem!")
    async def translate_Command(self, ctx: discord.ApplicationContext, language: str, *, text_or_problem_id: str|int):
        
        if text_or_problem_id.isnumeric():
            
            text_or_problem_id: tuple[str]|None = db.simple_select_data("Problems", "description", f'WHERE id = {text_or_problem_id}', True)
            
            if text_or_problem_id is None:
                await ctx.send("This problem don't exists!")
                return
            
            text_or_problem_id = text_or_problem_id[0]
            
        translator: Translator = Translator(to_lang=language.lower(), from_lang="autodetect",)
        
        await ctx.send(translator.translate(text_or_problem_id))

#region VERIFY BANS

async def verify_user(ctx: discord.ApplicationContext):
    
    await isbot(ctx.author)
    
    if db.simple_select_data("banned_users", "user_id", f'WHERE user_id = {ctx.author.id}', True) is not None:
        raise CommandInvokeError(BannedUser())
    
    if ctx.command.name in ["register", "help", "search", "see", "calc", "translate"]:
        return
    
    if not bool(db.simple_select_data("Users", "id", f'WHERE id = {ctx.author.id}', True)):
        raise CommandInvokeError(NotRegistered())

def verify_unbans():
    
    thread_db: Database = Database("Dimp_Data.db")
    
    while True:
        all_bans = thread_db.simple_select_data("banned_users", "*", f'WHERE unban_date IS NOT NULL')
        
        for row in all_bans:
            
            if datetime.datetime.now().date() >= datetime.datetime.strptime(row[2], "%Y-%m-%d").date():
                thread_db.simple_delete_data("banned_users", f'user_id = {row[0]}')
        
        time.sleep(60)
    
Thread(target=verify_unbans).start()

#region ON READY

@bot.event
async def on_ready():
    
    print(f"Conectado como: {bot.user}")
    
    bot.add_cog(Administrators(bot))
    bot.add_cog(User(bot))
    bot.add_cog(Problems(bot))
    bot.add_cog(Solutions(bot))
    bot.add_cog(Calculator(bot))
    bot.add_cog(Games(bot))
    bot.add_cog(General(bot))
    
    bot.before_invoke(verify_user)
    
    global creator
    
    creator = bot.get_user(creator)
    
    await bot.change_presence(activity=discord.Game("Use d!help for more info!"))
    
@bot.event
async def on_connect():
    print(f"Conectandose a discord")

bot.run(TOKEN)