import json
import os

def get_row_by_id(data, id):
    for item in data:
        if item["id"] == id:
            return item
        
    return None

def map_perks(champs_filename, champs_perks_filename, column_name_to_map_by):
    champs = []
    champs_perks = []
    mapped_perks = []

    champs_data_path = os.path.join('data', f'{champs_filename}.json')
    champs_perks_data_path = os.path.join('data', f'{champs_perks_filename}.json')

    with open(champs_data_path, 'r', encoding='utf-8') as f:
        champs = json.load(f)

    with open(champs_perks_data_path, 'r', encoding='utf-8') as f:
        champs_perks = json.load(f)

    for perk in champs_perks:
        mapped_perks.append({
            "id": perk["id"],
            "name": perk["name"],
            "owner_name": get_row_by_id(champs, perk[column_name_to_map_by])["name"]
        })

    return mapped_perks

