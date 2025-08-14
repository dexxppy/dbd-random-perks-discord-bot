import json
import os

def get_row_by_id(data, id, id_field_name):
    for item in data:
        if item[id_field_name] == id:
            return item
        
    return None

def get_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

def get_survivor_data():
    path = "data/survivor/survivors_list.json"
    data = get_data(path)

    survivor_id = 0
    survivors = []
    perk_id = 1
    perks = []

    for row in data:
        survivors.append({"survivor_id": survivor_id, "survivor_name": row["survivor_name"]})
        survivor_id += 1
        for perk in row["survivor_perks"]:
            perks.append({"survivor_perk_id": perk_id, "survivor_perk_name": perk,
                          "survivor_owner_name": row["survivor_name"]})
            perk_id += 1

    del survivors[0]
    return {"survivors": survivors, "perks": perks}


def get_killer_data():
    path = "data/killer/killers_list.json"
    data = get_data(path)

    killer_id = 0
    killers = []
    perk_id = 1
    perks = []
    addon_id = 1

    for row in data:
        killer = {"killer_id": killer_id, "killer_name": row["killer_name"]}
        killer_id += 1

        for perk in row["killer_perks"]:
            perks.append({"killer_perk_id": perk_id, "killer_perk_name": perk,
                          "killer_owner_name": row["killer"]})
            perk_id += 1

        addons = []
        for addon in row["killer_addons"]:
            addons.append({"killer_addon_id": addon_id, "killer_addon_name": addon["addon_name"],
                            "killer_addon_rarity": addon["addon_rarity"]})
            addon_id += 1

        killer["killer_addons"] = addons
        killers.append(killer)

    return {"killers": killers, "perks": perks}


def get_items_data():
    path = 'data/item/items_list.json'
    data = get_data(path)
    
    item_id = 1
    items = []
    addon_id = 1
    addons = []
    
    for row in data:
        family_name = row["item_family"]
        
        for item in row["items"]:
            items.append({"item_id": item_id, "item_name": item["item_name"],
                          "item_rarity": item["item_rarity"], "item_family": family_name})
            item_id += 1
            
        for addon in row["addons"]:
            addons.append({"addon_id": addon_id, "addon_name": addon["addon_name"],
                          "addon_rarity": addon["addon_rarity"], "item_family": family_name})
            addon_id += 1
            
    return {"items": items, "addons": addons}


def get_offering_data():
    path = 'data/offering/offerings_list.json'
    data = get_data(path)
    
    killer_offering_id = 1
    killer_offerings = []
    survivor_offering_id = 1
    survivor_offerings = []
    
    for row in data:
        if row["character_type"] == "All":
            for offering in row["offerings"]:
                killer_offerings.append({"offering_id": killer_offering_id, "offering_name": offering["offering_name"],
                                         "offering_rarity": offering["offering_rarity"]})
                killer_offering_id += 1
                
                survivor_offerings.append({"offering_id": survivor_offering_id, "offering_name": offering["offering_name"],
                                         "offering_rarity": offering["offering_rarity"]})
                survivor_offering_id += 1
        elif row["character_type"] == "Killer":
            for offering in row["offerings"]:
                killer_offerings.append({"offering_id": killer_offering_id, "offering_name": offering["offering_name"],
                                         "offering_rarity": offering["offering_rarity"]})
                killer_offering_id += 1
        elif row["character_type"] == "Survivor":
            for offering in row["offerings"]:
                survivor_offerings.append({"offering_id": survivor_offering_id, "offering_name": offering["offering_name"],
                                         "offering_rarity": offering["offering_rarity"]})
                survivor_offering_id += 1

    return {"killer_offerings": killer_offerings, "survivor_offerings": survivor_offerings}
