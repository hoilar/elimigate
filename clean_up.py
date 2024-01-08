import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage, CTkToplevel, CTkTextbox
from PIL import Image
from datetime import datetime
from tooltipimage import ToolTipImage as TTI
#from tktooltip import ToolTip
import random, pyaudio, wave, threading, sys
from collections import Counter
from constants import (
    profiles, 
    player_items, enemy_items, 
    card_images_d, card_images_h, card_images_p, card_images_i
)


# TODO Add logging to the game (mostlty done)
# TODO Add game logic (basics done)
# TODO Add game logic to GUI (basics done)
# TODO Add testing to game logic (mocking?)
# TODO Add sound effects // threading
# TODO Add background music
# TODO Add game win/lose
# TODO Add game win/lose to GUI
# TODO Add options menu
# TODO Add options menu to GUI
# TODO Add resulution options (This gonna be a nightmare)
# TODO Add animation (tkinters root.after) // scrap? 

class StyleGame:
    def __init__(self):
        self.bg_color = "#242426"
        self.fg_color = "#242426"
        self.font = ("Courier", 10, "bold")
        self.font_small = ("Courier", 8, "bold")
        self.font_large = ("Courier", 12, "bold")
        self.font_xlarge = ("Courier", 14, "bold")
        self.font_xxlarge = ("Courier", 16, "bold")
        self.font_xxxlarge = ("Courier", 20, "bold")
        self.font_xxxxlarge = ("Courier", 48, "bold")
        self.main_color = "transparent" # "red" for testing / "transparent"
        self.fill_color = "transparent" # "yellow" for testing / "transparent"
        self.center_color = "transparent" # "green" for testing / "transparent"

class ImageResizer: # TODO resize images to fit screen
    def __init__(self):
        pass

    @staticmethod 
    def delt(imagefile_url):
        image_width = 1627 / 2
        image_height = 121 / 2
        size = (image_width, image_height)  

        image = CTkImage(Image.open(imagefile_url), None, size)
        return image

    @staticmethod 
    def game_name(imagefile_url):
        image_width = 1667 / 2
        image_height = 150 / 2
        size = (image_width, image_height)  

        image = CTkImage(Image.open(imagefile_url), None, size)
        return image

    @staticmethod
    def main_bg(imagefile_url):
        # calculate scaling of indivdual resolutions
        image_width = 1600 
        image_height = 1100 
        size = (image_width, image_height)

        image = CTkImage(Image.open(imagefile_url), None, size)
        return image

    @staticmethod
    def side_bar(imagefile_url):
        # calcultate scaling of indivdual resolutions
        image_width = 290
        image_height = 330
        size = (image_width, image_height)

        image = CTkImage(Image.open(imagefile_url), None, size)
        return image
    
    @staticmethod
    def witnesses(imagefile_url):
        # calcultate scaling of indivdual resolutions
        image_width = 568
        image_height = 330
        size = (image_width, image_height)

        image = CTkImage(Image.open(imagefile_url), None, size)
        return image

    @staticmethod
    def examination(imagefile_url):
        # calcultate scaling of indivdual resolutions
        image_width = 890
        image_height = 330
        size = (image_width, image_height)

        image = CTkImage(Image.open(imagefile_url), None, size)
        return image
    
    @staticmethod
    def waiting_room(imagefile_url):
        # calcultate scaling of indivdual resolutions
        image_width = 890
        image_height = 330
        size = (image_width, image_height)

        image = CTkImage(Image.open(imagefile_url), None, size)
        return image

    @staticmethod 
    def card(imagefile_url):
        image_width = 140
        image_height = 210
        size = (image_width, image_height)  

        image = CTkImage(Image.open(imagefile_url), None, size)
        return image
    
    @staticmethod 
    def exit(imagefile_url):
        image_width = 180
        image_height = 180
        size = (image_width, image_height)  

        image = CTkImage(Image.open(imagefile_url), None, size)
        return image

class Sound:
    def __init__(self, file_path):
        self.chunk = 1024
        self.p = pyaudio.PyAudio()
        self.file_path = file_path
        self.stop_event = threading.Event()

    def play_sound(self):
        def play():
            f = wave.open(self.file_path, "rb")
            stream = self.p.open(
                format=self.p.get_format_from_width(f.getsampwidth()),
                channels=f.getnchannels(),
                rate=f.getframerate(),
                output=True
            )
            data = f.readframes(self.chunk)

            while data and not self.stop_event.is_set():
                stream.write(data)
                data = f.readframes(self.chunk)

            stream.stop_stream()
            stream.close()

        sound_thread = threading.Thread(target=play)
        sound_thread.start()

    def stop_sound(self):
        self.stop_event.set()

class Utils:
    def __init__(self, log_center_textbox):
        self.log_center_textbox = log_center_textbox

    def log(self, text):
        time_now = datetime.now()
        current_time = time_now.strftime("%H:%M:%S")
        self.log_center_textbox.configure("0.0", state="normal") 
        self.log_center_textbox.insert("0.0", f"{current_time}: {text}\n")
        self.log_center_textbox.configure("0.0", state="disabled")

    def get_perp(self):
        perp_got = self.random_perpetrator 
        return perp_got

    def ToolTipButton(button, key, type):
        sg = StyleGame()

        def tool_tip(key, data_source):
            type_info = data_source.get(key, None) # Find profile
            if type_info:
                return type_info.get("tooltip", None) # Find card-tooltip to profile
            else:
                return None

        if type == "profile": #! Replace image _delt with ToolTip Image for each profile
            TTI(button, msg=lambda: tool_tip(key, profiles), image_path=f"images/profiles/{key}_tt.png", image_size=(210,315), delay=0.2,
                parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                fg="#ffffff", bg="#1c1c1c", font=sg.font, padx=10, pady=10)

            #! Replace with this for text. Maybe replace this class with TTI? (Text will then align center)
            #ToolTip(button, msg=lambda: tool_tip(key, profiles), delay=0.2,
            #    parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
            #    fg="#ffffff", bg="#1c1c1c", font=sg.font, padx=10, pady=10)
            
        elif type == "player_item":
            TTI(button, msg=lambda: tool_tip(key, player_items), delay=0.2,
                parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                fg="#ffffff", bg="#1c1c1c", font=sg.font, padx=10, pady=10)
        
        elif type == "enemy_item":
            TTI(button, msg=lambda: tool_tip(key, enemy_items), image_path=f"images/items/e_{key}_tt.png", image_size=(200,200), delay=0.2,
                parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                fg="#ffffff", bg="#1c1c1c", font=sg.font, padx=10, pady=10)

class Bind:
    def __init__(self):
        pass
    
    def enter_d(event, name, card, card_images):
        card_img = ImageResizer.card(card_images[f"{name}_delt_hov.png"])
        card.configure(image=card_img, fg_color="transparent")

    def leave_d(event, name, card, card_images):
        card_img = ImageResizer.card(card_images[f"{name}_delt.png"])
        card.configure(image=card_img, fg_color="transparent")

    def enter_h(event, name, card, card_images):
        card_img = ImageResizer.card(card_images[f"{name}_hand_hov.png"])
        card.configure(image=card_img, fg_color="transparent")

    def leave_h(event, name, card, card_images):
        card_img = ImageResizer.card(card_images[f"{name}_hand.png"])
        card.configure(image=card_img, fg_color="transparent")

    def enter_p(event, name, card, card_images):
        card_img = ImageResizer.card(card_images[f"{name}_play_hov.png"])
        card.configure(image=card_img, fg_color="transparent")

    def leave_p(event, name, card, card_images):
        card_img = ImageResizer.card(card_images[f"{name}_play.png"])
        card.configure(image=card_img, fg_color="transparent")

    def enter_i(event, name, card, card_images):
        card_img = ImageResizer.card(card_images[f"{name}_hov.png"])
        card.configure(image=card_img, fg_color="transparent")

    def leave_i(event, name, card, card_images):
        card_img = ImageResizer.card(card_images[f"{name}.png"])
        card.configure(image=card_img, fg_color="transparent")

    def onEnter_end_day(event, end_day):
        img_btn_end = ImageResizer.exit(f"images/gui/btn_endH.png")
        end_day.configure(image = img_btn_end)

    def onLeave_end_day(event, end_day):
        img_btn_end = ImageResizer.exit(f"images/gui/btn_end.png")
        end_day.configure(image = img_btn_end)

    def onButton1_end_day(event, end_day):
        img_btn_end = ImageResizer.exit(f"images/gui/btn_endP.png")
        end_day.configure(image = img_btn_end)

    def onButtonRelease_end_day(event, end_day):
        img_btn_end = ImageResizer.exit(f"images/gui/btn_end.png")
        end_day.configure(image = img_btn_end)

class CardGame:
    def __init__(self):
        

        # Main window
        self.app = CTk()
        self.width = self.app.winfo_screenwidth()
        self.height = self.app.winfo_screenheight()

        #self.width = 1600 #! For testing
        #self.height = 1250 #! For testing

        self.app.geometry(f"{self.width}x{self.height}+0+0")
        self.app.title("Game title")
        self.app.attributes('-fullscreen', True)
        self.app.iconbitmap("images/GUI/ic.ico")

        self.app.iconify() # iconifies the window. Opens when cards are selected add_profiles_to_waiting_room

        # Game stats
        self.stats()

        # Lists and dictionaries
        self.lists_and_dicts()

        # Welcome window and create 5 profiles to choose from
        self.welcome_window()

        # Days left window
        self.days_left_window()
        self.days_left_level.withdraw()

        # Main board setup
        self.board_main()
        self.board_left()
        self.board_middle()
        self.board_right()
        
        # Populate board
        self.create_crime_scene("crime", "no") # Crime scene image
        self.create_random_witnesses() # Create witnesses
        self.create_new_item_in_locker() # Create new item in locker

        Utils(self.log_center_textbox) # Send log_center_textbox to Utils
        Utils.log(self, "Game started!") # Log welcome message

        # Won window
        self.won_window()
        self.won_splash_window.withdraw()

        # Start game
        self.app.mainloop()
    
    #def screen_size(self):
    #    self.width = self.app.winfo_screenwidth()
    #    self.height = self.app.winfo_screenheight()
    #    return self.width, self.height

    #? GAME STATS, LISTS AND DICTS
    def stats(self): # Called from main | # GAME STATS TO BE USED IN GAME LOGIC

        # Days stats
        self.days_left = 50

        # Action points stats
        self.ap_left = 2 # Action points
        self.ap_adjust = False #! Not in use

        self.sap_left = 0 # Special action points
        self.sap_adjust = False #! Not in use

        self.ap_cost_player_item = 1 # How many action points does it cost to play item
        self.sap_cost_player_special_item = 5 # How many action points does it cost to play special item

        self.ap_cost_examination = 1 # How many action points does it cost to play examination
        self.ap_cost_witness = 0 # How many action points does it cost to play witness

        # Profiles at start stats
        self.delt_profiles_max = 5 # How many cards to choose from at the beginning. Called from create_random_profiles
        self.start_profiles_max = 3 # How many cards that can be selected. Called from add_profiles_to_waiting_room

        # Waiting room stats
        self.waiting_room_max = 3 # How many cards can be in waiting room . Called from add_new_profile_to_waiting_room

        # Examinations stats
        self.examination_max = 3 # How many cards can be in examination. Called from add_profiles_to_examination

        # Witnesses stats
        self.witnesses_max = 3 # (3 is max.) How many witnesses can be in witnesses. Called from create_random_witnesses
        self.witnesses_points_max = 1 #! (4 max. 4=3, get 1 ekstra point at creation). How many witness points to identify perpetrator. Called from perpetrator_identified

        # Perpetrator stats
        self.perpetrator_active = False # Is perpetrator active. Called from multiple
        self.perpetrator_max = 3 # (4 max. 4=3, get 1 ekstra point at creation). How many perpetrator points can be in perpetrator. Called from perpetrator_identified
        self.ap_cost_profile_to_perpetrator = 0 # How many action points does it cost to play perpetrator. Called from witness_actions
        self.perpetrator_item_adjust = [0, 1] # If 1 keep item next round, if 0 perpetrator plays new item
        self.perpetrator_item_weight = [30, 70] # Chance in percent that perpetrator plays new item
        self.perpetrator_item_plays = 0 # How many times perpetrator have played the same item in row
        self.perpetrator_item_max_plays = 3 # How many times perpetrator can play same item in a row
       
    def lists_and_dicts(self): # Called from main

        # Profile lists and dictionaries
        self.choosen_profiles_list = [] # List of choosen profiles
        self.choosen_profiles_button_dict = {} # Button-name TK to forget.pack

        self.waiting_room_list = [] # List of waiting room profiles
        self.waiting_room_profiles_button_dict = {} # Button-name TK to forget.pack

        self.examination_list = [] # List of examination profiles
        self.examination_profiles_button_dict = {} # Button-name TK to forget.pack

        self.witnesses_list = [] # List of witnesses
        self.witnesses_start_list = [] # List of start witnesses
        self.witnesses_button_to_dict = {} # Button-name TK to forget.pack

        self.perpetrator_list = [] # List of perpetrator-points

        # Item lists and dictionaries
        self.player_locker_item = "" # Locker item
        self.player_locker_item_button = None # Locker item button
        self.player_locker_item_button_to_dict = {} # Button-name TK to forget.pack

        self.player_item_active = "" # Active item
        self.player_item_active_button = None # Active item button
        self.player_item_active_button_to_dict = {} # Button-name TK to forget.pack

        self.player_special_item_active = "" # Active special item
        self.player_special_item_active_button = None # Active speical item button
        self.player_special_item_active_button_to_dict = {} # Button-name TK to forget.pack

        self.enemy_item_active = "" # Active enemy item
        self.enemy_item_active_button = None # Active enemy item button
        self.enemy_item_active_button_to_dict = {} # Button-name CTK to forget.pack

    #? GAME ACTIONS
    def end_day_actions(self):# Called from board_right

        # Add a new card to waiting room
        self.add_new_profile_to_waiting_room()

        # Add new item to locker
        self.create_new_item_in_locker()
        # add new active enemy item

        # Reset action points
        self.ap_left = 2
        self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")

        # STANDARD ITEM MATCH - != "hat" or "mail" or "note" SPECIAL ITEMS
        if self.player_special_item_active != "hat" or self.player_special_item_active != "mail" or self.player_special_item_active != "note":
            for profile in self.examination_list: # Check if item is in examination, then add one action
                if profiles[profile]['playitem'] in player_items and player_items[profiles[profile]['playitem']]['type'] == 'item' and profiles[profile]['playitem'] == self.player_item_active:
                    self.ap_left += 1
                    self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}") # Update actions left label  

        # Deduct days left
        self.days_left -= 1
        self.days_left_text.configure(text=f"Days left: {self.days_left}")

        # Play sound
        Sound("wav/end_day.wav").play_sound()

        # Check if perpetrator is identified
        self.perpetrator_identified()

        # Add new enemy item if perpetrator is active
        if self.perpetrator_active :
            if self.perpetrator_item_plays >= self.perpetrator_item_max_plays or random.choices(self.perpetrator_item_adjust, self.perpetrator_item_weight, k=1)[0] == 0:
                self.create_enemy_item()
                self.perpetrator_item_plays = 0
            else:
                self.perpetrator_item_plays += 1
                Utils.log(self, f"Perpetrator keeps item") # Log
        
        # Perpetrator item actions
        self.perpetrator_item_actions()

        # Special item actions
        self.player_special_item_actions()

        # End day pop-up window
        self.days_left_popup() 

    def examinations_actions(self, profile_name): # Called from add_profiles_to_examination
        if len(self.examination_list) < self.examination_max:
            if self.ap_left >= self.ap_cost_examination:
                self.ap_left -= self.ap_cost_examination
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
                Utils.log(self, f"{str(profile_name).capitalize()} to examination") # Log
                return True
            else:
                Utils.log(self, f"Not enough AP: {str(profile_name).capitalize()}") # Log  
                Sound("wav/fail.wav").play_sound()
                return False
        else:
            Utils.log(self, f"Examination-room full: {str(profile_name).capitalize()}") # Log  
            Sound("wav/fail.wav").play_sound()

    def witness_actions(self, profile_name): # Called from add_profiles_to_examination
        ir = ImageResizer()
        

        if self.perpetrator_active == False: # If perpetrator is not active
            if self.ap_left >= self.ap_cost_witness:
                self.ap_left -= self.ap_cost_witness
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")

                self.examination_list.remove(profile_name) # Update list for further referance
                self.examination_profiles_button_dict[profile_name].pack_forget() # remove profile from examination


                Sound("wav/card.wav").play_sound()

                count = self.witnesses_list.count(profile_name)
                if profile_name in self.witnesses_list:
                    if 1 <= count < self.witnesses_points_max:
                        self.witnesses_list.append(profile_name) # Add witness to list
                        new_image = f"images/profiles/{profile_name}_w{count}.png"
                        self.witnesses_button_to_dict[profile_name].configure(image=ir.card(new_image))
                        Utils.log(self, f"{str(profile_name).capitalize()} is added to witness") # Log
                        Sound("wav/swosh.wav").play_sound()
                    else:
                        Utils.log(self, f"Witness is full, {str(profile_name).capitalize()}") # Log
                else:
                    Utils.log(self, f"{str(profile_name).capitalize()} not in witnesses-list") # Log #! Should not go trough, self.perpetrator_active == True
            else:
                Utils.log(self, f"Not enough AP: {str(profile_name).capitalize()}") # Log
                Sound("wav/fail.wav").play_sound()

        elif self.perpetrator_active == True: # If perpetrator is active

            self.examination_list.remove(profile_name) # Update list for further referance
            self.examination_profiles_button_dict[profile_name].pack_forget() # remove profile from examination

            count = self.perpetrator_list.count(profile_name)
            if profile_name == self.random_perpetrator:
                if 1 <= count < self.perpetrator_max:
                    self.perpetrator_list.append(profile_name) # Add perpetrator to list
                    new_image = f"images/profiles/{profile_name}_s{count}.png" # TODO Add more perpetrator images, so can count higher?
                    self.crime.configure(image=ir.card(new_image))
                    if self.ap_left >= self.ap_cost_profile_to_perpetrator: # If profile is perpetrator, deduct two action points
                        self.ap_left -= self.ap_cost_profile_to_perpetrator
                        self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
                    Utils.log(self, f"{str(profile_name).capitalize()} is perpetrator") # Log
                else:
                    Utils.log(self, f"you won!") # Log
                    self.won_window()
            else:
                self.sap_left += 1
                self.special_action_points_left_text.configure(text=f"Special AP: {self.sap_left}")
                if self.ap_left >= self.ap_cost_witness: # If profile is not perpetrator, deduct one action point
                    self.ap_left -= self.ap_cost_witness
                    self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
                Utils.log(self, f"{str(profile_name).capitalize()} not perpetrator") # Log

        self.profile_item_actions(profile_name) # Called from player_item_actions

    def player_item_actions(self, item_name): # Called from add_profiles_to_examination
        # Item type sort and action points deduction
        if player_items[item_name]['type'] == 'item':
            if self.ap_left >= self.ap_cost_player_item:
                self.ap_left -= self.ap_cost_player_item
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
                self.new_player_item_active(item_name)
                Utils.log(self, f"{str(item_name).capitalize()} is active") # Log
            else:
                Utils.log(self, f"Not enough AP: {str(item_name).capitalize()}") # Log   
        elif player_items[item_name]['type'] == 'special':
            if self.sap_left >= self.sap_cost_player_special_item:
                self.sap_left -= self.sap_cost_player_special_item
                self.special_action_points_left_text.configure(text=f"Special AP: {self.sap_left}")
                self.new_player_special_item_active(item_name)
                Utils.log(self, f"{str(item_name).capitalize()} is active") # Log
            else:
                Utils.log(self, f"Not enough AP: {str(item_name).capitalize()}") # Log     

    def profile_item_actions(self, profile_name): # Called from player_item_actions # TODO Add profile item actions
        ir = ImageResizer()
        profile_name = profile_name
        

        # Special item whiskey reversed
        if self.player_special_item_active == "whiskey": 
            item_type = "handitem"
        else:
            item_type = "playitem"


        # BATON - New profile to waiting room if room is not full
        if profiles[profile_name][f'{item_type}'] == "baton":
            if self.ap_left >= 1: # Total AP needed cost for this item-action
                self.ap_left -= 1 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
                self.add_new_profile_to_waiting_room()

        # DAGGER - Add witness-point 
        if profiles[profile_name][f'{item_type}'] == "dagger":
            if self.ap_left >= 3: # Total AP needed cost for this item-action
                self.ap_left -= 3 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
                
                if self.perpetrator_active == False:
                    witness_name = random.choice(self.witnesses_start_list)
                    count = self.witnesses_list.count(witness_name)
                    while count >= self.witnesses_points_max:
                        witness_name = random.choice(self.witnesses_start_list)
                    else:
                        self.witnesses_list.append(witness_name)
                        new_image = f"images/profiles/{witness_name}_w{count}.png"
                        self.witnesses_button_to_dict[witness_name].configure(image=ir.card(new_image))
                        Utils.log(self, f"{str(witness_name).capitalize()} is added to witness") # Log
                
                elif self.perpetrator_active == True:
                    self.sap_left += 1
                    self.special_action_points_left_text.configure(text=f"Special AP: {self.sap_left}")

        # GOGGLES - Resets Special AP to 3
        if profiles[profile_name][f'{item_type}'] == "goggles":
            if self.ap_left >= 1: # Total AP cost for this item-action
                self.ap_left -= 1 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
            
                self.sap_left = 3
                self.special_action_points_left_text.configure(text=f"Special AP: {self.sap_left}")

        # LANTERN - Add new random item to locker.
        if profiles[profile_name][f'{item_type}'] == "lantern":
            if self.ap_left >= 1: # Total AP cost for this item-action
                self.ap_left -= 1 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
                self.create_new_item_in_locker()

        # MAGNIFYINGGLASS - If suspect not found add witness-point. If suspect is found add 1 special AP.
        if profiles[profile_name][f'{item_type}'] == "magnifyingglass":
   
            if self.ap_left >= 3: # Total AP cost needed for this item-action
                self.ap_left -= 3 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")

                if self.perpetrator_active == False:
                    witness_name = random.choice(self.witnesses_start_list)
                    count = self.witnesses_list.count(witness_name)
                    while count >= self.witnesses_points_max:
                        witness_name = random.choice(self.witnesses_start_list)
                    else:
                        self.witnesses_list.append(witness_name)
                        new_image = f"images/profiles/{witness_name}_w{count}.png"
                        self.witnesses_button_to_dict[witness_name].configure(image=ir.card(new_image))
                        Utils.log(self, f"{str(witness_name).capitalize()} is added to witness") # Log
                
                elif self.perpetrator_active == True:
                    self.sap_left += 1
                    self.special_action_points_left_text.configure(text=f"Special AP: {self.sap_left}")

        # PIPE - Add witness-point, and empties waiting room. #! Is this making the game crash; while loop?
        if profiles[profile_name][f'{item_type}'] == "pipe":
            if self.ap_left >= 1: # Total AP needed cost for this item-action
                self.ap_left -= 1 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
                
                if self.perpetrator_active == False:
                    witness_name = random.choice(self.witnesses_start_list)
                    count = self.witnesses_list.count(witness_name)
                    while count >= self.witnesses_points_max:
                        witness_name = random.choice(self.witnesses_start_list)
                    else:
                        self.witnesses_list.append(witness_name)
                        new_image = f"images/profiles/{witness_name}_w{count}.png"
                        self.witnesses_button_to_dict[witness_name].configure(image=ir.card(new_image))
                        Utils.log(self, f"{str(witness_name).capitalize()} is added to witness") # Log

                        while len(self.waiting_room_list) > 0:
                            profile_name = random.choice(self.waiting_room_list)
                            self.waiting_room_list.remove(profile_name)
                            self.waiting_room_profiles_button_dict[profile_name].pack_forget()
                            Utils.log(self, f"Profile removed from waiting room") # Log
                            
                elif self.perpetrator_active == True:
                    self.sap_left += 1
                    self.special_action_points_left_text.configure(text=f"Special AP: {self.sap_left}")

        # TEAPOT - Fill examination room with profiles #! Is this making the game crash; for loop/remove profile?
        if profiles[profile_name][f'{item_type}'] == "teapot":
            examination_now = self.examination_max
            self.examination_max = 5
            if self.ap_left >= 2: # Total AP cost for this item-action
                self.ap_left -= 2 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")

                ne_profiles = self.examination_max - len(self.examination_list) 

                for ne in range(ne_profiles):
                    self.add_new_profile_to_examination()

            self.examination_max = examination_now

        # TOPHAT - Gain 2 extra special AP
        if profiles[profile_name][f'{item_type}'] == "tophat":
            if self.ap_left >= 1: # Total AP cost for this item-action
                self.ap_left -= 1 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")
            
                self.sap_left += 2
                self.special_action_points_left_text.configure(text=f"Special AP: {self.sap_left}")

        # VELOCIPEDE - Reset AP left to 2
        if profiles[profile_name][f'{item_type}'] == "bicycle":
            if self.ap_left >= 0: # Total AP cost for this item-action
                self.ap_left = 2 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")

        # WATCH - Add 1 extra day.
        if profiles[profile_name][f'{item_type}'] == "watch":
            if self.ap_left >= 3: # Total AP cost for this item-action
                self.ap_left -= 3 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")

                self.days_left += 1
                self.days_left_text.configure(text=f"Days left: {self.days_left}")

        # WHEELBARROW - Fill waiting room with profiles.
        if profiles[profile_name][f'{item_type}'] == "wheelbarrow": 
            waiting_room_now = self.waiting_room_max
            self.waiting_room_max = 5
            if self.ap_left >= 2: # Total AP cost for this item-action
                self.ap_left -= 2 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")

                nw_profiles = self.waiting_room_max - len(self.waiting_room_list) 

                for nw in range(nw_profiles):
                    self.add_new_profile_to_waiting_room()

            self.waiting_room_max = waiting_room_now

        # WHISTLE - Add new profile to examination room.
        if profiles[profile_name][f'{item_type}'] == "whistle": #! Is this making the game crash; remove profile?
            if self.ap_left >= 2: # Total AP cost for this item-action
                self.ap_left -= 2 # Extra AP cost for this item-action
                self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}")

                self.add_new_profile_to_examination()

    def player_special_item_actions(self): # Called from end_day_actions
        # Player special item actions
        # TODO INCREASE ROOM SIZE TO 5, BUT GO DOWN TO 2 IF PERPETRATOR USES MASK
        if self.player_special_item_active == "cab":
            self.waiting_room_max = 5

        # TODO DAYS NOT COUNTING DOWN, BUT 5 DAYS ARE LOST IF PERPETRATOR USES SHOVEL
        if self.player_special_item_active == "cell":
            self.days_left += 1
            self.days_left_text.configure(text=f"Days left: {self.days_left}")
        
        # TODO GAIN 1 RANDOM PROFILE TO EXAMINATION, EMPTIES IF PERPETRATOR USES GLOVES
        if self.player_special_item_active == "duster":
            self.add_new_profile_to_examination()

        # TODO PERP CHANCE TO PLAY NEW ITEM IS SET TO 20%
        if self.player_special_item_active == "fist":
            pass

       # TODO PERP CHANCE TO PLAY NEW ITEM IS SET TO 5% AS LONG AS WAITING ROOM HAS 2 PROFILES
        if self.player_special_item_active == "gun":
            pass

        # TODO
        if self.player_special_item_active == "hat":
            for profile in self.waiting_room_list: # Check if item is in examination, then add one action
                if profiles[profile]['handitem'] in player_items and player_items[profiles[profile]['handitem']]['type'] == 'item' and profiles[profile]['handitem'] == self.player_item_active:
                    self.ap_left += 3
                    self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}") # Update actions left label

        # TODO
        if self.player_special_item_active == "mail":
            for profile in self.examination_list: # Check if item is in examination, then add one action
                if profiles[profile]['playitem'] in player_items and player_items[profiles[profile]['playitem']]['type'] == 'item' and profiles[profile]['handitem'] == self.player_item_active:
                    self.ap_left += 3
                    self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}") # Update actions left label
        
        # TODO INCREASE ROOM SIZE TO 5, BUT GO DOWN TO 2 IF PERPETRATOR USES MASK
        if self.player_special_item_active == "newspaper":
            self.examination_max = 5

        # TODO 
        if self.player_special_item_active == "note":
            for profile in self.waiting_room_list: # Check if item is in examination, then add one action
                if profiles[profile]['handitem'] in player_items and player_items[profiles[profile]['handitem']]['type'] == 'item' and profiles[profile]['playitem'] == self.player_item_active:
                    self.ap_left += 3
                    self.action_points_left_text.configure(text=f"Actions left: {self.ap_left}") # Update actions left label
        
        # TODO INCREASE ROOM SIZES TO 4, BUT GO DOWN TO 2 IF PERPETRATOR USES MASK
        if self.player_special_item_active == "poster":
            self.waiting_room_max = 4
            self.examination_max = 4

        # TODO GAIN 4 SPECIAL AP EACH ROUND, BUT LOOSE ALL IF PERPETRATOR USES LOCKPICK
        if self.player_special_item_active == "safe":
            self.sap_left += 4
            self.special_action_points_left_text.configure(text=f"Actions left: {self.sap_left}") # Update actions left label

        # TODO GAIN 1 RANDOM PROFILE TO WAITING ROOM, EMPTIES IF PERPETRATOR USES CIPHER
        if self.player_special_item_active == "telegram":
            self.add_new_profile_to_waiting_room()
        
        # TODO REVERSE GREEN AND YELLOW ITEM ACTIONS # CONDITIONAL IN ADD_PROFILES_TO_EXAMINATION, PLAYER_ITEM_ACTIONS AND new_player_special_item_active
        if self.player_special_item_active == "whiskey":
            pass        

    def perpetrator_item_actions(self): # TODO Add perpetrator item actions 

        # Perpetrator item actions
        # TODO BAG - ONE PROFILE FROM EXAMINATION IS REMOVED
        if self.enemy_item_active == "bag":
            print(f"examination_list name: {self.waiting_room_list}")
            if len(self.waiting_room_list) > 0:
                profile_name = random.choice(self.waiting_room_list)
                self.waiting_room_list.remove(profile_name)
                self.waiting_room_profiles_button_dict[profile_name].pack_forget()
                Utils.log(self, f"Perpetrator removed profile from waiting room")

        # TODO BRIBE - ONE PROFILE FROM EXAMINATION IS REMOVED
        if self.enemy_item_active == "bribe":
            print(f"examination_list name: {self.examination_list}")
            if len(self.examination_list) > 0:
                # Find last profilename from exmination list and remove it
                profile_name = random.choice(self.examination_list) 
                self.examination_list.remove(profile_name) 
                self.examination_profiles_button_dict[profile_name].pack_forget()
                Utils.log(self, f"Perpetrator removed profile from examination")

        # TODO CIPHER - IF PLAYER SPECIAL ITEM "telegram" IS ACTIVE, THEN EMPTY WAITING ROOM
        if self.enemy_item_active == "cipher" and self.player_special_item_active == "telegram":
            self.waiting_room_list = []
            for profile_name in self.waiting_room_profiles_button_dict:
                self.waiting_room_profiles_button_dict[profile_name].pack_forget()
            Utils.log(self, f"Perpetrator emptied waiting room")

        # TODO GLOVES - IF PLAYER SPECIAL ITEM "duster" IS ACTIVE, THEN EMPTY EXAMINATION
        if self.enemy_item_active == "gloves" and self.player_special_item_active == "duster":
            self.examination_list = []
            for profile_name in self.examination_profiles_button_dict:
                self.examination_profiles_button_dict[profile_name].pack_forget()
            Utils.log(self, f"Perpetrator emptied examination")

        # TODO LADDER - LOOSE 1 EXTRA DAY
        if self.enemy_item_active == "ladder":
            self.days_left -= 1
            self.days_left_text.configure(text=f"Days left: {self.days_left}")

        # TODO LOCKPICK - IF PLAYER SPECIAL ITEM "safe" IS ACTIVE, THEN LOOSE ALL SPECIAL AP
        if self.enemy_item_active == "lockpick" and self.player_special_item_active == "safe":
            self.sap_left = 0
            self.special_action_points_left_text.configure(text=f"Actions left: {self.sap_left}") # Update actions left label

        # TODO MASK - IF PLAYER SPECIAL ITEM "cab", "newspaper" or "poster" IS ACTIVE, THEN ROOM SIZE IS 2
        if self.enemy_item_active == "mask" and self.player_special_item_active == "cab" or self.player_special_item_active == "newspaper" or self.player_special_item_active == "poster":
            self.waiting_room_max = 2
            self.examination_max = 2
        else:
            self.waiting_room_max = self.waiting_room_max #! check if this works
            self.examination_max = self.examination_max #! check if this works

        # TODO SHOVEL - IF PLAYER SPECIAL ITEM "cell" IS ACTIVE, THEN 3 DAYS ARE LOST 
        if self.enemy_item_active == "shovel" and self.player_special_item_active == "cell":
            self.days_left -= 3
            self.days_left_text.configure(text=f"Days left: {self.days_left}")

    #? START CARDS WINDOW AND LOGIC
    def start_cards_window(self): # Called from welcome_window
        sg = StyleGame() # Styles
        ir = ImageResizer() # image resizer

        self.start_cards = CTkToplevel(self.app)
        #self.start_cards.title(f"Choose witnesses for questioning")
        #c_window_w, c_window_h = 860, 400
        #widthc = int(self.width / 2) - int(c_window_w / 2)
        #self.start_cards.geometry(f"{c_window_w}x{c_window_h}+{widthc}+500")
        #self.start_cards.deiconify()

        # Window attributes
        self.start_cards.attributes('-fullscreen', True)
        #self.start_cards.overrideredirect(True)  # Hides window titlebar
        #self.start_cards.withdraw() # temporary for testing main window.

        # Start Pop-Up window
        self.start_cards_main = CTkFrame(self.start_cards, fg_color=sg.fg_color)
        self.start_cards_main.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        #! Header GUI
        self.start_cards_label = CTkLabel(self.start_cards_main, text="", image=ir.delt("images/gui/delt_profiles.png"), fg_color=sg.fg_color)
        self.start_cards_label.pack(side="top", ipady=20)

        # Start cards fill
        self.start_cards_fill = CTkFrame(self.start_cards_main, fg_color=sg.fg_color)
        self.start_cards_fill.pack(side="top")

        #! Create the cards to choose from
        self.create_random_profiles() # Create the cards to choose from

        #! Quit button
        self.options_button = CTkButton(self.start_cards_main, text="Quit game", 
            fg_color="grey", hover_color="red",
            command=lambda: sys.exit() 
            )
        self.options_button.pack(pady=30, side="bottom")

    def create_random_profiles(self): # Called from start_cards_window
        delt_profiles = random.sample(profiles.keys(), k=self.delt_profiles_max) #! k=How many profiles to choose from at the beginning
        for name in delt_profiles: # Loop through the random choices and create the profiles
            card = self.create_profiles_buttons(name) # Create the profiles
            self.choosen_profiles_list.append(name) # Append card to list for further referance
            self.choosen_profiles_button_dict[name] = card # Store the profile in the dictionary

    def create_profiles_buttons(self, profile_name): # Called from create_random_profiles
        ir = ImageResizer()

        profile_button = CTkButton( #! Rename self.card to self.start_card?
            self.start_cards_fill, 
            text="",  
            image=ir.card(card_images_d[f"{profile_name}_delt.png"]),
            fg_color="transparent",
            command=lambda n=profile_name: self.add_profiles_to_waiting_room(self.choosen_profiles_button_dict[n], n),
            hover=("False")
        )
        profile_button.pack(side="left", padx=0)

        profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_d(event, n, c, card_images_d))
        profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_d(event, n, c, card_images_d))
        Utils.ToolTipButton(profile_button, profile_name, "profile")
        
        return profile_button

    #? WAITING ROOM
    def add_profiles_to_waiting_room(self, profile_button, profile_name): # From delt to waiting room
        profile_button.pack_forget()
        self.choosen_profiles_list.remove(profile_name) # Update list for further reference
        self.waiting_room_list.append(profile_name) # Append card to list for further reference

        # Close choose-cards-window when X cards are selected
        if len(self.waiting_room_list) >= self.start_profiles_max:
            profiles_forget = self.start_profiles_max - self.delt_profiles_max # How many profiles to forget
            last_card_names = self.choosen_profiles_list[profiles_forget:]
            for name in last_card_names:
                last_card = self.choosen_profiles_button_dict[name]
                last_card.pack_forget()

            self.start_cards.withdraw() # Close choose-profiles-window when X cards are selected
            self.app.deiconify() # deiconifies the game

        profile_button = CTkButton(
            self.waiting_room_center, 
            text="", 
            image=ImageResizer().card(f"images/profiles/{profile_name}_delt.png"),
            fg_color="transparent",
            command=lambda c=profile_button, n=profile_name: self.add_profiles_to_examination(c, n),
            hover=("False")
        )
        profile_button.pack(padx=0, side="left")

        profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_d(event, n, c, card_images_d))
        profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_d(event, n, c, card_images_d))
        Utils.ToolTipButton(profile_button, profile_name, "profile")
        
        self.waiting_room_profiles_button_dict[profile_name] = profile_button # Store the card in the dictionary

    def add_new_profile_to_waiting_room(self): # Called from end_day_actions
        ir = ImageResizer()
        profile_button = None # Comes from thin air so needs to be defined

        profile_name = random.choice(list(profiles.keys()))
        while profile_name in self.waiting_room_list or profile_name in self.examination_list: # While card exists on the board, pick new random card from the deck.
            profile_name = random.choice(list(profiles.keys()))

        if len(self.waiting_room_list) < self.waiting_room_max: #! How many cards can be in waiting room
            profile_button = CTkButton(
                self.waiting_room_center, text="", 
                image=ir.card(f"images/profiles/{profile_name}_delt.png"),
                fg_color="transparent",
                command=lambda c=profile_button, n=profile_name: self.add_profiles_to_examination(c, n),
                hover=("False")
            )
            profile_button.pack(padx=0, side="left")

            profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_d(event, n, c, card_images_d))
            profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_d(event, n, c, card_images_d))
            Utils.ToolTipButton(profile_button, profile_name, "profile")
            
            self.waiting_room_list.append(profile_name) # Append card to list for further reference
            self.waiting_room_profiles_button_dict[profile_name] = profile_button     

            Utils.log(self, f"{str(profile_name).capitalize()} added to waiting room") # Log
        else:
            Utils.log(self, f"Not enough room. {str(profile_name).capitalize()} never arrived!") # Log

    #? EXAMINATION
    def add_profiles_to_examination(self, profile_button, profile_name): # Called from add_profiles_to_waiting_room
        ir = ImageResizer()

        if self.player_special_item_active == "whiskey":
            hover = "hand"
        else:
            hover = "play"

        if self.examinations_actions(profile_name) == True:

            if len(self.examination_list) < self.examination_max: #! How many cards can be in examination
                self.waiting_room_profiles_button_dict[profile_name].pack_forget() # remove button from waiting room
                self.waiting_room_list.remove(profile_name) # Update list for further reference
                self.examination_list.append(profile_name) # Append card to list for further reference

                profile_button = CTkButton(
                    self.examination_center, 
                    text="", 
                    image=ir.card(f"images/profiles/{profile_name}_{hover}.png"),
                    fg_color="transparent",
                    command=lambda n=profile_name: self.witness_actions(n),
                    hover=("False")
                )
                profile_button.pack(padx=0, side="left")

                if self.player_special_item_active == "whiskey":
                    profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_h(event, n, c, card_images_h))
                    profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_h(event, n, c, card_images_h))
                else:
                    profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_p(event, n, c, card_images_p))
                    profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_p(event, n, c, card_images_p))

                Utils.ToolTipButton(profile_button, profile_name, "profile")
                
                self.examination_profiles_button_dict[profile_name] = profile_button

                Sound("wav/card.wav").play_sound()

    def add_new_profile_to_examination(self): # Called from end_day_actions
        ir = ImageResizer()
        profile_button = None # Comes from thin air so needs to be defined

        if self.player_special_item_active == "whiskey":
            hover = "hand"
        else:
            hover = "play"

        profile_name = random.choice(list(profiles.keys()))
        while profile_name in self.waiting_room_list or profile_name in self.examination_list: # While card exists on the board, pick new random card from the deck.
            profile_name = random.choice(list(profiles.keys()))

        if len(self.examination_list) < self.examination_max: #! How many cards can be in waiting room
            profile_button = CTkButton(
                self.examination_center, text="", 
                image=ir.card(f"images/profiles/{profile_name}_{hover}.png"),
                fg_color="transparent",
                command=lambda n=profile_name: self.witness_actions(n),
                hover=("False")
            )
            profile_button.pack(padx=0, side="left")

            if self.player_special_item_active == "whiskey":
                profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_h(event, n, c, card_images_h))
                profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_h(event, n, c, card_images_h))
            else:
                profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_p(event, n, c, card_images_p))
                profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_p(event, n, c, card_images_p))

            Utils.ToolTipButton(profile_button, profile_name, "profile")
            
            self.examination_list.append(profile_name) # Append card to list for further reference
            self.examination_profiles_button_dict[profile_name] = profile_button     

            Utils.log(self, f"{str(profile_name).capitalize()} added to examination") # Log
        else:
            Utils.log(self, f"Not enough room. {str(profile_name).capitalize()} never arrived!") # Log

    #? WITNESSES 
    def create_random_witnesses(self): # Called from main
        witness_cards = random.sample(profiles.keys(), k=self.witnesses_max) # k=How many witnesses (standard=3)
        for name in witness_cards: # Loop through the random choices and create the witnesses
            self.witnesses_list.append(name) # Append witness to list for further referance
            self.witnesses_start_list.append(name) # Append witness to list for further referance
            #card_log(name, log_type="card", text="witness created") # TODO Log the witnesses creation
            self.create_witnesses_buttons(name) # Create witness-cards

    def create_witnesses_buttons(self, profile_name): # Called from create_random_witnesses
        ir = ImageResizer()

        witness = CTkLabel(
            self.witnesses_center, text="",  
            image=ir.card(f"images/profiles/{profile_name}_wit.png"),
            fg_color="transparent")         
        witness.pack(side="left", padx=5)
        self.witnesses_button_to_dict[profile_name] = witness
        return witness

    #? PLAYER ITEMS 
    def create_new_item_in_locker(self): # Called from end_day_actions
        ir = ImageResizer()
 
        if self.perpetrator_active == False: # TODO CHANGE TO TRUE/FALSE FOR TESTING. False = no perp, True = perp
            player_item_keys = [key for key, value in player_items.items() if value['type'] == 'item']
            locker_item = random.choice(player_item_keys)
        else:
            locker_item = random.choice(list(player_items.keys()))

        if self.player_locker_item_button:
            self.player_locker_item_button.pack_forget()

        self.player_locker_item_button = CTkButton(
            self.left_bottom_center, 
            text="", 
            image=ir.card(f"images/items/{locker_item}.png"),
            fg_color="transparent",
            command=lambda n=locker_item: self.player_item_actions(n),
            hover=("False")
        )
        self.player_locker_item_button.pack(padx=0, side="left")

        self.player_locker_item_button.bind('<Enter>', lambda event, n=locker_item, c=self.player_locker_item_button: Bind.enter_i(event, n, c, card_images_i))
        self.player_locker_item_button.bind('<Leave>', lambda event, n=locker_item, c=self.player_locker_item_button: Bind.leave_i(event, n, c, card_images_i))
        Utils.ToolTipButton(self.player_locker_item_button, locker_item, "player_item")
        
        self.player_locker_item = locker_item #! Item in locker
        self.player_locker_item_button[locker_item] = self.player_locker_item_button # Store the card in the dictionary
        self.player_locker_item_button_to_dict[locker_item] = self.player_locker_item_button  # Store the card in the dictionary

    def new_player_item_active(self, item_name): # Called from player_item_type_active
        ir = ImageResizer()
          
        self.player_locker_item_button_to_dict[item_name].pack_forget()

        if self.player_item_active_button:
            self.player_item_active_button.pack_forget()
        
        self.player_item_active_button = CTkButton(
            self.left_middle_center, 
            text="", 
            image=ir.card(f"images/items/{item_name}.png"),
            fg_color="transparent",
            command="",
            hover=("False")
        )
        self.player_item_active_button.pack(padx=0, side="left")

        Utils.ToolTipButton(self.player_item_active_button, item_name, "player_item")
        Sound("wav/swish.wav").play_sound()

        self.player_item_active = item_name #! Active item
        self.player_item_active_button_to_dict[item_name] = self.player_item_active_button

    def new_player_special_item_active(self, item_name): # Called from player_item_type_active
        ir = ImageResizer()
          
        self.player_locker_item_button_to_dict[item_name].pack_forget()

        if self.player_special_item_active_button:
            self.player_special_item_active_button.pack_forget()
        
        self.player_special_item_active_button = CTkButton(
            self.left_top_center, 
            text="", 
            image=ir.card(f"images/items/{item_name}.png"),
            fg_color="transparent",
            command="",
            hover=("False")
        )
        self.player_special_item_active_button.pack(padx=0, side="left")

        Utils.ToolTipButton(self.player_special_item_active_button, item_name, "player_item")
        Sound("wav/swish.wav").play_sound()

        self.player_special_item_active = item_name #! Active special item
        self.player_special_item_active_button_to_dict[item_name] = self.player_special_item_active_button 

        # Changes excisting cards to right image when special item is activated
        if item_name == "whiskey":
            for profile in self.examination_profiles_button_dict:
                image_new=ImageResizer().card(f"images/profiles/{profile}_hand.png")
                profile_button = self.examination_profiles_button_dict[profile]
                
                profile_button.configure(image=image_new)
                profile_button.bind('<Enter>', lambda event, n=profile, c=profile_button: Bind.enter_h(event, n, c, card_images_h))
                profile_button.bind('<Leave>', lambda event, n=profile, c=profile_button: Bind.leave_h(event, n, c, card_images_h))
                
        if item_name != "whiskey":
            for profile in self.examination_profiles_button_dict:
                image_new=ImageResizer().card(f"images/profiles/{profile}_play.png")
                profile_button = self.examination_profiles_button_dict[profile]
                
                profile_button.configure(image=image_new)
                profile_button.bind('<Enter>', lambda event, n=profile, c=profile_button: Bind.enter_p(event, n, c, card_images_p))
                profile_button.bind('<Leave>', lambda event, n=profile, c=profile_button: Bind.leave_p(event, n, c, card_images_p))
    
    #? CRIMESCENE
    def create_crime_scene(self, image_name, new_image): # Called from main
        ir = ImageResizer()

        if new_image == "no":
            self.crime = CTkLabel(
                self.perpetrator_center, 
                text="", 
                image=ir.card(f"images/profiles/{image_name}.png"),
                fg_color="transparent"
            )
            self.crime.pack(padx=0, side="left")     
        elif new_image == "yes":
            self.crime.configure(image=ir.card(f"images/profiles/{image_name}.png"))

    #? PERPETRATOR
    def perpetrator_identified(self): # Called from end_day_actions
        ir = ImageResizer()

        if self.perpetrator_active == False: # If perpetrator is not active
            counts = Counter(self.witnesses_list)
            if len([witness for witness, count in counts.items() if count >= self.witnesses_points_max]) >= self.witnesses_max: # If witness has 4 witness points (wit.png + w1.png + w2.png + w3.png)
                self.random_perpetrator = random.choice(list(profiles.keys())) # Find random perp
                while self.random_perpetrator in self.witnesses_start_list: # While witness exists, pick new random perp from the deck.
                    self.random_perpetrator = random.choice(list(profiles.keys())) # Find another random perp
                self.create_crime_scene(f"{self.random_perpetrator}_sus", "yes") # Crime scene image
                self.perpetrator_fill_gui.configure(image=ir.side_bar(f"images/gui/sidebar_suspect.png")) # Sidebar image
                self.perpetrator_active = True # Perpetrator is active
                self.perpetrator_list.append(self.random_perpetrator) # Add perpetrator to list
                Utils.log(self, f"Pereptrator point added!") # Log  

    #? PERPETRATOR ITEMS
    def create_enemy_item(self): # Called from end_day_actions
        ir = ImageResizer()

        enemy_item_keys = [key for key, value in enemy_items.items() if value['type'] == 'enemyitem']
        enemy_item = random.choice(enemy_item_keys)

        if self.enemy_item_active_button:
            self.enemy_item_active_button.pack_forget()                

        self.enemy_item_active_button = CTkButton(
            self.perpetrator_item_center, text="", 
            image=ir.card(f"images/items/e_{enemy_item}.png"),
            fg_color="transparent",
            command="",
            hover=("False")
        )
        self.enemy_item_active_button.pack(padx=0, side="left")

        Utils.ToolTipButton(self.enemy_item_active_button, enemy_item, "enemy_item")

        self.enemy_item_active = enemy_item #! Active enemy item
        self.enemy_item_active_button_to_dict[enemy_item] = self.enemy_item_active_button   

    #? WELCOME WINDOW
    def welcome_window(self): # Called in main
        ir = ImageResizer()
        sg = StyleGame()

        # Window
        self.welcome_splash_window = ctk.CTkToplevel(self.app)
        self.welcome_splash_window.title("Inspector's Chronicles")
        window_width = self.width # 900
        window_height = self.height # 300

        # Center the window
        widthc = int(self.width / 2) - int(window_width / 2)
        self.welcome_splash_window.geometry(f"{window_width}x{window_height}+{widthc}+500")

        # Window attributes
        self.welcome_splash_window.attributes('-fullscreen', True)
        self.welcome_splash_window.attributes('-topmost', 'true')
        self.welcome_splash_window.overrideredirect(True) # removes titlebar
        self.welcome_splash_window.deiconify() # opens the window

        # Text-label inside window
        #label_welcome = CTkLabel(window, text="Game title", font=sg.font_xxxlarge)
        #label_welcome.pack(pady=20, padx=20, side="top") 

        welcome_frame = CTkFrame(self.welcome_splash_window, fg_color=sg.fg_color)
        welcome_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        #! Game name Image
        welcome_label = CTkLabel(welcome_frame, text="", image=ir.game_name(f"images/gui/game_name.png"))
        welcome_label.pack(pady=60, padx=20, side="top") 

        # Start game button
        start_game_button= CTkButton(
            welcome_frame, text="Start game",
            fg_color="grey", hover_color="Green",
            command=lambda: (self.welcome_splash_window.destroy(), self.start_cards_window()),
            )
        start_game_button.pack(pady=5)

        # How to play button
        how_to_play_button= CTkButton(
            welcome_frame, text="How to play",
            fg_color="grey", hover_color="orange",
            command=lambda: (self.welcome_splash_window.iconify(), ), # TODO How to play window
            )
        how_to_play_button.pack(pady=5)

        # Sound button
        how_to_play_button= CTkButton(
            welcome_frame, text="Sound",
            fg_color="grey", hover_color="orange",
            command=lambda: (self.welcome_splash_window.iconify(), ), 
            )
        how_to_play_button.pack(pady=5)

        # Quit game button
        self.quit_button = CTkButton(
            welcome_frame, text="Quit game", 
            fg_color="grey", hover_color="red",
            command=lambda: sys.exit() 
            )
        self.quit_button.pack(pady=30)

    #? WON WINDOW
    def won_window(self): # Called in main
        ir = ImageResizer()
        sg = StyleGame()

        # Window
        self.won_splash_window = ctk.CTkToplevel(self.app)
        self.won_splash_window.title("Inspector's Chronicles")
        window_width = self.width # 900
        window_height = self.height # 300

        # Center the window
        widthc = int(self.width / 2) - int(window_width / 2)
        self.won_splash_window.geometry(f"{window_width}x{window_height}+{widthc}+500")

        # Window attributes
        self.won_splash_window.attributes('-fullscreen', True)
        self.won_splash_window.attributes('-topmost', 'true')
        self.won_splash_window.overrideredirect(True) # removes titlebar
        self.won_splash_window.deiconify() # opens the window

        # Text-label inside window
        #label_won = CTkLabel(window, text="Game title", font=sg.font_xxxlarge)
        #label_won.pack(pady=20, padx=20, side="top") 

        won_frame = CTkFrame(self.won_splash_window, fg_color=sg.fg_color)
        won_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        #! Game name Image
        won_label = CTkLabel(won_frame, text="", image=ir.game_name(f"images/gui/game_name.png"))
        won_label.pack(pady=60, padx=20, side="top") 
        
        # Quit game button
        self.options_button = CTkButton(
            won_frame, text="Quit game", 
            fg_color="grey", hover_color="red",
            command=lambda: sys.exit() 
            )
        self.options_button.pack(pady=30)

    #? DAYS LEFT AND SUSPECT IDENTIFIED WINDOW
    def days_left_window(self): # Called in main
        sg = StyleGame()

        # Window
        self.days_left_level = ctk.CTkToplevel(self.app)
        self.days_left_level.wm_attributes('-alpha',0.8) #transparency
        self.days_left_level.title("End of day")
        window_width = 400
        window_height = 200

        # Center the window
        widthc = int(self.width / 2) - int(window_width / 2)
        self.days_left_level.geometry(f"{window_width}x{window_height}+{widthc}+500")

        # Window attributes
        self.days_left_level.attributes('-fullscreen', False)
        self.days_left_level.attributes('-topmost', 'true')
        self.days_left_level.overrideredirect(True) # removes titlebar
        self.days_left_level.deiconify() # opens the window

        self.days_end_frame = CTkFrame(self.days_left_level, fg_color="transparent")
        self.days_end_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        #! Days end label
        self.days_end_label = CTkLabel(self.days_end_frame, font=sg.font_xxxxlarge, fg_color="black", text_color="orange", text=f"Days left: {self.days_left-1}", corner_radius=15)
        self.days_end_label.pack(pady=60, padx=20, side="top") 

        #! Days end label
        self.sus_id_label = CTkLabel(self.days_end_frame, font=sg.font_xxxlarge, fg_color="orange", text_color="red", text=f"", corner_radius=15)
        self.sus_id_label.pack(pady=0, padx=20, side="bottom") 

    def days_left_popup(self): # Called from end_day_actions
        self.days_left_level.deiconify()
        self.days_end_label.configure(text=f"Days left: {self.days_left}")
        self.days_end_label.pack(pady=10, padx=20, side="top") 
        if self.perpetrator_active == True:
            self.sus_id_label.configure(text=f"Suspect identified!")
            self.sus_id_label.pack(pady=0, padx=20, side="bottom")
        else:
            self.sus_id_label.configure(text=f"Witnesses left: {((self.witnesses_max-1)*len(self.witnesses_start_list))-len(self.witnesses_list)}")
            self.sus_id_label.pack(pady=0, padx=20, side="bottom")
        self.days_left_level.after(2000, self.days_left_level.withdraw)

    #? BOARD
    def board_main(self): # Called from main
        sg = StyleGame() # Styles
        ir = ImageResizer() # image resizer

        # Main frame
        self.frame_main = CTkFrame(self.app, fg_color=sg.main_color)
        self.frame_main.place(relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Main frame center outside
        self.frame_main_center_outside = CTkFrame(self.frame_main, fg_color=sg.fill_color)
        self.frame_main_center_outside.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Main Options
        self.frame_main_center_options = CTkFrame(self.frame_main_center_outside, height=50, fg_color=sg.center_color)
        self.frame_main_center_options.grid(pady=10, padx=10, row=0, column=0, sticky = "w")

        #! Options button
        self.options_button = CTkButton(self.frame_main_center_options, text="Options", 
            fg_color="grey", hover_color="orange",
            command=lambda: self.welcome_window() 
            )
        self.options_button.pack(pady=0, padx=20, side="left")

        # Main Header
        self.frame_main_center_header = CTkFrame(self.frame_main_center_outside, height=50, fg_color=sg.center_color)
        self.frame_main_center_header.grid(pady=10, padx=10, row=0, column=1, sticky = "n")

        #! Game name Image
        self.perpetrator_main_label = CTkLabel(self.frame_main_center_header, text="", image=ir.game_name(f"images/gui/game_name.png"))
        self.perpetrator_main_label.pack(pady=0, padx=20, side="top")     

        # Main Header
        self.frame_main_center_quit = CTkFrame(self.frame_main_center_outside, height=50, fg_color=sg.center_color)
        self.frame_main_center_quit.grid(pady=10, padx=10, row=0, column=2, sticky = "e")

        #! Restart button
        def restart_game():
            self.app.destroy()
            self.__init__()

        self.restart_button = CTkButton(self.frame_main_center_quit, text="Restart game", 
            fg_color="grey", hover_color="red",
            command=lambda: restart_game()
            )
        self.restart_button.pack(pady=0, padx=20, side="left")

            
        #! Quit button
        self.quit_button = CTkButton(self.frame_main_center_quit, text="Quit game", 
            fg_color="grey", hover_color="red",
            command=lambda: sys.exit() 
            )
        self.quit_button.pack(pady=0, padx=20, side="right")

        # Main frame center
        self.frame_main_center = CTkFrame(self.frame_main_center_outside, fg_color="#1e2228") #sg.fg_color
        self.frame_main_center.grid(pady=10, padx=10, row=1, column=0, columnspan=3, sticky = "n")

        # ! Main frame center - BACKGROUND IMAGE label
        #self.frame_main_label = CTkLabel(self.frame_main_center, text="", image=ir.main_bg(f"images/gui/main_bg.png"))
        #self.frame_main_label.grid(row=0, column=0, columnspan=5, rowspan=3)

    def board_left(self): # Called from main
        sg = StyleGame() # Styles
        ir = ImageResizer() # image resizer

        #? LEFT TOP
        # Left top main
        self.left_top_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.left_top_main.grid(pady=10, padx=10, row=0, column=0, sticky = "n")

        # Left top fill
        self.left_top_fill = CTkFrame(self.left_top_main, width=300, height=340, fg_color=sg.fill_color)
        self.left_top_fill.grid(pady=2, padx=2, row=0, column=0, sticky = "n")

        #! Left top main - SPECIAL ITEM label
        #self.left_top_main_label = CTkLabel(self.left_top_main, text="Special item")
        #self.left_top_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Left top fill - GUI label
        self.left_top_fill_gui = CTkLabel(self.left_top_fill, text="", image=ir.side_bar(f"images/gui/sidebar_special.png"))
        self.left_top_fill_gui.place(x=5, y=170, anchor=ctk.W)   
        
        # Left top center
        self.left_top_center = CTkFrame(self.left_top_fill, width=10, height=10, fg_color=sg.center_color)
        self.left_top_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

        #? LEFT MIDDLE
        # Left middle main
        self.left_middle_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.left_middle_main.grid(pady=10, padx=10, row=1, column=0, sticky = "n")

        # Left middle fill
        self.left_middle_fill = CTkFrame(self.left_middle_main, width=300, height=340, fg_color=sg.fill_color)
        self.left_middle_fill.grid(pady=2, padx=2, row=0, column=0, sticky = "n")

        #! Left middle main - ACTIVE EVIDENCE label
        #self.left_middle_main_label = CTkLabel(self.left_middle_main, text="Active evidence")
        #self.left_middle_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Left middle fill - GUI label
        self.left_middle_fill_gui = CTkLabel(self.left_middle_fill, text="", image=ir.side_bar(f"images/gui/sidebar_e_active.png"))
        self.left_middle_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Left middle center
        self.left_middle_center = CTkFrame(self.left_middle_fill, width=10, height=10, fg_color=sg.center_color)
        self.left_middle_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

        #? LEFT BOTTOM
        # Left bottom main
        self.left_bottom_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.left_bottom_main.grid(pady=10, padx=10, row=2, column=0, sticky = "n")

        # Left bottom fill
        self.left_bottom_fill = CTkFrame(self.left_bottom_main, width=300, height=340, fg_color=sg.fill_color)
        self.left_bottom_fill.grid(pady=2, padx=2, row=0, column=0, sticky = "n")

        #! Left bottom main - EVIDENCE LOCKER label
        #self.left_bottom_main_label = CTkLabel(self.left_bottom_main, text="Evidence locker")
        #self.left_bottom_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Left bottom fill - GUI label
        self.left_bottom_fill_gui = CTkLabel(self.left_bottom_fill, text="", image=ir.side_bar(f"images/gui/sidebar_locker.png"))
        self.left_bottom_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Left bottom center
        self.left_bottom_center = CTkFrame(self.left_bottom_fill, width=10, height=10, fg_color=sg.center_color)
        self.left_bottom_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

    def board_middle(self): # Called from main
        sg = StyleGame() # Styles
        ir = ImageResizer() # image resizer

        #? MIDDLE TOP LEFT - WITNESSES
        # Witnesses main
        self.witnesses_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.witnesses_main.grid(pady=10, padx=10, row=0, column=1, sticky = "n")

        # Witnesses fill
        self.witnesses_fill = CTkFrame(self.witnesses_main, width=578, height=340, fg_color=sg.fill_color)
        self.witnesses_fill.grid(pady=2, padx=2, row=0, column=1)

        #! Witnesses main - WITNESSES label
        #self.witness_main_label = CTkLabel(self.witnesses_main, text="Witnesses")
        #self.witness_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Witnesses fill - GUI label
        self.witnesses_fill_gui = CTkLabel(self.witnesses_fill, text="", image=ir.witnesses(f"images/gui/witnesses.png"))
        self.witnesses_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Witnesses center
        self.witnesses_center = CTkFrame(self.witnesses_fill, width=10, height=10, fg_color=sg.center_color)
        self.witnesses_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

        #? MIDDLE TOP RIGHT - PERPETRATOR ITEM
        # Perpetrator item main
        self.perpetrator_item_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.perpetrator_item_main.grid(pady=10, padx=10, row=0, column=2, sticky = "n")

        # Perpetrator item fill
        self.perpetrator_item_fill = CTkFrame(self.perpetrator_item_main, width=300, height=340, fg_color=sg.fill_color)
        self.perpetrator_item_fill.grid(pady=2, padx=2, row=0, column=1)

        #! Perpetrator item main - PERPETRATOR ITEM label
        #self.perpetrator_item_main_label = CTkLabel(self.perpetrator_item_main, text="Perpetrator item")
        #self.perpetrator_item_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Perpetrator item fill - GUI label
        self.perpetrator_item_fill_gui = CTkLabel(self.perpetrator_item_fill, text="", image=ir.side_bar(f"images/gui/sidebar_perp_item.png"))
        self.perpetrator_item_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Perpetrator item center
        self.perpetrator_item_center = CTkFrame(self.perpetrator_item_fill, width=10, height=10, fg_color=sg.center_color)
        self.perpetrator_item_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

        #? MIDDLE MIDDLE - EXAMINATION
        # Examination main
        self.examination_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.examination_main.grid(pady=10, padx=10, row=1, column=1, columnspan=2, sticky = "n")

        # Examination fill
        self.examination_fill = CTkFrame(self.examination_main, width=900, height=340, fg_color=sg.fill_color)
        self.examination_fill.grid(pady=2, padx=2, row=0, column=1)

        #! Examination main - EXAMINATION label
        #self.examination_main_label = CTkLabel(self.examination_main, text="Examination")
        #self.examination_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Examination fill - GUI label
        self.examination_fill_gui = CTkLabel(self.examination_fill, text="", image=ir.examination(f"images/gui/examination.png"))
        self.examination_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Examination center
        self.examination_center = CTkFrame(self.examination_fill, width=10, height=10, fg_color=sg.center_color)
        self.examination_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)   

        #? MIDDLE BOTTOM - WAITING ROOM
        # Waiting room main
        self.waiting_room_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.waiting_room_main.grid(pady=10, padx=10, row=2, column=1, columnspan=2, sticky = "n")

        # Waiting room fill
        self.waiting_room_fill = CTkFrame(self.waiting_room_main, width=900, height=340, fg_color=sg.fill_color)
        self.waiting_room_fill.grid(pady=2, padx=2, row=0, column=1)

        #! Waiting room main - WAITING ROOM label
        #self.waiting_room_main_label = CTkLabel(self.waiting_room_main, text="Waiting room")
        #self.waiting_room_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Waiting room fill - GUI label
        self.waiting_room_fill_gui = CTkLabel(self.waiting_room_fill, text="", image=ir.waiting_room(f"images/gui/waiting_room.png"))
        self.waiting_room_fill_gui.place(x=5, y=170, anchor=ctk.W)           

        # Waiting room center
        self.waiting_room_center = CTkFrame(self.waiting_room_fill, width=10, height=10, fg_color=sg.center_color)
        self.waiting_room_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

    def board_right(self) : # Called from main
        sg = StyleGame() # Styles
        ir = ImageResizer() # image resizer

        #? RIGHT TOP - PERPETRATOR
        # Perpetrator main
        self.perpetrator_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.perpetrator_main.grid(pady=10, padx=10, row=0, column=3, sticky = "n")

        # Perpetrator fill
        self.perpetrator_fill = CTkFrame(self.perpetrator_main, width=300, height=340, fg_color=sg.fill_color)
        self.perpetrator_fill.grid(pady=2, padx=2, row=0, column=1)

        #! Perpetrator main - PERPETRATOR label
        #self.perpetrator_main_label = CTkLabel(self.perpetrator_main, text="Perpetrator")
        #self.perpetrator_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Perpetrator fill - GUI label
        self.perpetrator_fill_gui = CTkLabel(self.perpetrator_fill, text="", image=ir.side_bar(f"images/gui/sidebar_crime_scene.png"))
        self.perpetrator_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Perpetrator center
        self.perpetrator_center = CTkFrame(self.perpetrator_fill, width=10, height=10, fg_color=sg.center_color)
        self.perpetrator_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

        #? RIGHT MIDDLE - LOG
        # Log main
        self.log_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.log_main.grid(pady=10, padx=10, row=1, column=3, sticky = "n")

        # Log fill
        self.log_fill = CTkFrame(self.log_main, width=300, height=340, fg_color=sg.fill_color)
        self.log_fill.grid(pady=2, padx=2, row=0, column=1)

        #! Log main - LOG label
        #self.log_main_label = CTkLabel(self.log_main, text="Log")
        #self.log_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Log fill - GUI label
        self.log_fill_gui = CTkLabel(self.log_fill, text="", image=ir.side_bar(f"images/gui/sidebar_log.png"))
        self.log_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Log center
        self.log_center = CTkFrame(self.log_fill, width=200, height=200, fg_color=sg.center_color)
        self.log_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

        self.log_center_textbox = CTkTextbox(self.log_center, fg_color="#242426", width=200, height=200, wrap="word", state="disabled", corner_radius=0)
        self.log_center_textbox.place(x=0, y=101, anchor=ctk.W)

        #? RIGHT BOTTOM - STATS
        # Stats main
        self.stats_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.stats_main.grid(pady=10, padx=10, row=2, column=3, sticky = "n")

        # Stats fill
        self.stats_fill = CTkFrame(self.stats_main, width=300, height=340, fg_color=sg.fill_color)
        self.stats_fill.grid(pady=2, padx=2, row=0, column=1)

        #! Stats main - STATS label
        #self.stats_main_label = CTkLabel(self.stats_main, text="Stats")
        #self.stats_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Stats fill - GUI label
        self.stats_fill_gui = CTkLabel(self.stats_fill, text="", image=ir.side_bar(f"images/gui/desk.png"))
        self.stats_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Stats center
        self.stats_center = CTkFrame(self.stats_fill, width=10, height=10, fg_color=sg.center_color)
        self.stats_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

        #! Stats center - GUI Days left
        self.days_left_text= CTkLabel(self.stats_center, text=f"Days left: {self.days_left}", text_color="orange", font=sg.font_xlarge)
        self.days_left_text.pack(side="top")

        #! Stats center - GUI Action points left
        self.action_points_left_text= CTkLabel(self.stats_center, text=f"Actions left: {self.ap_left}", font=sg.font_xlarge)
        self.action_points_left_text.pack(side="top")

        #! Stats center - GUI Special sction points left
        self.special_action_points_left_text= CTkLabel(self.stats_center, text=f"Special AP: {self.sap_left}", text_color="purple", font=sg.font_xlarge)
        self.special_action_points_left_text.pack(side="top")

        #! Stats center - GUI Max profiles in examination
        self.examination_max_text= CTkLabel(self.stats_center, text=f"Examination max: {self.examination_max}", text_color="green", font=sg.font_xlarge)
        self.examination_max_text.pack(side="top")

        #! Stats center - GUI Max profiles in waiting room
        self.waiting_room_max_text= CTkLabel(self.stats_center, text=f"Waiting-room max: {self.waiting_room_max}", font=sg.font_xlarge)
        self.waiting_room_max_text.pack(side="top")

        #! Stats center - END DAY button 
        self.end_day_button = CTkButton(self.stats_center, text="End day", # TODO Replace with image
            fg_color="orange", hover_color="green", text_color="black", 
            font=sg.font_xxlarge, 
            command=lambda: self.end_day_actions()
            )
        self.end_day_button.pack(side="bottom", pady=10)



if __name__ == "__main__":
    CardGame()