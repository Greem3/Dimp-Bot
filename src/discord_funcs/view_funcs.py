import discord
from discord.ui import View, Button, Select, Item
from discord import SelectOption, ChannelType

async def create_view(items: dict[dict[str|int|bool]] = {}, timeout: int = 180, disable_on_timeout: bool = False) -> View:
    """_summary_

    Args:
        timeout (int, optional): Time limit to interact with objects. Defaults to 180.
        disable_on_timeout (bool, optional): Remove all objects from the message when the time is up. Defaults to False.
        items (dict[dict[str|int|bool|function]], optional): Buttons or Selects. Defaults to [].
        
    How to add Items:
        
    {
        "Button" : {
            "style" : discord.ButtonStyle.primary,
            "custom_id" : "si",
            "label" : "sexo",
            "emoji" : discord.Emoji,
            "url" : "https://pagina_cualquiera.com",
            "row" : 1,
            "callback" : function,
            "disabled" : False
        },
        "Select" : {
            "select_type" : discord.ComponentType.string_select,
            "custom_id" : "un_select_bro",
            "placeholder" : "Mira, soy un select",
            "min_values" : 1,
            "max_values" : 2,
            "values" : [1, 2],
            "select_options" : {
                "label" : str
                "value" : str,
                "emoji" : discord.Emoji,
                "description" : str,
            },
            "channel_types" : discord.ChannelTypes,
            "row" : int,
            "add_options" : [
                {
                    "label" : "Texto de la opcion",
                    "value" : "No se presenta a los usuarios",
                    "description" : "descripcion extra a la opcion",
                    "emoji" : discord.Emoji,
                    "default" : bool
                }
            ],
            "callback" : function,
            "disabled" : False
        }
    }
    """

    view = View(timeout=timeout, disable_on_timeout=disable_on_timeout)
    
    for item_type, configs in items.items():
        item_type: str = item_type.upper()
        configs: dict
        
        item: Button|Select
        
        if item_type == "BUTTON":
            item = Button(
                style=configs.pop("style"),
                custom_id=configs.pop("custom_id"), 
                label=configs.pop("label"), 
                emoji=configs.pop("emoji"), 
                url=configs.pop("url"),
                row=configs.pop("row"),
                disabled=configs.pop("disabled")
            )
        elif item_type == "SELECT":
            item = Select(
                select_type=configs.pop("select_type"),
                custom_id=configs.pop("custom_id"),
                placeholder=configs.pop("placeholder"),
                min_values=configs.pop("min_values"),
                max_values=configs.pop("max_values"),
                options=SelectOption(
                    label=configs["select_options"].pop("label"), 
                    value=configs["select_options"].pop("value"),
                    emoji=configs["select_options"].pop("emoji"),
                    description=configs["select_options"].pop("description")
                ) if configs.get("select_options") is not None else None,
                channel_types=configs.pop("channel_types"),
                disabled=configs.pop("disabled"),
                row=configs.pop("row")
            )
            
            try:
                for option in configs["add_options"]:
                    option: dict
                    
                    item.add_option(
                        label=option.pop("label"),
                        value=option.pop("value"),
                        description=option.pop("description"),
                        emoji=option.pop("emoji"),
                        default=option.pop("default")
                    )
            except:
                pass
        else:
            raise Exception("This Item don't exists")
        
        item.callback = configs.pop("callback")
        
        return item
            
    return view