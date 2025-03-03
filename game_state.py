import json
from typing import Any
import os
from copy import deepcopy
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
        self.__starting_data = None


    def get_synced_data(self):
        """ :return: The dictionary that contains all important gamestate data """
        #INFO every time you change something you modify self.__data, when the game is closed we call sync
        # any time you want to read/write you call get_synced_data

        if not self.__data:
            self.sync()
        return self.__data

    def sync(self):
        """ synchronizes all data with the json-file, specified for this GameState object.
        If the object is initialized, it will load the json-file.
        If the object loaded the json file and was modified, it will store the changes in the json file"""

        if not self.__data:
            # myvar = self.__read()
            self.__data = self.__read()
            self.__starting_data = deepcopy(self.__data)

        #if changes have been made (our data is different to when we started) write to json
        if self.__starting_data != self.__data:
            # self.__data = self.portfolio
            self.__write()
            self.__starting_data = deepcopy(self.__data)


    def __read(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as openfile:
                return json.load(openfile)
        else:
            empty_dict = {}
            with open(self.file_path, "w") as outfile:
                json.dump(empty_dict, outfile)


    def __write(self):
        with open(self.file_path, "w") as outfile:
            json.dump(self.__data, outfile)
