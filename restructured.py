import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage, CTkToplevel, CTkTextbox
from PIL import Image
from datetime import datetime
import random, pyaudio, wave, threading
from tktooltip import ToolTip
from collections import Counter
from constants import (
    profiles, 
    player_items, enemy_items, 
    card_images_d, card_images_h, card_images_p, card_images_w, card_images_e, card_images_i
)

# TODO Add logging to the game
# TODO Add perpetrator
# TODO Add perpetrator item
# TODO Add game logic
# TODO Add game logic to GUI
# TODO Add sound effects
# TODO Add background music
# TODO Add game win/lose

class StyleGame:
    def __init__(self):
        self.bg_color = "#242426"
        self.fg_color = "#242426"
        self.font = ("Courier", 16, "bold")
        self.font_small = ("Courier", 15, "bold")
        self.font_large = ("Courier", 30, "bold")
        self.font_xlarge = ("Courier", 40, "bold")
        self.font_xxlarge = ("Courier", 50, "bold")
        self.main_color = "red"
        self.fill_color = "yellow"
        self.center_color = "green"

class ImageResizer:
    def __init__(self):
        pass

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

class Utils:
    def __init__(self, app, log_center, width):
        self.app = app
        self.width = width
        self.log_center = log_center

    def log(self, card_name, log_type, text):
        time_now = datetime.now()
        current_time = time_now.strftime("%H:%M:%S")
        self.log_center.configure("0.0", state="normal") 
        card_name = str(card_name).capitalize()
        if log_type == "full":
            self.log_center.insert("0.0", f"{current_time}: {text}\n")
        elif log_type == "card":
            self.log_center.insert("0.0", f"{current_time}: {card_name} {text}!\n")
        elif log_type == "item":
            self.log_center.insert("0.0", f"{current_time}: {card_name} {text}!\n")
        self.log_center.configure("0.0", state="disabled")

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

class CardStats:
    def tool_tip(cardname):
        card_info = profiles.get(cardname, None) # Find profile
        if card_info:
            return card_info.get("tooltip", None) # Find card-tooltip to profile
        else:
            return None
    def tool_tip_items(cardname):
        card_info = player_items.get(cardname, None) # Find profile
        if card_info:
            return card_info.get("tooltip", None) # Find card-tooltip to profile
        else:
            return None
    def tool_tip_enemy_items(cardname):
        card_info = enemy_items.get(cardname, None) # Find profile
        if card_info:
            return card_info.get("tooltip", None) # Find card-tooltip to profile
        else:
            return None

class CardGame:
    def __init__(self):
        # Main window
        self.app = CTk()
        self.width = self.app.winfo_screenwidth()
        self.height = self.app.winfo_screenheight()
        self.app.geometry(f"{self.width}x{self.height}+0+0")

        # Game stats
        self.stats()

        # Lists and dictionaries
        self.lists_and_dicts()

        # Welcome window and create 5 profiles to choose from
        self.welcome_window("Welcome to the game!")

        # Main board setup
        self.board_main()
        self.board_left()
        self.board_middle()
        self.board_right()
        
        # Populate board
        self.create_crime_scene("crime", "no") # Crime scene image
        self.create_random_witnesses() # Create witnesses
        self.create_new_item_in_locker() # Create new item in locker

        # Start game
        self.app.mainloop()
    
    #def screen_size(self):
    #    self.width = self.app.winfo_screenwidth()
    #    self.height = self.app.winfo_screenheight()
    #    return self.width, self.height

    #? GAME STATS AND LOGIC
    def stats(self):
        self.days_left = 30
        self.ap_left = 2
        self.perp_active = False
        self.ap_adjust = False

    def lists_and_dicts(self):

        # Profile lists and dictionaries
        self.choosen_profiles_list = [] # List of choosen profiles
        self.choosen_profiles_button_dict = {} # Dictionary of button-name to profiles

        self.waiting_room_list = [] # List of waiting room profiles
        self.waiting_room_profiles_button_dict = {} # Dictionary of button-name to profiles

        self.examination_list = [] # List of examination profiles
        self.examination_profiles_button_dict = {} # Dictionary of button-name to profiles

        self.witnesses_list = [] # List of witnesses
        self.witnesses_start_list = [] # List of start witnesses
        self.witnesses_button_to_dict = {} # Dictionary of button-name to witnesses

        # Item lists and dictionaries
        self.player_locker_item = "" # Locker item
        self.player_locker_item_button = None # Locker item button
        self.player_locker_item_button_to_dict = {} # Button-name CTK to forget.pack

        self.player_item_active = "" # Active item
        self.player_item_active_button = None # Active item button
        self.player_item_active_button_to_dict = {} # Button-name CTK to forget.pack

        self.player_special_item_active = "" # Active special item
        self.player_special_item_active_button = None # Active speical item button
        self.player_special_item_active_button_to_dict = {} # Button-name CTK to forget.pack

    def end_day_actions(self):

        # Add a new card to waiting room
        self.add_new_profile_to_waiting_room()

        # Add new item to locker
        self.create_new_item_in_locker()
        # add new active enemy item

        # Reset action points
        self.ap_left = 2
        #TODO Add configure label to show action points

    def examinations_actions(self):

        # Deduct action points
        self.ap_left -= 1
        #TODO Add configure label to show action points

    def witness_actions(self):

        # Deduct action points
        self.ap_left -= 1
        #TODO Add configure label to show action points

    #? WELCOME WINDOW
    def welcome_window(self, text):
        ir = ImageResizer()
        sg = StyleGame()

        # Window
        window = ctk.CTkToplevel(self.app)
        window.title("Choose three witnesses for questioning")
        window_width = 860
        window_height = 350

        # Center the window
        widthc = int(self.width / 2) - int(window_width / 2)
        window.geometry(f"{window_width}x{window_height}+{widthc}+500")

        # Window attributes
        window.attributes('-topmost', 'true')
        window.overrideredirect(True) # removes titlebar
        window.deiconify() # opens the window

        # Text-label inside window
        label_welcome = CTkLabel(window, text=text, font=sg.font)
        label_welcome.pack(pady=20, padx=20, side="top") 

        # exit button
        exit_day= CTkButton(
            window, text="", 
            image = ir.exit(f"images/gui/btn_end.png"),
            fg_color="transparent",
            command=lambda: (window.destroy(), self.start_cards_window()),
            hover=("False")
            )
        exit_day.pack()

    #? START CARDS
    def start_cards_window(self):
        sg = StyleGame() # Styles
        ir = ImageResizer() # image resizer

        self.start_cards = CTkToplevel(self.app)
        self.start_cards.title("Choose three witnesses for questioning")
        c_window_w, c_window_h = 860, 350
        widthc = int(self.width / 2) - int(c_window_w / 2)
        self.start_cards.geometry(f"{c_window_w}x{c_window_h}+{widthc}+500")
        self.start_cards.deiconify()
        #self.start_cards.withdraw() # temporary for testing main window.
        #self.start_cards.overrideredirect(True)  # Hides window titlebar

        # Start Pop-Up window
        self.start_cards_main = CTkFrame(self.start_cards, fg_color=sg.fg_color)
        self.start_cards_main.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.start_cards_fill = CTkFrame(self.start_cards_main, fg_color=sg.fg_color)
        self.start_cards_fill.pack(side="bottom")

        self.start_cards_label = CTkLabel(self.start_cards_main, text="Choose three witnesses for questioning", text_color="orange", font=("Arial", 24))
        self.start_cards_label.pack(side="top", ipady=20)

        self.create_random_profiles() # Create the cards to choose from

    def create_random_profiles(self):
        delt_profiles = random.sample(profiles.keys(), k=5) #! k=How many profiles to choose from at the beginning
        for name in delt_profiles: # Loop through the random choices and create the profiles
            card = self.create_profiles_buttons(name) # Create the profiles
            self.choosen_profiles_list.append(name) # Append card to list for further referance
            self.choosen_profiles_button_dict[name] = card # Store the profile in the dictionary
            #log(name, log_type="card", text="is created") # TODO Log the profiles creation

    def create_profiles_buttons(self, profile_name): # Create the cards to choose from
        ir = ImageResizer()
        sg = StyleGame()

        card = CTkButton( #! Rename self.card to self.start_card?
            self.start_cards_fill, 
            text="",  
            image=ir.card(card_images_d[f"{profile_name}_delt.png"]),
            fg_color="transparent",
            command=lambda n=profile_name: self.add_profiles_to_waiting_room(self.choosen_profiles_button_dict[n], n) # TODO Change to hand
        )
        card.pack(side="left", padx=0)
        card.bind('<Enter>', lambda event, n=profile_name, c=card: Bind.enter_d(event, n, c, card_images_d))
        card.bind('<Leave>', lambda event, n=profile_name, c=card: Bind.leave_d(event, n, c, card_images_d))
        ToolTip(card, msg=lambda: CardStats.tool_tip(profile_name), delay=0.2,
            parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
            fg="#ffffff", bg="#1c1c1c", font=sg.font, padx=10, pady=10)
        return card

    #? PLAYER ITEMS 
    def create_new_item_in_locker(self): # call init
        ir = ImageResizer()
        sg = StyleGame()

        if self.perp_active == True: # TODO CHANGE TO TRUE/FALSE FOR TESTING. False = no perp, True = perp
            item_keys = [key for key, value in player_items.items() if value['type'] == 'item']
            locker_item = random.choice(item_keys)
        else:
            locker_item = random.choice(list(player_items.keys()))

        if self.player_locker_item_button:
            self.player_locker_item_button.pack_forget()

        self.player_locker_item_button = CTkButton(
            self.left_bottom_center, text="", 
            image=ir.card(f"images/items/{locker_item}.png"),
            fg_color="transparent",
            command=lambda n=locker_item: self.player_item_type_active(n),
            hover=("False")
        )
        self.player_locker_item_button.pack(padx=0, side="left")

        self.player_locker_item = locker_item #! Item in locker
        self.player_locker_item_button[locker_item] = self.player_locker_item_button # Store the card in the dictionary
        self.player_locker_item_button_to_dict[locker_item] = self.player_locker_item_button  # Store the card in the dictionary

        self.player_locker_item_button.bind('<Enter>', lambda event, n=locker_item, c=self.player_locker_item_button: Bind.enter_i(event, n, c, card_images_i))
        self.player_locker_item_button.bind('<Leave>', lambda event, n=locker_item, c=self.player_locker_item_button: Bind.leave_i(event, n, c, card_images_i))
        ToolTip(self.player_locker_item_button, msg=lambda: CardStats.tool_tip_items(locker_item), delay=0.2,
            parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
            fg="#ffffff", bg="#1c1c1c", font=sg.font, padx=10, pady=10)
        

        #card_log(picked_card, log_type="item", text="added to store") 

    def player_item_type_active(self, item_name): # Check kind of item from store
        if item_name in player_items and player_items[item_name]['type'] == 'item':
            self.new_player_item_active(item_name)
        elif item_name in player_items and player_items[item_name]['type'] == 'special':
            self.new_player_special_item_active(item_name)

    def new_player_item_active(self, item_name): # Add new item to active
        ir = ImageResizer()
        sg = StyleGame()
          
        self.player_locker_item_button_to_dict[item_name].pack_forget()

        if self.player_item_active_button:
            self.player_item_active_button.pack_forget()
        
        self.player_item_active_button = CTkButton(
            self.left_middle_center, text="", 
            image=ir.card(f"images/items/{item_name}.png"),
            fg_color="transparent",
            command="",
            hover=("False")
        )
        self.player_item_active_button.pack(padx=0, side="left")

        self.player_item_active = item_name #! Active item
        self.player_item_active_button_to_dict[item_name] = self.player_item_active_button  # Store the card in the dictionary

        ToolTip(self.player_item_active_button, msg=lambda: CardStats.tool_tip_items(item_name), delay=0,
            parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
            fg="#ffffff", bg="#1c1c1c", font=sg.font, padx=10, pady=10)
        
        #card_log(card_name, log_type="item", text="added to item active") # TODO Log the card creation    

    def new_player_special_item_active(self, item_name): # Add new special item to active
        ir = ImageResizer()
        sg = StyleGame()
          
        self.player_locker_item_button_to_dict[item_name].pack_forget()

        if self.player_special_item_active_button:
            self.player_special_item_active_button.pack_forget()
        
        self.player_special_item_active_button = CTkButton(
            self.left_top_center, text="", 
            image=ir.card(f"images/items/{item_name}.png"),
            fg_color="transparent",
            command="",
            hover=("False")
        )
        self.player_special_item_active_button.pack(padx=0, side="left")

        self.player_special_item_active = item_name #! Active special item
        self.player_special_item_active_button_to_dict[item_name] = self.player_special_item_active_button  # Store the card in the dictionary

        ToolTip(self.player_special_item_active_button, msg=lambda: CardStats.tool_tip_items(item_name), delay=0,
            parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
            fg="#ffffff", bg="#1c1c1c", font=sg.font, padx=10, pady=10)
        
        #card_log(card_name, log_type="item", text="added to item active") # TODO Log the card creation    

    #? WAITING ROOM
    def add_profiles_to_waiting_room(self, profile_button, profile_name): # From delt to waiting room
        profile_button.pack_forget()
        self.choosen_profiles_list.remove(profile_name) # Update list for further reference
        self.waiting_room_list.append(profile_name) # Append card to list for further reference

        # Close choose-cards-window when X cards are selected
        if len(self.waiting_room_list) >= 3:
            last_card_names = self.choosen_profiles_list[-2:]
            for name in last_card_names:
                last_card = self.choosen_profiles_button_dict[name]
                last_card.pack_forget()

            self.start_cards.withdraw() # Close choose-cards-window when 3 cards are selected

        profile_button = CTkButton(
            self.waiting_room_center, 
            text="", 
            image=ImageResizer().card(f"images/profiles/{profile_name}_hand.png"),
            fg_color="transparent",
            command=lambda c=profile_button, n=profile_name: self.add_profiles_to_examination(c, n)
        )
        profile_button.pack(padx=0, side="left")
        self.waiting_room_profiles_button_dict[profile_name] = profile_button
        profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_h(event, n, c, card_images_h))
        profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_h(event, n, c, card_images_h))
        ToolTip(profile_button, msg=lambda: CardStats.tool_tip(profile_name), delay=0.2,
            parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
            fg="#ffffff", bg="#1c1c1c", font=StyleGame().font, padx=10, pady=10)

    def add_new_profile_to_waiting_room(self):
        ir = ImageResizer()
        sg = StyleGame()

        profile_button = None

        profile_name = random.choice(list(profiles.keys()))
        while profile_name in self.waiting_room_list or profile_name in self.examination_list: # While card exists on the board, pick new random card from the deck.
            profile_name = random.choice(list(profiles.keys()))

        if len(self.waiting_room_list) < 5: # Make a new card if the hand has more than one empty slot else smoke it!
            profile_button = CTkButton(
                self.waiting_room_center, text="", 
                image=ir.card(f"images/profiles/{profile_name}_hand.png"),
                fg_color="transparent",
                command=lambda c=profile_button, n=profile_name: self.add_profiles_to_examination(c, n),
                hover=("False")
            )
            profile_button.pack(padx=0, side="left")
            
            self.waiting_room_list.append(profile_name)
            self.waiting_room_profiles_button_dict[profile_name] = profile_button

            profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_h(event, n, c, card_images_h))
            profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_h(event, n, c, card_images_h))
            ToolTip(profile_button, msg=lambda: CardStats.tool_tip(profile_name), delay=0,
                parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                fg="#ffffff", bg="#1c1c1c", font=sg.font, padx=10, pady=10)
            #card_log(check_card, log_type="card", text="added to hand") # TODO Log the card creation        

    #? EXAMINATION
    def add_profiles_to_examination(self, profile_button, profile_name): # Change card from hand to play

        if len(self.examination_list) <= 4:
            self.waiting_room_profiles_button_dict[profile_name].pack_forget() # remove button from waiting room
            self.waiting_room_list.remove(profile_name) # Update list for further reference
            self.examination_list.append(profile_name) # Append card to list for further reference
            profile_button = CTkButton(
                self.examination_center, 
                text="", 
                image=ImageResizer().card(f"images/profiles/{profile_name}_play.png"),
                fg_color="transparent",
                command=lambda n=profile_name: self.add_profiles_to_witnesses(n)
            )
            profile_button.pack(padx=0, side="left")
            self.examination_profiles_button_dict[profile_name] = profile_button
            profile_button.bind('<Enter>', lambda event, n=profile_name, c=profile_button: Bind.enter_p(event, n, c, card_images_p))
            profile_button.bind('<Leave>', lambda event, n=profile_name, c=profile_button: Bind.leave_p(event, n, c, card_images_p))
            ToolTip(profile_button, msg=lambda: CardStats.tool_tip(profile_name), delay=0.2,
                parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                fg="#ffffff", bg="#1c1c1c", font=StyleGame().font, padx=10, pady=10)

        else:
            print("Error") #insert play_board full

    #? WITNESSES 
    def create_random_witnesses(self):


        witness_cards = random.sample(profiles.keys(), k=3) # k=How many witnesses (standard=3)
        for name in witness_cards: # Loop through the random choices and create the witnesses
            self.witnesses_list.append(name) # Append witness to list for further referance
            self.witnesses_start_list.append(name) # Append witness to list for further referance
            #card_log(name, log_type="card", text="witness created") # TODO Log the witnesses creation
            self.create_witnesses_buttons(name) # Create witness-cards

    def create_witnesses_buttons(self, profile_name): # Create witness-cards
        ir = ImageResizer()

        witness = CTkLabel(
            self.witnesses_center, text="",  
            image=ir.card(card_images_w[f"{profile_name}_wit.png"]),
            fg_color="transparent")         
        witness.pack(side="left", padx=2)
        self.witnesses_button_to_dict[profile_name] = witness
        return witness

    def add_profiles_to_witnesses(self, profile_name):
        ir = ImageResizer()

        self.examination_list.remove(profile_name) # Update list for further referance
        self.examination_profiles_button_dict[profile_name].pack_forget() # remove card  

        print(self.examination_list)

        count = self.witnesses_list.count(profile_name)
        if count <= 3: # If witness has 4 witness points (wit.png + w1.png + w2.png + w3.png)
            if profile_name in self.witnesses_list:
                self.witnesses_list.append(profile_name) # Add witness to list
                print(self.witnesses_list)
                count = self.witnesses_list.count(profile_name) - 1 # -1 because of the append above
                if 1 <= count < 4:
                    new_image = f"images/profiles/{profile_name}_w{count}.png"
                    self.witnesses_button_to_dict[profile_name].configure(image=ir.card(new_image))
                    #card_log(profile_name, log_type = "card", text="point added") # TODO Log the witnesses creation

    #? CRIMESCENE AND PERPETRATOR
    def create_crime_scene(self, image_name, new_image): 

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

    #? BOARD
    def board_main(self):
        sg = StyleGame() # Styles
        ir = ImageResizer() # image resizer

        # Main frame
        self.frame_main = CTkFrame(self.app, fg_color=sg.fg_color)
        self.frame_main.place(relheight=1, relwidth=1, relx=0.5, rely=0.5, anchor=ctk.CENTER) 

        # Main frame center
        self.frame_main_center = CTkFrame(self.frame_main, fg_color=sg.fg_color)
        self.frame_main_center.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # ! Main frame center - BACKGROUND IMAGE label
        self.frame_main_label = CTkLabel(self.frame_main_center, text="", image=ir.main_bg(f"images/gui/main_bg.png"))
        self.frame_main_label.grid(row=0, column=0, columnspan=5, rowspan=3)

    def board_left(self):
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
        self.left_top_main_label = CTkLabel(self.left_top_main, text="Special item")
        self.left_top_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

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
        self.left_middle_main_label = CTkLabel(self.left_middle_main, text="Active evidence")
        self.left_middle_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

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
        self.left_bottom_main_label = CTkLabel(self.left_bottom_main, text="Evidence locker")
        self.left_bottom_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Left bottom fill - GUI label
        self.left_bottom_fill_gui = CTkLabel(self.left_bottom_fill, text="", image=ir.side_bar(f"images/gui/sidebar_locker.png"))
        self.left_bottom_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Left bottom center
        self.left_bottom_center = CTkFrame(self.left_bottom_fill, width=10, height=10, fg_color=sg.center_color)
        self.left_bottom_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

    def board_middle(self):
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
        self.witness_main_label = CTkLabel(self.witnesses_main, text="Witnesses")
        self.witness_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

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
        self.perpetrator_item_main_label = CTkLabel(self.perpetrator_item_main, text="Perpetrator item")
        self.perpetrator_item_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

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
        self.examination_main_label = CTkLabel(self.examination_main, text="Examination")
        self.examination_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

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
        self.waiting_room_main_label = CTkLabel(self.waiting_room_main, text="Waiting room")
        self.waiting_room_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Waiting room fill - GUI label
        self.waiting_room_fill_gui = CTkLabel(self.waiting_room_fill, text="", image=ir.waiting_room(f"images/gui/waiting_room.png"))
        self.waiting_room_fill_gui.place(x=5, y=170, anchor=ctk.W)           

        # Waiting room center
        self.waiting_room_center = CTkFrame(self.waiting_room_fill, width=10, height=10, fg_color=sg.center_color)
        self.waiting_room_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

    def board_right(self):
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
        self.perpetrator_main_label = CTkLabel(self.perpetrator_main, text="Perpetrator")
        self.perpetrator_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Perpetrator fill - GUI label
        self.perpetrator_fill_gui = CTkLabel(self.perpetrator_fill, text="", image=ir.side_bar(f"images/gui/sidebar_active.png"))
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
        self.log_main_label = CTkLabel(self.log_main, text="Log")
        self.log_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Log fill - GUI label
        self.log_fill_gui = CTkLabel(self.log_fill, text="", image=ir.side_bar(f"images/gui/sidebar_active.png"))
        self.log_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Log center
        self.log_center = CTkFrame(self.log_fill, width=10, height=10, fg_color=sg.center_color)
        self.log_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

        #? RIGHT BOTTOM - STATS
        # Stats main
        self.stats_main = CTkFrame(self.frame_main_center, fg_color=sg.main_color)
        self.stats_main.grid(pady=10, padx=10, row=2, column=3, sticky = "n")

        # Stats fill
        self.stats_fill = CTkFrame(self.stats_main, width=300, height=340, fg_color=sg.fill_color)
        self.stats_fill.grid(pady=2, padx=2, row=0, column=1)

        #! Stats main - STATS label
        self.stats_main_label = CTkLabel(self.stats_main, text="Stats")
        self.stats_main_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        #! Stats fill - GUI label
        self.stats_fill_gui = CTkLabel(self.stats_fill, text="", image=ir.side_bar(f"images/gui/sidebar_active.png"))
        self.stats_fill_gui.place(x=5, y=170, anchor=ctk.W)

        # Stats center
        self.stats_center = CTkFrame(self.stats_fill, width=10, height=10, fg_color=sg.center_color)
        self.stats_center.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

        #! Stats center - END DAY button
        self.end_day = CTkButton(self.stats_center, text="", image = ir.card(f"images/gui/btn_end.png"),
            fg_color="transparent", command=lambda: self.end_day_actions(), hover=("False")
            )
        self.end_day.pack(side="bottom")

if __name__ == "__main__":
    CardGame()
