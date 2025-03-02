import json
from typing import Any
"""
    #creates a new game-state synced with the file.json
    >>> game_state = GameState("path/to/file.json")
    #add portfolio to game state data
    >>> game_state.get_synced_data()['portfolio'] = current_portfolio
    #sync changed data with the file
    >>> game_state.sync()
"""


class GameState:

    def __init__(self, file_path):
        """ :param file_path: path to the json file this GameState instance synchronizes with """
        self.file_path = file_path
        #self.__data - private instance var so only methods belonging to this class can modify data
        self.__data: dict[str, Any] | None = None #internal dict that contains all the synced game state data


    def get_synced_data(self):
        """ :return: The dictionary that contains all important gamestate data """
        # self.__data = self.sync().read(self.file_path)
        return self.__data

    def sync(self):
        """ synchronizes all data with the json-file, specified for this GameState object.
        If the object is initialized, it will load the json-file.
        If the object loaded the json file and was modified, it will store the changes in the json file"""
        


    def _read(self):
        with open(self.file_path, "r") as openfile:
            json_loaded = True
            return json.load(openfile)


    def _write(self):
        with open(self.file_path, "w") as outfile:
            json.dump(self.__data, outfile)