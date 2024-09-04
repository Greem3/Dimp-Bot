import discord, requests
from discord.ext import commands
from typing import Union

class table_name: pass

class table_description: pass

class table_inline: pass

class table_subtables: pass

class image_url: pass

def verify_icon_url(url: image_url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def change_channel_permissions(channel: discord.ChannelType, roles: discord.Role|list[discord.Role]):
    pass

def verify_permissions(user_roles: list[discord.Role], custom_role_id: discord.Role|list[discord.Role]):
    
    if isinstance(custom_role_id, list):
        
        for i in custom_role_id:
            if i in user_roles:
                return True
        
        raise commands.MissingPermissions()
    
    return True if custom_role_id in user_roles else commands.MissingPermissions([''])

def toRole(server_roles: list[discord.Role], value: int|list[int]):
    
    if (isinstance(value, list)) | (isinstance(value, tuple)):
        role: list = []
        
        for i in value:
            role.append(discord.utils.get(server_roles, id=i))
    else:
        role = discord.utils.get(server_roles, id=value)
    
    return role