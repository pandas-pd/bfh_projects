import pygame as pg
import pygame
import sys
from pygame.locals import *
import os
import time
import play
import json

path = os.path.dirname(os.path.abspath(__file__))

class Controller():

    ui_quit         = False
    selected_button = 0         #is used within the Controller.Loop to determine which loop to go to next
    ui_enter        = False
    main_menu       = True      #determine if user is in main_menu to coordinate the esc-key press

    typing          = False
    key_press       = None
    backspace       = False

    music           = True

    class Loop():

        @staticmethod
        def opening(profile_del = False):
            View.update_opening()
            show_time = pg.time.get_ticks()
            display_time = 3000 #miliseconds

            while True:
                for event in pg.event.get():
                    if event.type == QUIT:
                        exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            exit()
                if pg.time.get_ticks() > show_time+display_time:
                    break
                View.update_screen()
                
            Model.unpause_music()
            Controller.Loop.select_profile()

        @staticmethod
        def select_profile():
            Controller.selected_button = 0

            Buttons = ["Create New Profile"]
            profiles = Model.Profiles.get() #returns all existing profiles

            if len(profiles) > 0:
                list(map(lambda profile: Buttons.append(profile), profiles))

            if Controller.main_menu == False:
                Buttons.append("Back") #if user is in main_manu, ther will be a "Back butto". If the game just booted, ther will not be one

            View.update_wallpaper()
            Model.init_buttons(Buttons)
            Model.init_select()

            if Controller.main_menu == False: #button will not be displayed when first entering this submenu, after the opening
                Model.add_title("Select Profile")

            while Controller.ui_quit == False:
                Controller.navigate()
                Model.correct_button_select(len(Buttons)-1)
                Model.update_select()

                if Controller.ui_enter == True:
                    Controller.ui_enter = False

                    #if's go here:
                    if Controller.selected_button == 0 and len(Model.Profiles.get()) < 3:
                        Controller.Loop.create_name()

                    if Controller.main_menu == False: #changes profile to selected one
                        if len(Buttons)-1 > Controller.selected_button > 0:

                            Model.Profiles.change(profiles[int(Controller.selected_button - 1)])

                        if Controller.selected_button == len(Buttons)-1 and Controller.main_menu == False:
                            Controller.Loop.menu()
                    
                    if Controller.selected_button > 0:
                        Model.Profiles.change(profiles[int(Controller.selected_button - 1)])

                View.update_screen()

        @staticmethod
        def delet_profile():
            
            profile_file = open(os.path.join(path, "profiles","selected_profile.json"), "r") #reads currently selected profile
            dict_prof = json.load(profile_file) #displays currently selected profile
            name = dict_prof["Name"]
            profile_file.close()

            Buttons = [f"Delete {name}s save","Are you sure" ,"","Yes", "No"]

            Controller.selected_button = 4

            View.update_wallpaper()

            Model.add_title("Settings")
            Model.init_buttons(Buttons)
            Model.init_select()

            Model.add_title(str(f"Highscore    {Model.Profiles.score()}"), X_Pos = 40, Y_Pos=443, Size = 40, orientation="tl")

            while Controller.ui_quit == False:
                Controller.navigate()
                Model.correct_button_select(max_num = len(Buttons)-1, min_num= 3)
                Model.update_select()

                #ifs go here
                if Controller.ui_enter == True:
                    Controller.ui_enter = False

                    if Controller.selected_button == 3:
                        os.remove(os.path.join(path, "profiles",f"{name}.json"))
                        Controller.main_menu = True
                        Controller.Loop.select_profile()

                    if Controller.selected_button == 4:
                        Controller.Loop.settings()

                View.update_screen()

        class Name(): #used to make backspace work correctly within the create_name()
            ui = []

        @staticmethod
        def create_name():
            
            Text = ["Enter a name", "cant be changed later"]

            View.update_wallpaper()
            Model.init_buttons(Text)

            char = 0
            Model.draw_name( str("".join(Controller.Loop.Name.ui)) )

            while Controller.ui_quit == False:
                
                Controller.writting()

                if Controller.typing == True or Controller.ui_enter == True:
                    
                    #saves json and name
                    if Controller.ui_enter == True:
                        Controller.ui_enter = False

                        if char > 0:
                            Model.Profiles.create( str("".join(Controller.Loop.Name.ui)))
                            Controller.Loop.Name.ui = []
                            Controller.Loop.select_profile()

                    #adds typed charaters
                    if Controller.typing == True and Controller.backspace == False and char < 7:
                        Controller.typing = False
                        
                        Controller.Loop.Name.ui.append(Controller.key_press)
                        Controller.key_press = None

                        char += 1

                        Model.draw_name( str("".join(Controller.Loop.Name.ui)) )

                    #goes back to setting loop
                    if Controller.backspace == True:
                        Controller.backspace, Controller.typing = False, False

                        try:
                            Controller.Loop.Name.ui.pop(-1)
                            char -= 1
                            View.update_screen()
                            Controller.Loop.create_name()

                        except:
                            pass

                View.update_screen()

        @staticmethod
        def menu():
            
            Controller.selected_button = 0

            Buttons = ["Start", "Settings", "Select Profile", "Quit"]

            Controller.main_menu = True
            View.update_wallpaper()
            Model.init_buttons(Buttons)
            Model.init_select()

            profile_file = open(os.path.join(path, "profiles","selected_profile.json"), "r") #reads currently selected profile
            dict_prof = json.load(profile_file) #displays currently selected profile
            Model.add_title(dict_prof["Name"])
            profile_file.close()

            #Controller.h_score = Model.Profiles.score(Model.score)
            Model.add_title(str(f"Highscore    {Model.Profiles.score()}"), X_Pos = 40, Y_Pos=443, Size = 40, orientation="tl")

            while Controller.ui_quit == False:
                Controller.navigate()
                Model.correct_button_select(len(Buttons)-1)
                Model.update_select()

                if Controller.ui_enter == True:
        
                    Controller.ui_enter = False

                    #starts game
                    if Controller.selected_button == 0:
                        Controller.main_menu = False
                        #Model.end_music()
                        play.Game.intro_loop()
                        
                    #opens settings
                    if Controller.selected_button == 1:
                        Controller.main_menu = False
                        Controller.Loop.settings()

                    #opens select Profile
                    if Controller.selected_button == 2:
                        Controller.main_menu = False
                        Controller.Loop.select_profile()

                    if Controller.selected_button == 3:
                        pg.quit()
                        quit()    

                View.update_screen()

            pg.quit()
            quit()

        @staticmethod
        def settings():

            Buttons = ["Delete profile", "Music   ON", "Back"]
            
            if Controller.music == True:
                Buttons[1] = "Music   ON"
            else:
                Buttons[1] = "Music   OFF"

            Controller.selected_button = 0

            View.update_wallpaper()

            Model.add_title("Settings")
            Model.init_buttons(Buttons)
            Model.init_select()

            Model.add_title(str(f"Highscore    {Model.Profiles.score()}"), X_Pos = 40, Y_Pos=443, Size = 40, orientation="tl")

            while Controller.ui_quit == False:
                Controller.navigate()
                Model.correct_button_select(len(Buttons)-1)
                Model.update_select()

                if Controller.ui_enter == True:
                    Controller.ui_enter = False

                    if Controller.selected_button == 0:
                        Controller.Loop.delet_profile()

                    if Controller.selected_button == 1:
                        
                        #pause and unpause music
                        if Controller.music == True:
                            Controller.music = False
                            Model.pause_music()
                            Buttons[1] = "Music   OFF"

                        elif Controller.music == False:
                            Controller.music = True
                            Model.unpause_music()
                            Buttons[1] = "Music   ON"
                        
                        #relode page to refresh the music button
                        View.update_wallpaper()
                        Model.add_title("Settings")
                        Model.init_buttons(Buttons)
                        Model.init_select()
                        Model.add_title(str(f"Highscore    {Model.Profiles.score()}"), X_Pos = 40, Y_Pos=443, Size = 40, orientation="tl")
                        Model.init_buttons(Buttons)


                    if Controller.selected_button == 2:
                        Controller.Loop.menu()


                View.update_screen()

    @staticmethod
    def navigate():
        """Arrow up, Arrow down, W, S, enter, esc"""
        for event in pg.event.get():
            if event.type == KEYDOWN:

                if event.key == K_w or event.key == K_UP:
                    Controller.selected_button -= 1 #changes value according to key press

                if event.key == K_s or event.key == K_DOWN:
                    Controller.selected_button += 1 #changes value according to key press

                if event.key == K_RETURN:
                    Controller.ui_enter = True

                if event.key == K_ESCAPE:
                    if Controller.main_menu == True:
                        Controller.ui_quit = True
                    else:
                        Controller.Loop.menu()

    @staticmethod
    def writting():

        #only used during create_name()
        possible_keys = [
            K_q, K_w, K_e, K_r, K_t, K_z, K_u, K_i, K_o, K_p,
            K_a, K_s, K_d, K_f, K_g, K_h, K_j, K_k, K_l,
            K_y, K_x, K_c, K_v, K_b, K_n, K_m
        ]
        for event in pg.event.get():
            if event.type == KEYDOWN:

                if event.key == K_RETURN:
                    Controller.ui_enter = True
                    break
                
                if event.key == K_ESCAPE:
                    Controller.Loop.Name.ui = []
                    Controller.Loop.select_profile()
                
                if event.key == K_BACKSPACE:
                    Controller.backspace = True
                    Controller.typing = True

                if event.key == K_SPACE:
                    Controller.typing = True
                    ui_key = " "
                    Controller.key_press = ui_key

                if event.key in possible_keys:
                    #add keys witch return their value
                    Controller.typing = True
                    ui_key = pg.key.name(event.key)
                    Controller.key_press = ui_key
                    
                else:
                    continue

class Model():

    class Profiles():

        count = 0 #number of profiles, max is 3

        def create(name):
            """ creates new profile with base stats"""

            Model.Profiles.get()
            if Model.Profiles.count == 3:
                Controller.Loop.select_profile()

            Model.Profiles.count += 1
            profile_name = str(name)

            empty_profile = { #base stats of every profile
                "Name": profile_name,
                "High-Score": 0,
            }

            profile = open(os.path.join(path,"profiles",f"{name}.json"), "w") #saves the newly created profile
            json.dump(empty_profile, profile)
            profile.close()

            Model.Profiles.count -= 1 #keeps track of the number of created profiles. The max is 5
            #Controller.Loop.select_profile()

        def get():
            """returns list of profiles"""

            try: #returns the selected profile if the folder and file exists
                profiles_file = os.listdir(os.path.join(path,"profiles"))
                profiles_file.remove("selected_profile.json")
                
                profile_list = []

                for profile in profiles_file:
                    profile_list.append(profile[:-5])

                Model.Profiles.count = len(profile_list)

                return profile_list
            
            except: #creates the folder and file in case they are missing or not yet created
                os.mkdir(os.path.join(path, "profiles"))
                selected = open(os.path.join(path, "profiles","selected_profile.json"), "w")
                selected.close()
                return []

        def change(name):
            
            profile_file = open(os.path.join(path,"profiles",f"{name}.json"), "r")
            profile = json.load(profile_file)
            select = open(os.path.join(path, "profiles","selected_profile.json"), "w")
            json.dump(profile, select) #overwrites the selected_profile.json with the newly selected one
            select.close()
            profile_file.close()

            Controller.Loop.menu()
        
        @staticmethod
        def score(score  = 0):
            
            #updating profile file
            selected_file = open(os.path.join(path, "profiles","selected_profile.json"), "r")
            selected = json.load(selected_file)
            selected_file.close()

            name = selected['Name']

            profile_file = open(os.path.join(path, "profiles",f"{name}.json"), "r")
            profile = json.load(profile_file)
            profile_file.close()

            if score < profile["High-Score"]:
                score = profile["High-Score"]

            update = {
                "Name": selected["Name"],
                "High-Score": score}

            profile_file = open(os.path.join(path, "profiles",f"{name}.json"), "w")
            json.dump(update, profile_file)
            profile_file.close()

            #updating selected profile
            selected_file = open(os.path.join(path, "profiles","selected_profile.json"), "w")
            json.dump(update, selected_file)
            selected_file.close()

            return score


    @staticmethod
    def start_new():
        """inits pygame, sets wallpaper, sets screen resolution"""

        pg.init()
        pg.font.init()
        pg.display.set_caption('Nebula')
        Model.load_music()
        Model.pause_music()
        screen_x, screen_y = 1280, 720 #standart resolution, 16:9

        Model.MainClock = pg.time.Clock()
        
        Model.screen = pg.display.set_mode((screen_x,screen_y), pg.FULLSCREEN)
        
        Model.Wallpaper, Model.Logo, Model.Font = Model.get_images() #gets all needed images and the font for the main menu 
        #self.Font = pg.font.SysFont(View.Font, View.Font_size)
        Model.Font = pg.font.Font(os.path.join(path,"content","fonts","ARCADECLASSIC.ttf"),View.Font_size)
        Model.wallpaper_scaled = Model.image_scaling(Model.Wallpaper, (screen_x, screen_y))
        Model.logo_scaled = Model.image_scaling(Model.Logo, (screen_x, screen_y))
        #Model.score = 0
        #self.logo_scaled = Model.image_scaling(self.Logo, (self.screen_x, self.screen_y))
        Controller.Loop.opening()

    @staticmethod
    def back_to_same_profile(score):

        #Entry point from game loop, saves new high score
        Model.end_music()
        Model.load_music()
        Model.Profiles.score(int(score))
        Controller.Loop.menu()

    @staticmethod    
    def init_buttons(buttons,x_offset = 0):
        """initiates and draws the needed buttons on the screen"""

        start_pos_x = 50 + x_offset
        start_pos_y = 50

        for button in buttons:
            View.draw_buttons(button, Model.Font, View.Text_color, Model.screen, start_pos_x, start_pos_y)
            start_pos_y += 65

    @staticmethod
    def draw_name(name):
        View.draw_name(name, Model.Font, View.Text_color, Model.screen)

    @staticmethod
    def init_select():
        """initiates the the button, which inidcates the selection"""

        Distance = 65
        X_pos = 30
        Y_pos = 64
        y_offset = Distance*Controller.selected_button
        size = 8

        Model.select_rect = pg.Rect(X_pos, (Y_pos+y_offset), size,size)
        Model.select_rect_2 = pg.Rect(X_pos+3, (Y_pos+y_offset)+3, size,size)

        View.draw_select(Model.screen, (0,100,100), Model.select_rect_2)
        View.draw_select(Model.screen, (0,255,255), Model.select_rect)

    @staticmethod
    def update_select():
        """changes the postion of the select_button"""
        black_rect = pg.Rect(30,57,13,330)
        View.draw_select(Model.screen, (0,0,0), black_rect) # change if Background changes
        Model.init_select()

    @staticmethod
    def image_scaling(picture, resolution):
        """returns scaled image to given resolution (as tuple)"""

        scaled_pic = pygame.transform.scale(picture, resolution)
        return scaled_pic

    @staticmethod
    def get_images():
        """reads all the needed images and the font from the folders"""

        Wallpaper = pg.image.load(os.path.join(path,"content","images","menu","menu3_wallpaper.png")).convert()
        Logo = pg.image.load(os.path.join(path,"content","images","menu","opening.png")).convert()
        Font = pg.font.SysFont("Impact", 55)

        return Wallpaper,Logo,Font

    @staticmethod
    def correct_button_select(max_num, min_num = 0):
        """restricts the user from gowing further up or down (in the menus) than needed"""

        if Controller.selected_button > max_num:
            Controller.selected_button = max_num
        
        if Controller.selected_button < min_num:
            Controller.selected_button = min_num

    @staticmethod
    def add_title(title, X_Pos = 1250, Y_Pos = 15, Size = 100, orientation = "tr"):
        """Draws text on the bottom left corner to indicate where the user is"""

        View.draw_buttons(title, pg.font.Font(os.path.join(path,"content","fonts","ARCADECLASSIC.ttf"),Size), View.Text_color, Model.screen, X_Pos, Y_Pos, orientation = orientation)

    @staticmethod
    def load_music():
        pygame.mixer.quit()
        pygame.mixer.init(frequency=48000)#plays too slow
        pg.mixer.music.load(os.path.join(path,"content","sound","menu_music_Daniel Deluxe-Star Eater.mp3"))
        pygame.mixer.music.play(loops=-1)

    @staticmethod
    def end_music():
        pygame.mixer.music.fadeout(2000)

    @staticmethod
    def pause_music():
        pygame.mixer.music.pause()

    @staticmethod
    def unpause_music():
        pygame.mixer.music.unpause()

class View():

    Font = "Potra"
    Font_size = 40
    Text_color = (200,0,100)
    
    @staticmethod
    def draw_buttons(text, font, color , surface , x, y, orientation = "tl"):
        """draws the button or text on the screen at the given coordintes"""

        obj = font.render(text, 1, color)
        rect = obj.get_rect()

        if orientation == "tl":
            rect.topleft = (x,y)
        if orientation == "tr":
            rect.topright = (x,y)
        surface.blit(obj, rect)

    @staticmethod
    def draw_name(text, font, color, surface):

        obj = font.render(text, 1, color)
        rect = obj.get_rect()
        rect.topleft = ((80), (200))
        surface.blit(obj, rect)

    @staticmethod
    def draw_select(screen, color, button_select):
        pg.draw.rect(screen, color, button_select)

    @staticmethod
    def update_wallpaper():
        Model.screen.blit(Model.wallpaper_scaled,(0,0))

    def update_opening():
        """blits the logo on the screen"""
        Model.screen.blit(Model.logo_scaled,(0,0,))

    @staticmethod
    def update_screen():
        pg.display.update()
        Model.MainClock.tick(60)

if __name__ == "__main__":
    Model.start_new()
    Controller.Loop.select_profile()