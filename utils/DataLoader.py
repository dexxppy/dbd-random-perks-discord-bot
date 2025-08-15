from funcs.data_funcs import get_killer_data, get_survivor_data, get_items_data, get_offerings_data

class DataLoader:
    def __init__(self, character_type):
        self.character_type = character_type
        self._characters_list = None
        self._perks_list = None
        self._items_list = None
        self._offerings_list = None
        
        self._data_loader = {
            "killer": get_killer_data,
            "survivor": get_survivor_data
        }.get(self.character_type)
        
        if self._data_loader is None:
            raise ValueError(f"Unknown character type: {self.character_type}")
        
    @property
    def perks_list(self):
        if self._perks_list is None:
            data = self._data_loader()
            self._characters_list = data[f"{self.character_type}s"]
            self._perks_list = data["perks"]
            
        return self._perks_list
    
    @property
    def characters_list(self):
        if self._characters_list is None:
            _ = self.perks_list
            
        return self._characters_list
    
    @property
    def items_list(self):
        if self._items_list is None:
            self._items_list = get_items_data()
            
        return self._items_list
    
    @property
    def offerings_list(self):
        if self._offerings_list is None:
            self._offerings_list = get_offerings_data()
            
        return self._items_list