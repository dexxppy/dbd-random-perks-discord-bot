import discord
from funcs.randomize_funcs import get_random_item_addons_set

def get_options_for_select(results, object_type, character_type):
    options = [
        discord.SelectOption(
            label=str(item[f"{object_type}_data"][f"{character_type}_{object_type}_name"]), 
            value=str(item[f"{object_type}_data"][f"{character_type}_{object_type}_id"])
        )
        for item in results
    ]
    
    return options

# SetupState = SetupState("survivor")
# addons = SetupState.items_list["addons"]

# random_addons = get_random_item_addons_set(addons, None, "Med Kits")["random_addons"]

# print(get_options_for_select(random_addons, "addon", "survivor"))