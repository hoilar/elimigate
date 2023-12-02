import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage, CTkToplevel
from PIL import Image, ImageTk
import random, time


# constants
max_cards_in_hands = 3
global days_left, points, cur_multiplier
days_left = 30
points = 0
cur_multiplier = 0

class Bind:
    def __init__(self):
        pass
    
    def enter(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}_sus.png"])
        card.configure(image=card_img, fg_color="transparent")

    def leave(event, name, card, card_images):
        card_img = CardResizer.resize_cards(card_images[f"{name}_wit.png"])
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
    def resize_cards(cardtext, size=(140, 200)):
        our_card_img = Image.open(cardtext)
        our_card_resize_image = our_card_img.resize(size)
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)
        return our_card_image

    @staticmethod
    def resize_f_labels(label, size=(260, 130)):
        our_card_img = Image.open(label)
        our_card_resize_image = our_card_img.resize(size)
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)
        return our_card_image

    @staticmethod
    def r_s_p(label, size=(900, 360)):
        our_card_img = Image.open(label)
        our_card_resize_image = our_card_img.resize(size)
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)
        return our_card_image

    @staticmethod
    def resize_f(label, size=(800, 120)):
        our_card_img = Image.open(label)
        our_card_resize_image = our_card_img.resize(size)
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)
        return our_card_image
    
    @staticmethod
    def resize_button(label, size=(180, 180)):
        our_card_img = Image.open(label)
        our_card_resize_image = our_card_img.resize(size)
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)
        return our_card_image

    @staticmethod
    def r_s_m(label, size=(260, 350)):
        our_card_img = Image.open(label)
        our_card_resize_image = our_card_img.resize(size)
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)
        return our_card_image


class CardGameApp:
    def __init__(self):
        self.card_resizer = CardResizer()

        self.app = CTk()
        width, height = self.app.winfo_screenwidth(), self.app.winfo_screenheight()
        self.app.geometry(f"{width}x{height}+0+0")

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
        global days_left

        # Start Pop-Up window
        section_delt_main = CTkFrame(self.choosecards_window, fg_color=Style.fc)
        section_delt_main.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        section_delt = CTkFrame(section_delt_main, fg_color=Style.fc)
        section_delt.pack(side="bottom")

        section_delt_label = CTkLabel(section_delt_main, text="Choose 3 cards")
        section_delt_label.pack(side="top", ipady=20)

        # Main frame
        frame_main_i = CTkFrame(self.app, fg_color="#dfe0e3")
        frame_main_i.place(relheight=1, relwidth=1, relx=0.5, rely=0.5, anchor=ctk.CENTER)

        frame_main = CTkFrame(frame_main_i, fg_color="transparent")
        frame_main.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Left section
        section_left = CTkFrame(frame_main, fg_color="black")
        section_left.grid(pady=5, padx=5, ipady=5, ipadx=5, row=0, column=0, rowspan=3, sticky = "n")

        section_left_t = CTkFrame(section_left, fg_color= Style.fc)
        section_left_t.grid(pady=20, padx=20, ipady=60, ipadx=40, row=0, column=0, sticky = "n")

        def slider_event(value):
            print(value)

        slider = ctk.CTkSlider(section_left_t, from_=0, to=5, command=slider_event)
        slider.pack()
        slider.configure(number_of_steps=5)

        section_left_m = CTkFrame(section_left, fg_color=Style.fc)
        section_left_m.grid(pady=20, padx=20, ipady=60, ipadx=40, row=1, column=0, sticky = "n")

        section_left_b = CTkFrame(section_left, fg_color=Style.fc)
        section_left_b.grid(pady=0, padx=0, ipady=0, ipadx=0, row=2, column=0, sticky = "n")

        section_left_b_img = CTkLabel(section_left_b, text="", image=CardResizer.r_s_m(f"images/gui/section_left_m_off.png"))
        section_left_b_img.grid(pady=0, row=0, column=0, sticky = "n")

        section_left_b_text = CTkLabel(section_left_b, text="test", fg_color="#242426")
        section_left_b_text.place(x=10, y=100, anchor=ctk.W)

        # Enemy section
        section_enemy_m = CTkFrame(frame_main, fg_color="transparent")
        section_enemy_m.grid(pady=10, padx=20, ipady=10, row=0, column=1, columnspan=2, sticky = "n")

        section_enemy_card = CTkFrame(section_enemy_m, width=900, height=340, fg_color="transparent")
        section_enemy_card.grid(pady=10, padx=20, ipady=10, row=1, column=1, columnspan=2)

        section_enemy_label = CTkLabel(section_enemy_card, text="", image=CardResizer.r_s_p(f"images/gui/section_enemy.png"))
        section_enemy_label.grid(row=0, column=1, columnspan=2)

        section_enemy = CTkFrame(section_enemy_card, fg_color="transparent")
        section_enemy.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Play section
        section_play_m = CTkFrame(frame_main, fg_color="transparent")
        section_play_m.grid(pady=10, padx=20, ipady=10, row=1, column=1, columnspan=2, sticky = "n")

        #section_play_label = CTkLabel(section_play_m, text="", image=CardResizer.resize_f_labels(f"images/play.png"))
        #section_play_label.grid(pady=5, row=0, column=1, columnspan=2)

        section_play_card = CTkFrame(section_play_m, width=900, height=340, fg_color="transparent")
        section_play_card.grid(pady=0, padx=20, ipady=10, row=1, column=1, columnspan=2)

        section_play_label = CTkLabel(section_play_card, text="", image=CardResizer.r_s_p(f"images/gui/section_play.png"))
        section_play_label.place(x=0, y=180, anchor=ctk.W)

        section_play = CTkFrame(section_play_card, fg_color="transparent")
        section_play.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

        # Hand section
        section_hand_m = CTkFrame(frame_main, fg_color="transparent")
        section_hand_m.grid(pady=10, padx=20, ipady=0, row=2, column=1, columnspan=2, sticky = "n")

        section_hand_card = CTkFrame(section_hand_m, width=900, fg_color="transparent")
        section_hand_card.grid(pady=5, padx=20, ipady=0, row=2, column=1, columnspan=2)

        section_hand_label = CTkLabel(section_hand_card, text="", image=CardResizer.r_s_p(f"images/gui/section_hand.png"))
        section_hand_label.grid(pady=0, row=0, column=1, columnspan=2)        

        section_hand = CTkFrame(section_hand_card, fg_color="transparent")
        section_hand.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

        # Right section
        section_right = CTkFrame(frame_main, fg_color=Style.fc)
        section_right.grid(pady=5, padx=5, ipady=5, ipadx=5, row=0, column=4, rowspan=3, sticky = "n")

        section_right_t = CTkFrame(section_right, fg_color=Style.fc)
        section_right_t.grid(pady=20, padx=20, ipady=60, ipadx=40, row=0, column=0, sticky = "n")

        section_right_t_label = CTkLabel(section_right_t, text="DAYS LEFT: " + str(days_left))
        section_right_t_label.grid(pady=0, row=0, column=1, columnspan=2, sticky = "n")

        section_right_m = CTkFrame(section_right, fg_color=Style.fc)
        section_right_m.grid(pady=20, padx=20, ipady=60, ipadx=40, row=1, column=0, sticky = "n")

        section_right_m_label = CTkLabel(section_right_m, text="Points: ")
        section_right_m_label.grid(pady=0, row=0, column=1, columnspan=2, sticky = "n")

        section_right_b = CTkFrame(section_right, fg_color=Style.fc)
        section_right_b.grid(pady=20, padx=20, ipady=60, ipadx=40, row=2, column=0, sticky = "n")

        end_day = CTkButton(
            section_right_b, text="", 
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

        #section_main_label = CTkLabel(frame_main_i, text="", image=CardResizer.r_s_p(f"images/gui/section_enemy.png"), fg_color="transparent")
        #section_main_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        def day_ended_full(text):
            end_day_full_window = ctk.CTkToplevel(self.app)
            end_day_full_window.title("Day Ended")
            d_window_w = 860
            d_window_h = 350
            # CENTER WINDOW
            widthc = int(width / 2) - int(d_window_w / 2)
            heightc = int(height / 2) - int(d_window_h / 2)
            end_day_full_window.geometry(f"{d_window_w}x{d_window_h}+{widthc}+500")
            end_day_full_window.attributes('-topmost', 'true')
            end_day_full_window.overrideredirect(True)
            end_day_full_window.deiconify()

            label_too_many_in_hand= CTkLabel(end_day_full_window, text=text)
            label_too_many_in_hand.pack()

            exit_day= CTkButton(
                end_day_full_window, text="", 
                image = CardResizer.resize_button(f"images/gui/btn_end.png"),
                fg_color="transparent",
                command=lambda: end_day_full_window.withdraw(),
                hover=("False")
                )
            exit_day.pack()                     

        deck = [
                "adventurer", 
                "agent", 
                "archeolog", 
                "barber", 
                "barkeeper", 
                "butcher", 
                "coalworker", 
                "curator", 
                "detective", 
                "doctor", 
                "fisherman", 
                "hobo", 
                "housewife",
                "hunter", 
                "inventor", 
                "magician", 
                "maid", 
                "mayor", 
                "pi",
                "policeman", 
                "postman",
                "professor", 
                "scientist", 
                "vodouisant", 
            ]

        # Dictionary of card images
        card_images = {f"{name}.png": f"images/profiles/{name}.png" for name in deck}
        card_images.update({f"{name}_sus.png": f"images/profiles/{name}_sus.png" for name in deck})
        card_images.update({f"{name}_wit.png": f"images/profiles/{name}_wit.png" for name in deck})

        # 5 random cards to choose from
        deltcards = random.sample(deck, k=5)

        choosen_cards_list = []
        card_name_to_card = {}

        def create_cards(name, section_delt):
            card = CTkButton(
                section_delt, text="",  
                image=CardResizer.resize_cards(card_images[f"{name}.png"]),
                fg_color="transparent",
                command=lambda n=name: change_to_hand(card_name_to_card[n], n)
            )
            card.pack(side="left", padx=0)
            card.bind('<Enter>', lambda event, n=name, c=card: Bind.enter(event, n, c, card_images))
            card.bind('<Leave>', lambda event, n=name, c=card: Bind.leave(event, n, c, card_images))
            return card

        for name in deltcards:
            card = create_cards(name, section_delt)
            choosen_cards_list.append(name)
            card_name_to_card[name] = card

        hand_cards_list = []
        hand_card_name_to_card = {}

        def change_to_hand(card, card_name):
            card.pack_forget()
            choosen_cards_list.remove(card_name)
            hand_cards_list.append(card_name)

            # Close choose-cards-window when X cards are selected
            if len(hand_cards_list) >= max_cards_in_hands:
                last_card_names = choosen_cards_list[-2:]
                for name in last_card_names:
                    last_card = card_name_to_card[name]
                    last_card.pack_forget()
                self.choosecards_window.withdraw() # Call the method to close the window

            card = CTkButton(
                section_hand, text="", 
                image=CardResizer.resize_cards(f"images/profiles/{card_name}.png"),
                fg_color="transparent",
                command=lambda c=card, n=card_name: change_to_play(c, n)
            )
            card.pack(padx=0, side="left")
            hand_card_name_to_card[card_name] = card
            card.bind('<Enter>', lambda event, n=card_name, c=card: Bind.enter(event, n, c, card_images))
            card.bind('<Leave>', lambda event, n=card_name, c=card: Bind.leave(event, n, c, card_images))
            return card

        global play_cards_list
        play_cards_list = []
        play_card_name_to_card = {}

        def change_to_play(card, card_name):
            if len(play_cards_list) <= 4:
                hand_card = hand_card_name_to_card[card_name]
                hand_card.pack_forget()
                hand_cards_list.remove(card_name)
                play_cards_list.append(card_name)
                card = CTkButton(
                    section_play, text="", 
                    image=CardResizer.resize_cards(f"images/profiles/{card_name}.png"),
                    fg_color="transparent",
                    command=lambda n=card_name: purge_card(n),
                    hover=("False")
                )
                card.pack(padx=0, side="left")
                play_card_name_to_card[card_name] = card
                card.bind('<Enter>', lambda event, n=card_name, c=card: Bind.enter(event, n, c, card_images))
                card.bind('<Leave>', lambda event, n=card_name, c=card: Bind.leave(event, n, c, card_images))

                card_in_play()

            else:
                print("feil") #insert play_board full
      
        purge_one = [
                "adventurer", 
                "agent", 
                "archeolog", 
                "barber", 
                "barkeeper", 
                "butcher", 
                "coalworker", 
                "curator",  
            ]
        
        purge_two = [
                "detective", 
                "doctor", 
                "fisherman", 
                "hobo", 
                "housewife",
                "hunter", 
                "inventor", 
                "magician", 
                "maid", 
                "mayor", 
                "pi",
            ]
        
        purge_three = [
                "policeman", 
                "postman",
                "professor", 
                "scientist", 
                "vodouisant", 
            ]

        def purge_card(card_name):
            global points
            play_cards_list.remove(card_name)
            play_card_name_to_card[card_name].pack_forget()
            if card_name in purge_one:
                points += 1 + cur_multiplier
                section_right_m_label.configure(section_right_m, text="Points: " + str(points))
            elif card_name in purge_two:
                points += 2 + cur_multiplier
                section_right_m_label.configure(section_right_m, text="Points: " + str(points))
            elif card_name in purge_three:
                points += 3 + cur_multiplier
                section_right_m_label.configure(section_right_m, text="Points: " + str(points))
            
            card_in_play()
        
        new_card_name = {}

        def new_card(): #END DAY
            check_card = random.choice(deck)

            while check_card in hand_cards_list or check_card in play_cards_list:
                check_card = random.choice(deck)

            if len(hand_cards_list) < 5:
                hand_card = CTkButton(
                    section_hand, text="", 
                    image=CardResizer.resize_cards(f"images/profiles/{check_card}.png"),
                    fg_color="transparent",
                    command=lambda new_card_name=new_card_name, n=check_card: change_to_play(new_card_name[n], n),
                    hover=("False")
                )
                hand_card.pack(padx=0, side="left")
                hand_cards_list.append(check_card)
                hand_card_name_to_card[check_card] = hand_card
                hand_card.bind('<Enter>', lambda event, n=check_card, c=hand_card: Bind.enter(event, n, c, card_images))
                hand_card.bind('<Leave>', lambda event, n=check_card, c=hand_card: Bind.leave(event, n, c, card_images))
                new_card_name[check_card] = hand_card  # Store the card in the dictionary
            else:
                text = f"Hands full! \n{str(check_card)[0].upper() + str(check_card)[1:].lower()} smoked!"
                day_ended_full(text)

        def card_in_play():
            if "curator" in play_cards_list:
                section_left_b_img.configure(image=CardResizer.r_s_m(f"images/gui/section_left_m_on.png"))
                section_left_b_text.configure(text="CURATOR IN PLAY!")

            elif "curator" not in play_cards_list:
                section_left_b_img.configure(image=CardResizer.r_s_m(f"images/gui/section_left_m_off.png"))
                section_left_b_text.configure(text="SPECIAL!")      
            return card     

        def game_rules():
            global play_cards_list
            global cur_multiplier
            global days_left
            if days_left > 1:
                # Countdown each end day
                days_left -= 1 
                section_right_t_label.configure(text="DAYS LEFT: " + str(days_left))
            else:
                section_right_t_label.configure(text="GAME FINISHED!")
        






if __name__ == "__main__":
    CardGameApp()
