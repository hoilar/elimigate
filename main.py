import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage, CTkToplevel, CTkTextbox
from PIL import Image
from datetime import datetime
import random, pyaudio, wave, threading
from tktooltip import ToolTip
from collections import Counter

# constants
n_delt_cards = 5
max_cards_to_hands = 3
days_left = 30
actions_left = 2
points = 0
cur_multiplier = 0
item_card_active = None

# The deck of cards(Profiles)
Deck = {
    "adventurer": {"tooltip": "Lantern when in hand gives xxx. \nVelocipede when in play gives xxx", "handitem": "lantern", "playitem": "bicycle"},
    "agent": {"tooltip": "Magnifying glass when in hand gives xxx. \nPocket-watch when in play gives xxx", "handitem": "magnifyingglass", "playitem": "watch"},
    "archeolog": {"tooltip": "Magnifying glass when in hand gives xxx. \nWheelbarrow when in play gives xxx", "handitem": "magnifyingglass", "playitem": "wheelbarrow"},
    "barber": {"tooltip": "Goggles when in hand gives xxx. \nDagger when in play gives xxx", "handitem": "goggles", "playitem": "dagger"},
    "barkeeper": {"tooltip": "Tophat when in hand gives xxx. \nTeapot when in play gives xxx", "handitem": "tophat", "playitem": "teapot"},
    "butcher": {"tooltip": "Pipe when in hand gives xxx. \nDagger when in play gives xxx", "handitem": "pipe", "playitem": "dagger"},
    "coalworker": {"tooltip": "Goggles when in hand gives xxx. \nWheelbarrow when in play gives xxx", "handitem": "goggles", "playitem": "wheelbarrow"},
    "curator": {"tooltip": "Wheelbarrow when in hand gives xxx. \nTophat when in play gives xxx", "handitem": "wheelbarrow", "playitem": "tophat"},
    "detective": {"tooltip": "Whistle when in hand gives xxx. \nPipe when in play gives xxx", "handitem": "whistle", "playitem": "pipe"},
    "doctor": {"tooltip": "Velocipede when in hand gives xxx. \nGoggles when in play gives xxx", "handitem": "bicycle", "playitem": "goggles"},
    "fisherman": {"tooltip": "Dagger when in hand gives xxx. \nLantern when in play gives xxx", "handitem": "dagger", "playitem": "lantern"},
    "hobo": {"tooltip": "Baton when in hand gives xxx. \nPipe when in play gives xxx", "handitem": "baton", "playitem": "pipe"},
    "housewife": {"tooltip": "Teapot when in hand gives xxx. \nWhistle when in play gives xxx", "handitem": "whistle", "playitem": "teapot"},
    "hunter": {"tooltip": "Lantern when in hand gives xxx. \nDagger when in play gives xxx", "handitem": "lantern", "playitem": "dagger"},
    "inventor": {"tooltip": "Goggles when in hand gives xxx. \nMagnifying glass when in play gives xxx", "handitem": "goggles", "playitem": "magnifyingglass"},
    "magician": {"tooltip": "Lantern when in hand gives xxx. \nPocket-watch when in play gives xxx", "handitem": "lantern", "playitem": "watch"},
    "maid": {"tooltip": "Whistle when in hand gives xxx. \nTeapot when in play gives xxx", "handitem": "teapot", "playitem": "whistle"},
    "mayor": {"tooltip": "Teapot when in hand gives xxx. \nTophat when in play gives xxx", "handitem": "teapot", "playitem": "tophat"},
    "pi": {"tooltip": "Baton when in hand gives xxx. \nMagnifying glass when in play gives xxx", "handitem": "baton", "playitem": "magnifyingglass"},
    "policeman": {"tooltip": "Whistle when in hand gives xxx. \nBaton when in play gives xxx", "handitem": "whistle", "playitem": "baton"},
    "postman": {"tooltip": "Velocipede when in hand gives xxx. \nLantern when in play gives xxx", "handitem": "bicycle", "playitem": "lantern"},
    "professor": {"tooltip":"Tophat when in hand gives xxx. \nPocket-watch when in play gives xxx", "handitem": "tophat", "playitem": "watch"},
    "scientist": {"tooltip": "Pocket-watch when in hand gives xxx. \nGoggles when in play gives xxx", "handitem": "watch", "playitem": "goggles"},
    "vodouisant": {"tooltip": "Pocket-watch when in hand gives xxx. \nLantern when in play gives xxx", "handitem": "watch", "playitem": "dagger"},
}

Items = {
    "baton": {"tooltip": "xxx"},
    "bicycle": {"tooltip": "xxx"},
    "cab": {"tooltip": "S"},
    "cell": {"tooltip": "S"},
    "dagger": {"tooltip": "xxx"},
    "duster": {"tooltip": "S"},
    "fist": {"tooltip": "S"},
    "goggles": {"tooltip": "xxx"},
    "gun": {"tooltip": "S"},
    "hat": {"tooltip": "S"},
    "lantern": {"tooltip": "xxx"},
    "magnifyingglass": {"tooltip": "xxx"},
    "mail": {"tooltip": "S"},
    "newspaper": {"tooltip": "S"},
    "note": {"tooltip": "S"},
    "pipe": {"tooltip": "xxx"},
    "poster": {"tooltip": "S"},
    "safe": {"tooltip": "S"},
    "teapot": {"tooltip": "xxx"},
    "telegram": {"tooltip": "S"},
    "tophat": {"tooltip": "xxx"},
    "watch": {"tooltip": "xxx"},
    "wheelbarrow": {"tooltip": "xxx"},
    "whiskey": {"tooltip": "S"},
    "whistle": {"tooltip": "xxx"}
}

# Delt cards images update on mouse-hover 
card_images_d = {f"{name}_delt.png": f"images/profiles/{name}_delt.png" for name in Deck.keys()}
card_images_d.update({f"{name}_delt_hov.png": f"images/profiles/{name}_delt_hov.png" for name in Deck.keys()})
card_images_d.update({f"{name}_delt.png": f"images/profiles/{name}_delt.png" for name in Deck.keys()})

# Hand cards images update on mouse-hover 
card_images_h = {f"{name}_hand.png": f"images/profiles/{name}_hand.png" for name in Deck.keys()}
card_images_h.update({f"{name}_hand_hov.png": f"images/profiles/{name}_hand_hov.png" for name in Deck.keys()})
card_images_h.update({f"{name}_hand.png": f"images/profiles/{name}_hand.png" for name in Deck.keys()})

# Played cards images update on mouse-hover 
card_images_p = {f"{name}_play.png": f"images/profiles/{name}_play.png" for name in Deck.keys()}
card_images_p.update({f"{name}_play_hov.png": f"images/profiles/{name}_play_hov.png" for name in Deck.keys()})
card_images_p.update({f"{name}_play.png": f"images/profiles/{name}_play.png" for name in Deck.keys()})

# Witneess images
card_images_w = {f"{name}_wit.png": f"images/profiles/{name}_wit.png" for name in Deck.keys()}

# Played cards images update on mouse-hover 
card_images_i = {f"{name}.png": f"images/items/{name}.png" for name in Items.keys()}
card_images_i.update({f"{name}_hov.png": f"images/items/{name}_hov.png" for name in Items.keys()})
card_images_i.update({f"{name}.png": f"images/items/{name}.png" for name in Items.keys()})


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

class Bind:
    def __init__(self):
        pass
    
    def enter_d(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}_delt_hov.png"])
        card.configure(image=card_img, fg_color="transparent")

    def leave_d(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}_delt.png"])
        card.configure(image=card_img, fg_color="transparent")

    def enter_h(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}_hand_hov.png"])
        card.configure(image=card_img, fg_color="transparent")

    def leave_h(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}_hand.png"])
        card.configure(image=card_img, fg_color="transparent")

    def enter_p(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}_play_hov.png"])
        card.configure(image=card_img, fg_color="transparent")

    def leave_p(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}_play.png"])
        card.configure(image=card_img, fg_color="transparent")

    def enter_i(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}_hov.png"])
        card.configure(image=card_img, fg_color="transparent")

    def leave_i(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}.png"])
        card.configure(image=card_img, fg_color="transparent")

    def onEnter_end_day(event, end_day):
        img_btn_end = CardResizer.resize_button(f"images/gui/btn_endH.png")
        end_day.configure(image = img_btn_end)

    def onLeave_end_day(event, end_day):
        img_btn_end = CardResizer.resize_button(f"images/gui/btn_end.png")
        end_day.configure(image = img_btn_end)

    def onButton1_end_day(event, end_day):
        img_btn_end = CardResizer.resize_button(f"images/gui/btn_endP.png")
        end_day.configure(image = img_btn_end)

    def onButtonRelease_end_day(event, end_day):
        img_btn_end = CardResizer.resize_button(f"images/gui/btn_end.png")
        end_day.configure(image = img_btn_end)

class Style:
    def __init__(self):
        pass
    fc = "grey"

class CardResizer:
    def __init__(self):
        pass

    @staticmethod
    def r_main_bg(imagefile_url):
        # calcultate scaling of indivdual resolutions
        image_width = 1600 
        image_height = 1100 
        size = (image_width, image_height)

        our_card_image = CTkImage(Image.open(imagefile_url), None, size)
        return our_card_image

    @staticmethod 
    def resize_cards(imagefile_url):
        # calcultate scaling of indivdual resolutions
        card_size_width = 400
        card_size_height = 600
        image_width = (width / card_size_width) * 22 # change size of cards
        image_height = (height / card_size_height) * 88 # change size of cards
        size = (image_width, image_height)

        our_card_image = CTkImage(Image.open(imagefile_url), None, size)
        return our_card_image

    @staticmethod
    def resize_f_labels(imagefile_url, size=(260, 130)):
        our_card_image = CTkImage(Image.open(imagefile_url), None, size)
        return our_card_image

    @staticmethod
    def r_s_p(imagefile_url):
        # calcultate scaling of indivdual resolutions
        rsp_size_width = 900
        rsp_size_height = 360
        image_width = (width / rsp_size_width) * 320
        image_height = (height / rsp_size_height) * 90
        size = (image_width, image_height)

        our_card_image = CTkImage(Image.open(imagefile_url), None, size)
        return our_card_image

    @staticmethod
    def resize_f(imagefile_url, size=(800, 120)):
        our_card_image = CTkImage(Image.open(imagefile_url), None, size)
        return our_card_image
    
    @staticmethod
    def resize_button(imagefile_url, size=(180, 180)):
        our_card_image = CTkImage(Image.open(imagefile_url), None, size)
        return our_card_image

    @staticmethod
    def r_s_m(imagefile_url, size=(260, 350)):
        our_card_image = CTkImage(Image.open(imagefile_url), None, size)
        return our_card_image

class CardStats:
    def tool_tip(cardname):
        card_info = Deck.get(cardname, None) # Find profile
        if card_info:
            return card_info.get("tooltip", None) # Find card-tooltip to profile
        else:
            return None
    def tool_tip_items(cardname):
        card_info = Items.get(cardname, None) # Find profile
        if card_info:
            return card_info.get("tooltip", None) # Find card-tooltip to profile
        else:
            return None
        

class CardGame:
    
    def __init__(self):
        global height, width

        # Main window
        self.app = CTk()
        width, height = self.app.winfo_screenwidth(), self.app.winfo_screenheight()
        self.app.geometry(f"{width}x{height}+0+0")

        # Choose-cards window
        self.choosecards_window = CTkToplevel(self.app)
        self.choosecards_window.title("Choose three cards")
        self.configure_choosecards_window(width, height)
        self.setup_main_board(width, height)

        self.app.mainloop()

    def configure_choosecards_window(self, width, height):
        c_window_w, c_window_h = 860, 350
        widthc = int(width / 2) - int(c_window_w / 2)
        #heightc = int(height / 2) - int(c_window_h / 2)
        self.choosecards_window.geometry(f"{c_window_w}x{c_window_h}+{widthc}+500")
        self.choosecards_window.deiconify()
        #self.choosecards_window.withdraw() # temporary for testing main window.
        self.choosecards_window.overrideredirect(True)  # Hides window titlebar


    def setup_main_board(self, width, height):
        # Globals
        global days_left
        global choosen_cards_list
        global hand_cards_list
        global play_cards_list
        global item_cards_list
        global item_active
        global witness_cards_list

        # Delt cards lists
        choosen_cards_list = []
        card_name_to_card = {}

        # Hand cards lists
        hand_cards_list = []
        hand_card_name_to_card = {}

        # Play cards lists
        play_cards_list = []
        play_card_name_to_card = {}

        # Item lists
        item_cards_list = []
        item_active = ""
        item_card_name_to_card = {}
        new_item_name = {}
        active_item_name = {}

        # End day, new card list
        new_card_name = {}

        # Witnes cards list
        witness_cards_list = []
        witnesses_list = []
        witness_card_name_to_card = {}

         # Card-action logging
        def card_log(card_name, log_type):
            time_now = datetime.now()
            current_time = time_now.strftime("%H:%M:%S")
            section_left_b_log.configure("0.0", state="normal") 
            card_name = str(card_name).capitalize()
            if log_type == "full":
                section_left_b_log.insert("0.0", f"{current_time}: board is full!\n")
            else:
                section_left_b_log.insert("0.0", f"{current_time}: {card_name} is {log_type}!\n")
            section_left_b_log.configure("0.0", state="disabled")

        # Start Pop-Up window
        section_delt_main = CTkFrame(self.choosecards_window, fg_color="transparent")
        section_delt_main.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        section_delt = CTkFrame(section_delt_main, fg_color="transparent")
        section_delt.pack(side="bottom")

        section_delt_label = CTkLabel(section_delt_main, text="Choose 3 profiles", text_color="Orange", font=("Arial", 24))
        section_delt_label.pack(side="top", ipady=20)

        # Main frame
        frame_main_i = CTkFrame(self.app, fg_color="red")
        frame_main_i.place(relheight=1, relwidth=1, relx=0.5, rely=0.5, anchor=ctk.CENTER)

        frame_main = CTkFrame(frame_main_i, fg_color="yellow")
        frame_main.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        #### main image-frame
        frame_main_label = CTkLabel(frame_main, text="", image=CardResizer.r_main_bg(f"images/gui/main_bg.png"))
        frame_main_label.grid(row=0, column=0, columnspan=5, rowspan=3)

        ## Left top
        section_left_tm = CTkFrame(frame_main, fg_color="red")
        section_left_tm.grid(pady=10, padx=10, row=0, column=0, sticky = "n")

        ### Left top
        section_left_t = CTkFrame(section_left_tm, width=300, height=340, fg_color=Style.fc)
        section_left_t.grid(pady=2, padx=2, row=0, column=0, sticky = "n")

        #### Perp item label
        section_perp_item_label = CTkLabel(section_left_tm, text="Perp item")
        section_perp_item_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        ### Left top center
        section_left_t_c = CTkFrame(section_left_t, fg_color= "cyan")
        section_left_t_c.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ## Left middle
        section_left_mm = CTkFrame(frame_main, fg_color="red")
        section_left_mm.grid(pady=10, padx=10, row=1, column=0, sticky = "n")

        ### Left middle
        section_left_m = CTkFrame(section_left_mm, width=300, height=340, fg_color=Style.fc)
        section_left_m.grid(pady=2, padx=2, row=1, column=0, sticky = "n")

        #### Active item label
        section_active_label = CTkLabel(section_left_mm, text="Active item")
        section_active_label.grid(pady=0, padx=20, row=1, column=0, columnspan=4, sticky = "n")

        ### Left middle center
        section_left_m_c = CTkFrame(section_left_m, fg_color="cyan")
        section_left_m_c.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ## Left bottom
        section_left_bm = CTkFrame(frame_main, fg_color="red")
        section_left_bm.grid(pady=10, padx=10, ipadx=0, row=2, column=0, sticky = "n")

        ### Left bottom
        section_left_b = CTkFrame(section_left_bm, width=300, height=340, fg_color=Style.fc)
        section_left_b.grid(pady=2, padx=2, row=1, column=0, sticky = "n")

        #### Store label
        section_store_label = CTkLabel(section_left_bm, text="Todays item")
        section_store_label.grid(pady=0, padx=20, row=1, column=0, columnspan=4, sticky = "n")

        ### Left bottom center
        section_left_b_c = CTkFrame(section_left_b, fg_color="cyan")
        section_left_b_c.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ## Enemy section
        section_enemy_m = CTkFrame(frame_main, fg_color="red")
        section_enemy_m.grid(pady=10, padx=10, row=0, column=1, columnspan=1, sticky = "n")

        ### Frame for enemy-frame-image and cards
        section_enemy_card = CTkFrame(section_enemy_m, width=300, height=340, fg_color=Style.fc)
        section_enemy_card.grid(pady=2, padx=2, row=1, column=1, columnspan=2)

        #### enemy label
        section_enemy_label = CTkLabel(section_enemy_m, text="Perp unknown")
        section_enemy_label.grid(pady=0, padx=0, row=1, column=0, columnspan=3, sticky = "n")

        #### Enemy image-frame
        #section_enemy_label = CTkLabel(section_enemy_card, text="", image=CardResizer.r_s_p(f"images/gui/section_enemy.png"))
        #section_enemy_label.grid(row=0, column=1, columnspan=2)

        #### Where enemy cards in hand goes
        section_enemy = CTkFrame(section_enemy_card, fg_color="cyan")
        section_enemy.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ## Witness section
        section_witness_m = CTkFrame(frame_main, fg_color="red")
        section_witness_m.grid(pady=10, padx=0, row=0, column=2, columnspan=1, sticky = "n")

        ### Frame for witness-frame-image and cards
        section_witness_card = CTkFrame(section_witness_m, width=578, height=340, fg_color=Style.fc)
        section_witness_card.grid(pady=2, padx=2, row=1, column=1, columnspan=2)

        #### Witness label
        section_witness_label = CTkLabel(section_witness_m, text="Witnesses")
        section_witness_label.grid(pady=0, padx=10, row=1, column=0, columnspan=3, sticky = "n")

        #### Witness image-frame
        #section_witness_label = CTkLabel(section_witness_card, text="", image=CardResizer.r_s_p(f"images/gui/section_enemy.png"))
        #section_witness_label.grid(row=0, column=1, columnspan=2)

        #### Where witness cards in hand goes
        section_witness = CTkFrame(section_witness_card, fg_color="cyan")
        section_witness.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ## Play section
        section_play_m = CTkFrame(frame_main, fg_color="red")
        section_play_m.grid(pady=10, padx=10, row=1, column=1, columnspan=2, sticky = "n")

        ### Frame for play-frame-image and cards
        section_play_card = CTkFrame(section_play_m, width=900, height=340, fg_color=Style.fc)
        section_play_card.grid(pady=2, padx=2, row=1, column=1, columnspan=2)

        #### Play label
        section_play_label = CTkLabel(section_play_m, text="Examination")
        section_play_label.grid(pady=0, padx=20, row=1, column=0, columnspan=4, sticky = "n")

        #### Play image-frame
        #section_play_label = CTkLabel(section_play_card, text="", image=CardResizer.r_s_p(f"images/gui/section_play.png"))
        #section_play_label.place(x=0, y=180, anchor=ctk.W)
       
        #### Where played card goes
        section_play = CTkFrame(section_play_card, fg_color="cyan")
        section_play.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ## Hand section
        section_hand_m = CTkFrame(frame_main, fg_color="red")
        section_hand_m.grid(pady=10, padx=10, row=2, column=1, columnspan=2, sticky = "n")

        ### Frame for hand-frame-image and cards
        section_hand_card = CTkFrame(section_hand_m, width=900, height=340, fg_color=Style.fc)
        section_hand_card.grid(pady=2, padx=2, row=1, column=1, columnspan=2)

        #### hand label
        section_hand_label = CTkLabel(section_hand_m, text="Profiles")
        section_hand_label.grid(pady=0, padx=20, row=1, column=0, columnspan=4, sticky = "n")

        #### Hand image-frame
        #section_hand_label = CTkLabel(section_hand_card, text="", image=CardResizer.r_s_p(f"images/gui/section_hand.png"))
        #section_hand_label.grid(pady=0, row=0, column=1, columnspan=2)       

        #### Where cards in hand goes
        section_hand = CTkFrame(section_hand_card, fg_color="cyan")
        section_hand.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Right top
        section_right_tm = CTkFrame(frame_main, fg_color="red")
        section_right_tm.grid(pady=10, padx=10, row=0, column=4, sticky = "n")

        ## Right top
        section_right_t = CTkFrame(section_right_tm, width=300, height=340, fg_color=Style.fc)
        section_right_t.grid(pady=2, padx=2, row=0, column=0, sticky = "n")

        #### Perp label
        section_perp_label = CTkLabel(section_right_tm, text="Perp")
        section_perp_label.grid(pady=0, padx=20, row=0, column=0, columnspan=4, sticky = "n")

        ### Right top center
        section_right_t_c = CTkFrame(section_right_t, fg_color="cyan")
        section_right_t_c.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Right middle
        section_right_mm = CTkFrame(frame_main, fg_color="red")
        section_right_mm.grid(pady=10, padx=10, row=1, column=4, sticky = "n")

        ## Right middle
        section_right_m = CTkFrame(section_right_mm, width=300, height=340, fg_color=Style.fc)
        section_right_m.grid(pady=2, padx=2, row=1, column=0, sticky = "n")

        #### Log label
        section_log_label = CTkLabel(section_right_mm, text="Log")
        section_log_label.grid(pady=0, padx=20, row=1, column=0, columnspan=4, sticky = "n")

        ### Right middle center
        section_right_m_c = CTkFrame(section_right_m, fg_color="cyan")
        section_right_m_c.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ### Log textbox
        section_left_b_log = CTkTextbox(section_right_m_c, fg_color="#242426", width=180, height=200, wrap="word", state="disabled", corner_radius=0)
        section_left_b_log.place(x=10, y=101, anchor=ctk.W)

        # Right bottom
        section_right_bm = CTkFrame(frame_main, fg_color="red")
        section_right_bm.grid(pady=10, padx=10, row=2, column=4, sticky = "n")

        ## Right bottom
        section_right_b = CTkFrame(section_right_bm, width=300, height=340, fg_color=Style.fc)
        section_right_b.grid(pady=2, padx=2, row=1, column=0, sticky = "n")

        #### End day label
        section_end_label = CTkLabel(section_right_bm, text="End day++")
        section_end_label.grid(pady=0, padx=20, row=1, column=0, columnspan=4, sticky = "n")

        ### Right bottom center
        section_right_b_c = CTkFrame(section_right_b, fg_color="cyan")
        section_right_b_c.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        #### Days left label
        days_left_label = CTkLabel(section_right_b_c, text=f"Days left: {days_left}", font=("Arial", 24), fg_color="transparent", text_color="red")
        days_left_label.pack(side="top", pady=2)

        #### AP left label
        ap_left_label = CTkLabel(section_right_b_c, text=f"Actions left: {actions_left}", font=("Arial", 24), fg_color="transparent", text_color="red")
        ap_left_label.pack(side="top", pady=2)

        ### Sound test
        # sound_instance2 = Sound("bg_sound.wav")
        # sound_bg_btn_play = CTkButton (section_right_b_c , text="Music", command=lambda: sound_instance2.play_sound()) 
        # sound_bg_btn_play.pack(side="bottom")
        # sound_bg_btn_stop = CTkButton (section_right_b_c , text="Stop", command=lambda: sound_instance2.stop_sound()) 
        # sound_bg_btn_stop.pack(side="bottom")


        # Per ?
        def crime_scene(): # Make random new card to hand        
            crime = CTkButton(
                section_enemy, text="", 
                image=CardResizer.resize_cards(f"images/profiles/crime.png"),
                fg_color="transparent",
                command="",
                hover=("False")
            )
            crime.pack(padx=0, side="left")
        crime_scene()

        # New item card
        def new_item(): # Make random new card to hand
            global item_card
            global item_card_active
            picked_card = random.choice(list(Items.keys()))
        
            item_card = CTkButton(
                section_left_b_c, text="", 
                image=CardResizer.resize_cards(f"images/items/{picked_card}.png"),
                fg_color="transparent",
                command=lambda n=picked_card: new_item_active(new_item_name[n], n),
                hover=("False")
            )
            item_card.pack(padx=0, side="left")
            item_cards_list.append(picked_card) # Append card to list for further referance
            item_card_name_to_card[picked_card] = item_card
            item_card.bind('<Enter>', lambda event, n=picked_card, c=item_card: Bind.enter_i(event, n, c, card_images_i))
            item_card.bind('<Leave>', lambda event, n=picked_card, c=item_card: Bind.leave_i(event, n, c, card_images_i))
            ToolTip(item_card, msg=lambda: CardStats.tool_tip_items(picked_card), delay=0.2,
                parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                fg="#ffffff", bg="#1c1c1c", font=("Agency FB", 18), padx=10, pady=10)
            new_item_name[picked_card] = item_card  # Store the card in the dictionary
            card_log(picked_card, log_type="item")

        new_item() # New item

        # WITNESSES
        def create_witnesses(card_name): #Create the cards to choose from
            
            cardw = CTkButton(
                section_witness, text="",  
                image=CardResizer.resize_cards(card_images_w[f"{card_name}_wit.png"]),
                fg_color="transparent",
                hover=("False"),
                command="")            
            cardw.pack(side="left", padx=0)
            witness_card_name_to_card[card_name] = cardw
            return cardw
        
        witness_cards = random.sample(Deck.keys(), k=3) # k=How many cards to choose from at the beginning
        for name in witness_cards: # Loop through the random choices and create the cards
            card = create_witnesses(name)
            witness_cards_list.append(name) # Append card to list for further referance
            card_log(name, log_type="Witness created")
        
        # DELT
        def create_cards(card_name): #Create the cards to choose from
            card = CTkButton(
                section_delt, text="",  
                image=CardResizer.resize_cards(card_images_d[f"{card_name}_delt.png"]),
                fg_color="transparent",
                command=lambda n=card_name: change_to_hand(card_name_to_card[n], n)
            )
            card.pack(side="left", padx=0)
            card.bind('<Enter>', lambda event, n=card_name, c=card: Bind.enter_d(event, n, c, card_images_d))
            card.bind('<Leave>', lambda event, n=card_name, c=card: Bind.leave_d(event, n, c, card_images_d))
            ToolTip(card, msg=lambda: CardStats.tool_tip(card_name), delay=0.2,
                parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                fg="#ffffff", bg="#1c1c1c", font=("Agency FB", 18), padx=10, pady=10)
            return card
        
        deltcards = random.sample(Deck.keys(), k=n_delt_cards) # k=How many cards to choose from at the beginning
        for name in deltcards: # Loop through the random choices and create the cards
            card = create_cards(name)
            choosen_cards_list.append(name) # Append card to list for further referance
            card_name_to_card[name] = card
            card_log(name, log_type="created")

        # New active item card
        def new_item_active(card, card_name): # Make random new card to hand
            global item_card_active
            global item_active
            global actions_left

            actions_left -= 1 # Remove 1 action
            ap_left_label.configure(text=f"Actions left: {actions_left}") # Update actions left label
            
            item_card.pack_forget()

            if item_card_active:
                item_card_active.pack_forget()
            
            item_card_active = CTkButton(
                section_left_m_c, text="", 
                image=CardResizer.resize_cards(f"images/items/{card_name}.png"),
                fg_color="transparent",
                command="",
                hover=("False")
            )
            item_card_active.pack(padx=0, side="left")
            item_active = card_name # empty item_active_list and append new card
            item_card_name_to_card[card] = item_card_active
           # item_card.bind('<Enter>', lambda event, n=card, c=card: Bind.enter_i(event, n, c, card_images_i))
           # item_card.bind('<Leave>', lambda event, n=card, c=card: Bind.leave_i(event, n, c, card_images_i))
            ToolTip(item_card_active, msg=lambda: CardStats.tool_tip_items(card_name), delay=0,
                parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                fg="#ffffff", bg="#1c1c1c", font=("Agency FB", 18), padx=10, pady=10)
            active_item_name[card_name] = item_card_active  # Store the card in the dictionary
            card_log(card_name, log_type="item")

        # HAND
        def change_to_hand(card, card_name): # Change card from choosen to hand
            card.pack_forget()
            choosen_cards_list.remove(card_name) # Update list for further referance
            hand_cards_list.append(card_name) # Append card to list for further referance
            
            # Close choose-cards-window when X cards are selected
            if len(hand_cards_list) >= max_cards_to_hands:
                last_card_names = choosen_cards_list[-2:]
                for name in last_card_names:
                    last_card = card_name_to_card[name]
                    last_card.pack_forget()
                    
                self.choosecards_window.withdraw() # Close choose-cards-window when 3 cards are selected

            card = CTkButton(
                section_hand, text="", 
                image=CardResizer.resize_cards(f"images/profiles/{card_name}_hand.png"),
                fg_color="transparent",
                command=lambda c=card, n=card_name: change_to_play(c, n)
            )
            card.pack(padx=0, side="left")
            hand_card_name_to_card[card_name] = card
            card.bind('<Enter>', lambda event, n=card_name, c=card: Bind.enter_h(event, n, c, card_images_h))
            card.bind('<Leave>', lambda event, n=card_name, c=card: Bind.leave_h(event, n, c, card_images_h))
            ToolTip(card, msg=lambda: CardStats.tool_tip(card_name), delay=0.2,
                parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                fg="#ffffff", bg="#1c1c1c", font=("Agency FB", 18), padx=10, pady=10)
            card_to_hand(card_name)

        def card_to_hand(card_name): # When card travels to hand actions 
            sound_instance1 = Sound("card.wav")
            sound_instance1.play_sound()
            card_log(card_name, log_type="selected")

        # PLAY
        def change_to_play(card, card_name): # Change card from hand to play
            global actions_left

            if actions_left <= 0:    
                text = f"Actions left: {actions_left} \nYou need to end day!"
                max_cards_reached(text)
                # add sound🔊
            else:

                actions_left -= 1 # Remove 1 action
                ap_left_label.configure(text=f"Actions left: {actions_left}") # Update actions left label

                if len(play_cards_list) <= 4:
                    hand_card = hand_card_name_to_card[card_name]
                    hand_card.pack_forget() # remove card
                    hand_cards_list.remove(card_name) # Update list for further referance
                    play_cards_list.append(card_name) # Append card to list for further referance
                    card = CTkButton(
                        section_play, text="", 
                        image=CardResizer.resize_cards(f"images/profiles/{card_name}_play.png"),
                        fg_color="transparent",
                        command=lambda n=card_name: purge_card(n),
                        hover=("False")
                    )
                    card.pack(padx=0, side="left")
                    play_card_name_to_card[card_name] = card
                    card.bind('<Enter>', lambda event, n=card_name, c=card: Bind.enter_p(event, n, c, card_images_p))
                    card.bind('<Leave>', lambda event, n=card_name, c=card: Bind.leave_p(event, n, c, card_images_p))
                    ToolTip(card, msg=lambda: CardStats.tool_tip(card_name), delay=0.2,
                        parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                        fg="#ffffff", bg="#1c1c1c", font=("Agency FB", 18), padx=10, pady=10)
                    card_in_play(card_name) # card actions

                else:
                    print("feil") #insert play_board full
                    card_log(card_name, log_type = "full")  
                    text = f"Max cards are played. \nYou need to purge card first!"
                    max_cards_reached(text)
                    # add sound🔊


        def card_in_play(card_name): # When card travels to play actions 
            sound_instance1 = Sound("card.wav")
            sound_instance1.play_sound()
            card_log(card_name, log_type = "played")  

            print(item_active)
            
        def purge_card(card_name): # When card is purged travels to hand 
            global witness_cards_list
            global actions_left

            if actions_left <= 0:    
                text = f"Actions left: {actions_left} \nYou need to end day!"
                max_cards_reached(text)
                # add sound🔊
            else:
                actions_left -= 1 # Remove 1 action
                ap_left_label.configure(text=f"Actions left: {actions_left}") # Update actions left label

                witnesses_list.append(card_name)
                play_cards_list.remove(card_name)
                play_card_name_to_card[card_name].pack_forget()

                sound_instance3 = Sound("purged.wav")
                sound_instance3.play_sound()
                card_log(card_name, log_type = "purged")

                if card_name in witness_cards_list:
                    count = witnesses_list.count(card_name)
                    if 1 <= count < 4:
                        new_image = f"images/profiles/{card_name}_w{count}.png"
                        witness_card_name_to_card[card_name].configure(image=CardResizer.resize_cards(new_image))

        # END DAY
        end_day = CTkButton( # End day button. Initialize check cards attributes for game rules
            section_right_b_c, text="", 
            image = CardResizer.resize_button(f"images/gui/btn_end.png"),
            fg_color="transparent",
            command=lambda: (new_card(), game_rules()),
            hover=("False")
            )
        end_day.pack(side="bottom")
        end_day.bind('<Enter>',  lambda event, e=end_day: Bind.onEnter_end_day(event, e))
        end_day.bind('<Leave>',  lambda event, e=end_day: Bind.onLeave_end_day(event, e))
        end_day.bind('<Button-1>',  lambda event, e=end_day: Bind.onButton1_end_day(event, e))
        end_day.bind('<ButtonRelease>',  lambda event, e=end_day: Bind.onButtonRelease_end_day(event, e))


        # NEW CARD end day button
        def new_card(): # Make random new card to hand
            check_card = random.choice(list(Deck.keys()))
            #self.choosecards_window.deiconify() # New pop-up choose-cards window?
            #create_cards(name, section_delt) # New pop-up choose-cards window?

            while check_card in hand_cards_list or check_card in play_cards_list: # While card exists on the board, pick new random card from the deck.
                check_card = random.choice(list(Deck.keys()))

            if len(hand_cards_list) < 5: # Make a new card if the hand has more than one empty slot else smoke it!
                hand_card = CTkButton(
                    section_hand, text="", 
                    image=CardResizer.resize_cards(f"images/profiles/{check_card}_hand.png"),
                    fg_color="transparent",
                    command=lambda new_card_name=new_card_name, n=check_card: change_to_play(new_card_name[n], n),
                    hover=("False")
                )
                hand_card.pack(padx=0, side="left")
                hand_cards_list.append(check_card) # Append card to list for further referance
                hand_card_name_to_card[check_card] = hand_card
                hand_card.bind('<Enter>', lambda event, n=check_card, c=hand_card: Bind.enter_h(event, n, c, card_images_h))
                hand_card.bind('<Leave>', lambda event, n=check_card, c=hand_card: Bind.leave_h(event, n, c, card_images_h))
                ToolTip(hand_card, msg=lambda: CardStats.tool_tip(check_card), delay=0,
                    parent_kwargs={"bg": "black", "padx": 2, "pady": 2},
                    fg="#ffffff", bg="#1c1c1c", font=("Agency FB", 18), padx=10, pady=10)
                new_card_name[check_card] = hand_card  # Store the card in the dictionary
                card_log(check_card, log_type="handed")
                
                print(f"testprint: {item_card}")
                item_card.pack_forget() # Remove item card
                new_item() # New item card
            else:
                item_card.pack_forget() # Remove item card
                new_item() # New item card
                text = f"Hands full! \n{str(check_card)[0].upper() + str(check_card)[1:].lower()} smoked!" # Tell what card is missed if hand is full
                card_log(check_card, log_type="smoked")
                # add sound🔊
                max_cards_reached(text)

        def game_rules():
            global days_left
            global actions_left # Reset actions left
            days_left -= 1 # Remove 1 day
            days_left_label.configure(text=f"Days left: {days_left}") # Update days left label
            actions_left = 2 # Reset actions left
            ap_left_label.configure(text=f"Actions left: {actions_left}") # Update actions left label
            
            counts = Counter(witnesses_list)
            if list(counts.values()).count(3) >= 3:
                print("Perp identified!") # create perp card (top right)
        
            for card in play_cards_list:
                if Deck[card]['playitem'] == item_active: # Replace item_active with actual item name
                    print(f"The item {item_active} is in play.") # Game logic
                else:
                    print(f"The item {item_active} is not in play.")

            '''Example

            for card in play_cards_list:
                if Deck[card]['playitem'] in Items and Items[Deck[card]['playitem']]['tooltip'] == 'xxx':
                    if Deck[card]['playitem'] == 'baton': 
                        action_points += 1
                    elif Deck[card]['playitem'] == 'bicycle':
                        action_points += 2
                    elif Deck[card]['playitem'] == 'dagger':
                        action_points += 3
                    elif Deck[card]['playitem'] == 'goggles':
                        action_points += 4
                    elif Deck[card]['playitem'] == 'lantern':
                        action_points += 5
                    elif Deck[card]['playitem'] == 'magnifyingglass':
                        action_points += 6
                    elif Deck[card]['playitem'] == 'pipe':
                        action_points += 7
                    elif Deck[card]['playitem'] == 'teapot':
                        action_points += 8
                    elif Deck[card]['playitem'] == 'tophat':
                        action_points += 9
                    elif Deck[card]['playitem'] == 'watch':
                        action_points += 10
                    elif Deck[card]['playitem'] == 'wheelbarrow':
                        action_points += 11
                    elif Deck[card]['playitem'] == 'whistle':
                        action_points += 12
            '''

        # Pop-up window
        def max_cards_reached(text):
            max_cards_window = ctk.CTkToplevel(self.app)
            d_window_w = 860
            d_window_h = 350

            # Center the window
            widthc = int(width / 2) - int(d_window_w / 2)
            heightc = int(height / 2) - int(d_window_h / 2)
            max_cards_window.geometry(f"{d_window_w}x{d_window_h}+{widthc}+500")

            # Window attributes
            max_cards_window.attributes('-topmost', 'true')
            max_cards_window.overrideredirect(True) # removes titlebar
            max_cards_window.deiconify() # opens the window

            # Text-label inside window
            label_too_many= CTkLabel(max_cards_window, text=text)
            label_too_many.pack() 

            # exit button
            exit_day= CTkButton(
                max_cards_window, text="", 
                image = CardResizer.resize_button(f"images/gui/btn_end.png"),
                fg_color="transparent",
                command=lambda: max_cards_window.destroy(),
                hover=("False")
                )
            exit_day.pack()      

if __name__ == "__main__":
    CardGame()


## use this for enemy dec: https://github.com/TheCheapestPixels/pychology/blob/main/README.md
