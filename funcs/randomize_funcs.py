import random
from funcs.data_funcs import get_row_by_id, map_perks

def get_random_id(start, end, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    while True:
        random_id = random.randint(start, end)
        if random_id not in exclude_ids:
            return random_id
        
def get_random_perk(all_perks_list, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    perk_id = get_random_id(1, len(all_perks_list), exclude_ids)
    return get_row_by_id(all_perks_list, perk_id)


def get_random_perks(all_perks_list, initial_perk_list, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    random_perks = []

    if not initial_perk_list:
        while len(random_perks) < 4:
            random_perk = get_random_perk(all_perks_list, exclude_ids)
            exclude_ids.append(random_perk["id"])
            random_perks.append({"replace": False, "perk_data": random_perk})
    else:
        for perk in initial_perk_list:
            if not perk["replace"]:
                random_perks.append({"replace": False, "perk_data": perk["perk_data"]})
            else:
                random_perk = get_random_perk(all_perks_list, exclude_ids)
                exclude_ids.append(random_perk["id"])
                random_perks.append({"replace": False, "perk_data": random_perk})

    return {"random_perks": random_perks, "exclude_ids": exclude_ids}

