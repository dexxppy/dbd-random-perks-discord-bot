import discord


def get_options_for_select(results, object_type, character_type):
    options = [
        discord.SelectOption(
            label=str(item[f"{object_type}_data"][f"{character_type}_{object_type}_name"]), 
            value=str(item[f"{object_type}_data"][f"{character_type}_{object_type}_id"])
        )
        for item in results
    ]
    
    return options