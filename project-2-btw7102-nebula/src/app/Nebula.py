import menu
import pygame as pg


class Flow():
    
    @staticmethod
    def start_new_game():
        pg.init()
        menu.Model.start_new()

    @staticmethod
    def get_back_to_menu(score=0):
        menu.Model.back_to_same_profile(score)


if __name__ == "__main__":
    Flow.start_new_game()