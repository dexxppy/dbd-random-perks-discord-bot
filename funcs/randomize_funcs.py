import random
from funcs.data_funcs import get_row_by_id

def get_random_id(start, end, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    while True:
        random_id = random.randint(start, end)
        if random_id not in exclude_ids:
            return random_id
        
def get_random_perk(all_perks_list, character_type, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    perk_id = get_random_id(1, len(all_perks_list), exclude_ids)
    id_field_name = character_type+"_perk_id"
    return get_row_by_id(all_perks_list, perk_id, id_field_name)


def get_random_perks(all_perks_list, initial_perk_list, character_type, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    random_perks = []
    id_field_name = character_type+"_perk_id"

    if not initial_perk_list:
        while len(random_perks) < 4:
            random_perk = get_random_perk(all_perks_list, character_type, exclude_ids)
            exclude_ids.append(random_perk[id_field_name])
            random_perks.append({"replace": False, "perk_data": random_perk})
    else:
        for perk in initial_perk_list:
            if not perk["replace"]:
                random_perks.append({"replace": False, "perk_data": perk["perk_data"]})
            else:
                random_perk = get_random_perk(all_perks_list, character_type, exclude_ids)
                exclude_ids.append(random_perk[id_field_name])
                random_perks.append({"replace": False, "perk_data": random_perk})

    return {"random_perks": random_perks, "exclude_ids": exclude_ids}

def get_random_character(all_characters_list, character_type, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    random_id = get_random_id(1, len(all_characters_list), exclude_ids)
    random_character = get_row_by_id(all_characters_list, random_id, character_type+"_id")
    exclude_ids.append(random_id)

    return {f"random_{character_type}": random_character, "exclude_ids": exclude_ids}

def get_random_killer_addon(all_addons_list, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    start = all_addons_list[0].get("killer_addon_id")
    end = all_addons_list[-1].get("killer_addon_id")

    addon_id = get_random_id(start, end, exclude_ids)
    return get_row_by_id(all_addons_list, addon_id, "killer_addon_id")


def get_random_killer_addons_set(all_addons_list, initial_addons_list, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    random_addons = []

    if not initial_addons_list:
        while len(random_addons) < 2:
            random_addon = get_random_killer_addon(all_addons_list, exclude_ids)
            exclude_ids.append(random_addon["killer_addon_id"])
            random_addons.append({"replace": False, "addon_data": random_addon})
    else:
        for addon in initial_addons_list:
            if not addon["replace"]:
                random_addons.append({"replace": False, "addon_data": addon["addon_data"]})
            else:
                random_addon = get_random_killer_addon(all_addons_list, exclude_ids)
                exclude_ids.append(random_addon["killer_addon_id"])
                random_addons.append({"replace": False, "addon_data": random_addon})

    return {"random_addons": random_addons, "exclude_ids": exclude_ids}



