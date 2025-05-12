import pygame
from colors import Colors
import body
from camera import Camera
from level import Level
import copy
import random
import ui
import math
from enum import Enum
from configparser import ConfigParser
from resources import Resources
from functools import partial



# class Screen:
#     def __init__(self, game: Game):
#         self.state
#     def run(self):
#         while self.state == GameState.IN_SETTINGS:
#             self.window.fill(self.background_color)
#             self.handle_events(pygame.event.get())
#             for button in self.buttons:
#                 button.tick()
#                 button.draw(self.window)


#             pygame.display.flip()
#             self.clock.tick(self.target_fps)   



class Game:
    def __init__(self) -> None:
        pygame.init()


        # Settings
        self.background_color: tuple[int, int, int] = Colors.black
        self.background = body.Sprite(Resources.background_image)
        self.background.centered = False

        self.screen_width: int = 1280
        self.screen_height: int = 720

        self.target_fps: int = 60
        # Implement vSync later, supported by pygame

        self.window: pygame.Surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.fullscreen = False
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.state: GameState
        self.config = ConfigParser() 
        self.levels = ["test", "level_1", "level_2", "level_3", "level_4", "level_5", "level_6"]
        self.current_level = 0

    def get_unit_vector(pos1: tuple[float, float], pos2: tuple[float, float]) -> tuple[float, float]:
        angle = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
        return (math.cos(angle), math.sin(angle))
    
    def get_vector(pos1: tuple[float, float], pos2: tuple[float, float]) -> tuple[float, float]:
        return (pos2[0]-pos1[0]), (pos2[1]-pos1[1])

    def start(self) -> None:
        self.state = GameState.IN_MENU
        while self.state != GameState.QUITTING:
            self.call_next()

    def play_button_clicked(self) -> None:
        self.state = GameState.LEVEL_SELECT

    def level_button_clicked(self, level) -> None:
        self.state = GameState.PLAYING
        self.current_level = level

    def quit_button_clicked(self) -> None:
        self.state = GameState.QUITTING

    def settings_button_clicked(self) -> None:
        self.state = GameState.IN_SETTINGS

    def how_to_play_button_clicked(self) -> None:
        self.state = GameState.IN_HOW_TO_PLAY

    def editor_button_clicked(self) -> None:
        self.state = GameState.IN_EDITOR

    def back_to_menu_button_cliked(self) -> None:
        self.state = GameState.IN_MENU

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((self.screen_width, self.screen_height))

    def call_next(self) -> None:
        if self.state == GameState.QUITTING:
            self.quit()
        elif self.state == GameState.IN_MENU:
            self.main_menu()
        elif self.state == GameState.IN_SETTINGS:
            self.settings()
        elif self.state == GameState.IN_HOW_TO_PLAY:
            self.how_to_play()
        elif self.state == GameState.PLAYING:
            self.play()
        elif self.state == GameState.IN_EDITOR:
            self.editor()
        elif self.state == GameState.LEVEL_SELECT:
            self.level_select()
        else:
            print("Holy [CL]ap louis")
            self.state = GameState.QUITTING
            self.quit()

    def save_level(self, level_name: str) -> None:
        config = ConfigParser()
        saved_level_data = self.level.to_str("|", ":")
        config[level_name] = {}
        config[level_name]['data'] = saved_level_data
        with open(f'levels/{level_name}'+'.ini', 'w') as configfile:
            config.write(configfile)

    # def draw_prediction(self, num_ticks, tickrate):
    #     predictionsRealCoords = self.predict_pos(num_ticks, tickrate)
    #     predictions = [(self.x/scale+camera_x, self.y/scale+camera_y)]
    #     for p in predictionsRealCoords:
    #         predictions.append((p[0]/scale+camera_x, p[1]/scale+camera_y))
    #     if len(predictions) > 1:
    #         pygame.draw.lines(window, self.color, False, predictions)

    def mouse_over_ui(self):
        for button in self.buttons:
            if button.mouse_over():
                return True
        return False

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            # Universal Keybinds - Do the same thing no matter what gamestate is
            if event.type == pygame.QUIT:
                self.state = GameState.QUITTING
                return
            


            
            # Specific Keybinds

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.IN_MENU:
                        self.state = GameState.QUITTING
                        return
                    
                    if self.state == GameState.PLAYING:
                        self.state = GameState.IN_MENU
                        print("Krill")

                if event.key == pygame.K_1:
                    if self.state == GameState.IN_EDITOR:
                        self.selected = Selection.DELETE
                
                if event.key == pygame.K_2:
                    if self.state == GameState.IN_EDITOR:
                        self.selected = Selection.EDIT

                if event.key == pygame.K_3:
                    if self.state == GameState.IN_EDITOR:
                        self.selected = Selection.PLAYER

                if event.key == pygame.K_4:
                    if self.state == GameState.IN_EDITOR:
                        self.selected = Selection.TARGET
                
                if event.key == pygame.K_5:
                    if self.state == GameState.IN_EDITOR:
                        self.selected = Selection.PLANET
                
                if event.key == pygame.K_6:
                    if self.state == GameState.IN_EDITOR:
                        self.selected = Selection.STAR

                if event.key == pygame.K_r:
                    if self.state == GameState.PLAYING:
                        self.load_level(self.levels[self.current_level])
                        print("ligk")


                
                # if event.key == pygame.K_s:
                #     if self.state == GameState.IN_EDITOR:
                #         self.save_level("temp")

                # if event.key == pygame.K_l:
                #     if self.state == GameState.IN_EDITOR:
                #         self.load_level("temp")
            


            if event.type == pygame.MOUSEWHEEL and (self.state == GameState.PLAYING or self.state == GameState.IN_EDITOR):
                x, y = self.camera.get_screen_pos(pygame.mouse.get_pos())
                scale = self.camera.scale
                mult = -event.y/20
                scale *= 1-mult
                if scale <= 0.1:
                    scale = 0.1
                else:
                    self.camera.set_scale(scale)
                    self.camera.x -= x*mult/scale
                    self.camera.y -= y*mult/scale

            if event.type == pygame.MOUSEBUTTONDOWN and not self.mouse_over_ui():
                if event.button == 1:
                    if self.state == GameState.PLAYING:
                        if not self.player.launched:
                            mouse_pos = pygame.mouse.get_pos()
                            player_pos = self.camera.get_pos((self.player.x, self.player.y))
                            player_radius = self.player.radius/self.camera.scale
                            buffer = 5 # Amount the mouse can be off and still activate
                            if Game.calc_distance(mouse_pos, player_pos) <= player_radius + buffer:
                                self.launching_player = True
                                self.launch_pos_initial = self.camera.get_screen_pos(mouse_pos)
                                print("You click da player")

                    if self.state == GameState.IN_EDITOR:
                        if self.selected == Selection.DELETE:
                            x, y = self.camera.get_screen_pos(pygame.mouse.get_pos())
                            for object in self.level.objects:
                                buffer = 2
                                if Game.calc_distance((x, y), (object.x, object.y)) < object.radius + buffer:
                                    self.level.remove_object(object)

                        if self.selected == Selection.PLAYER:
                            object: body.Player = body.Player()
                            object.x, object.y = self.camera.get_screen_pos(pygame.mouse.get_pos())
                            self.level.add_object(object)
                        
                        if self.selected == Selection.TARGET:
                            object: body.Target = body.Target()
                            object.x, object.y = self.camera.get_screen_pos(pygame.mouse.get_pos())
                            self.level.add_object(object)

                        if self.selected == Selection.PLANET:
                            object: body.Planet = body.Planet()
                            object.x, object.y = self.camera.get_screen_pos(pygame.mouse.get_pos())
                            self.level.add_object(object)

                        if self.selected == Selection.STAR:
                            object: body.Star = body.Star()
                            object.x, object.y = self.camera.get_screen_pos(pygame.mouse.get_pos())
                            self.level.add_object(object)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.state == GameState.PLAYING:
                        if self.launching_player:
                            self.launch_pos_final = self.camera.get_screen_pos(pygame.mouse.get_pos())
                            vector = Game.get_vector(self.launch_pos_final, self.launch_pos_initial)
                            self.player.xvel = vector[0]/10
                            self.player.yvel = vector[1]/10

                            print("You release da player")
                            self.launching_player = False
                            self.player.launched = True

    def main_menu(self) -> None:
        self.buttons = []
        button_x = self.screen_width/25
        button_spacing = self.screen_height/10
        button_width = self.screen_width/5
        button_height = self.screen_height/10
        play_button =        ui.Button(button_x, button_spacing*1, button_width, button_height, "PLAY",        self.play_button_clicked)
        editor_button =      ui.Button(button_x, button_spacing*2, button_width, button_height, "EDITOR",      self.editor_button_clicked)
        settings_button =    ui.Button(button_x, button_spacing*3, button_width, button_height, "SETTINGS",    self.settings_button_clicked)
        how_to_play_button = ui.Button(button_x, button_spacing*4, button_width, button_height, "HOW TO PLAY", self.how_to_play_button_clicked)
        quit_button =        ui.Button(button_x, button_spacing*5, button_width, button_height, "QUIT",        self.quit_button_clicked)
        
        play_button.set_theme(Colors.dark_blue)
        
        self.buttons.append(play_button)
        self.buttons.append(editor_button)
        self.buttons.append(settings_button)
        self.buttons.append(how_to_play_button)
        self.buttons.append(quit_button)
        while self.state == GameState.IN_MENU:
            self.window.fill(self.background_color)
            self.background.set_size(self.window.get_size()[0], self.window.get_size()[1])
            self.background.draw(self.window)

            self.handle_events(pygame.event.get())

            for button in self.buttons:
                button.tick()

            for button in self.buttons:
                button.draw(self.window)
                
            pygame.display.flip()
            self.clock.tick(self.target_fps)   

    def settings(self) -> None:
        self.buttons = []
        button_x = self.screen_width/25
        button_spacing = self.screen_height/10
        button_width = self.screen_width/5
        button_height = self.screen_height/10
        fullscreen_button = ui.Button(button_x, button_spacing*1, button_width, button_height, "TOGGLE FULLSCREEN", self.toggle_fullscreen)

        back_to_menu_button = ui.Button(button_x, button_spacing*2, button_width, button_height, "BACK TO MENU", self.back_to_menu_button_cliked)
        self.buttons.append(fullscreen_button)
        self.buttons.append(back_to_menu_button)
        while self.state == GameState.IN_SETTINGS:
            self.window.fill(self.background_color)
            self.background.set_size(self.window.get_size()[0], self.window.get_size()[1])
            self.background.draw(self.window)
            self.handle_events(pygame.event.get())
            for button in self.buttons:
                button.tick()
                button.draw(self.window)


            pygame.display.flip()
            self.clock.tick(self.target_fps)   

    def editor(self) -> None:
        self.camera: Camera = Camera(self.window)
        self.selected: Selection = None
        self.level: Level = Level()
        self.level.name = "level"
        self.buttons = []
        button_x = self.screen_width/250
        button_spacing = self.screen_height/10
        button_width = self.screen_width/5
        button_height = self.screen_height/10

        back_to_menu_button = ui.Button(button_x, button_spacing*1, button_width, button_height, "BACK TO MENU", self.back_to_menu_button_cliked)
        save_box = ui.TextBox(button_x, button_spacing*2, button_width, button_height, self.save_level)
        load_box = ui.TextBox(button_x, button_spacing*3, button_width, button_height, self.load_level)

        delete_button = ui.Button(button_x+button_width*0, self.screen_height-button_height, button_width, button_height, "DELETE")
        edit_button =   ui.Button(button_x+button_width*1, self.screen_height-button_height, button_width, button_height, "EDIT")
        player_button = ui.Button(button_x+button_width*2, self.screen_height-button_height, button_width, button_height, "PLAYER")
        target_button = ui.Button(button_x+button_width*3, self.screen_height-button_height, button_width, button_height, "TARGET")
        planet_button = ui.Button(button_x+button_width*4, self.screen_height-button_height, button_width, button_height, "PLANET")


        self.buttons.append(back_to_menu_button)
        self.buttons.append(save_box)
        self.buttons.append(load_box)
        self.buttons.append(delete_button)
        self.buttons.append(edit_button)
        self.buttons.append(player_button)
        self.buttons.append(target_button)
        self.buttons.append(planet_button)

        while self.state == GameState.IN_EDITOR:
            self.window.fill(self.background_color)
            self.background.set_size(self.window.get_size()[0], self.window.get_size()[1])
            self.background.draw(self.window)
            self.events = pygame.event.get()
            self.handle_events(self.events)

            for object in self.level.objects:
                object.draw(self.camera)

            for button in self.buttons:
                button.events = self.events
                button.tick()

            for button in self.buttons:
                button.draw(self.window)
                
            pygame.display.flip()
            self.clock.tick(self.target_fps)   

    def quit(self) -> None:
        pygame.quit()

    def pause_menu(self) -> None:
        pass

    def calc_distance(point1: tuple, point2: tuple) -> float:
        return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    
    def level_select(self) -> None:
        self.buttons = []
        button_x = 0
        button_y = 0
        button_spacing_y = self.screen_height/10
        button_spacing_x = self.screen_width/5
        button_width = self.screen_width/5
        button_height = self.screen_height/10
        level_count = 0
        for level_name in self.levels:
            level_button = ui.Button(button_x, button_y, button_width, button_height, level_name, partial(self.level_button_clicked, level_count))
            self.buttons.append(level_button)
            level_count += 1
            button_y += button_spacing_y
            if button_y > self.screen_height-button_height:
                button_y = 0
                button_x += button_spacing_x

        while self.state == GameState.LEVEL_SELECT:
            self.window.fill(self.background_color)
            self.background.set_size(self.window.get_size()[0], self.window.get_size()[1])
            self.background.draw(self.window)
            self.events = pygame.event.get()
            self.handle_events(self.events)

            for button in self.buttons:
                button.tick()

            for button in self.buttons:
                button.draw(self.window)
                
            pygame.display.flip()
            self.clock.tick(self.target_fps)   


    def pause_menu(self) -> None:
        self.buttons = []


    def play(self) -> None:

        # Create Objects - Placeholder
        self.objects: list[body.GameObject] = []
        self.launching_player = False
        self.buttons = []
        self.background = body.Sprite(Resources.background_image)
        self.background.centered = False
        self.camera: Camera = Camera(self.window)
        self.load_level(self.levels[self.current_level])


        

        while self.state == GameState.PLAYING:
            self.window.fill(self.background_color)
            self.background.set_size(self.window.get_size()[0], self.window.get_size()[1])
            self.background.draw(self.window)
            # Get User Input
            self.handle_events(pygame.event.get())


            # Tick game logic
            self.tick(1/self.target_fps)


            # Draw game
            self.draw()

            pygame.display.flip()

            self.clock.tick(self.target_fps)

    def all_pair(objects: list, func) -> None: #Calls function with all pairs of data set
        for i in range(len(objects)):
            obj1 = objects[i]
            for j in range(i+1, len(objects)):
                obj2 = objects[j]
                func(obj1, obj2)

    def tick(self, dt: float) -> None:
        bodies = [object for object in self.objects if isinstance(object, body.Body)]
        Game.all_pair(bodies, body.Body.apply_collision)
        Game.all_pair(bodies, body.Body.apply_gravity)

        for object in self.objects:
            object.tick(dt)
        for player in [obj for obj in self.objects if type(obj) == body.Player]:
            if player.reached_target:
                self.current_level += 1
                self.load_level(self.levels[self.current_level])
                Resources.win_sfx.play()

            

    def draw(self) -> None:
        for object in self.objects:
            object.draw(self.camera)

 #   def get_level(self, level: Level) -> None:
 #       self.objects = copy.deepcopy(level.objects)
 #       self.camera.set_scale(self.screen_height/level.size)


    def load_level(self, level_name: str) -> None:
        config = ConfigParser()
        file_name = f'levels/{level_name}.ini'
        config.read(file_name)
        saved_level_data = config.get((level_name), ('data'))
        self.level = Level.from_str(saved_level_data, "|", ":")
        self.level.name = level_name
        self.level.size = self.level.calc_size()
        self.camera.set_scale(self.level.size/self.screen_height)
        #self.objects = copy.deepcopy(self.level.objects)
        self.objects = self.level.objects
        for object in self.objects:
            if type(object) == body.Player:
                self.player = object
            # if type(object) == body.Planet:
            #     object.make_sprite(Resources.planet_default_image)
        #self.get_level(self.level)

class GameState(Enum):
    QUITTING = 0
    PLAYING = 1
    IN_MENU = 2
    IN_SETTINGS = 3
    IN_EDITOR = 4
    IN_HOW_TO_PLAY = 5
    LEVEL_SELECT = 6
    PAUSE_MENU = 7

class Selection(Enum):
    DELETE = 0
    EDIT = 1
    PLAYER = 2
    TARGET = 3
    PLANET = 4
    STAR = 5

def main() -> None:
    game = Game()
    game.start()

if __name__ == "__main__":
    main()