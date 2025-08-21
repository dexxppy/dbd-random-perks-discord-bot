import random
from core.data_funcs import get_row_by_id

def list_depleted(objects_list, exclude_ids):
    if len(objects_list) == len(exclude_ids):
        return True
    
    return False

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
        
    if list_depleted(all_perks_list, exclude_ids):
        return {"random_perks": initial_perk_list, "exclude_ids": exclude_ids}

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

def get_random_character(all_characters_list, character_type, exclude_ids=None, last_drawn_character=None):
    if exclude_ids is None:
        exclude_ids = []
        
    if list_depleted(all_characters_list, exclude_ids):
        return {f"random_{character_type}": last_drawn_character, "exclude_ids": exclude_ids}
        
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
        
    if list_depleted(all_addons_list, exclude_ids):
        return {"random_addons": initial_addons_list, "exclude_ids": exclude_ids}

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

def get_random_item_addon(items_addons_list, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    start = items_addons_list[0].get("survivor_addon_id")
    end = items_addons_list[-1].get("survivor_addon_id")

    addon_id = get_random_id(start, end, exclude_ids)
    return get_row_by_id(items_addons_list, addon_id, "survivor_addon_id")

def get_random_item_addons_set(all_addons_list, initial_addons_list, item_family_name, exclude_ids = None):
    if exclude_ids is None:
        exclude_ids = []
        
    if list_depleted(all_addons_list, exclude_ids):
        return {"random_addons": initial_addons_list, "exclude_ids": exclude_ids}
        
    random_addons = []
    
    start_id = None
    end_id = None
    
    for addon in all_addons_list:
        if addon["survivor_item_family"] == item_family_name and start_id is None:
            start_id = addon["survivor_addon_id"]
        elif start_id is not None and addon["survivor_item_family"] != item_family_name:
            end_id = addon["survivor_addon_id"]
            break
        
    all_addons_list = all_addons_list[start_id-1 : end_id]
        
    if not initial_addons_list:
        while len(random_addons) < 2:
            random_addon = get_random_item_addon(all_addons_list, exclude_ids)
            exclude_ids.append(random_addon["survivor_addon_id"])
            random_addons.append({"replace": False, "addon_data": random_addon})
    else:
        for addon in initial_addons_list:
            if not addon["replace"]:
                random_addons.append({"replace": False, "addon_data": addon["addon_data"]})
            else:
                random_addon = get_random_item_addon(all_addons_list, exclude_ids)
                exclude_ids.append(random_addon["survivor_addon_id"])
                random_addons.append({"replace": False, "addon_data": random_addon})
                
    return {"random_addons": random_addons, "exclude_ids": exclude_ids}

    
def get_random_item_with_addons(all_items_list, all_addons_list, exclude_ids_item = None, exclude_ids_addons = None, last_drawn_item_with_addons = None):
    if exclude_ids_item is None:
        exclude_ids_item = []
        
    if exclude_ids_addons is None:
        exclude_ids_addons = []
        
    if list_depleted(all_items_list, exclude_ids_item):
        return last_drawn_item_with_addons
    
    item_id = get_random_id(1, len(all_items_list), exclude_ids_item)
    exclude_ids_item.append(item_id)
    random_item = get_row_by_id(all_items_list, item_id, "survivor_item_id")
    random_addons_set_data = get_random_item_addons_set(all_addons_list, None, random_item["survivor_item_family"], exclude_ids_addons)
    
    random_addons_set = random_addons_set_data["random_addons"]
    exclude_ids_addons.append(random_addons_set_data["exclude_ids"])
    
    random_item_set = {"item": random_item, "addons": random_addons_set}
    
    return {"random_item_set": random_item_set, "exclude_ids_item": exclude_ids_item, "exclude_ids_addons": exclude_ids_addons}


def get_random_offering(all_offerings_list, exclude_ids=None, last_drawn_offering=None):
    if exclude_ids is None:
        exclude_ids = []
        
    if list_depleted(all_offerings_list, exclude_ids):
        return last_drawn_offering
    
    offering_id = get_random_id(1, len(all_offerings_list), exclude_ids)
    exclude_ids.append(offering_id)
    random_offering = get_row_by_id(all_offerings_list, offering_id, "offering_id")
    
    return {"random_offering": random_offering, "exclude_ids": exclude_ids}

