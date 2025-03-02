import json
from typing import Any
import os
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

        # self.__data = self.sync().read(self.file_path)
        if not self.__data:
            self.sync()
        return self.__data

    def sync(self):
        """ synchronizes all data with the json-file, specified for this GameState object.
        If the object is initialized, it will load the json-file.
        If the object loaded the json file and was modified, it will store the changes in the json file"""

        if not self.__data:
            self.__data = self.__read()
            self.__starting_data = self.__data

        #if changes have been made (our data is different to when we started) write to json
        if self.__starting_data != self.__data:
            #TODO != only does a shallow comparison and doesn't keep track of changes YOU NEED TO GOOGLE THIS NEXT
            # STREAM
            self.__write()
            self.__starting_data = self.__data

    def update(self):
        #info from Sora on last stream
        def __update(self, new_data):
            if self.__data:
                tmp_dict = self.__data
                for k, v in new_data.items():  # k(ey), v(alue)
                    tmp_dict[k] = v

                self.__data = tmp_dict
            else:
                self.__data = new_data

            self.__write()


    def __read(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as openfile:
                return json.load(openfile)
        else:
            empty_dict = {}
            with open(self.file_path, "w") as outfile:
                json.dump(empty_dict, outfile)

#INFO what you want to do: 1. grab json data 2. create a dict from that data
# 3. update json keys as wanted 4. save new json into file


    def __write(self):
        with open(self.file_path, "w") as outfile:
            json.dump(self.__data, outfile)
