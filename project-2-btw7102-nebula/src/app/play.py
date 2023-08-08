import pygame as pg
from pygame.locals import *
import numpy as np
import os 
import time
import random
import menu
import mutagen
import Nebula
import pickle
import neat


"""
Start this from Nebula.py

"""
 
######### SETUP #########

class Setup():

    """
    This class contains all important values for the game setup. Can not be instanced.
    """

    FPS                 =   60 #frames per seconds
    screen_x            =   1280 #windowsize width in px
    screen_y            =   720 #windowsize height in px
    map_size            =   (6000, 6000) #(width,height) in px
    screen              =   pg.display.set_mode((screen_x,screen_y),0,32) #setup the screen
    clock               =   pg.time.Clock() #set a main clock

class Paths():
    """
    Save paths to folders and documents here. Please use absolute path "path" as reference.
    """

    path            =   os.path.dirname(os.path.abspath(__file__))
    
    path_ai         =   os.path.join(path,"ai")
    path_config     =   os.path.join(path_ai,"config_ai.txt")
    path_pickled    =   os.path.join(path_ai,"genomes")

    list_of_genomes = [
        "aulus_plautius.pickle",
        "gaius_marius.pickle",
        "pompeius_magnus.pickle",
        "scipio_aemilianus.pickle"
    ]

    path_genome     =   os.path.join(path_pickled,list_of_genomes[3])

    path_images     =   os.path.join(path,"content","images")
    path_spaceships =   os.path.join(path_images,"space_ships")
    path_upgrades   =   os.path.join(path_images,"upgrades")
    path_bars       =   os.path.join(path_images,"bars")
    path_settings   =   os.path.join(path_images,"settings")
    path_asteroids  =   os.path.join(path_images,"asteroids")
    path_background =   os.path.join(path_images,"background")
    path_fonts      =   os.path.join(path,"content","fonts")
    path_songs      =   os.path.join(path,"content","sound")
    path_songs_it1  =   os.path.join(path_songs,"intensity01")
    path_songs_it2  =   os.path.join(path_songs,"intensity02")
    path_songs_it3  =   os.path.join(path_songs,"intensity03")

class Sprites():
    """
    Set Images of sprites and their respective groups as variables for easy use.
    Please use paths from the Paths class for continuity.
    """
    # Sprite Groups
    all_sprites_list    =   pg.sprite.Group()
    entity_list         =   pg.sprite.Group()
    shot_list           =   pg.sprite.Group()
    enemy_shot_list     =   pg.sprite.Group()
    enemy_list          =   pg.sprite.Group()
    ammo_list           =   pg.sprite.Group()
    player_list         =   pg.sprite.Group()
    no_ressource_list   =   pg.sprite.Group()
    upgrade_list        =   pg.sprite.Group()
    stars_list          =   pg.sprite.Group()
    render_list         =   pg.sprite.Group()
    rockets_list        =   pg.sprite.Group()
    rocket_aim          =   pg.sprite.Group()
    flame_thrower_list  =   pg.sprite.Group()
    asteroid_belt       =   pg.sprite.Group()
    ai_list             =   pg.sprite.Group()
    overlay_0_list      =   pg.sprite.Group()
    overlay_1_list      =   pg.sprite.Group()
    shock_wave_list     =   pg.sprite.Group()
    ai_look_list        =   pg.sprite.Group()
    ai_shot_list        =   pg.sprite.Group()



    # Sprite Images
    player_sprite_s     =   pg.image.load(os.path.join(Paths.path_spaceships,"space_ship_1_static.png")).convert_alpha()
    player_sprite_k     =   pg.image.load(os.path.join(Paths.path_spaceships,"space_ship_1_kinetic.png")).convert_alpha()

    player_plane_s      =   pg.image.load(os.path.join(Paths.path_spaceships,"player_sprite2_static.png")).convert_alpha()
    player_plane_k      =   pg.image.load(os.path.join(Paths.path_spaceships,"player_sprite2_kinetic.png")).convert_alpha()


    empty_sprite        =   pg.image.load(os.path.join(Paths.path_spaceships,"empty_sprite.png")).convert_alpha()
    enemy_sprite        =   pg.image.load(os.path.join(Paths.path_spaceships,"enemy_sprite.png")).convert_alpha()
    shot                =   pg.image.load(os.path.join(Paths.path_spaceships,"shot.png")).convert_alpha()
    enemy_shot          =   pg.image.load(os.path.join(Paths.path_spaceships,"enemy_shot.png")).convert_alpha()
    ai_sprite           =   pg.image.load(os.path.join(Paths.path_spaceships,"enemy_sprite_2.png")).convert_alpha()
    ai_sprite_moving    =   pg.image.load(os.path.join(Paths.path_spaceships,"enemy_sprite_2.png")).convert_alpha() #get some

    # Weapon Systems

    shot                =   pg.image.load(os.path.join(Paths.path_spaceships,"shot.png")).convert_alpha()


    # Unarmed Entities
    asteroid_1          =   pg.image.load(os.path.join(Paths.path_asteroids,"asteroid.png")).convert_alpha()
    asteroid_2          =   pg.image.load(os.path.join(Paths.path_asteroids,"asteroid_2.png")).convert_alpha()
    asteroid_3          =   pg.image.load(os.path.join(Paths.path_asteroids,"asteroid_3.png")).convert_alpha()
    asteroid_4          =   pg.image.load(os.path.join(Paths.path_asteroids,"asteroid_4.png")).convert_alpha()
    all_asteroids       =   [asteroid_1,asteroid_2,asteroid_3,asteroid_4]
    mine                =   pg.image.load(os.path.join(Paths.path_upgrades,"mine_2.png")).convert_alpha()

    # Upgrade Images
    life                =   pg.image.load(os.path.join(Paths.path_upgrades,"life.png")).convert_alpha()
    speed               =   pg.image.load(os.path.join(Paths.path_upgrades,"speed.png")).convert_alpha()
    mining_speed        =   pg.image.load(os.path.join(Paths.path_upgrades,"mining_speed.png")).convert_alpha()
    regenerate_speed    =   pg.image.load(os.path.join(Paths.path_upgrades,"repair.png")).convert_alpha()
    ammo_store          =   pg.image.load(os.path.join(Paths.path_upgrades,"ammo_store.png")).convert_alpha()
    shooting_speed      =   pg.image.load(os.path.join(Paths.path_upgrades,"bullet_speed.png")).convert_alpha()
    all_upgrades        =   [life,regenerate_speed,speed,ammo_store,shooting_speed,mining_speed]

    @staticmethod
    def rotate(sprite,angle):
        """
        Function to rotate a sprite. Takes sprite image and angle to rotate
        in degrees. Returns rotated image.
        """
        rotated = pg.transform.rotate(sprite,angle)
        return rotated

    @staticmethod
    def set_plane_sprite():
        Sprites.player_sprite_s     =   pg.transform.scale(Sprites.player_plane_s,(48,48))
        Sprites.player_sprite_k     =   pg.transform.scale(Sprites.player_plane_k,(48,48))
    
    @staticmethod
    def set_tank_sprite():
        Sprites.player_sprite_s     =   pg.image.load(os.path.join(Paths.path_spaceships,"space_ship_1_static.png")).convert_alpha()
        Sprites.player_sprite_k     =   pg.image.load(os.path.join(Paths.path_spaceships,"space_ship_1_kinetic.png")).convert_alpha()
    
class World():

    """
    Sets up the background and it's respective parallax layer.
    The game_surface is the main surface, where every sprite and entity is blited on.
    """

    game_surface    =   pg.Surface(Setup.map_size)

    wallpaper       =   random.choice(["wallpaper_1.png","wallpaper_2_layer2.png"])
    background      =   pg.image.load(os.path.join(Paths.path_background,wallpaper))
    background      =   pg.transform.scale(background,Setup.map_size)


    parallax        =   pg.image.load(os.path.join(Paths.path_background,wallpaper)).convert()
    parallax        =   pg.transform.scale(parallax,(int(Setup.map_size[0]/2),int(Setup.map_size[1]/2)))
    
    black_out       =   pg.Surface(Setup.map_size)
    black_out.fill((0,0,0))

    @staticmethod
    def  render_map():
        """
        This function is called from the game loop. Renders all existing background elements
        according to the players position to the screen.
        """
        Setup.screen.blit(World.game_surface,(Player.camera[0],Player.camera[1]))
        World.game_surface.blit(World.parallax,(int(0-Player.camera[0]/4*3),int(0-Player.camera[1]/4*3)))
        
        Sprites.overlay_1_list.update()
        Sprites.overlay_1_list.draw(World.game_surface)
        Sprites.overlay_0_list.draw(World.game_surface)
    
    class Overlay(pg.sprite.Sprite):
        """
        Using the pygame sprite parentclass to create elements for 
        the parallax layers.
        """

        elements        = []
        elements_amount = 500
        random_color    = (random.randint(150,255))

        @staticmethod
        def elements_creator():
            """
            Funtcion to instace all paralax elements.
            """
            for element in range(World.Overlay.elements_amount):
                World.Overlay()

        def __init__(self):
            """
            Adds parallax entities randomly to different parallax layers.
            """
            super(World.Overlay, self).__init__()
            self.random_size    = random.randint(1,8)
            self.surf           = pg.Surface((self.random_size,self.random_size))
            self.color_offset   = random.randint(-20,0)
            self.surf.fill(
                (World.Overlay.random_color + self.color_offset,
                World.Overlay.random_color + self.color_offset,
                World.Overlay.random_color + self.color_offset)
                )

            self.image  = self.surf
            self.rect   = self.surf.get_rect(center = (random.randint(0,Setup.map_size[0]), random.randint(0,Setup.map_size[1])))


            self.layer = random.choice([0,1])
            if self.layer == 0:
                Sprites.overlay_0_list.add(self)
            
            elif self.layer == 1:
                Sprites.overlay_1_list.add(self)

        def update(self):
            pass

######### DIFFICULTY SETTING #########

class Level():
    """ 
    Change level settings in the level_reset() function.
    Change difficulty setting change in the level_update() function.
    """
    #General
    level                   = 1     #self explaining
    level_up_speed          = 120   #seconds until next level-up

    #Music 
    intensity_1             = 5    #chooses until this level from this playlist
    intensity_2             = 10    #chooses until this level from this playlist
    intensity_3             = 15    #chooses until this level from this playlist
    @staticmethod
    def level_check(time):
        """
        Checks if it is time to make the game harder through raising the Level. Returns boolean.
        """
        if int(((time-Timer.game_start)/1000)) > Level.level * Level.level_up_speed:
            Level.level += 1
            return True
        return False
    
    @staticmethod 
    def level_update():
        """
        Change difficulty change here. The difficulty change is per level_up_speed.
        """
        Level.level                   += 1
        Level.enemies                 += 0.25  
        Level.enemy_damage            += 0.25  
        Level.enemy_shooting_speed    += 10   
        Level.enemy_field_of_view     += 10
        Level.enemy_max_moving_speed  += 10
        Level.enemy_following_skalar  += 1   
        Level.entities                += 20    
        Level.entity_damage           += 2    
        Level.entity_moving_max       += 5   

    @staticmethod 
    def level_reset():
        """
        Change starting difficulty here:
        """
        Level.level                   = 1     #self explaining
        Level.enemies                 = 10    #amount of enemies on map
        Level.enemy_damage            = 0.5   #damage done by 1 enemy shot
        Level.enemy_shooting_speed    = 600  #shot speed in pixels per seconds
        Level.enemy_field_of_view     = 250   #in pixels
        Level.enemy_max_moving_speed  = 60   
        Level.enemy_following_skalar  = 10
        Level.entities                = 300    #amount of entities on map
        Level.entity_damage           = 20    #damage don by 1 entity hit
        Level.entity_moving_max       = 100  #max possible moving speed in pixel per seconds
        Level.off_map_damage          = 1     #damage done to player when cruising off map
        Level.total_ai                = 1     #amount of ai opponents on the map
        Level.collecting_time         = 8000  #time to collect upgrade in seconds

class Upgrades(pg.sprite.Sprite):
    """
    Visual representation of Upgrades to collect. Class contains also Upgrade starting and 
    current parameters.
    """
    @staticmethod
    def set_upgrades():
        # Starting parameters
        if Controller.setting_mode is False:
            Upgrades.moving_speed        = 500   #in pixel per seconds
            Upgrades.shooting_speed      = Upgrades.moving_speed *1.6   #shot speed in pixels per seconds
            Upgrades.acceleration        = 20
        else:
            Upgrades.moving_speed        = 400   #in pixel per seconds
            Upgrades.shooting_speed      = Upgrades.moving_speed*1.6  #shot speed in pixels per seconds
            Upgrades.acceleration        = 10

        Upgrades.shot_damage         = 2     #damage per shot on enemies
        Upgrades.rof                 = 600   #time to shoot continuously in miliseconds
        Upgrades.ammo_store          = 250   #possible ammunition inventory
        Upgrades.health_store        = 100   #possible health store
        Upgrades.gun_cool_down       = 3000  #time to cool down the gun in miliseconds
        Upgrades.mining_speed        = 1     #ammunition mining speed
        Upgrades.regeneration_speed  = 0.5   #regenerating health points per second
        Upgrades.dash_capacity       = 100   #
        Upgrades.dash_reg_speed      = 10
        Upgrades.rocket_damage       = 100
        Upgrades.flame_damage        = 25
        Upgrades.secondary_store     = 0
       
        # Levels (this is for the visual representation in the gui)
        Upgrades.level_healthstore          = 0
        Upgrades.level_regeneration_speed   = 0
        Upgrades.level_moving_speed         = 0
        Upgrades.level_ammo_store           = 0
        Upgrades.level_shooting_speed       = 0
        Upgrades.level_mining_speed         = 0

        # Maxima
        Upgrades.total_upgrades             = 0
        Upgrades.maximum                    = 30

    def __init__(self,position):
        super(Upgrades, self).__init__()

        self.spawn_time     = pg.time.get_ticks()
        self.surf           = random.choice(Sprites.all_upgrades)
        self.image          = self.surf
        self.spawn_x        = position[0]
        self.spawn_y        = position[1]
        self.rect           = self.surf.get_rect(
            center=(
                self.spawn_x,
                self.spawn_y,
            )
        )

        Sprites.upgrade_list.add(self)
        Sprites.all_sprites_list.add(self)

    def update(self,time):
        if self.spawn_time + Level.collecting_time < pg.time.get_ticks():
            self.kill()

######### SPRITES #########

class Player(pg.sprite.Sprite):

    """
    This class contains all data of the player.
    It instaces a transparent hitbox for collision checks.
    All data is kept in a numpy array as following:
    
    sprite_image    =   data_player[0]
    position_x      =   data_player[1]
    position_y      =   data_player[2]
    speed           =   data_player[3]
    angle           =   data_player[4]
    health          =   data_player[5]
    score           =   data_player[6]
    ammo_count      =   data_player[7]
    dash_level      =   data_player[8]
    secondary_count =   data_player[9]
    """
    camera          =   np.array([0,0])
    mover           =   np.array([0,0]) # acceleration for player
    all_sprites     =   [Sprites.player_sprite_s,] # to be completed by upgrade ships
    data_player     =   np.array([
        0,
        (int(Setup.screen_x/2))-(Sprites.player_sprite_s.get_width()/2),
        (int(Setup.screen_y/2))-(Sprites.player_sprite_s.get_height()/2),
        400,
        0,
        100,
        0,
        100,
        100,
        0])

    diagonal_factor =   0.7071

    def __init__(self):
        """
        Pygame sprite child to track players movement on map and collisions 
        with other entities.
        """

        super(Player, self).__init__()
        self.hitbox_size= (32,32)
        self.moving     = False
        self.surf       = pg.Surface(self.hitbox_size, pg.SRCALPHA)
        self.image      = self.surf.convert_alpha()
        self.height     = self.hitbox_size[0]
        self.width      = self.hitbox_size[1]
        self.rect = self.surf.get_rect(
            center=(
                Player.camera[0]*-1  + Player.data_player[1],
                Player.camera[1]*-1   + Player.data_player[2],
            )
        )

        Sprites.all_sprites_list.add(self)
        Sprites.player_list.add(self)

    def update(self,time):
        """
        Updates players position according to camera. Returns None
        """
        self.rect.x = Player.camera[0]*-1+ Player.data_player[1]
        self.rect.y = Player.camera[1]*-1 + Player.data_player[2]

    @staticmethod
    def regenerate(time):
        """
        Function to regenerate the players health. Returns None
        """
        if Player.data_player[5] < Upgrades.health_store:
            Player.data_player[5] += (Upgrades.regeneration_speed)*time

        if Player.data_player[8] < Upgrades.dash_capacity:
            Player.data_player[8] += (Upgrades.dash_reg_speed)*time

    @staticmethod
    def health_check():
        """
        Function to check if player is still alive. Returns boolean.
        """
        if Player.data_player[5] <= 0 :
            return False
        
        return True

    @staticmethod
    def render_sprite(background,sprite,x,y):
        """
        Function to blit player sprite to surface. This is used to produce
        a very stable image in the middle of the screen. Returns None
        """
        background.blit(sprite,(x,y))

class Mining_Reach(pg.sprite.Sprite):
    """
    Child class of pygame sprite class: Is used to check collisions of 
    ressources with player. Much more efficient than working with vector geometry
    Moves with players position. Is transparent surface.
    """

    def __init__(self):
        super(Mining_Reach, self).__init__()
        self.size       = (300,300)

        self.mining_reach        = pg.Surface(self.size,pg.SRCALPHA).convert_alpha()

        self.moving     = False
        self.surf       = self.mining_reach
        self.image      = self.mining_reach
        self.height     = self.image.get_height()
        self.width      = self.image.get_width()
        self.rect = self.surf.get_rect(
            center=(
                Player.camera[0]*-1  + Player.data_player[1],
                Player.camera[1]*-1   + Player.data_player[2],
            )
        )

        Sprites.all_sprites_list.add(self)


    def update(self,time):
        self.rect.x = Player.camera[0]*-1+ Player.data_player[1] - self.size[0]/4 -15
        self.rect.y = Player.camera[1]*-1 + Player.data_player[2]- self.size[1]/4 -15

class Rendering_Window(pg.sprite.Sprite):
    """
    Pygame sprite childclass: Is transparent surface in screen size. Is used to check
    collisions with all entities. Game runs smoother when only entities in view
    (colided with rendering_window) are blited.
    """

    def __init__(self):
        super(Rendering_Window, self).__init__()
        self.size       = (Setup.screen_x+100,Setup.screen_y+100)

        self.mining_reach        = pg.Surface(self.size,pg.SRCALPHA).convert_alpha()

        self.moving     = False
        self.surf       = self.mining_reach
        self.image      = self.mining_reach
        self.height     = self.image.get_height()
        self.width      = self.image.get_width()
        self.rect = self.surf.get_rect(
            center=(
                Player.camera[0]*-1  + Player.data_player[1],
                Player.camera[1]*-1   + Player.data_player[2],
            )
        )

        Sprites.all_sprites_list.add(self)


    def update(self,time):
        self.rect.x = Player.camera[0]*-1+ Player.data_player[1] - self.size[0]/2 -15
        self.rect.y = Player.camera[1]*-1 + Player.data_player[2]- self.size[1]/2 -15

class Entity(pg.sprite.Sprite):
    """
    Pygame sprite childclass: Creates random asteroids, places them randomly out off map,
    directs asteroids speed, kills asteroids falling off map.
    """

    def __init__(self):
        super(Entity, self).__init__()
        random_number= random.randint(0,3) #set type of asteroid

        randomchoice = pg.transform.rotate(
            Sprites.all_asteroids[random_number],
            random.randint(0,360)
            )

        self.spawn_x = random.randint(0,Setup.map_size[0])
        if self.spawn_x-Setup.map_size[0]/2 == 0:
            self.spawn_x += 1
        factor       = random.choice([-1,1])
        self.spawn_y  = (
            Setup.map_size[0]+factor*np.sqrt(
                Setup.map_size[0]**2-4*(Setup.map_size[0]-(Setup.map_size[0]**2)/(self.spawn_x-Setup.map_size[0]/2)**2))
        )/2


        self.surf    = randomchoice
        self.image   = randomchoice

        self.x_speed = random.randint(
            -int(Level.entity_moving_max),
            int(Level.entity_moving_max)
            )

        if factor > 0: 
            self.y_speed = random.randint(-int(Level.entity_moving_max), -1)
        else: 
            self.y_speed = random.randint(1,int(Level.entity_moving_max))


        self.rect = self.surf.get_rect(
            center=(
                self.spawn_x,
                self.spawn_y
            )
        )
        
        Sprites.all_sprites_list.add(self)

        # Add entity to respective group:
        if random_number == 3:
            Sprites.ammo_list.add(self)
            self.ammo_amount = 100
        else:
            Sprites.no_ressource_list.add(self)
        Sprites.entity_list.add(self)

    def update(self,time):
        self.rect.move_ip(self.x_speed*time, self.y_speed*time)

        if (self.rect.x - Setup.map_size[0]/2)**2 + (self.rect.y - Setup.map_size[1]/2)**2 > (Setup.map_size[0]/2)**2+(Setup.map_size[0]/2)**2+60 :
            self.kill()

class Asteroid_Belt():
    """
    This class handles the boarder of the map symbolized by a circling asteroid belt.
    Asteroids in the belt are instances of Asteroid class. 
    """
    border = 100
    radius = Setup.map_size[0]/2 - border
    amount = int(Setup.map_size[0]/10)

    @staticmethod
    def load_belt():
        """
        This instances an asteroid. It's called by the gameloop.
        Keeps the asteroid count in the belt constant.
        """
        if len(Sprites.asteroid_belt) < Asteroid_Belt.amount:
            Asteroid_Belt.Asteroid()

    class Asteroid(pg.sprite.Sprite):
        """
        Pygame sprite subclass: Circular movement around random radius in set range. 
        """

        def __init__(self):
            super(Asteroid_Belt.Asteroid, self).__init__()
            self.surf = pg.transform.rotate(Sprites.asteroid_1,random.randint(0,360))
            self.image = self.surf
            self.rect = self.surf.get_rect()
                

            # The "center" the sprite will orbit
            self.center_x = Setup.map_size[0]/2
            self.center_y = Setup.map_size[1]/2
    
            # Current angle in radians
            self.angle = 0 + random.uniform(-2*np.pi,2*np.pi)
    
            # How far away from the center to orbit, in pixels
            self.radius = Asteroid_Belt.radius+ random.randint(-400,0)
    
            # How fast to orbit, in radians per frame
            self.speed = 0.02


            Sprites.all_sprites_list.add(self)
            Sprites.asteroid_belt.add(self)

        def update(self,time):

            """ Update the ball's position. """
            # Calculate a new x, y
            self.rect.x = self.radius * np.sin(self.angle) + self.center_x
            self.rect.y = self.radius * np.cos(self.angle) + self.center_y
    
            # Increase the angle in prep for the next round.
            self.angle += self.speed*time

class Enemy_shooting(pg.sprite.Sprite):
    """
    Handles automated shooting by enemy drones through vector calculations.
    Is instanced by Enemy class. 
    """
    shot_count = 0
    def __init__(self,direction,position):
        super(Enemy_shooting, self).__init__()
        Enemy_shooting.shot_count += 1
        self.surf       = Sprites.enemy_shot
        self.image      = Sprites.enemy_shot
        self.absolute   = np.sqrt(((direction[0]-position[0])**2)+((direction[1]-position[1])**2))
        self.x_speed    = np.round((direction[0]-position[0])/self.absolute,decimals=2)
        self.y_speed    = np.round((direction[1]-position[1])/self.absolute, decimals=2)


        self.rect = self.surf.get_rect(
            center=(
                position[0],
                position[1]
            )
        )
        Sprites.enemy_shot_list.add(self)
        Sprites.all_sprites_list.add(self)

    def update(self,time):
        """
        Selfdistructs if off map. Moves according to speed (scalar) and vector.
        """
        self.rect.move_ip(self.x_speed*Level.enemy_shooting_speed*time, self.y_speed*Level.enemy_shooting_speed*time)
        
        if self.rect.x < -10:
            self.kill()
        elif self.rect.x > Setup.map_size[0]+10:
            self.kill()
        elif self.rect.y < -10:
            self.kill()
        elif self.rect.y > Setup.map_size[1]+10:
            self.kill()

class Enemy(pg.sprite.Sprite):
    """
    Pygame Sprite childclass: Random spawn off map, sets randomspeed, sets viewing field
    according to players level. Is hardcoded player enemy. Patrols map until contact with player.
    Starts patrolling again after loosing player out of sight. 
    """
    def __init__(self):
        super(Enemy, self).__init__()
        self.following_mode = False
        self.surf           = pg.Surface(Sprites.enemy_sprite.get_size())
        self.image          = Sprites.enemy_sprite
        self.spawn_x        = random.choice([random.randint(-10,-5),random.randint(Setup.map_size[0]+5,Setup.map_size[0]+10)])
        self.spawn_y        = random.choice([random.randint(-10,-5),random.randint(Setup.map_size[1]+5,Setup.map_size[1]+10)])
        self.view_field     = Level.enemy_field_of_view
        
        self.health         = 100
        self.ammo_count     = 100

        self.speed_x        = random.choice([
            random.randint(-int(Level.enemy_max_moving_speed),-1),
            random.randint(1,int(Level.enemy_max_moving_speed))
            ])

        self.speed_y        = random.choice([
            random.randint(-int(Level.enemy_max_moving_speed),-1),
            random.randint(1,int(Level.enemy_max_moving_speed))
            ])

        self.angle          = 0
        self.rect           = self.surf.get_rect(
            center=(
                self.spawn_x,
                self.spawn_y,
            )
        )

        Sprites.enemy_list.add(self)
        Sprites.all_sprites_list.add(self)

    def update(self,time):
        """
        Updates Enemy's position. Turns direction if it goes off map.
        In case off death: Removes itself off all lists, spawns upgrades at 
        death position, gives player weaponsystem points.
        """

        self.rect.x += self.speed_x*time
        self.rect.y += self.speed_y*time

        if self.rect.x < -200 :
            self.speed_x *= -1
        elif self.rect.x > Setup.map_size[0]+200:
            self.speed_x *= -1
        elif self.rect.y < -200 :
            self.speed_y *= -1
        elif self.rect.y > Setup.map_size[1]+200:
            self.speed_y *= -1
        if self.health <=0:
            self.kill_sequence()

    def look(self):
        """
        Method for scanning viewing field. Follows player, as soon as detected.
        If player is lost, Enemy continues on random direction.
        """
        for player in Sprites.player_list:
            if player.rect.x in range(self.rect.x-self.view_field,self.rect.x+self.view_field) and player.rect.y in range(self.rect.y-self.view_field,self.rect.y+self.view_field):
                
                Enemy_shooting(
                    (player.rect.x,player.rect.y),
                    (self.rect.x+self.rect.width/2,self.rect.y+self.rect.height/2))

                self.follow(
                    (player.rect.x,player.rect.y),
                    (self.rect.x+self.rect.width/2,self.rect.y+self.rect.height/2))

                self.following_mode = True
            
            else:
                if self.following_mode is True:
                    self.speed_x        = random.choice([
                        random.randint(-int(Level.enemy_max_moving_speed),-1),
                        random.randint(1,int(Level.enemy_max_moving_speed))
                        ])

                    self.speed_y        = random.choice([
                        random.randint(-int(Level.enemy_max_moving_speed),-1),
                        random.randint(1,int(Level.enemy_max_moving_speed))
                        ])

                    self.following_mode = False

                else:
                    pass

    def follow(self,direction,position):
        """
        Method to calculate following direction.
        """
        self.absolute   = np.sqrt(((direction[0]-position[0])**2)+((direction[1]-position[1])**2))
        self.speed_x    += np.round(Level.enemy_following_skalar*(direction[0]-position[0])/self.absolute,decimals=2)
        self.speed_y    += np.round(Level.enemy_following_skalar*(direction[1]-position[1])/self.absolute, decimals=2)

    def kill_sequence(self):
        Weapon_Systems.Earning_System.secondary_state +=1
        Sprites.enemy_list.remove(self)
        Sprites.all_sprites_list.remove(self)
        Upgrades((self.rect.x,self.rect.y))
        Explosion.Shocks(self.rect.x,self.rect.y)
        Explosion.Waves(self.rect.x,self.rect.y)

        Weapon_Systems.Earning_System.earned()
        self.kill()

    def rotate(self):
        """
        Method to rotate sprite's image. Uses Math.get_angle to calculate rotation.
        """
        self.image = pg.transform.rotate(self.image,Maths.get_angle((self.speed_x,self.speed_y)))

class Stars(pg.sprite.Sprite):
    """
    Stars objects for Intro and Pause menu. Stars have:
    random size in set range, random color in set range, random speed in set range.
    Stars fall from top of the screen to the bottom with increasing speed.
    """
    total = 800
    speed = 100

    def __init__(self):
        super(Stars, self).__init__()
        randomchoice = random.randint(1,8)
        self.spawn_x = random.randint(0,Setup.screen_x)
        self.spawn_y = random.randint(-5000,-50)
        self.surf = pg.Surface((randomchoice,randomchoice))
        self.image = pg.Surface((randomchoice,randomchoice))
        self.image.fill((random.randint(200,255),random.randint(200,255),random.randint(200,255)))
        self.x_speed = 0
        self.y_speed = 1
        self.rect = self.surf.get_rect(
            center=(
                self.spawn_x,
                self.spawn_y
            )
        )

       
        Sprites.stars_list.add(self)

    def update(self,time):
        """
        Stars selfdistruct if off map.
        """
        self.rect.move_ip(self.x_speed, Stars.speed * time)


        if self.rect.y > Setup.map_size[1]+20:
            self.kill()

    @staticmethod 
    def check_amount():
        """
        Method to check constant amount of stars on map. Returns boolean.
        """
        if len(Sprites.stars_list) < Stars.total:
            return False
        return True

class Weapon_Systems():
    """
    Handles all the different weapons of the player. 
    """
    tank            = False
    plane           = False

    gun             = True

    machine_gun     = False
    laser           = False

    flamethrower    = False
    rockets         = False

    @staticmethod
    def add_secondary():

        Gui.Messages.skipped = False

        if Controller.setting_mode is True:
            Weapon_Systems.flamethrower = True

        else:

            Weapon_Systems.rockets      = True
            Weapon_Systems.Plane.Rockets_Aim()

    @staticmethod
    def store_secondary():
        if Player.data_player[9] > 0:
            Player.data_player[9] -= 1

    @staticmethod
    def add_third():
        """
        Not in use yet.
        """
        if Controller.setting_mode is True:
            Weapon_Systems.machine_gun = True
        else:
            Weapon_Systems.laser      = True

    class General():
        """
        Gun that is in use by both weapon system modes
        """

        class Gun(pg.sprite.Sprite):

            shot_count     = 0
            firing         = False
            time_first_shot= 0

            def __init__(self,direction):
                super(Weapon_Systems.General.Gun, self).__init__()

                Weapon_Systems.General.Gun.shot_count += 1
                Player.data_player[7] -= 1
                self.surf       = Sprites.shot
                self.image      = Sprites.shot
                self.x_speed    = direction[0]
                self.y_speed    = direction[1]
                self.rect = self.surf.get_rect(
                    center=(
                        Player.data_player[1]-Player.camera[0]+(Sprites.player_sprite_s.get_width()/2),
                        Player.data_player[2]-Player.camera[1]+(Sprites.player_sprite_s.get_height()/2)
                    )
                )
                Sprites.shot_list.add(self)
                Sprites.all_sprites_list.add(self)

            def update(self,time):
                self.rect.move_ip(self.x_speed*Upgrades.shooting_speed*time, self.y_speed*Upgrades.shooting_speed*time)
                
                if self.rect.x < -10:
                    self.kill()
                elif self.rect.x > Setup.map_size[0]+10:
                    self.kill()
                elif self.rect.y < -10:
                    self.kill()
                elif self.rect.y > Setup.map_size[1]+10:
                    self.kill()

            @staticmethod
            def rof():
                """
                Function to check if players gun is overheating. Returns boolean.
                """
                if Weapon_Systems.General.Gun.firing is True:
                    if pg.time.get_ticks()-Weapon_Systems.General.Gun.time_first_shot > Upgrades.rof:
                        return False
                return True


        class Machine_Gun():

            """
            Here goes the none overheating gun
            """
            pass

        class Laser():
            """
            Beam weapon
            """
            pass
        pass

    class Tank():
        """
        Weapons only accessable by weapon system mode tank.
        """
        class Flamethrower(pg.sprite.Sprite):
            """
            Is measured in bursts. Costs player ammunition per burst length.
            """

            burst_count     = 0
            burst_length    = 8
            
            def __init__(self):
                
                super(Weapon_Systems.Tank.Flamethrower, self).__init__()
                Weapon_Systems.Tank.Flamethrower.burst_count += 1
                self.limiter    = 400
                self.speed      = random.randint(15,25)
                self.travelled  = 0
                self.spawn_x    = Player.data_player[1]-Player.camera[0]+(Sprites.player_sprite_s.get_width()/2)
                self.spawn_y    = Player.data_player[2]-Player.camera[1]+(Sprites.player_sprite_s.get_height()/2)

                self.vector     = self.set_direction()
                self.size       = random.randint(4,8)
                self.surf       = pg.Surface((self.size,self.size))
                self.surf.fill(Gui.pink)
                self.image      = self.surf.convert()

                self.speed_x    = self.vector[0]+ (random.randint(-6,6)/10)
                self.speed_y    = self.vector[1]+ (random.randint(-6,6)/10)

                self.rect = self.surf.get_rect(
                    center=(
                        self.spawn_x,
                        self.spawn_y
                    )
                )

                Sprites.all_sprites_list.add(self)
                Sprites.flame_thrower_list.add(self)

            def update(self,time):

                self.burst_handler()

                self.rect.x += int(self.speed_x * self.speed * time)
                self.rect.y += int(self.speed_y * self.speed * time)


                if self.travelled >= self.limiter:
                    self.kill()

                self.travelled  += np.abs(int(self.speed_x * self.speed * time))+np.abs(int(self.speed_y * self.speed * time))

            def burst_handler(self):
                
                if Weapon_Systems.Tank.Flamethrower.burst_count >= Weapon_Systems.Tank.Flamethrower.burst_length:
                    Weapon_Systems.store_secondary()
                    Weapon_Systems.Tank.Flamethrower.burst_count = 0

            def set_direction(self):
                diagonal    = Player.diagonal_factor
                angle       = Player.data_player[4]
                if angle == 0:
                    return (0, self.speed * -1 , False)
                elif angle == 45:
                    return (self.speed * -1 * diagonal,self.speed * -1 * diagonal, True)
                elif angle == 90:
                    return (self.speed * -1 ,0, False)
                elif angle == 135:
                    return (self.speed * -1 * diagonal,self.speed * diagonal,True)
                elif angle == 180:
                    return (0,self.speed,False)
                elif angle  == 225:
                    return (self.speed  * diagonal,self.speed * diagonal,True)
                elif angle == 270:
                    return (self.speed,0,False)
                elif angle == 315:
                    return (self.speed * diagonal,self.speed * -1 * diagonal, True)

    class Plane():
        """
        Weapons only accessable by weapon system mode plane
        """
        class Rockets(pg.sprite.Sprite):
            """
            Self guiding missles. Need to have a target when fired. Target is inherited from Rocket Aim.
            If target is destroyed, all rockets sent after target are destroyed as well
            """
            def __init__(self,target):
                super(Weapon_Systems.Plane.Rockets, self).__init__()
                Weapon_Systems.store_secondary()
                self.target     = target
                self.surf       = pg.Surface((10,10))
                self.surf.fill(Gui.pink)
                self.image      = self.surf.convert()
                self.speed      = 100
                self.rect = self.surf.get_rect(
                    center=(
                        Player.data_player[1]-Player.camera[0]+(Sprites.player_sprite_s.get_width()/2),
                        Player.data_player[2]-Player.camera[1]+(Sprites.player_sprite_s.get_height()/2)
                    )
                )
                Sprites.rockets_list.add(self)
                Sprites.all_sprites_list.add(self)
            
            def update(self,time):

                if self.target.alive() is False:
                    self.kill()

                self.follow_target()


                try:
                    self.rect.x += self.speed_x * self.speed * time
                    self.rect.y += self.speed_y * self.speed * time
                    Weapon_Systems.Plane.Rockets.Rocket_Burn(self.rect.center[0],self.rect.center[1],self.speed_x,self.speed_y)
                
                except: 
                    self.kill()

            def follow_target(self):

                direction    = (self.target.rect.center[0],self.target.rect.center[1])
                position     = (self.rect.x,self.rect.y)
                
                self.absolute   = np.sqrt(((direction[0]-position[0])**2)+((direction[1]-position[1])**2))
                self.speed_x    = np.round((direction[0]-position[0])/self.absolute,decimals=2)
                self.speed_y    = np.round((direction[1]-position[1])/self.absolute, decimals=2)

            class Rocket_Burn(pg.sprite.Sprite):
                """
                Visual effect for every rocket.
                """
                def __init__(self,spawn_x,spawn_y,direction_x,direction_y):
                    super(Weapon_Systems.Plane.Rockets.Rocket_Burn, self).__init__()
                    randomchoice = random.randint(1,4)

                    self.distance = 0

                    self.spawn_x = spawn_x
                    self.spawn_y = spawn_y
                    self.surf = pg.Surface((randomchoice,randomchoice))
                    self.image = pg.Surface((randomchoice,randomchoice))
                    self.image.fill((random.randint(150,255),random.randint(150,255),random.randint(150,255)))
                    self.x_speed = random.randint(1,250) * direction_x * (-1)
                    self.y_speed = random.randint(1,250) * direction_y * (-1)

                    if self.x_speed == 0 and self.y_speed == 0:
                        self.x_speed = 10
                        self.y_speed = -10


                    self.rect = self.surf.get_rect(
                        center=(
                            self.spawn_x,
                            self.spawn_y
                        )
                    )

                    Sprites.all_sprites_list.add(self)

                def update(self,time):
                    self.rect.move_ip(self.x_speed*time, self.y_speed*time)
                    self.distance += np.abs(self.x_speed*time) + np.abs(self.y_speed*time)

                    if self.distance > 200:
                        self.kill()

        class Rockets_Aim(pg.sprite.Sprite):
            """ This is the mirror to Gui.Weapon_Aiming_System.Rocket_aim
            we need this for collision checking and target locking.
            """

            aiming_distance = 300
            locked = False

            def __init__(self):

                super(Weapon_Systems.Plane.Rockets_Aim, self).__init__()
                self.dimension  = 46
                self.surf       = pg.Surface((self.dimension,self.dimension),pg.SRCALPHA)
                self.image      = self.surf.convert_alpha()
                self.correct    = self.set_position()
                self.position   = (
                    Player.data_player[1]-Player.camera[0]+(Sprites.player_sprite_s.get_width()/2)+self.correct[0], 
                    Player.data_player[2]-Player.camera[1]+(Sprites.player_sprite_s.get_height()/2)+self.correct[1]
                    )

                self.rect = self.surf.get_rect(
                    center=(
                        self.position[0],
                        self.position[1]
                    )
                )

                Sprites.rocket_aim.add(self)
                Sprites.all_sprites_list.add(self)
      
            def update(self,time):

                self.correct    = self.set_position()
                self.position   = (
                    Player.data_player[1]-Player.camera[0]+(Sprites.player_sprite_s.get_width()/2)+self.correct[0], 
                    Player.data_player[2]-Player.camera[1]+(Sprites.player_sprite_s.get_height()/2)+self.correct[1]
                    )
                self.rect.x     = self.position[0]
                self.rect.y     = self.position[1]

            def set_position(self):
                diagonal    = Player.diagonal_factor
                angle       = Player.data_player[4]
                if angle == 0:
                    return (0,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1)
                elif angle == 45:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 * diagonal,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 * diagonal)
                elif angle == 90:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 ,0)
                elif angle == 135:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 * diagonal,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * diagonal)
                elif angle == 180:
                    return (0,Weapon_Systems.Plane.Rockets_Aim.aiming_distance)
                elif angle  == 225:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance  * diagonal,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * diagonal)
                elif angle == 270:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance ,0)

                elif angle == 315:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance  * diagonal,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 * diagonal)


                else: 
                    return (0,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1)

    class Earning_System():
        """
        If condition is reached, player gets new weapon. Needs to be reset with every levelstart.
        """

        @staticmethod
        def earned():
            if Weapon_Systems.rockets is False and Weapon_Systems.flamethrower is False:
                Upgrades.secondary_store += 1

            if Player.data_player[9] < Weapon_Systems.Earning_System.secondary_condition:
                Player.data_player[9] += 1

        @staticmethod
        def set_conditions():
            Weapon_Systems.Earning_System.secondary_condition   = 5
            Weapon_Systems.Earning_System.secondary_state       = 0
            Weapon_Systems.machine_gun     = False
            Weapon_Systems.laser           = False

            Weapon_Systems.flamethrower    = False
            Weapon_Systems.rockets         = False

        @staticmethod
        def earn_secondary():
            if Upgrades.secondary_store >= Weapon_Systems.Earning_System.secondary_condition:
                Weapon_Systems.add_secondary()

class Explosion():
    """
    Visual effects, triggered by collisions. 
    """
    fractures_amount = 20

    @staticmethod
    def explode(spawn_x,spawn_y):
        """
        Handles shot collision effect.
        """
        for fracture in range(Explosion.fractures_amount):
            Explosion.Fracture(spawn_x,spawn_y)

    class Fracture(pg.sprite.Sprite):
        """
        Tiny element of explosion visual effect. Selfdestructs after travelling to its set limit.
        """
        def __init__(self,spawn_x,spawn_y):
            super(Explosion.Fracture, self).__init__()
            randomchoice = random.randint(1,4)

            self.distance = 0

            self.spawn_x = spawn_x
            self.spawn_y = spawn_y
            self.surf = pg.Surface((randomchoice,randomchoice))
            self.image = pg.Surface((randomchoice,randomchoice))
            self.image.fill((random.randint(150,255),random.randint(150,255),random.randint(150,255)))
            self.x_speed = random.randint(-250,250)
            self.y_speed = random.randint(-250,250)

            if self.x_speed == 0 and self.y_speed == 0:
                self.x_speed = 10
                self.y_speed = -10


            self.rect = self.surf.get_rect(
                center=(
                    self.spawn_x,
                    self.spawn_y
                )
            )

            Sprites.all_sprites_list.add(self)

        def update(self,time):
            self.rect.move_ip(self.x_speed*time, self.y_speed*time)
            self.distance += np.abs(self.x_speed*time) + np.abs(self.y_speed*time)

            if self.distance > 200:
                self.kill()

    class Shocks(pg.sprite.Sprite):
        """
        Round explosion core, set off by enemy kill sequence. 
        Imitates explosion flash. Needs spawning coordinates.
        """
        def __init__(self,spawn_x,spawn_y):
            super(Explosion.Shocks, self).__init__()
            self.scale   = 4
            self.factor = 1000
            self.spawn_x = spawn_x 
            self.spawn_y = spawn_y 
            self.surf = pg.Surface((self.scale,self.scale),pg.SRCALPHA)
            pg.draw.circle(self.surf,(255,255,255),(int(self.scale/2),int(self.scale/2)),int(self.scale/2))
            self.image = self.surf.convert_alpha()
            self.rect = self.surf.get_rect(
                center=(
                    self.spawn_x,
                    self.spawn_y
                )
            )

            Sprites.all_sprites_list.add(self)

        def update(self, time):
            self.surf   = pg.Surface((self.scale,self.scale),pg.SRCALPHA)
            pg.draw.circle(self.surf,(255,255,255),(int(self.scale/2),int(self.scale/2)),int(self.scale/2))
            self.image = self.surf.convert_alpha()
            self.rect = self.surf.get_rect(
                center=(
                    self.spawn_x,
                    self.spawn_y
                )
            )
            
            if self.scale > 120:
                self.factor *= -1

            self.scale += self.factor * time
        
            if self.scale < 10 and self.factor < 0:
                self.kill()

    class Waves(pg.sprite.Sprite):
        """
        Round, travelling and growing shockwave. Radius increases as oppacity and line thickness decreases.
        Set off by enemy kill sequence. Needs spawnig coordinates. Self distructs before becoming too large 
        for computer memory to calculate. :D
        """
        def __init__(self,spawn_x,spawn_y):
            super(Explosion.Waves, self).__init__()
            self.scale   = 40
            self.alpha   = 40
            self.width   = 20
            self.spawn_x = spawn_x
            self.spawn_y = spawn_y 
            self.surf = pg.Surface((self.scale,self.scale),pg.SRCALPHA)
            pg.draw.circle(
                self.surf,
                (255,255,255,int(self.alpha)),
                (int(self.scale/2),int(self.scale/2)),
                int(self.scale/2),
                int(self.width)
                )
            self.image = self.surf.convert_alpha()
            self.rect = self.surf.get_rect(
                center=(
                    self.spawn_x,
                    self.spawn_y
                )
            )

            Sprites.all_sprites_list.add(self)
            Sprites.shock_wave_list.add(self)

        def update(self, time):
            self.surf   = pg.Surface((self.scale,self.scale),pg.SRCALPHA)
            pg.draw.circle(
                self.surf,
                (255,255,255,int(self.alpha)),
                (int(self.scale/2),int(self.scale/2)),
                int(self.scale/2),
                int(self.width)
                )

            self.image = self.surf.convert_alpha()
            self.rect = self.surf.get_rect(
                center=(
                    self.spawn_x,
                    self.spawn_y
                )
            )
            self.scale += 600 * time
            self.alpha -= 20 * time
            self.width -= 5 * time
            if self.width < 2 or self.alpha < 2 or self.scale > 1400:
                self.kill()

######## AI #########

class AI():
    """
    This class loads a pretrained neural network. The neural networks were trained in a special enviroment.
    The network evolved over hundreds of failed atttempts to survive in the game. The networks topology is 
    generated randomly by neat algorithm. The best perfoming networks were saved and can be loaded in 
    replay_genome funtion.

    Only the movements of the opponent are controlled by the network. 
    Shooting is hardcoded solution.
    """
    @staticmethod
    def replay_genome(config_file, genome_path, new_game):
        """
        Load requried NEAT configuration file. Must be the same the network is trained on!
        Unpickle saved genome, load into neat compatible data structure. Run game with
        genome loaded.
        """ 
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

        with open(genome_path, "rb") as f:
            genome = pickle.load(f)

        genomes = [(1, genome)]
        new_game.game_loop(genomes, config)

    @staticmethod
    def set_up_neural_network(genomes, config):
        """
        AI needs three components: its saved net, its pygame sprite class, its genome.
        There is the possibility to train the network further more throughout gameplay.
        Further training is not implemented though.
        """
        AI.nets = []
        AI.opponents = []
        AI.ge = []

        for genome_id,genome in genomes:
            genome.fitness = 0.0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            AI.nets.append(net)
            AI.opponents.append(AI.Opponent())
            AI.ge.append(genome)

    @staticmethod
    def think():
        """
        Network gets inputs from pygame sprite class of itself and its pygame sprrite class viewing window. 
        The four input neurons take the players position and the position of any entity collided with
        its viewing window. Every output controls one of the four direction the sprite can move towards.

        """
        for x, opponent in enumerate(AI.opponents):  

            target_list = opponent.look()
            
            for target in target_list:
                output = AI.nets[AI.opponents.index(opponent)].activate((
                    opponent.rect.center[0],
                    opponent.rect.center[1],
                    opponent.rect.center[0]-target.rect.center[0],
                    opponent.rect.center[1]-target.rect.center[1]
                    ))

                if output[0] > 0.5:  
                    opponent.up()
                if output[1] > 0.5:
                    opponent.down()
                if output[2] > 0.5:
                    opponent.right()
                if output[3] > 0.5:
                    opponent.left()

    @staticmethod
    def handle(time):
        """
        If opponent sprite dies, remove genome and network so network and genome can be loaded freshly.
        Force opponent to shoot at targets and regenerate its health.
        """
        for opponent in AI.opponents:
            if opponent.data_ai[5] < 1:
                AI.nets.pop(AI.opponents.index(opponent))
                AI.ge.pop(AI.opponents.index(opponent))
                AI.opponents.pop(AI.opponents.index(opponent))
                opponent.kill()
                
        for opponent in Sprites.ai_list:
            opponent.hunt()
            opponent.regenerate(time)
           

    class Opponent(pg.sprite.Sprite):

        def __init__(self):

            """
            This is the AI Entity class. It handles the mechanics of the sprite.
            Shooting is automated. The movement gets contolled by the neural network
            via the AI.think function.

            All important values are stored in a numpy array as following:

            sprite_image    =   data_ai[0]
            position_x      =   data_ai[1]
            position_y      =   data_ai[2]
            speed           =   data_ai[3]
            angle           =   data_ai[4]
            health          =   data_ai[5]
            score           =   data_ai[6]
            ammo_count      =   data_ai[7]
            dash_level      =   data_ai[8]
            """

            super(AI.Opponent, self).__init__()
            self.is_moving  = False
            self.mover      = np.array([0,0])
            spawn_x         = 2000 #int(random.randint(Setup.map_size[0]/4,Setup.map_size[0]/4*3))
            spawn_y         = 2000 #int(random.randint(Setup.map_size[1]/4,Setup.map_size[1]/4*3))
            self.data_ai    = np.array([0,spawn_x,spawn_y,400,0,100,0,100,100])
            self.moving     = False
            self.surf       = pg.transform.rotate(Sprites.ai_sprite,self.data_ai[4])
            self.image      = self.surf
            self.rect       = self.surf.get_rect(
                center=(
                    self.data_ai[1],
                    self.data_ai[2],
                )
            )

            ### Properties (a lot of these are not in use yet!) ###
            self.shot_count             = 0
            self.shot_damage            = 2     #damage per shot on enemies
            self.rof                    = 600   #time to shoot continuously in miliseconds
            self.ammo_store             = 250   #possible ammunition inventory
            self.health_store           = 100   #possible health store
            self.gun_cool_down          = 3000  #time to cool down the gun in miliseconds
            self.mining_speed           = 1     #ammunition mining speed
            self.regeneration_speed     = 0.5   #regenerating health points per second
            self.dash_capacity          = 100   #distance Ai can jump with dash move
            self.dash_reg_speed         = 10    #the higher the value, the slower regeneration 
            self.rocket_damage          = 100   #how much damage rockets cause
            self.flame_damage           = 25    #how much damage flames cause
            self.field_of_view          = (300,300) #how far can this monster look ahead?

            self.speed_factor           = 0.7

            self.sector                 = AI.Sector(self)
            for player in Sprites.player_list:
                self.find_player = player.rect.center

            self.target_x = -1
            self.target_y = -1


            Sprites.ai_list.add(self)

        def update(self,time):
            """
            rotates the sprite's image around it's center and moves it, according to it's
            acceleration (called mover). 
            """
            self.data_ai[1] += self.mover[0] * time
            self.data_ai[2] += self.mover[1] * time

            image = Sprites.ai_sprite

            if self.is_moving is True:
                image = Sprites.ai_sprite_moving 

            self.surf       = pg.transform.rotate(image,self.data_ai[4])
            self.image      = self.surf
            self.rect       = self.surf.get_rect(
                center=(
                    self.data_ai[1],
                    self.data_ai[2],
                )
            )

            #if self.health_check() is False:
            #    self.kill()

        def look(self):

            detected_targets = pg.sprite.spritecollide(self.sector, Sprites.all_sprites_list, False)
            
            return detected_targets

        def regenerate(self,time):
            """
            handles self regeneration of the AI entity
            """
            if self.data_ai[5] < self.health_store:
                self.data_ai[5] += (self.regeneration_speed)*time

        def health_check(self):
            """
            returns life status of AI, False means dead
            """
            if self.data_ai[5] <= 0 :
                return False
            return True

        def up(self):

            self.is_moving = True
            self.data_ai[4] = 0
            if self.mover[1] > -int(Upgrades.moving_speed*self.speed_factor):
                    self.mover[1]  += Upgrades.acceleration * (-1)

        def down(self):
            self.is_moving = True
            self.data_ai[4] = 180
            if self.mover[1] < int(Upgrades.moving_speed*self.speed_factor):
                self.mover[1] += Upgrades.acceleration          
            
        def right(self):
            self.is_moving = True
            self.data_ai[4] = 270
            if self.mover[0] < int(Upgrades.moving_speed*self.speed_factor):
                self.mover[0] += Upgrades.acceleration  
        
        def left(self):
            self.is_moving = True
            self.data_ai[4] = 90
            if self.mover[0] > -int(Upgrades.moving_speed*self.speed_factor):
                self.mover[0]  += Upgrades.acceleration * (-1)

        def hunt(self):
            """
            AI hunts for same ressources as player. 
            """

            detected_targets = []
            detected_targets += pg.sprite.spritecollide(self.sector, Sprites.entity_list, False)
            detected_targets += pg.sprite.spritecollide(self.sector, Sprites.player_list, False)
            detected_targets += pg.sprite.spritecollide(self.sector, Sprites.enemy_list, False)


            for entity in detected_targets:

                ### Handles 4 - directional shooting

                if entity.rect.center[0] > self.rect.center[0]-20 and entity.rect.center[0] < self.rect.center[0]+20:
                    self.shot_count += 1
                    if self.shot_count % 3 == 0:
                        AI_shooting(self.shooting_direction(entity,axis='y'),(self.rect.center))


                elif entity.rect.center[1] > self.rect.center[1]-20 and entity.rect.center[1] < self.rect.center[1]+20:
                    self.shot_count += 1
                    if self.shot_count % 3 == 0:
                        AI_shooting(self.shooting_direction(entity,axis='x'),(self.rect.center))

                else: 
                    continue
            
            if detected_targets:
                self.target_x = entity.rect.center[0]
                self.target_y = entity.rect.center[1]
            
            else:
                self.target_x = -1
                self.target_y = -1

        def shooting_direction(self,entity,axis):

            """
            this method returns the directional vector for the AI's target.
            """

            if axis == 'x':
                if entity.rect.x < self.rect.x :
                    self.data_ai[4] = 90
                    return (self.rect.center[0]-10,self.rect.center[1])

                elif entity.rect.x > self.rect.x :
                    self.data_ai[4] = 270
                    return (self.rect.center[0]+10,self.rect.center[1])

                else:
                    return (self.rect.center[0]-10,self.rect.center[1]-10)

            if axis == 'y':
                if entity.rect.y < self.rect.y :
                    self.data_ai[4] = 0
                    return (self.rect.center[0],self.rect.center[1]-10)

                elif entity.rect.y > self.rect.y :
                    self.data_ai[4] = 180
                    return (self.rect.center[0],self.rect.center[1]+10)

                else:
                    return (self.rect.center[0]-10,self.rect.center[1]-10)
  
        def check_speed(self):
            """
            DO NOT GIVE AI UNLIMITED SPEED! DO NOT! :)
            """

            if self.mover[0] > -Upgrades.moving_speed and self.mover[0] < Upgrades.moving_speed:
                if self.mover[1] > -Upgrades.moving_speed and self.mover[1] < Upgrades.moving_speed:
                    return True
            
            return False

        def get_pushed(self,vector):

            self.mover[0] += vector [0] 
            self.mover[1] += vector [1]

    class Sector(pg.sprite.Sprite):
        def __init__(self,opponent):
            super(AI.Sector,self).__init__()
            self.ship       = opponent
            self.size       = (600,600)
            self.mining_reach        = pg.Surface(self.size,pg.SRCALPHA).convert_alpha()

            self.moving     = False
            self.surf       = self.mining_reach
            self.image      = self.mining_reach
            self.height     = self.image.get_height()
            self.width      = self.image.get_width()
            self.rect = self.surf.get_rect(
                center=(
                    self.ship.data_ai[1],
                    self.ship.data_ai[2],
                )
            )

            Sprites.ai_look_list.add(self)


        def update(self,time):
            self.rect.center = self.ship.data_ai[1], self.ship.data_ai[2]
            if self.ship.alive() is False:
                self.kill()

class AI_shooting(pg.sprite.Sprite):
    """
    Handles automated shooting by ai opponents through vector calculations.
    Is instanced by AI.opponent class. Needs to be seperat class from enemy shooting,
    or neural network will be confused by its own shooting. 
    """
    shot_count = 0
    def __init__(self,direction,position):
        super(AI_shooting, self).__init__()
        Enemy_shooting.shot_count += 1
        self.surf       = Sprites.enemy_shot
        self.image      = Sprites.enemy_shot
        self.absolute   = np.sqrt(((direction[0]-position[0])**2)+((direction[1]-position[1])**2))
        self.x_speed    = np.round((direction[0]-position[0])/self.absolute,decimals=2)
        self.y_speed    = np.round((direction[1]-position[1])/self.absolute, decimals=2)


        self.rect = self.surf.get_rect(
            center=(
                position[0],
                position[1]
            )
        )
        Sprites.ai_shot_list.add(self)

    def update(self,time):
        """
        Selfdistructs if off map. Moves according to speed (scalar) and vector.
        """
        self.rect.move_ip(self.x_speed*Level.enemy_shooting_speed*time, self.y_speed*Level.enemy_shooting_speed*time)
        
        if self.rect.x < -10:
            self.kill()
        elif self.rect.x > Setup.map_size[0]+10:
            self.kill()
        elif self.rect.y < -10:
            self.kill()
        elif self.rect.y > Setup.map_size[1]+10:
            self.kill()


######### UI / UX #########

class Gui():
    """
    All visual elements of the user interface, blited on screen not on map.
    Sorry for all the repetitions -> This part of the code is very old but still works.
    Should have worked more with child and subclasses.
    """
    #General
    main_font   = os.path.join(Paths.path_fonts,"ARCADECLASSIC.ttf")
    pink        = (200,0,100)
    white       = (255,255,255)
    black       = (0,0,0)

    class Bars():
        """
        Handles all bars. Upgrade bars are static, blited images. Every other bar 
        is a dynamic bar.
        """

        class Upgrade_Bars():

            bar_0       =   pg.image.load(os.path.join(Paths.path_bars,"bar_0.png")).convert_alpha()
            bar_1       =   pg.image.load(os.path.join(Paths.path_bars,"bar_1.png")).convert_alpha()
            bar_2       =   pg.image.load(os.path.join(Paths.path_bars,"bar_2.png")).convert_alpha()
            bar_3       =   pg.image.load(os.path.join(Paths.path_bars,"bar_3.png")).convert_alpha()
            bar_4       =   pg.image.load(os.path.join(Paths.path_bars,"bar_4.png")).convert_alpha()
            bar_5       =   pg.image.load(os.path.join(Paths.path_bars,"bar_5.png")).convert_alpha()
            bar_6       =   pg.image.load(os.path.join(Paths.path_bars,"bar_6.png")).convert_alpha()
            bar_7       =   pg.image.load(os.path.join(Paths.path_bars,"bar_7.png")).convert_alpha()
            bar_8       =   pg.image.load(os.path.join(Paths.path_bars,"bar_8.png")).convert_alpha()
            bar_9       =   pg.image.load(os.path.join(Paths.path_bars,"bar_9.png")).convert_alpha()
            bar_10      =   pg.image.load(os.path.join(Paths.path_bars,"bar_10.png")).convert_alpha()
            bar_list    =   [bar_0,bar_1,bar_2,bar_3,bar_4,bar_5,bar_6,bar_7,bar_8,bar_9,bar_10]

        class Health_Bar():
            @staticmethod
            def health_bar():
                Gui.Bars.Health_Bar.set_parameters()
                Gui.Bars.Health_Bar.build_rect()
            
            @staticmethod
            def set_parameters():
                scalar                          = 2
                Gui.Bars.Health_Bar.height      = 32
                Gui.Bars.Health_Bar.max         = Upgrades.health_store * scalar
                Gui.Bars.Health_Bar.value       = Player.data_player[5] * scalar
                Gui.Bars.Health_Bar.position    = (Setup.screen_x/2-Gui.Bars.Health_Bar.max/2,Setup.screen_y/10-Gui.Bars.Health_Bar.height/2)

            @staticmethod
            def build_rect():
                surface = pg.Surface((Gui.Bars.Health_Bar.max, Gui.Bars.Health_Bar.height), pg.SRCALPHA)
                lining  = pg.draw.rect(surface, [200, 0, 100], [0, 0, Gui.Bars.Health_Bar.max, Gui.Bars.Health_Bar.height], 1)
                block   = pg.draw.rect(surface, [200, 0, 100], ((0,0),(Gui.Bars.Health_Bar.value,Gui.Bars.Health_Bar.height)))
                Setup.screen.blit(surface, Gui.Bars.Health_Bar.position)

        class Ammo_Bar():

            @staticmethod
            def ammo_bar():
                Gui.Bars.Ammo_Bar.set_parameters()
                Gui.Bars.Ammo_Bar.build_rect()
            
            @staticmethod
            def set_parameters():
                scalar                        = 1
                Gui.Bars.Ammo_Bar.width       = 32
                Gui.Bars.Ammo_Bar.max         = Upgrades.ammo_store * scalar
                Gui.Bars.Ammo_Bar.value       = Player.data_player[7] * scalar
                Gui.Bars.Ammo_Bar.position    = (Setup.screen_x/16- Gui.Bars.Ammo_Bar.width/2, int(Setup.screen_y/16*14.5)-Gui.Bars.Ammo_Bar.max)

            @staticmethod
            def build_rect():
                surface = pg.Surface((Gui.Bars.Ammo_Bar.width, Gui.Bars.Ammo_Bar.max), pg.SRCALPHA)
                lining  = pg.draw.rect(surface, [200, 0, 100], [0, 0, Gui.Bars.Ammo_Bar.width ,Gui.Bars.Ammo_Bar.max], 1)
                block   = pg.draw.rect(surface, [200, 0, 100], ((0,Gui.Bars.Ammo_Bar.max),(Gui.Bars.Ammo_Bar.width, -Gui.Bars.Ammo_Bar.value)))
                Setup.screen.blit(surface, Gui.Bars.Ammo_Bar.position)

        class Secondary_Bar():

            @staticmethod
            def secondary_bar():
                Gui.Bars.Secondary_Bar.set_parameters()
                Gui.Bars.Secondary_Bar.build_rect()
            
            @staticmethod
            def set_parameters():
                scalar                             = 20
                Gui.Bars.Secondary_Bar.width       = 8
                Gui.Bars.Secondary_Bar.max         = Upgrades.secondary_store * scalar
                Gui.Bars.Secondary_Bar.value       = Player.data_player[9] * scalar
                Gui.Bars.Secondary_Bar.position    = (Setup.screen_x/12- Gui.Bars.Secondary_Bar.width/2, int(Setup.screen_y/16*14.5)-Gui.Bars.Secondary_Bar.max)

            @staticmethod
            def build_rect():
                surface = pg.Surface((Gui.Bars.Secondary_Bar.width, Gui.Bars.Secondary_Bar.max), pg.SRCALPHA)
                lining  = pg.draw.rect(surface, [200, 0, 100], [0, 0, Gui.Bars.Secondary_Bar.width ,Gui.Bars.Secondary_Bar.max], 1)
                block   = pg.draw.rect(surface, [200, 0, 100], ((0,Gui.Bars.Secondary_Bar.max),(Gui.Bars.Secondary_Bar.width, -Gui.Bars.Secondary_Bar.value)))
                Setup.screen.blit(surface, Gui.Bars.Secondary_Bar.position)

        class Dash_Bar():
            @staticmethod
            def dash_bar():
                Gui.Bars.Dash_Bar.set_parameters()
                Gui.Bars.Dash_Bar.build_rect()
            
            @staticmethod
            def set_parameters():
                scalar                        = 1
                Gui.Bars.Dash_Bar.height      = 5
                Gui.Bars.Dash_Bar.max         = Upgrades.dash_capacity * scalar
                Gui.Bars.Dash_Bar.value       = Player.data_player[8] * scalar
                Gui.Bars.Dash_Bar.position    = (Setup.screen_x/2-Gui.Bars.Dash_Bar.max/2,Setup.screen_y/14-Gui.Bars.Dash_Bar.height/2)

            @staticmethod
            def build_rect():
                surface = pg.Surface((Gui.Bars.Dash_Bar.max, Gui.Bars.Dash_Bar.height), pg.SRCALPHA)
                lining  = pg.draw.rect(surface, [200, 0, 100], [0, 0, Gui.Bars.Dash_Bar.max, Gui.Bars.Dash_Bar.height], 1)
                block   = pg.draw.rect(surface, [200, 0, 100], ((0,0),(Gui.Bars.Dash_Bar.value,Gui.Bars.Dash_Bar.height)))
                Setup.screen.blit(surface, Gui.Bars.Dash_Bar.position)

    class Weapon_Aiming_Systems():
        """
        If the aiming systems are blitted on the World it does not run smoothly,
        that's why we blit on the main screen.
        """

        class Rocket_Aim():

            dimension = 40
            surface   = pg.Surface((40,40),pg.SRCALPHA)

            @staticmethod
            def render():
                if Weapon_Systems.rockets is True:

                    if Weapon_Systems.Plane.Rockets_Aim.locked is True:
                        aimer      = pg.draw.circle(
                            Gui.Weapon_Aiming_Systems.Rocket_Aim.surface,Gui.pink,
                            (int(Gui.Weapon_Aiming_Systems.Rocket_Aim.dimension/2),
                            int(Gui.Weapon_Aiming_Systems.Rocket_Aim.dimension/2)),
                            int(Gui.Weapon_Aiming_Systems.Rocket_Aim.dimension/2),3
                            )
                    else: 
                        aimer      = pg.draw.circle(
                            Gui.Weapon_Aiming_Systems.Rocket_Aim.surface,Gui.white,
                            (int(Gui.Weapon_Aiming_Systems.Rocket_Aim.dimension/2),
                            int(Gui.Weapon_Aiming_Systems.Rocket_Aim.dimension/2)),
                            int(Gui.Weapon_Aiming_Systems.Rocket_Aim.dimension/2),3
                            )

                    position    = Gui.Weapon_Aiming_Systems.Rocket_Aim.set_position()
                    position_x  = position[0]+Setup.screen_x/2-Gui.Weapon_Aiming_Systems.Rocket_Aim.dimension/2
                    position_y  = position[1]+Setup.screen_y/2-Gui.Weapon_Aiming_Systems.Rocket_Aim.dimension/2

                    Setup.screen.blit(Gui.Weapon_Aiming_Systems.Rocket_Aim.surface,(position_x,position_y))

            @staticmethod
            def set_position():
                diagonal    = Player.diagonal_factor
                angle       = Player.data_player[4]
                if angle == 0:
                    return (0,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1)
                elif angle == 45:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 * diagonal,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 * diagonal)
                elif angle == 90:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 ,0)
                elif angle == 135:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 * diagonal,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * diagonal)
                elif angle == 180:
                    return (0,Weapon_Systems.Plane.Rockets_Aim.aiming_distance)
                elif angle  == 225:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance  * diagonal,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * diagonal)
                elif angle == 270:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance ,0)
                elif angle == 315:
                    return (Weapon_Systems.Plane.Rockets_Aim.aiming_distance  * diagonal,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1 * diagonal)


                else: 
                    return (0,Weapon_Systems.Plane.Rockets_Aim.aiming_distance * -1)

    class Choose_Controller():
        """
        Handles all elements on Weapon System choosing screen
        """
        def __init__(self):
            self.positioning()
            self.fonts()
            self.texts()
            self.rects()
            self.selector()
            self. moving            = False

        def selector(self):
            self.setting_mode  = True

            self.selector_size_x         =   400
            self.selector_size_y         =   110
            self.selector_surface        =   pg.Surface((self.selector_size_x,self.selector_size_y), pg.SRCALPHA, 32)
            pg.draw.rect(self.selector_surface, [200, 0, 100], [0,0,self.selector_size_x,self.selector_size_y], 5)

            if self.setting_mode is True:
                self.pos_selector_x         =   Setup.screen_x/2 - self.selector_size_x
            else:
                self.pos_selector_x         =   Setup.screen_x/2

            self.pos_selector_y         =   Setup.screen_y/3*2 - self.selector_size_y/2

        def fonts(self):
            self.font               = pg.font.Font(Gui.main_font, 32) 
            self.font_large         = pg.font.Font(Gui.main_font, 100)
        
        def positioning(self):
            self.pos_explaination_x = Setup.screen_x/2
            self.pos_explaination_y = Setup.screen_y/5*2

            self.pos_tank_x         = Setup.screen_x / 3
            self.pos_tank_y         = Setup.screen_y/3*2

            self.pos_plane_x        = Setup.screen_x / 3*2
            self.pos_plane_y        = Setup.screen_y/3*2

        def texts(self):
            self.text_explaination  = self.font.render('CHOOSE  YOUR  WEAPON  SYSTEM MODE', True, Gui.pink)
            self.text_tank          = self.font_large.render('TANK', True, Gui.pink)
            self.text_plane         = self.font_large.render('PLANE', True, Gui.pink)

        def rects(self):

            self.textRect_exp           = self.text_explaination.get_rect()  
            self.textRect_exp.center    = (self.pos_explaination_x,self.pos_explaination_y)

            self.textRect_tank          = self.text_tank.get_rect()  
            self.textRect_tank.center   = (self.pos_tank_x,self.pos_tank_y)

            self.textRect_plane         = self.text_plane.get_rect()  
            self.textRect_plane.center  = (self.pos_plane_x,self.pos_plane_y)

        def render(self):
            
            self.repositioning()

            Setup.screen.blit(self.text_explaination, self.textRect_exp)
            Setup.screen.blit(self.text_tank, self.textRect_tank)
            Setup.screen.blit(self.text_plane, self.textRect_plane)
            Setup.screen.blit(self.selector_surface,(self.pos_selector_x,self.pos_selector_y))


        def move(self,time):

            self.pos_explaination_y += Stars.speed * time
            self.pos_tank_y         += Stars.speed * time
            self.pos_plane_y        += Stars.speed * time
            self.pos_selector_y     += Stars.speed * time

        def repositioning(self):

            self.textRect_exp.center    = (self.pos_explaination_x,self.pos_explaination_y)
            self.textRect_tank.center   = (self.pos_tank_x,self.pos_tank_y)
            self.textRect_plane.center  = (self.pos_plane_x,self.pos_plane_y)

            if self.setting_mode is True:
                self.pos_selector_x         =   Setup.screen_x/2 - self.selector_size_x
            else:
                self.pos_selector_x         =   Setup.screen_x/2

        def off_screen(self):
            if self.pos_explaination_y > Setup.screen_y + 50:
                return True
            return False
  
    class Pause_Menu():
        """
        Pause Menu elements. Very similar to choose_controller but with ohter aspects and ratios.
        """
        def __init__(self):
            self.positioning()
            self.fonts()
            self.texts()
            self.rects()
            self.selector()
            self.moving            = False

        def selector(self):
            self.setting_mode  = True
            self.selected      = False

            self.selector_size_x         =   Setup.screen_x/2
            self.selector_size_y         =   110
            self.selector_surface        =   pg.Surface((self.selector_size_x,self.selector_size_y), pg.SRCALPHA, 32)
            pg.draw.rect(self.selector_surface, [200, 0, 100], [0,0,self.selector_size_x,self.selector_size_y], 5)

            if self.setting_mode is True:
                self.pos_selector_x         =   Setup.screen_x/2 - self.selector_size_x
            else:
                self.pos_selector_x         =   Setup.screen_x/2

            self.pos_selector_y         =   Setup.screen_y/3*2 - self.selector_size_y/2

        def fonts(self):
            self.font               = pg.font.Font(Gui.main_font, 32) 
            self.font_large         = pg.font.Font(Gui.main_font, 100)
        
        def positioning(self):
            self.pos_explaination_x = Setup.screen_x/2
            self.pos_explaination_y = Setup.screen_y/5*2

            self.pos_tank_x         = Setup.screen_x / 4
            self.pos_tank_y         = Setup.screen_y/3*2

            self.pos_plane_x        = Setup.screen_x / 4*3
            self.pos_plane_y        = Setup.screen_y/3*2

        def texts(self):
            self.text_explaination  = self.font.render('PAUSE', True, Gui.pink)
            self.text_tank          = self.font_large.render('SETTINGS', True, Gui.pink)
            self.text_plane         = self.font_large.render('CONTINUE', True, Gui.pink)

        def rects(self):

            self.textRect_exp           = self.text_explaination.get_rect()  
            self.textRect_exp.center    = (self.pos_explaination_x,self.pos_explaination_y)

            self.textRect_tank          = self.text_tank.get_rect()  
            self.textRect_tank.center   = (self.pos_tank_x,self.pos_tank_y)

            self.textRect_plane         = self.text_plane.get_rect()  
            self.textRect_plane.center  = (self.pos_plane_x,self.pos_plane_y)

        def render(self):
            
            self.repositioning()

            Setup.screen.blit(self.text_explaination, self.textRect_exp)
            Setup.screen.blit(self.text_tank, self.textRect_tank)
            Setup.screen.blit(self.text_plane, self.textRect_plane)
            Setup.screen.blit(self.selector_surface,(self.pos_selector_x,self.pos_selector_y))

        def move(self,time):

            self.pos_explaination_y += Stars.speed * time
            self.pos_tank_y         += Stars.speed * time
            self.pos_plane_y        += Stars.speed * time
            self.pos_selector_y     += Stars.speed * time

        def repositioning(self):

            self.textRect_exp.center    = (self.pos_explaination_x,self.pos_explaination_y)
            self.textRect_tank.center   = (self.pos_tank_x,self.pos_tank_y)
            self.textRect_plane.center  = (self.pos_plane_x,self.pos_plane_y)

            if self.setting_mode is True:
                self.pos_selector_x         =   Setup.screen_x/2 - self.selector_size_x
            else:
                self.pos_selector_x         =   Setup.screen_x/2

        def off_screen(self):
            if self.pos_explaination_y > Setup.screen_y + 50:
                return True
            return False

    class Setting_Menu(Pause_Menu):
        """
        Pause menu same same
        """
        def __init__(self):
            super(Gui.Setting_Menu, self).__init__()
            self.text_explaination  = self.font.render('SETTINGS', True, Gui.pink)
            self.text_tank          = self.font_large.render('SOUND ON', True, Gui.pink)
            self.text_plane         = self.font_large.render('SOUNF OFF', True, Gui.pink)

    class Quitting_Menu(Pause_Menu):
        """
        Pause menu same same
        """
        
        def __init__(self):
            super(Gui.Quitting_Menu, self).__init__()
            self.text_explaination  = self.font.render(' ', True, Gui.pink)
            self.text_tank          = self.font_large.render('QUIT GAME', True, Gui.pink)
            self.text_plane         = self.font_large.render('CONTINUE', True, Gui.pink)

    class Messages():

        """
        Used to display tutorial instructions in beginning of level
        and when weapon is upgraded. Messages can be skipped
        """
        
        
        texts = [
            "PRESS  RETURN  TO  SKIP  TUTORIAL ",
            "PRESS  ASDW  TO  STEER",
            "PRESS  ARROWS  TO  SHOOT",
            "PRESS  SPACE  TO  DASH",
            "SHOOT  ASTEROIDS  TO  EARN  POINTS",
            'GATHER  AMMO  NEAR  PURPLE  ASTEROIDS', 
            'DESTROY  5  DRONES  TO  UPGRADE  WEAPONSYSTEM',
            'COLLECT  ADDITIONAL  UPGRADES  WHEN  YOU  DESTROY  DRONES',
            "PRESS  Q  TO  DISPLAY  YOUR  UPGRADES",
        ]

        texts_secondary = [

            "SECONDARY  WEAPONSYSTEM  UPGRADED",
            "PRESS  SHIFT  TO  FIRE  FLAMETHROWER",
            "PRESS  LEFT  ARROW  TO  FIRE  ROCKET  WHEN  AIM  IS  LOCKED"  
        ]

        intro_counter       = 0
        secondary_counter   = 0
        displaying_time     = 5000 
        displaying          = False
        skipped             = False
        in_intro            = True
        in_secondary        = False

        @staticmethod
        def set_all():
            Gui.Messages.intro_counter       = 0
            Gui.Messages.secondary_counter   = 0
            Gui.Messages.displaying_time     = 5000 
            Gui.Messages.displaying          = False
            Gui.Messages.skipped             = False
            Gui.Messages.in_intro            = True
            Gui.Messages.in_secondary        = False

        @staticmethod
        def handle():

            if Gui.Messages.in_intro is True: 
                Gui.Messages.intro_count()

                if Gui.Messages.skipped is False and Gui.Messages.displaying is False:
                    Gui.Messages.new_message = Gui.Messages(Gui.Messages.texts[Gui.Messages.intro_counter])
                
                elif Gui.Messages.skipped is False and Gui.Messages.displaying is True:
                    Gui.Messages.new_message.render()
                    Gui.Messages.new_message.check_timing()

            elif Gui.Messages.in_secondary is True:
                Gui.Messages.secondary_count()

                if Gui.Messages.skipped is False and Gui.Messages.displaying is False:
                    Gui.Messages.new_message = Gui.Messages(Gui.Messages.texts_secondary[Gui.Messages.secondary_counter])
                
                elif Gui.Messages.skipped is False and Gui.Messages.displaying is True:
                    Gui.Messages.new_message.render()
                    Gui.Messages.new_message.check_timing()

        @staticmethod
        def intro_count():
            if Gui.Messages.intro_counter == len(Gui.Messages.texts):
                Gui.Messages.in_intro = False
                Gui.Messages.in_secondary = True
                Gui.Messages.skipped = True

        @staticmethod
        def secondary_count():
            if Gui.Messages.secondary_counter >= len(Gui.Messages.texts_secondary):
                Gui.Messages.in_intro = False
                Gui.Messages.in_secondary = False
                Gui.Messages.skipped = True

            if Weapon_Systems.flamethrower is True:
                if Gui.Messages.secondary_counter == 2:
                    Gui.Messages.in_intro = False
                    Gui.Messages.in_secondary = False
                    Gui.Messages.skipped = True

        @staticmethod
        def skip():
            if Gui.Messages.in_intro is True:
                Gui.Messages.skip_intro()
            
            elif Gui.Messages.in_secondary is True:
                Gui.Messages.skip_secondary() 

        @staticmethod
        def skip_intro():
            Gui.Messages.skipped = True
            Gui.Messages.in_intro = False
            Gui.Messages.in_secondary = True
            Gui.Messages.displaying  = False

        @staticmethod
        def skip_secondary():
            Gui.Messages.in_intro = False
            Gui.Messages.in_secondary = False
            Gui.Messages.skipped = True
            Gui.Messages.displaying  = False


        def __init__(self,txt):
            self.start_time = pg.time.get_ticks()
            self.positioning()
            self.fonts()
            self.txt = txt
            self.text_set()
            self.rects()
            Gui.Messages.displaying = True

        def positioning(self):

            self.x = Setup.screen_x/2
            self.y = Setup.screen_y/5*2

        def fonts(self):
            self.font = pg.font.Font(Gui.main_font, 32)

        def text_set(self):
            self.text = self.font.render(self.txt, True, Gui.pink)     

        def rects(self):
            self.rect = self.text.get_rect()
            self.rect.center = self.x, self.y   

        def render(self):           
            Setup.screen.blit(self.text,self.rect)

        def check_timing(self):
            if pg.time.get_ticks() > self.start_time + Gui.Messages.displaying_time:
                
                if Gui.Messages.in_intro is True:
                    Gui.Messages.intro_counter    +=1

                elif Gui.Messages.in_secondary is True:
                    if Weapon_Systems.flamethrower is True:
                        Gui.Messages.secondary_counter +=1
                    else:
                        Gui.Messages.secondary_counter +=2


                Gui.Messages.displaying  = False
            

    ####### MAIN GUI OBJECT #######


    def __init__(self):
        self.positioning()
        self.fonts()
        self.texts()
        self.rects()

        self.mining_angle   = 0

    def fonts(self):

        self.font           = pg.font.Font(Gui.main_font, 32) 
        self.font_go        = pg.font.Font(Gui.main_font, 180) 
        self.font_rs        = pg.font.Font(Gui.main_font, 50)
        self.font_off_map   = pg.font.Font(Gui.main_font, 100)

    def positioning(self):

        self.x_score    = Setup.screen_x/10*9
        self.y_score    = Setup.screen_y/10
        self.x_overheat = Setup.screen_x/2
        self.y_overheat = Setup.screen_y/6*2
        self.x_ammo     = Setup.screen_x/16
        self.y_ammo     = Setup.screen_y/16*15
        self.x_off_map  = Setup.screen_x/2
        self.y_off_map  = Setup.screen_y/5

    def rects(self):

        self.textRect_score = self.text_score.get_rect()  
        self.textRect_score.center = (self.x_score,self.y_score)

        self.textRect_overheat = self.text_overheat.get_rect()  
        self.textRect_overheat.center = (self.x_overheat,self.y_overheat)

        self.textRect_ammo = self.text_ammo.get_rect()  
        self.textRect_ammo.center = (self.x_ammo,self.y_ammo)
        # Gameover
        self.textRect_go = self.text_go.get_rect()  
        self.textRect_go.center = (Setup.screen_x/2,Setup.screen_y/2)
        # Restart
        self.textRect_rs = self.text_rs.get_rect()  
        self.textRect_rs.center = (Setup.screen_x/2,Setup.screen_y/2+100)
        # Save Score
        self.textRect_save_score = self.text_save_score.get_rect()  
        self.textRect_save_score.center = (Setup.screen_x/2,Setup.screen_y/6*2)

        #Upgrades
        self.textRect_no_upgrade = self.text_no_upgrade.get_rect()  
        self.textRect_no_upgrade.center = (Setup.screen_x/2,Setup.screen_y/4*6)
        self.textRect_max_upgrade = self.text_max_upgrade.get_rect()  
        self.textRect_max_upgrade.center = (Setup.screen_x/2,Setup.screen_y/5*6)


        self.textRect_off_map = self.text_off_map.get_rect()  
        self.textRect_off_map.center = (self.x_off_map,self.y_off_map)

    def texts(self):

        self.text_score         = self.font.render('SCORE  {}'.format(int(Player.data_player[6])), True, Gui.pink) 
        self.text_overheat      = self.font.render('YOUR GUN IS OVERHEATING', True, Gui.pink)
        self.text_no_upgrade    = self.font.render('UPGRADE NOT POSSIBLE', True, Gui.pink)
        self.text_max_upgrade   = self.font.render('MAXIMUM UPGRADES REACHED', True, Gui.pink)
        self.text_ammo          = self.font.render('AMMO', True, Gui.pink) 
        self.text_go            = self.font_go.render('GAME OVER', True, Gui.pink)
        self.text_save_score    = self.font_rs.render('PRESS  ESC  TO  SAVE  SCORE', True, Gui.pink)
        self.text_rs            = self.font_rs.render('PRESS  SHIFT  TO  RESTART', True, Gui.pink)
        self.text_off_map       = self.font_off_map.render('GET BACK OR DIE', True, Gui.pink)

    def render(self):

        self.text_score = self.font.render('Score  {}'.format(int(Player.data_player[6])), True, Gui.pink)

        Setup.screen.blit(self.text_score, self.textRect_score)
        Setup.screen.blit(self.text_ammo, self.textRect_ammo)
        
        Gui.Bars.Health_Bar.health_bar()
        Gui.Bars.Ammo_Bar.ammo_bar()
        Gui.Bars.Dash_Bar.dash_bar()
        Gui.Bars.Secondary_Bar.secondary_bar()

        if Weapon_Systems.rockets is True:
            Gui.Weapon_Aiming_Systems.Rocket_Aim.render()
            
    def game_over(self):
        
        Setup.screen.blit(self.text_save_score, self.textRect_save_score)
        Setup.screen.blit(self.text_go, self.textRect_go)
        Setup.screen.blit(self.text_rs, self.textRect_rs)

    @staticmethod
    def build_upgrades():
        all_levels = [Upgrades.level_healthstore,Upgrades.level_regeneration_speed,Upgrades.level_moving_speed,Upgrades.level_ammo_store,Upgrades.level_shooting_speed,Upgrades.level_mining_speed]
        size = (440,640)
        upgrade_surface     =   pg.Surface(size, pg.SRCALPHA, 32)


        for i in range(len(Sprites.all_upgrades)):

            level   = all_levels[i]
            line    = Gui.build_upgrade_line(Sprites.all_upgrades[i],level)
            height  = i*32+64
            upgrade_surface.blit(line,(20,height))

        Setup.screen.blit(upgrade_surface,(Setup.screen_x - size[0],Setup.screen_y/2))

    @staticmethod
    def build_upgrade_line(image,level):
        line_surface = pg.Surface((384,32), pg.SRCALPHA, 32)
        line_surface.blit(image,(0,0))
        try:
            bar = pg.transform.scale(Gui.Bars.Upgrade_Bars.bar_list[level],(320,32))
        except:
            bar = pg.transform.scale(Gui.Bars.Upgrade_Bars.bar_list[10],(320,32))
            #screen alert goes here: maximum updates reached
        line_surface.blit(bar,(64,0))
        return line_surface

    def mining(self):
        
        sprite              = pg.transform.scale(Sprites.mine,(40,40))
        position            = Setup.screen_x/2 , Setup.screen_y/20*12

        rotated             = pg.transform.rotate(sprite, self.mining_angle)
        rect                = rotated.get_rect(center = position)
        Setup.screen.blit(rotated,rect)

    def overheat(self):

        Setup.screen.blit(self.text_overheat, self.textRect_overheat)

    def off_map(self):

        Setup.screen.blit(self.text_off_map, self.textRect_off_map)

    def no_upgrade(self):
        Setup.screen.blit(self.text_no_upgrade, self.textRect_no_upgrade)

    def max_upgrade(self):
        Setup.screen.blit(self.text_max_upgrade, self.textRect_max_upgrade)

class Music():
    """
    Loads music according to the games intensity. 
    """

    paused = False

    def __init__ (self):
        self.folder     = Music.define_intensity()
        self.track      = random.choice(os.listdir(self.folder))
        self.path       = os.path.join(self.folder,self.track)
        self.samplerate = self.get_sample_rate(self.path)

        pg.mixer.quit()
        pg.mixer.init(frequency=self.samplerate)
        pg.mixer.music.load(self.path)
        pg.mixer.music.play()

    @staticmethod
    def end_music():
        pg.mixer.music.fadeout(2000)

    @staticmethod
    def pause_music():
        pg.mixer.music.pause()
        Music.paused = True
    
    @staticmethod
    def unpause_music():
        pg.mixer.music.unpause()
        Music.paused = False

    def get_sample_rate(self,file):
        audio_info = mutagen.File(file).info
        return audio_info.sample_rate

    @staticmethod
    def define_intensity():
        if Level.level <= Level.intensity_1:
            return Paths.path_songs_it1
        elif Level.level <= Level.intensity_2 and Level.level > Level.intensity_1:
            return Paths.path_songs_it2
        elif Level.level > Level.intensity_2:
            return Paths.path_songs_it3

    @staticmethod
    def check_if_playing():
        return pg.mixer.music.get_busy() #returns boolean

class Camera():
    """
    Visual effects for the camera movement
    """
    moves = []
    class Shock_Wave_Shake():
        """
        when player collides with shock wave, short sequence of 
        camera moves are executed, frame by frame. 
        """
        
        def __init__(self,vector):
            self.move_x      = [
                20  * vector[0],
                -20 * vector[0],
                15  * vector[0],
                -15 * vector[0],
                10  * vector[0],
                -10 * vector[0],
                5   * vector[0],
                -5  * vector[0]
                ]

            self.move_y     = [
                20  * vector[1],
                -20 * vector[1],
                15  * vector[1],
                -15 * vector[1],
                10  * vector[1],
                -10 * vector[1],
                5   * vector[1],
                -5  * vector[1]
                ] 

            self.move_count = 0
            Camera.moves.append(self)

        def move(self):
            if self.move_count < len(self.move_x):
                Player.camera[0] += int(self.move_x[self.move_count])
                Player.camera[1] += int(self.move_y[self.move_count])
                self.move_count  += 1
            else: 
                Camera.moves.remove(self)


######### CALCULATIONS #########

class Timer():
    """
    Mostly unused timer. Important for gun overheating
    """
    running  = False
    game_start= 0
    def __init__(self):
        self.time   =   pg.time.get_ticks()
        Timer.running = True

    def check(self,criteria):
        if pg.time.get_ticks() >= self.time + criteria:
            Timer.running = False

    @staticmethod
    def set_game_start():
        Timer.game_start = pg.time.get_ticks()

    class Display_Timer():

        def __init__(self,seconds):
            self.time           = pg.time.get_ticks()
            self.display_time   = seconds * 1000
            self.disappear       = self.time + self.display_time
        
        def check_alive(self):
            if pg.time.get_ticks() >= self.disappear:
                return False
            return True

class Maths():
    """
    Plain vector geometry, catering to different needs.
    """
    @staticmethod
    def get_angle(vector_1):
        vector_2        = (0,1)
        scalar_product  = vector_1[0]* vector_2[0] + vector_1[1]* vector_2[1]
        absolute        = np.sqrt(vector_1[0]**2 + vector_1[1]**2) * np.sqrt(vector_2[0]**2 + vector_2[1]**2)
        return np.arccos(scalar_product/absolute)

    @staticmethod
    def get_impact_direction(impact_vector,player):
        if player.moving is False:
            return impact_vector
        else:
            player_vector   = Maths.get_player_vector()
            direction = (-(impact_vector[0]-player_vector[0]),-(impact_vector[1]-player_vector[1]))
            
            return direction

    @staticmethod
    def get_player_vector():
        angle    = Player.data_player[5]
        distance = Upgrades.moving_speed / 10
        if angle == 45:
            player_vector = (-distance * Player.diagonal_factor,-distance * Player.diagonal_factor)
        elif angle == 90:
            player_vector = (-distance,0)
        elif angle == 135:
            player_vector = (-distance * Player.diagonal_factor,distance * Player.diagonal_factor)
        elif angle == 180:
            player_vector = (0, distance)
        elif angle == 225:
            player_vector = (distance * Player.diagonal_factor,distance * Player.diagonal_factor)
        elif angle == 270:
            player_vector = (distance,0)
        elif angle == 315:
            player_vector = (distance * Player.diagonal_factor,-distance * Player.diagonal_factor)
        elif angle == 0:
            player_vector = (0, -distance)

        return player_vector

    @staticmethod
    def get_shockwave_vector(player,wave_source):
        vector      = (
            player.rect.x - wave_source.rect.x,
            player.rect.y - wave_source.rect.y
        )

        absolute    = np.sqrt(vector[0]**2+vector[1]**2)
        normalized  = (vector[0]/absolute , vector[1] / absolute)

        return normalized

    
    @staticmethod
    def get_normalized_vector(vector_a,vector_b):
        vector      = (
            vector_b[0] - vector_a[0],
            vector_b[1] - vector_a[1]
        )

        absolute    = np.sqrt(vector[0]**2+vector[1]**2)
        normalized  = np.array([np.ceil(vector[0]/absolute) ,np.ceil(vector[1] / absolute)])

        return normalized

class Controller():
    """
    Takes user input and calls appropriate functions and methods. 
    get_pushed funtion does not belong here, but is here because no reason.
    Important to know: There are two different shooting funtions, according
    to the weapon system mode.
    """
    setting_mode = True #tank == True ; plane == False

    @staticmethod
    def movement(time):
        pressed_keys = pg.key.get_pressed()
        is_moving = False
        

        Player.camera[0] += Player.mover[0]  * time 
        Player.camera[1] += Player.mover[1]  * time

        if pressed_keys[K_a]:
            is_moving = True
            if Player.mover[0] < Upgrades.moving_speed:
                Player.mover[0]  += Upgrades.acceleration 

        
        if pressed_keys[K_d]:
            is_moving = True
            if Player.mover[0] > -Upgrades.moving_speed:
                Player.mover[0] += Upgrades.acceleration * (-1)

        if pressed_keys[K_w]:
            is_moving = True
            if Player.mover[1] < Upgrades.moving_speed:
                Player.mover[1]  += Upgrades.acceleration 

        
        if pressed_keys[K_s]:
            is_moving = True
            if Player.mover[1] > -Upgrades.moving_speed:
                Player.mover[1] += Upgrades.acceleration * (-1)


        
        if pressed_keys[K_SPACE]:
            if Player.data_player[8] >= Upgrades.dash_capacity:
                is_moving = True
                Player.data_player[8] -= 100
                distance = 250
                angle    = Player.data_player[4] 
                if angle == 45:
                    Player.camera[0] += distance * Player.diagonal_factor
                    Player.camera[1] += distance * Player.diagonal_factor
                elif angle == 90:
                    Player.camera[0] += distance
                elif angle == 135:
                    Player.camera[0] += distance * Player.diagonal_factor
                    Player.camera[1] -= distance * Player.diagonal_factor
                elif angle == 180:
                    Player.camera[1] -= distance
                elif angle == 225:
                    Player.camera[0] -= distance * Player.diagonal_factor
                    Player.camera[1] -= distance * Player.diagonal_factor
                elif angle == 270:
                    Player.camera[0] -= distance
                elif angle == 315:
                    Player.camera[0] -= distance * Player.diagonal_factor
                    Player.camera[1] += distance * Player.diagonal_factor
                elif angle == 0:
                    Player.camera[1] += distance

        
        return is_moving

    @staticmethod
    def get_pushed(vector):

        Player.mover[0] -= vector [0] 
        Player.mover[1] -= vector [1] 

    @staticmethod
    def shooting():
        if Controller.setting_mode is True:
            Controller.shooting_tank()

        else:
            Controller.shooting_plane()

    @staticmethod
    def shooting_tank():
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[K_LEFT]:

            if pressed_keys[K_UP]:
                Weapon_Systems.General.Gun((-0.7071,-0.7071))
            elif pressed_keys[K_DOWN]:
                Weapon_Systems.General.Gun((-0.7071,0.7071))
            else:
                Weapon_Systems.General.Gun((-1,0))

        elif pressed_keys[K_DOWN]:

            if pressed_keys[K_LEFT]:
                Weapon_Systems.General.Gun((-0.7071,0.7071))
            elif pressed_keys[K_RIGHT]:
                Weapon_Systems.General.Gun((0.7071,0.7071))
            else: 
                Weapon_Systems.General.Gun((0,1))

        elif pressed_keys[K_RIGHT]:

            if pressed_keys[K_UP]:
                Weapon_Systems.General.Gun((0.7071,-0.7071))
            elif pressed_keys[K_DOWN]:
                Weapon_Systems.General.Gun((0.7071,0.7071))
            else:
                Weapon_Systems.General.Gun((1,0))

        elif pressed_keys[K_UP]:

            if pressed_keys[K_LEFT]:
                Weapon_Systems.General.Gun((-0.7071,-0.7071))
            elif pressed_keys[K_RIGHT]:
                Weapon_Systems.General.Gun((0.7071,-0.7071))
            else:
                Weapon_Systems.General.Gun((0,-1))

        if Weapon_Systems.flamethrower is True:
            if Player.data_player[9] > 0:
                if pressed_keys[K_LSHIFT] or pressed_keys[K_RSHIFT]:
                    Weapon_Systems.Tank.Flamethrower()

    @staticmethod
    def shooting_plane():
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[K_UP]:
            if Player.data_player[4] == 0:
                Weapon_Systems.General.Gun((0,-1))
            elif Player.data_player[4] == 45:
                Weapon_Systems.General.Gun((-0.7071,-0.7071))
            elif Player.data_player[4] == 90:
                Weapon_Systems.General.Gun((-1,0))
            elif Player.data_player[4] == 135:
                Weapon_Systems.General.Gun((-0.7071,0.7071))
            elif Player.data_player[4] == 180:
                Weapon_Systems.General.Gun((0,1))
            elif Player.data_player[4] == 225:
                Weapon_Systems.General.Gun((0.7071,0.7071))
            elif Player.data_player[4] == 270:
                Weapon_Systems.General.Gun((1,0))
            elif Player.data_player[4] == 315:
                Weapon_Systems.General.Gun((0.7071,-0.7071))

        if Weapon_Systems.rockets is True: 
            if Weapon_Systems.Plane.Rockets_Aim.locked is True:
                if Player.data_player[9] > 0:      
                    if pressed_keys[K_LEFT]:
                        Weapon_Systems.Plane.Rockets(Collisions.locking_rocket_aim()[-1])

    @staticmethod
    def turning():
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[K_a]:
            if pressed_keys[K_w]:
                Player.data_player[4] = 45
            elif pressed_keys[K_s]:
                Player.data_player[4] = 135
            else:
                Player.data_player[4] = 90

        elif pressed_keys[K_s]:
            if pressed_keys[K_a]:
                Player.data_player[4] = 135
            elif pressed_keys[K_d]:
                Player.data_player[4] = 225
            else: 
                Player.data_player[4] = 180

        elif pressed_keys[K_d]:
            if pressed_keys[K_w]:
                Player.data_player[4] = 315
            elif pressed_keys[K_s]:
                Player.data_player[4] = 225
            else:
                Player.data_player[4] = 270

        elif pressed_keys[K_w]:
            if pressed_keys[K_a]:
                Player.data_player[4] = 45
            elif pressed_keys[K_d]:
                Player.data_player[4] = 315
            else:
                Player.data_player[4] = 0

    @staticmethod
    def upgrade_gui():
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[K_q]:
            Gui.build_upgrades()

    @staticmethod
    def game_over():
        for event in pg.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        Nebula.Flow.get_back_to_menu(Player.data_player[6])
                    elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                        Game.intro_loop()

    @staticmethod
    def paused(paused_gui):
        pressed_keys = pg.key.get_pressed()

        Controller.pause_chosen = False

        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            paused_gui.setting_mode = True
        
        elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            paused_gui.setting_mode = False
        
        elif pressed_keys[K_RETURN]:
            Controller.pause_chosen = True
            paused_gui.selected = True
            

    @staticmethod
    def choose_controller(cc_gui):
        pressed_keys = pg.key.get_pressed()

        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            cc_gui.setting_mode = True
        elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            cc_gui.setting_mode = False

class Collisions():
    """
    Uses sprite.spritecollide function call to determine collisions between
    entities on map. Different checks have different consequences. 
    """
    upgrade_collected   = False

    @staticmethod
    def check_all(player,gui,mining_reach):
        Collisions.player_fire(player)
        Collisions.collecting_upgrades(player,gui)
        Collisions.ammo_mining(mining_reach)
        Collisions.enemy_fire(player)
        Collisions.ua_entitiy_hit(player)
        Collisions.belt_collision(player)
        Collisions.enemy_hit(player)
        Collisions.shock_wave(player)
        Collisions.ai_fire(player)

    @staticmethod
    def player_fire(player):

        for shot in Sprites.shot_list:
            entity_hit_list             = pg.sprite.spritecollide(shot, Sprites.entity_list, True)
            enemy_hitting_list          = pg.sprite.spritecollide(shot, Sprites.enemy_list, False)
            belt_shots_list             = pg.sprite.spritecollide(shot, Sprites.asteroid_belt, False)
            ai_hit_list                 = pg.sprite.spritecollide(shot, Sprites.ai_list, False)
            for entity in entity_hit_list:
                Explosion.explode(shot.rect.x, shot.rect.y)
                shot.kill()
                Player.data_player[6]   += 1
            for enemy in enemy_hitting_list:
                enemy.health               -= Upgrades.shot_damage
                Explosion.explode(shot.rect.x, shot.rect.y)
                shot.kill()
                Player.data_player[6]   += 1
            for belt in belt_shots_list:
                Explosion.explode(shot.rect.x, shot.rect.y)
                shot.kill()
            
            for ai in ai_hit_list:
                ai.data_ai[5]              -= Upgrades.shot_damage
                if ai.data_ai[5]< 5:
                    Player.data_player[6]   += 500
                Explosion.explode(shot.rect.x, shot.rect.y)
                shot.kill()
                Player.data_player[6]   += 10
            

        if Weapon_Systems.rockets is True:
            hit = False 
            for rocket in Sprites.rockets_list:
                rocket_hit_list          = pg.sprite.spritecollide(rocket, Sprites.enemy_list, False)
                for hit_enemy in rocket_hit_list:
                    hit_enemy.health -=Upgrades.rocket_damage
                    rocket.kill()
                    hit = True
                if hit is True:
                    rocket.kill()
            hit = False

        if Weapon_Systems.flamethrower is True:

            for flame in Sprites.flame_thrower_list:
                flame_hit_list          = pg.sprite.spritecollide(flame, Sprites.enemy_list, False)
                for hit_enemy in flame_hit_list:
                    hit_enemy.health -=Upgrades.flame_damage
                    flame.kill()

    @staticmethod
    def belt_collision(player):

        belt_hit_list = pg.sprite.spritecollide(player, Sprites.asteroid_belt, True)

        for hit in belt_hit_list:
            Player.data_player[5]       -=    Level.entity_damage
            Explosion.explode(player.rect.center[0],player.rect.center[1])

        for ai in Sprites.ai_list:
            belt_collisions = pg.sprite.spritecollide(ai, Sprites.asteroid_belt, True)
            for belt_hit in belt_collisions:
                ai.data_ai[5]       -=    Level.entity_damage*8
                Explosion.explode(ai.rect.center[0],ai.rect.center[1])

    @staticmethod
    def collecting_upgrades(player,gui):

        upgrade_hit_list                = pg.sprite.spritecollide(player, Sprites.upgrade_list, True)
        for upgrade in upgrade_hit_list:
            if Upgrades.total_upgrades < Upgrades.maximum:
                if upgrade.image == Sprites.life:
                    Upgrades.health_store               += 20
                    Upgrades.level_healthstore          += 1
                    Upgrades.total_upgrades             += 1

                elif upgrade.image == Sprites.speed:
                    Upgrades.moving_speed               += 20
                    Upgrades.level_moving_speed         += 1
                    Upgrades.total_upgrades             += 1

                elif upgrade.image == Sprites.mining_speed:
                    Upgrades.mining_speed               += 1
                    Upgrades.level_mining_speed         += 1
                    Upgrades.total_upgrades             += 1

                elif upgrade.image == Sprites.regenerate_speed:
                    Upgrades.regeneration_speed         += 0.5
                    Upgrades.level_regeneration_speed   += 1
                    Upgrades.total_upgrades             += 1

                elif upgrade.image == Sprites.shooting_speed:
                    Upgrades.shooting_speed             += 40
                    Upgrades.level_shooting_speed       += 1
                    Upgrades.total_upgrades             += 1

                elif upgrade.image == Sprites.ammo_store:
                    Upgrades.ammo_store                 += 50
                    Upgrades.level_ammo_store           += 1
                    Upgrades.total_upgrades             += 1

                else:
                    pass

            else: 
                pass

            Collisions.upgrade_collected = True

    @staticmethod
    def ua_entitiy_hit(player):

        entity_hit_list     = pg.sprite.spritecollide(player, Sprites.entity_list, True)
        for entity in entity_hit_list:
            Player.data_player[6]       +=    1
            Player.data_player[5]       -=    Level.entity_damage
            if Player.data_player[5]    <= 0:
                Player.data_player[5]    = 0
            Explosion.explode(player.rect.center[0],player.rect.center[1])
            Controller.get_pushed((entity.x_speed, entity.y_speed))

        for ai in Sprites.ai_list:
            entity_hits_ai_list = pg.sprite.spritecollide(ai, Sprites.entity_list, True)

            for entity in entity_hits_ai_list:
                ai.data_ai[5] -=    Level.entity_damage
                Explosion.explode(ai.rect.center[0],ai.rect.center[1])
                ai.get_pushed((entity.x_speed, entity.y_speed))

    @staticmethod
    def ammo_mining(mining_reach):


        ammo_hit_list                   = pg.sprite.spritecollide(mining_reach,Sprites.ammo_list,False)
        for ammo in ammo_hit_list:
            if Player.data_player[7]    <  Upgrades.ammo_store:
                Player.data_player[7]   += Upgrades.mining_speed
                ammo.ammo_amount        -= Upgrades.mining_speed
                if ammo.ammo_amount     <=0:
                    ammo.kill()

    @staticmethod
    def mining_check(mining_reach):
        ammo_hit_list                   = pg.sprite.spritecollide(mining_reach,Sprites.ammo_list,False)
        if len(ammo_hit_list) > 0:
            return True

    @staticmethod
    def enemy_fire(player):
        enemy_hit_list                   =   pg.sprite.spritecollide(player,Sprites.enemy_shot_list,True)
        for hit in enemy_hit_list:
            Player.data_player[5]       -= Level.enemy_damage
            if Player.data_player[5]    <= 0:
                Player.data_player[5]    = 0
            Explosion.explode(player.rect.center[0],player.rect.center[1])

        for shot in Sprites.enemy_shot_list:
            entity_hit_list             =   pg.sprite.spritecollide(shot,Sprites.entity_list,True)
            for hit in entity_hit_list:
                Explosion.explode(shot.rect.x,shot.rect.y)

            ai_on_ai_list               =   pg.sprite.spritecollide(shot, Sprites.ai_list,False)
            for ai in ai_on_ai_list:
                ai.data_ai[5]           -=  Level.enemy_damage 
                Explosion.explode(shot.rect.x,shot.rect.y)

    @staticmethod
    def ai_fire(player):
        for shot in Sprites.ai_shot_list:
            entity_hit_list             =   pg.sprite.spritecollide(shot,Sprites.entity_list,True)
            for hit in entity_hit_list:
                Explosion.explode(shot.rect.x,shot.rect.y)

            enemy_hitting_list          = pg.sprite.spritecollide(shot, Sprites.enemy_list, False)
            for enemy in enemy_hitting_list:
                enemy.health               -= Upgrades.shot_damage
                Explosion.explode(shot.rect.x, shot.rect.y)
                shot.kill()
                Player.data_player[6]   += 1

            belt_shots_list             = pg.sprite.spritecollide(shot, Sprites.asteroid_belt, False)
            for belt in belt_shots_list:
                Explosion.explode(shot.rect.x, shot.rect.y)
                shot.kill()
            
        
        ai_hit_list                   =   pg.sprite.spritecollide(player,Sprites.ai_shot_list,True)
        for hit in ai_hit_list:
            Player.data_player[5]       -= Level.enemy_damage
            if Player.data_player[5]    <= 0:
                Player.data_player[5]    = 0
            Explosion.explode(player.rect.center[0],player.rect.center[1])

    @staticmethod
    def enemy_hit(player):
        enemy_hit_list     = pg.sprite.spritecollide(player, Sprites.enemy_list, False)
        for enemy in enemy_hit_list:
            Player.data_player[5]       -=  Level.entity_damage
            enemy.health                -=  Level.entity_damage
            if Player.data_player[5]    <= 0:
                Player.data_player[5]    = 0
            Explosion.explode(player.rect.center[0],player.rect.center[1])
            Controller.get_pushed((enemy.speed_x, enemy.speed_y))
        
        ai_player_hit      = pg.sprite.spritecollide(player, Sprites.ai_list, False)
        for ai in ai_player_hit:
            Player.data_player[5]       -=  int(Level.entity_damage/10)
            ai.data_ai[5]                -=  Level.entity_damage
            if Player.data_player[5]    <= 0:
                Player.data_player[5]    = 0
            Explosion.explode(player.rect.center[0],player.rect.center[1])
            Controller.get_pushed((int(ai.mover[0]/2),int(ai.mover[1]/2)))
        
        for ai in Sprites.ai_list:
            ai_on_enemy_list            = pg.sprite.spritecollide(ai, Sprites.enemy_list, False)

            for enemy in ai_on_enemy_list:
                ai.data_ai[5]       -=  Level.entity_damage
                Explosion.explode(ai.rect.center[0],ai.rect.center[1])
                ai.get_pushed((enemy.speed_x, enemy.speed_y))
            
            Sprites.ai_list.remove(ai)

            ai_on_ai_hit  = pg.sprite.spritecollide(ai, Sprites.ai_list, False)
            for ai_hit in ai_on_ai_hit:
                ai.data_ai[5]       -=  Level.entity_damage
                Explosion.explode(ai.rect.center[0],ai.rect.center[1])
                ai.get_pushed((ai_hit.mover[0],ai_hit.mover[1]))
            
            Sprites.ai_list.add(ai)
                   
    @staticmethod
    def ai_offmap():
        for ai in Sprites.ai_list:
            if ai.rect.x < 0 or ai.rect.x > Setup.map_size[0] or ai.rect.y < 0 or ai.rect.y > Setup.map_size[1]:
                ai.data_ai[5] -= Level.off_map_damage

    @staticmethod
    def off_map_check(player):
        if (player.rect.x - Setup.map_size[0]/2)**2 + (player.rect.y - Setup.map_size[1]/2)**2 > Asteroid_Belt.radius ** 2:
            return True

        if player.rect.x < 0 or player.rect.x > Setup.map_size[0]- player.width or player.rect.y < 0 or player.rect.y > Setup.map_size[1]-player.height:
            return True
        return False

    @staticmethod
    def off_map_damage():
        Player.data_player[5] -= Level.off_map_damage

    @staticmethod
    def locking_rocket_aim():

        for aimer in Sprites.rocket_aim:
            target_list = pg.sprite.spritecollide(aimer,Sprites.enemy_list,False)
            if len(target_list) > 0:
                Weapon_Systems.Plane.Rockets_Aim.locked = True
            else:
                Weapon_Systems.Plane.Rockets_Aim.locked = False
            return target_list

    @staticmethod
    def shock_wave(player):
        shock_wave_hit = pg.sprite.spritecollide(player,Sprites.shock_wave_list, False)

        for shock_wave in shock_wave_hit:
            Camera.Shock_Wave_Shake(Maths.get_shockwave_vector(player, shock_wave))
            Sprites.shock_wave_list.remove(shock_wave)

######### FLOW #########

class Game():
    """
    Class containing all the necessary loops for the game to run smoothly.
    Every new game is instanced and setup freshly.
    """
    start_game = False

    def __init__(self):
        pg.init()
        pg.display.set_caption('Nebula')    
        self.gui                 =   Gui()
        self.player              =   Player()
        self.mining_reach        =   Mining_Reach()
        self.rendering_window    =   Rendering_Window()
        self.counter = 2
        
        World.Overlay.elements_creator()

        #setup boarder with asteroid belt
        for asteroid in range(Asteroid_Belt.amount):
            Asteroid_Belt.Asteroid()

    def game_loop(self, genomes, config):
        """
        Core loop. Everything in the gameplay is calculated here.
        """
        AI.set_up_neural_network(genomes,config)

        while True:

            #how long did the last loop (clock.tick) take in seconds
            time_passed = Setup.clock.tick(Setup.FPS)
            time_passed_seconds = time_passed/1000 
            
            # make sure the space stays black and the astroid belt keeps existing
            Setup.screen.fill((0,0,0)) 
            Asteroid_Belt.load_belt()
            
            # make sure there is an acting ai in game
            if len(AI.opponents) == 0:
                AI.set_up_neural_network(genomes,config)
            AI.think()
            AI.handle(time_passed_seconds)

            # some slack for the weak players 
            Player.regenerate(time_passed_seconds)
            
            # handle some key inputs, could also sit in controller class 
            for event in pg.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pause_loop()
                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        Weapon_Systems.General.Gun.firing = True
                        Weapon_Systems.General.Gun.time_first_shot = pg.time.get_ticks()
                    if event.key == K_2:
                        Weapon_Systems.Earning_System.earned()
                    if event.key == K_p:
                        if Music.paused is False:
                            Music.pause_music()
                        else:
                            Music.unpause_music()
                    if event.key == K_RETURN:
                        Gui.Messages.skip()

                if event.type == KEYUP:
                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        Weapon_Systems.General.Gun.firing = False

            # make sure space exists
            World.render_map()

            #difference between moving sprite and static sprite
            move_check = Controller.movement(time_passed_seconds)
            if move_check is False:
                Player.render_sprite(Setup.screen,Sprites.rotate(Sprites.player_sprite_s,int(Player.data_player[4])),Player.data_player[1],Player.data_player[2])
            elif move_check is True:
                Player.render_sprite(Setup.screen,Sprites.rotate(Sprites.player_sprite_k,int(Player.data_player[4])),Player.data_player[1],Player.data_player[2])

            # let player take control
            Controller.turning()
            Controller.upgrade_gui()

            # manage shooting and overheating
            if Timer.running == False:
                if Player.data_player[7] > 0:
                    if Weapon_Systems.General.Gun.rof() == True:
                        Controller.shooting()
                    else:
                        timer = Timer()
                else:
                    pass
            else:
                self.gui.overheat()
                timer.check(Upgrades.gun_cool_down)

            # remind player that deep space is dangerous
            if Collisions.off_map_check(self.player) is True:
                self.gui.off_map()
                Collisions.off_map_damage()

            # display mining sign
            if Collisions.mining_check(self.mining_reach) is True:                
                self.gui.mining()
                self.gui.mining_angle += 5
                

            #checks done every other loop, mostly calculating stuff. Never use for bliting and drawing.
            if self.counter %2 == 0: 
                for move in Camera.moves:
                    move.move()


                if Collisions.upgrade_collected is True:
                    pass

                Collisions.check_all(self.player,self.gui,self.mining_reach)

                for e in Sprites.enemy_list:
                    e.look()

                if len(Sprites.enemy_list) < int(Level.enemies):
                    Enemy()

                if len(Sprites.entity_list) < Level.entities:
                    Entity()

                if Level.level_check(pg.time.get_ticks()) is True:
                    Level.level_update()

                if Music.check_if_playing() == False:
                    Music()

                if Player.health_check() == False:
                    self.game_over_loop()

            #checks done every tentht loop: uninportant side tasks
            if self.counter %10 == 0:
                
                Weapon_Systems.Earning_System.earn_secondary()

            ### draw and update all entities and gui ###

            # draw and update ai, needs to be seperately calculated, because ai can not be in all_entity list
            Sprites.ai_look_list.update(time_passed_seconds)
            Sprites.ai_list.update(time_passed_seconds)
            Sprites.ai_shot_list.update(time_passed_seconds)
            Sprites.ai_look_list.draw(World.game_surface)
            Sprites.ai_list.draw(World.game_surface)
            Sprites.ai_shot_list.draw(World.game_surface)

            #checks which sprites are actually in view
            render_list = pg.sprite.spritecollide(self.rendering_window, Sprites.all_sprites_list, False) 
            Sprites.render_list.add(render_list) #adds sprites to render into group
            Sprites.render_list.draw(World.game_surface) #group.draw is more efficient than blit every entity one by one
            Sprites.render_list.empty() #make main render list empty for next frame

            # move all entities on map, render all gui elements 
            Sprites.all_sprites_list.update(time_passed_seconds)
            self.gui.render()

            #display timed messages
            Gui.Messages.handle()

            # draw and update rocket aiming mechanics
            if Weapon_Systems.rockets is True:
                Collisions.locking_rocket_aim()
                Sprites.rocket_aim.update(time)

            pg.display.update()
            self.counter += 1

    def game_over_loop(self):
        """
        Freezes screen when player loses game.
        """
        Weapon_Systems.Earning_System.set_conditions()
        
        while True:
            self.gui.game_over()
            Controller.game_over()
            pg.display.update()

    @staticmethod
    def intro_loop():
        """
        Landing screen from main menu, player chooses prefered weapon system mode
        """

        through     = 0

        pg.init()
        pg.display.set_caption('Nebula')
        Game.reset_all()
        cc_gui = Gui.Choose_Controller()


        while True:

            Setup.screen.fill(Gui.black)
            time_passed = Setup.clock.tick(Setup.FPS)
            time_passed_seconds = time_passed/1000

            Controller.choose_controller(cc_gui)

            
            for event in pg.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        Nebula.Flow.get_back_to_menu()
                    elif event.key == K_RETURN:
                        Controller.setting_mode = cc_gui.setting_mode
                        if cc_gui.setting_mode is True:
                            Weapon_Systems.tank = True
                            Sprites.set_tank_sprite()
                        else:
                            Weapon_Systems.plane = True
                            Sprites.set_plane_sprite()

                        cc_gui.moving = True

            if Game.start_game is True:
                Game.start_game = False
                Game.new_game()


            if Stars.check_amount() is False:
                Stars()

            Stars.speed +=0.1
            Sprites.stars_list.draw(Setup.screen)
            Sprites.stars_list.update(time_passed_seconds)


            if through < 60:
                Player.render_sprite(Setup.screen,Sprites.rotate(Sprites.player_sprite_s,int(Player.data_player[4])),Player.data_player[1],Player.data_player[2])
            else:
                Player.render_sprite(Setup.screen,Sprites.rotate(Sprites.player_sprite_k,int(Player.data_player[4])),Player.data_player[1],Player.data_player[2])

            cc_gui.render()
            if cc_gui.moving is True:
                Music.end_music()
                cc_gui.move(time_passed_seconds)

            if cc_gui.off_screen() is True:
                Game.start_game = True

            pg.display.update()
            through +=1
            
    @staticmethod
    def reset_all():
        """ 
        Before each gameloop all settings need to 
        be reset. Otherwise difficulty would always increase 
        with each gamestart. Also, the world would overpopulate
        quickly. 
        """

        for ai in Sprites.ai_list:
            ai.kill()

        for ai_look in Sprites.ai_look_list:
            ai_look.kill()

        Upgrades.set_upgrades()
        Stars.speed             = 100
        Gui.Messages.set_all()
        Player.data_player[4]   = 0
        Player.data_player[5]   = 100
        Player.data_player[6]   = 0
        Player.data_player[7]   = 100
        Player.camera           = np.array([-1280,-720])
        Player.mover            = np.array([0,0])
        for entity in Sprites.all_sprites_list:
            entity.kill()
        Timer.running           = False
        Timer.set_game_start()
        Weapon_Systems.General.Gun.shot_count     = 0

        Weapon_Systems.Earning_System.set_conditions()

        Level.level_reset()

        # world reset #
        World.wallpaper               =   random.choice(["wallpaper_1.png","wallpaper_2_layer2.png"])
        World.parallax                =   pg.image.load(os.path.join(Paths.path_background,World.wallpaper)).convert()
        World.parallax                =   pg.transform.scale(World.parallax,(int(Setup.map_size[0]/2),int(Setup.map_size[1]/2)))

    @staticmethod
    def new_game():
        """
        Calls AI to load its genome, and run game with it. Is called from main.py
        """
        Game.reset_all()
        new_game                = Game()
        AI.replay_genome(Paths.path_config,Paths.path_genome,new_game)

    def pause_loop(self):
        """
        Game screen is overdrawn with pause screen. Player can leave game or shut off music
        """
        pause_gui       = Gui.Pause_Menu()
        continue_game   = False
        while True:
            Setup.screen.fill(Gui.black)
            time_passed = Setup.clock.tick(Setup.FPS)
            time_passed_seconds = time_passed/1000

            for event in pg.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quitting_loop()
                        continue_game = True
            
            if continue_game is True:
                break

            if Stars.check_amount() is False:
                Stars()

            Stars.speed +=0.1
            Sprites.stars_list.draw(Setup.screen)
            Sprites.stars_list.update(time_passed_seconds)

            Controller.paused(pause_gui)
            pause_gui.render()
            pg.display.update()

            if pause_gui.selected is True:
                pause_gui.move(time_passed_seconds)


            if pause_gui.off_screen() is True:
                if pause_gui.setting_mode is True:
                    pause_gui.selected = False
                    self.setting_loop()
                    pause_gui.setting_mode = False
                else:
                    pause_gui.selected = False
                    break

    def setting_loop(self):
        """
        Pause loop buddy. player can shut off music here
        """
        setting_gui   = Gui.Setting_Menu()

        while True:
            Setup.screen.fill(Gui.black)
            time_passed = Setup.clock.tick(Setup.FPS)
            time_passed_seconds = time_passed/1000

            for event in pg.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        break

            if Stars.check_amount() is False:
                Stars()

            Stars.speed +=0.1
            Sprites.stars_list.draw(Setup.screen)
            Sprites.stars_list.update(time_passed_seconds)

            Controller.paused(setting_gui)
            setting_gui.render()
            pg.display.update()

            if setting_gui.selected is True:
                setting_gui.move(time_passed_seconds)


            if setting_gui.off_screen() is True:
                if setting_gui.setting_mode is True:
                    setting_gui.selected = False
                    Music.unpause_music()
                    break
                else:
                    Music.pause_music()
                    break

    def quitting_loop(self):
        """
        Alert screen for accidental use of esc key. Gives player the oppurtunity to rethink
        his quitting desire.
        """
        quitting_gui   = Gui.Quitting_Menu()

        while True:
            Setup.screen.fill(Gui.black)
            time_passed = Setup.clock.tick(Setup.FPS)
            time_passed_seconds = time_passed/1000

            for event in pg.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        Nebula.Flow.get_back_to_menu(Player.data_player[6])

            if Stars.check_amount() is False:
                Stars()

            Stars.speed +=0.1
            Sprites.stars_list.draw(Setup.screen)
            Sprites.stars_list.update(time_passed_seconds)

            Controller.paused(quitting_gui)
            quitting_gui.render()
            pg.display.update()

            if quitting_gui.selected is True:
                quitting_gui.move(time_passed_seconds)


            if quitting_gui.off_screen() is True:
                if quitting_gui.setting_mode is True:
                    quitting_gui.selected = False
                    Nebula.Flow.get_back_to_menu(Player.data_player[6])
                else:
                    break


if __name__ == "__main__":
    Game.intro_loop() 