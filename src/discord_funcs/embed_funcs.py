import discord, datetime, requests
from discord import Embed
from typing import Union

class table_name: pass

class table_description: pass

class table_inline: pass

class table_subtables: pass

class image_url: pass

def create_embed(em_title: str, em_description: str, em_color: discord.Color = None, author: tuple[str, image_url] = None, footer: tuple[str, image_url] = None, tables: list[tuple[Union[table_name, table_description, table_inline, table_subtables]]] = None, image: image_url = None, thumbnail: image_url = None, em_timestamp: datetime.datetime = None) -> Embed:
    """
    Create a simple Discord Embed
    """
    
    def create_embed_tables(embed: discord.Embed, tables: list[Union[table_name, table_description, table_inline, table_subtables]]):
    
        try:
            for object in tables: # Espaciado entre columnas
                embed.add_field(name=object[0], value=object[1], inline=object[2])
                    
                if len(object) > 3:
                    create_embed_tables(embed, object[3])
        except (ValueError, IndexError, TypeError) as error:
            print('An error has passed while adding the tables')
            embed.add_field(name='Create Table Error', value=error, inline=False)
    
    Embed: discord.Embed = discord.Embed(
        title=em_title,
        description=em_description,
        color=em_color,
        timestamp=em_timestamp
    )
    
    if author != None:
        try:
            Embed.set_author(name=author[0], icon_url=author[1])
        except (ValueError, IndexError, TypeError, discord.errors.HTTPException) as error:
            print('An error has passed while adding the author')
            Embed.set_author(name=f'Create Author Error \r \r Error: {error}')
            
    if footer != None:
        try:
            Embed.set_footer(text=footer[0], icon_url=footer[1])
        except (ValueError, IndexError, TypeError, discord.errors.HTTPException) as error:
            print('An error has passed while adding the footer')
            Embed.set_footer(text=f'Create Footer Error \r \r Error: {error}')
            
    if tables != None:
        create_embed_tables(Embed, tables)
            
    if image != None:
        try:
            Embed.set_image(url=f'attachment://{image}')
        except (ValueError, IndexError, TypeError, discord.HTTPException) as error:
            print('An error has passed while adding a image to the embed')
            Embed.add_field(name='Add Image Error', value=error, inline=False)
    
    if thumbnail != None:
        try:
            Embed.set_thumbnail(url=thumbnail)
        except (ValueError, IndexError, TypeError, discord.HTTPException) as error:
            print('An error has passed while adding a thumbnail to the embed')
            Embed.add_field(name='Add Thumbnail Error', value=error, inline=False)
            
    return Embed

def edit_embed(section: str, value: str|tuple|image_url):
    pass