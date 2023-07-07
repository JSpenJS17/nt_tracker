"""
Author: Pierce Lane
Last Updated: 07/06/2023
Created: 07/01/2023
"""
import tkinter as tk
import config
import time

from requests import get



class Crowns_Manager:
    """This class manages the tkinter window that displays the current crown 
    data."""
    def __init__(self, char_dict):
        """Sets up the window and stores resource and window data"""
        print("Instantiating window manager...")
        #the order of the crown data is different than the order that they are
        #displayed in game. risk and luck are swapped.
        self._display_crown_order = [
                                     'death', 'life', 'haste', 'guns', 
                                     'hatred', 'blood','destiny', 'love',
                                     'luck', 'curses', 'risk', 'protection'
                                    ]

        self._data_crown_order =    [
                                     'death', 'life', 'haste', 'guns', 
                                     'hatred', 'blood', 'destiny', 'love', 
                                     'risk', 'curses', 'luck', 'protection'
                                    ]

        #the character names in the order they appear in game
        self._char_names = [
                            "Fish",
                            "Crystal",
                            "Eyes",
                            "Melting",
                            "Plant",
                            "Y.V.",
                            "Steroids",
                            "Robot",
                            "Chicken",
                            "Rebel",
                            "Horror",
                            "Rogue"
                           ]

        #has all of the save data
        self._char_data = char_dict
        #the current character that we're displaying
        self._cur_char = 1
        self._cur_char_name = tk.Label(root, text = self._char_names[0])
        self._cur_char_name.config(font = ("Arial", 20, "bold"))
        self._cur_char_name.grid(row = 0, column = 1)

        #will store references to the crown images
        self._blk_images = {}
        self._reg_images = {}

        #will store references to the buttons and their states
        self._crown_images = {}


        crown_index = 0
        for row in range(3):
            for col in range(4):
                #grab the crown name from the display order
                crown = self._display_crown_order[crown_index]

                #find the black image of the crown and store it
                img_blk = tk.PhotoImage(file = f"resources\\{crown}_black.png")
                self._blk_images[crown] = img_blk

                #find the regular image and store it
                img_reg = tk.PhotoImage(file = f"resources\\{crown}.png")
                self._reg_images[crown] = img_reg

                #create the images with the crown_black images on them
                crown_image = tk.Label(root, image = img_blk, 
                                       width = 160, height = 160)
                crown_image.grid(row = row+1, column = col+1)

                #store them and their black or not state for later use
                self._crown_images[crown] = [crown_image, 0]

                crown_index += 1

    def _display_page(self):
        """Displays the current selected page"""

        char_crowns = self._char_data[self._cur_char]
        for crown_index in range(12):
            set_to = char_crowns[crown_index]
            crown_name = self._display_crown_order[crown_index]
            cur_at = self._crown_images[crown_name][1]
            if set_to != cur_at:
                values = self._crown_images[crown_name]
                cur_state = values[1]
                if cur_state == 0:
                    values[0].config(image=self._reg_images[crown_name])
                    values[1] = 1
                else:
                    values[0].config(image=self._blk_images[crown_name])
                    values[1] = 0

    def update_char_data(self, new_char_dict):
        """Update the crown data in the class crown dictionary"""
        self._char_data = new_char_dict

    def change_page(self, char_num):
        """Changes pages to the page of the character associated with the
        number given. Valid numbers are 1-12"""
        if char_num:
            self._cur_char = char_num
        else:
            self._cur_char = 1

        self._cur_char_name.config(text = self._char_names[self._cur_char-1])
        self._display_page()

def get_char_dict():
    """Grabs the user's NT save data based on the path given in config.py
    Does some manipulation to get the character crown data into a dictionary.
    
    #NOTE: there is probably a faster way to do this, but it only runs every
    15 seconds so I didn't optimize it."""
    print("Getting save data...")
    save_string = ""
    try:
        with open(config.save_file_path, "r") as file:
            for line in file:
                save_string += line
    except FileNotFoundError:
        raise FileNotFoundError(f"No save data at path {config.save_file_path}")

    in_brackets = False
    char_index = 0
    crowns_data = [""]
    for char in save_string:
        if char == "[":
            in_brackets = True
            continue

        elif char == "]":
            in_brackets = False
            crowns_data[char_index] = crowns_data[char_index].strip()
            char_index += 1
            crowns_data.append("")
            continue

        if in_brackets:
            crowns_data[char_index] += char
    crowns_data.pop(-1)


    char_order = [4, 2, 6, 8, 15, 11, 17, 13, 5, 1, 9, 7, 3, 10, 14, 12, 16]
    char_dict = {}
    for char_index, char_data in enumerate(crowns_data):
        char_data = char_data.split(", ")
        char_data = char_data[2:]

        for index, crown in enumerate(char_data):
            char_data[index] = int(float(crown))
            
        crowns_data[char_index] = char_data
        char_dict[char_order[char_index]] = crowns_data[char_index]
        
    for char_num in char_order:
        if char_num >= 13:
            char_dict.pop(char_num)

    return char_dict

def callback():
    """Callback function for when the window is closed. Needs to tell the main
    while loop to stop and also close the window."""
    global quitting_time
    print("Quitting...")
    root.destroy()
    quitting_time = True
    
def get_cur_char_num(url):
    """Returns the characer number that is currently being used in the run
    If no character is selected, defaults to Fish"""
    print("Getting current player character data...")
    cur_char_num = get(url).json()["current"]
    if not cur_char_num:
        cur_char_num = 1
        print("No player character data found, defaulting to 1")
    else:
        cur_char_num = cur_char_num["char"]
        print(f"Player character data retrieved successfully, player character is: {cur_char_num}")

    return cur_char_num

quitting_time = False
root = tk.Tk()
root.title("NT Crown Tracker")
root.protocol("WM_DELETE_WINDOW", callback)

def main():
    #the api url based on their IDs in config.py
    url = f"https://tb-api.xyz/stream/get?s={config.steam_ID}&key={config.game_stream_ID}"

    #the dictionary containing each character and their crown unlocks
    char_dict = get_char_dict()
    #the current character number being broadcast to the url
    cur_char_num = get_cur_char_num(url)

    #window manager
    crowns_manager = Crowns_Manager(char_dict)
    #change pages to the current character's page
    crowns_manager.change_page(cur_char_num)

    #set times for measuring when 15 seconds have passed
    start_time = time.time()
    cur_time = time.time()

    print("Running main loop...")
    #loop until the window callback on destroy sets quitting_time to False
    while not quitting_time:
        #update the current time
        cur_time = time.time()

        #if 15 seconds have passed
        if cur_time - start_time >= 15:
            print("Updating window...")
            #grab the current character number
            cur_char_num = get_cur_char_num(url)
            #set a new starting time
            start_time = time.time()
            #update the crown data to the current data in the save file
            crowns_manager.update_char_data(get_char_dict())
            #change pages if needed
            crowns_manager.change_page(cur_char_num)

        #update the window every .25 seconds, so that closing it doesn't take up
        #to 15 seconds to happen
        root.update()
        time.sleep(.25)


if __name__ == "__main__":
    main()

