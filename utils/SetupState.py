from funcs.data_funcs import get_killer_data, get_survivor_data, get_items_data, get_offerings_data

class SetupState:
    def __init__(self, user_id):
        self.user_id = user_id
        self.character = None
        self.perks = []
        self.item = {}
        self.killer_addons = []
        self.offering = None
                

        