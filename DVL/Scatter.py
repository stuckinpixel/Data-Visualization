
import pygame, sys, time, random, json
from pygame.locals import *

pygame.font.init()
font = pygame.font.SysFont('Calibri', 23)


class Scatter:
    def __init__(self, x=[], y=[]):
        self.x = x
        self.y = y
        self.surface = None
        self.play = True
        self.mouse=None
        self.click=None
        self.color = {
            "background": (255, 255, 255),
            "alpha": (30, 210, 180),
            "primary": (30, 50, 40)
        }
        self.fps=64
        self.ft=None
        self.MIN_WIDTH = 400
        self.MIN_HEIGHT = 450
        self.WIDTH, self.HEIGHT = 400, 450
        self.margin_offset = 50
        self.bottom_offset = 50
        self.margin_bar_lengths = 10
        self.margin_bar_counts = 10
        self.offset_unit = 5
        self.min_x = min(self.x)-self.offset_unit
        self.max_x = max(self.x)+self.offset_unit
        self.min_y = min(self.y)-self.offset_unit
        self.max_y = max(self.y)+self.offset_unit
        self.pool_width_value = self.max_x-self.min_x
        self.pool_height_value = self.max_y-self.min_y
        self.plot_point_radius = 3
    def plot(self):
        pygame.init()
        self.surface=pygame.display.set_mode((self.WIDTH, self.HEIGHT),pygame.RESIZABLE,32)
        self.ft=pygame.time.Clock()
        pygame.display.set_caption("Scatter")
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.run()
    def update_window_size(self):
        self.WIDTH, self.HEIGHT = pygame.display.get_surface().get_size()
        width_to_resize, height_to_resize = self.WIDTH, self.HEIGHT
        can_we_resize = False
        if self.WIDTH<self.MIN_WIDTH:
            width_to_resize = self.MIN_WIDTH
            can_we_resize = True
        if self.HEIGHT<self.MIN_HEIGHT:
            height_to_resize = self.MIN_HEIGHT
            can_we_resize = True
        if can_we_resize:
            self.surface=pygame.display.set_mode((width_to_resize, height_to_resize),pygame.RESIZABLE,32)
    def render(self):
        x1, y1 = self.margin_offset, self.margin_offset
        x2, y2 = self.margin_offset, self.HEIGHT-self.margin_offset-self.bottom_offset
        x3, y3 = self.WIDTH-self.margin_offset, self.HEIGHT-self.margin_offset-self.bottom_offset
        # draw margin left
        pygame.draw.line(self.surface, self.color["primary"], (x1, y1), (x2, y2), 1)
        # draw margin bottom
        pygame.draw.line(self.surface, self.color["primary"], (x2, y2), (x3, y3), 1)
        # draw bottom bar
        pygame.draw.line(self.surface, self.color["primary"], (0, self.HEIGHT-self.bottom_offset), (self.WIDTH, self.HEIGHT-self.bottom_offset), 1)
        # draw margin bars left
        total_length = y2-y1
        left_gap_between_bars = total_length/self.margin_bar_counts
        for i in range(self.margin_bar_counts+1):
            left_x1, left_x2 = x1-self.margin_bar_lengths, x1
            y = self.margin_offset+(i*left_gap_between_bars)
            pygame.draw.line(self.surface, self.color["primary"], (left_x1, y), (left_x2, y), 1)
        # draw max y value in margin
        textsurface = font.render(str(self.max_y), True, self.color["primary"])
        top_text_x, top_text_y = 10, self.margin_offset-10
        self.surface.blit(textsurface, (top_text_x, top_text_y))
        # draw min y value in margin
        textsurface = font.render(str(self.min_y), True, self.color["primary"])
        bottom_text_x, bottom_text_y = 10, self.margin_offset+(self.margin_bar_counts*left_gap_between_bars)-10
        self.surface.blit(textsurface, (bottom_text_x, bottom_text_y))
        # draw margin bars bottom
        total_length = x3-x2
        bottom_gap_between_bars = total_length/self.margin_bar_counts
        for i in range(self.margin_bar_counts+1):
            x = self.margin_offset+(i*bottom_gap_between_bars)
            top_y1, top_y2 = y2, y2+self.margin_bar_lengths
            pygame.draw.line(self.surface, self.color["primary"], (x, top_y1), (x, top_y2), 1)
        # draw min x value in margin
        textsurface = font.render(str(self.min_x), True, self.color["primary"])
        left_text_x, left_text_y = self.margin_offset-10, self.margin_offset+(self.margin_bar_counts*left_gap_between_bars)+10
        self.surface.blit(textsurface, (left_text_x, left_text_y))
        # draw max x value in margin
        textsurface = font.render(str(self.max_x), True, self.color["primary"])
        right_text_x, right_text_y = self.margin_offset+(self.margin_bar_counts*bottom_gap_between_bars)-10, self.margin_offset+(self.margin_bar_counts*left_gap_between_bars)+10
        self.surface.blit(textsurface, (right_text_x, right_text_y))
        # plot graph
        self.render_graph(x1, y1, x3-x1, y3-y1)
    def window_point_to_graph_point(self, x, y, offset_x, offset_y, plane_width, plane_height):
        plane_x = offset_x+(((x-self.min_x)/(self.max_x-self.min_x))*plane_width)
        plane_y = offset_y+((1-((y-self.min_y) / (self.max_y-self.min_y)))*plane_height)
        return plane_x, plane_y
    def render_graph(self, offset_x, offset_y, plane_width, plane_height):
        # plane surrounding - optional
        # pygame.draw.rect(self.surface, self.color["primary"], (offset_x, offset_y, plane_width, plane_height), 1)
        # plot each points
        iterations = min(len(self.x), len(self.y))
        for index in range(iterations):
            x, y = self.x[index], self.y[index]
            plane_x, plane_y = self.window_point_to_graph_point(x, y, offset_x, offset_y, plane_width, plane_height)
            pygame.draw.circle(self.surface, self.color["primary"], (plane_x, plane_y), self.plot_point_radius)
    def run(self):
        while self.play:
            self.surface.fill(self.color["background"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
                    elif event.key==K_SPACE:
                        self.enable_replay()
            #--------------------------------------------------------------
            self.update_window_size()
            self.render()
            # -------------------------------------------------------------
            pygame.display.update()
            self.ft.tick(self.fps)


