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

    killer_id = 1
    killers = []
    perk_id = 1
    perks = []
    addon_id = 1
    # TODO: scrape shared killer perks and pop all killers from

    for row in data:
        killer = {"killer_id": killer_id, "killer_name": row["killer"]}
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
