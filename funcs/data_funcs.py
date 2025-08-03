import json
import os

def get_row_by_id(data, id):
    for item in data:
        if item["id"] == id:
            return item
        
    return None

def map_perks(filepath, champs_filename, perks_filename, column_name_to_map_by):
    champs = []
    perks = []
    mapped_perks = []

    champs_data_path = os.path.join(filepath, f'{champs_filename}.json')
    perks_data_path = os.path.join(filepath, f'{perks_filename}.json')

    with open(champs_data_path, 'r', encoding='utf-8') as f:
        champs = json.load(f)

    with open(perks_data_path, 'r', encoding='utf-8') as f:
        perks = json.load(f)

    for perk in perks:
        mapped_perks.append({
            "id": perk["id"],
            "name": perk["name"],
            "owner_name": get_row_by_id(champs, perk[column_name_to_map_by])["name"]
        })

    return mapped_perks

