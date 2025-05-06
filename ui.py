import pygame
import math
from colors import Colors
pygame.init()

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, onclick=None, image_file: pygame.surface.Surface=None) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.border_width: int = int(min(self.width, self.height)/15)
        self.color: tuple[int, int, int] = (64, 64, 64)
        self.border_mult: float = 2
        self.highlight_mult: float = 1.25
        self.clicked_mult: float = 1.5
        self.text: str = text
        self.set_theme(self.color)
        if self.text:
            # self.text_color = Colors.set_luminosity(self.color, 255)
            # self.text_size = round(width/len(text)*2.5)
            # self.font_name = 'Cascadia Code'
            # self.font = pygame.font.SysFont(self.font_name, self.text_size)
            # self.disp_text = self.font.render(self.text, True, self.text_color)
            self.font_name = 'Cascadia Code'
            self.set_text(self.text)
        # self.border_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)*self.border_mult)
        # self.highlight_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)*self.highlight_mult)
        # self.clicked_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)*self.clicked_mult)
        
        self.being_clicked: bool = False
        self.enabled: bool = True
        self.moving: bool = False
        self.movable: bool = False
        self.fancy: bool = True
        self.onclick = onclick
        self.source_image: pygame.surface.Surface = image_file
        self.image: pygame.surface.Surface = None
        if self.source_image:

            self.update_image()

    def update_image(self) -> None:
        if self.width != self.image.get_width() or self.height != self.image.get_height:
            self.image = pygame.transform.smoothscale(self.source_image, (round(self.width), round(self.height)))

    def set_text(self, text: str) -> None:
        self.text = text
        self.rect = pygame.Rect(self.x+min(self.width, self.height)/20, self.y+min(self.width, self.height)/20, self.width-min(self.width, self.height)/10, self.height-min(self.width, self.height)/10)
        if self.text:
            self.text_size = int(min(self.width/len(self.text), self.height)*2)
            self.font = pygame.font.SysFont(self.font_name, self.text_size)
            self.disp_text = self.font.render(self.text, True, self.text_color)

    def set_pos(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def set_dimensions(self, rect: tuple[int, int, int, int]) -> None:
        x, y, width, height = rect
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.border_width = int(min(self.width, self.height)/25+1)
        
    def draw(self, surface: pygame.Surface) -> None:
        if self.enabled:
            if self.image:
                surface.blit(self.image, (self.x, self.y))
                return
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if self.being_clicked:
                pygame.draw.rect(surface, self.clicked_color, self.rect)
            elif self.mouse_over():
                pygame.draw.rect(surface, self.highlight_color, self.rect)
            else:
                pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
            if self.text:
                #surface.blit(self.disp_text, (self.rect[0], self.rect[1]))
                text_rect = self.disp_text.get_rect(center=(self.x+self.width/2, self.y+self.height/2))
                surface.blit(self.disp_text, text_rect)
            
    def update(self) -> None:
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.movable and pygame.mouse.get_pressed()[2] and self.mouse_over():
            if self.moving:
                self.x += mouse_x-self.last_mouse_x
                self.y += mouse_y-self.last_mouse_y
            else:
                self.moving = True
                self.x += mouse_x-self.last_mouse_x
                self.y += mouse_y-self.last_mouse_y
                
        else:
            if self.moving and pygame.mouse.get_pressed()[2]:
                self.x += mouse_x-self.last_mouse_x
                self.y += mouse_y-self.last_mouse_y
            else:
                self.moving = False
        self.last_mouse_x, self.last_mouse_y = pygame.mouse.get_pos()

    def tick(self):
        self.update()
        if pygame.mouse.get_pressed()[0] and self.mouse_over() and self.enabled:
            if not self.being_clicked:
                self.being_clicked = True
                self.rect = pygame.Rect(self.x+min(self.width, self.height)/20, self.y+min(self.width, self.height)/20, self.width-min(self.width, self.height)/10, self.height-min(self.width, self.height)/10)
                if self.text:
                    self.text_size = int(min(self.width/len(self.text), self.height)*2)
                    self.disp_text = self.font.render(self.text, True, self.text_color)
                return False
        else:
            if self.being_clicked == True:
                self.being_clicked = False
                self.update()
                if self.text:
                    self.text_size = int(min(self.width/len(self.text), self.height)*2)
                    self.disp_text = self.font.render(self.text, True, self.text_color)
                is_clicked = self.mouse_over()
                if is_clicked and self.onclick:
                    self.onclick()
                return is_clicked
            
            return False


    def mouse_over(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def set_theme(self, color: tuple[int, int, int]) -> None:

        self.color = color
        if Colors.get_luminosity(self.color) <= 128: # If background color is dark, make other things such as text color brighter (for contrast)
            self.border_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)*self.border_mult)
            self.highlight_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)*self.highlight_mult)
            self.clicked_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)*self.clicked_mult)
            self.text_color = Colors.set_luminosity(self.color, 255)
        else: # Otherwise make other things dark
            self.border_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)/self.border_mult)
            self.highlight_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)/self.highlight_mult)
            self.clicked_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)/self.clicked_mult)
            self.text_color = Colors.set_luminosity(self.color, Colors.get_luminosity(self.color)/self.clicked_mult/3)
        self.text_size = int(min(self.width/len(self.text), self.height)*2)
        self.font = pygame.font.SysFont('Cascadia Code', self.text_size)
        self.disp_text = self.font.render(self.text, True, self.text_color)

        # if theme == "blue":
        #     self.color = (32, 42, 98)
        #     self.border_color = (48, 64, 164)
        #     self.text_color = (96, 96, 255)

        # if theme == "red":
        #     self.color = (128, 32, 32)
        #     self.border_color = (196, 48, 48)
        #     self.text_color = (255, 64, 64)

class TextBox:
    def __init__(self, x, y, width, height, onclick = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = ''
        self.active_color = (64, 64, 64)
        self.inactive_color = (32, 32, 32)
        self.border_color = (128, 128, 128)
        self.text_color = (192, 192, 192)
        self.color = self.inactive_color
        self.active = False
        self.events = None
        self.text_size = 25
        self.font = pygame.font.SysFont('Cascadia Code', self.text_size)
        self.disp_text = self.font.render(self.text, True, self.text_color)
        self.onclick = onclick

    def draw(self, surface):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, round(min(self.width, self.height)/25))
        surface.blit(self.disp_text, (self.rect[0], self.rect[1]))
        
    def mouse_over(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def tick(self):
        done = False
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_over():
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.active_color if self.active else self.inactive_color
            if self.active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.ret_text = self.text
                        self.text = ''
                        self.disp_text = self.font.render(self.text, True, self.text_color)
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                        self.disp_text = self.font.render(self.text, True, self.text_color)
                    else:
                        self.text += event.unicode
                        self.disp_text = self.font.render(self.text, True, self.text_color)
        if done and self.onclick:
            self.onclick(self.ret_text)
        return done

class Menu:
    def __init__(self, x, y, width, height, columns, rows):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rows = rows
        self.columns = columns
        self.buttons = []
        self.color = (64, 64, 64)
        self.border_color = (128, 128, 128)
        self.enabled = True
        
    def add_button(self, button: Button):
        if len(self.buttons) > self.columns*self.rows:
            return
        button.width = self.width/self.columns *.8
        button.height = self.height/self.rows *.8
        button_column = len(self.buttons)%self.columns
        button_row = len(self.buttons)//self.columns
        button.x = self.x + self.width*(button_column/self.columns) + button.width/10
        button.y = self.y + self.height*(button_row/self.rows) + button.height/10
        
        button.rect = pygame.Rect(button.x, button.y, button.width, button.height)
        if button.text:
            button.text_size = round(button.width/len(button.text)*2.5)
            button.font = pygame.font.SysFont('Cascadia Code', button.text_size)
            button.disp_text = button.font.render(button.text, True, button.text_color)
        button.update_image()
        self.buttons.append(button)

    def draw(self, surface):
        if self.enabled:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, self.border_color, self.rect, round(min(self.width, self.height)/25))

            for button in self.buttons:
                button.draw(surface)

    def mouse_over(self):
        self.rect.collidepoint(pygame.mouse.get_pos())

    def tick(self):
        if self.enabled:
            for button in self.buttons:
                button.get_clicked()
    
class Slider:
    def __init__(self, x, y, width, height, value_range, step_amount, text, slider_pos, onclick=None, logarithmic = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.minimum, self.maximum = value_range
        self.step_amount = step_amount
        self.steps = int(abs((self.maximum-self.minimum)/self.step_amount))
        self.text = text
        self.slider_pos = self.width*((slider_pos-self.minimum)/(self.maximum-self.minimum))
        self.color = (64, 64, 64)
        self.border_color = (96, 96, 96)
        self.text_color = (0, 255, 0)
        self.slider_color = (96, 96, 96)
        self.slider_highlighted_color = Colors.set_luminosity(self.slider_color, Colors.get_luminosity(self.slider_color)*1.25)
        self.slide_color = (112, 112, 112)
        self.slide_color_dark = (164, 164, 164)
        self.enabled = True
        self.being_clicked = False
        self.text_size = int(self.height/3)
        self.font = pygame.font.SysFont('Times New Roman', self.text_size)
        self.text2 = str(self.get_value())
        self.slider_size = min(self.width, self.height)/5
        self.moving = False
        self.disp_text = self.font.render(self.text, False, self.text_color)
        self.disp_text2 = self.font.render(self.text2, False, self.text_color)
        self.fancy = False
        self.shine_color = (255, 255, 255)
        self.slider_outline_color = (32, 32, 32)
        self.onclick = onclick
        self.events = None
        self.being_dragged = False
        self.logarithmic = logarithmic

        
    def draw(self, surface):
        if self.enabled:
            pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, self.border_color, self.rect, int(min(self.width, self.height)/25))
            pygame.draw.line(surface, self.slide_color, (self.x,self.y+self.height/2), (self.x+self.slider_pos,self.y+self.height/2), width = round(min(self.width, self.height)/10))
            pygame.draw.line(surface, self.slide_color_dark, (self.x+self.slider_pos,self.y+self.height/2), (self.x+self.width,self.y+self.height/2), width = round(min(self.width, self.height)/10))
            surface.blit(self.disp_text, (self.x, self.y))
            surface.blit(self.disp_text2, (self.x, self.y+self.height/3*2))
            self.steps = int(abs((self.maximum-self.minimum)/self.step_amount))
            if self.steps < self.width/3:
                for i in range(self.steps):

                    pygame.draw.line(surface, self.slide_color, (self.x+self.width/self.steps*i, self.y+self.height/2.5), (self.x+self.width/self.steps*i, self.y+self.height-self.height/2.5))

            pygame.gfxdraw.filled_circle(surface, round(self.x+self.slider_pos), round(self.y+self.height/2), round(self.slider_size), self.slider_highlighted_color if self.mouse_on_slide() else self.slider_color)
            pygame.gfxdraw.aacircle(surface, round(self.x+self.slider_pos), round(self.y+self.height/2), round(self.slider_size), self.slider_outline_color)
            pygame.draw.circle(surface, self.shine_color, (round(self.x+self.slider_pos), round(self.y+self.height/2)), round(self.slider_size*0.8), round(self.slider_size/5), draw_top_right=True)
            

    def mouse_over(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def mouse_on_slide(self):
        x, y = pygame.mouse.get_pos()
        if x >= self.x and x <= self.x+self.width and self.enabled:
            return y >= self.y+self.height/4 and y <= self.y+self.height-self.height/4
        return False

    def get_pos_of_nearest_step(self, steps):
        return self.slider_pos+(self.width/steps/2)-((self.slider_pos+(self.width/steps/2))%(self.width/steps))

    def set_fancy(self, fancy):
        self.text2 = str(self.get_value())
        self.fancy = fancy
        self.update_fancy()
            
    def update_fancy(self):
        if self.fancy:
            self.disp_text = self.font.render(self.text, True, self.text_color)
            self.disp_text2 = self.font.render(self.text2, True, self.text_color)
        else:
            self.disp_text = self.font.render(self.text, False, self.text_color)
            self.disp_text2 = self.font.render(self.text2, False, self.text_color)

    def set_theme(self, theme):

        if theme == "blue":
            self.slider_color = (32, 42, 98)
            self.slider_outline_color = (48, 64, 164)
            self.color = (32, 42, 98)
            self.border_color = (48, 64, 164)
            self.slide_color = (64, 84, 196)
            self.slide_color_dark = (64, 86, 164)
            self.text_color = (96, 96, 255)

        if theme == "red":
            self.slider_color = (196, 48, 48)
            self.slider_outline_color = (164, 28, 28)
            self.color = (128, 32, 32)
            self.border_color = (196, 48, 48)
            self.slide_color = (225, 64, 64)
            self.slide_color_dark = (196, 64, 64)
            self.shine_color = (255, 225, 225)
            self.text_color = (255, 64, 64)

        self.slider_highlighted_color = Colors.set_luminosity(self.slider_color, Colors.get_luminosity(self.slider_color)*1.25)

    def handle_events(self, events):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.enabled:
                if self.mouse_on_slide():
                    self.being_clicked = True
                else:
                    if self.mouse_over():
                        self.being_dragged = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.being_clicked = False
                self.being_dragged = False

        if self.enabled:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.being_clicked:
                self.slider_pos = mouse_x-self.x
                if self.slider_pos < 0:
                    self.slider_pos = 0
                if self.slider_pos > self.width:
                    self.slider_pos = self.width
                self.steps = int(abs((self.maximum-self.minimum)/self.step_amount))
                self.slider_pos = self.get_pos_of_nearest_step(self.steps)
                self.slider_size = min(self.width, self.height)/5
                if self.onclick:
                    self.onclick()
            
            else:
                self.slider_size = min(self.width, self.height)/6

            if self.being_dragged:
                
                self.x += mouse_x-self.last_mouse_x
                self.y += mouse_y-self.last_mouse_y

            self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y


    
    def tick(self, events):
        self.handle_events(events)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.text2 != str(self.get_value()):
            self.text2 = str(self.get_value())
            self.disp_text2 = self.font.render(self.text2, False, self.text_color)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[2] and self.mouse_over():
            if self.moving:
                self.x += mouse_x-self.last_mouse_x
                self.y += mouse_y-self.last_mouse_y
            else:
                self.moving = True
                self.x += mouse_x-self.last_mouse_x
                self.y += mouse_y-self.last_mouse_y
                
        else:
            if self.moving and pygame.mouse.get_pressed()[2]:
                self.x += mouse_x-self.last_mouse_x
                self.y += mouse_y-self.last_mouse_y
            else:
                self.moving = False
        self.last_mouse_x, self.last_mouse_y = pygame.mouse.get_pos()
                
            

    def get_value(self):
        val = round(self.minimum+(self.slider_pos/self.width)*(self.maximum-self.minimum), 12)

        if val == int(val):
            return int(val)
        
        return val

    def set_value(self, value):
        self.slider_pos = self.width*(value-self.minimum)/(self.maximum-self.minimum)