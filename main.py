'''
it doesnt feel right since i coded this around the Sokoban example. But i wasted a lot of time looking for textures
or drawing them myself. it was a fun experience nonetheless...
If i hadn't started the project so late... i would have tried to add:
different levels(easy, medium, hard, extreme), and the game would have asked to pick one before starting
maybe add abilities to grab and drag props
better textures which suited the theme
'''

import pygame

class Ralph:
    def __init__(self):
        pygame.init()

        self.load_images()
        self.new_game()

        self.height = len(self.map)
        self.width = len(self.map[0])
        self.scale = self.images[0].get_width()

        screen_height = self.scale * self.height
        screen_width = self.scale * self.width
        self.screen = pygame.display.set_mode((screen_width, self.scale + screen_height))

        self.font = pygame.font.SysFont("Arial", 24)
        self.over_font = pygame.font.SysFont("Arial", 40)

        pygame.display.set_caption("Ralph the Dino")

        self.mainloop()

    def load_images(self):
        self.images = []
        for name in ["coin", "wall", "fire", "portal", "dino", "burnt", "exit", "dino_portal", "escaped"]:
            self.images.append(pygame.image.load(name + ".png"))


    def new_game(self):
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 3, 1, 0, 0, 0, 0, 0, 1, 4, 0, 0, 1, 1, 1],
                    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.coins = 0

    def mainloop(self):
        while True:
            self.handle_events()
            self.draw_screen()

    def handle_events(self):
        try:                                            #while working with the code find_dino method was causing issues and was
            current_y, current_x = self.find_dino()     #returning "None" since i kept forgetting to update the method's return value
        except TypeError:                               #thought it would be funny that the game cant find the dino anymore as we step 
            self.escaped()                              #on the exit tile. 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                if event.key == pygame.K_UP:
                    self.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    self.move(1, 0)

                if event.key == pygame.K_F2:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_f and self.map[current_y][current_x] == 7:
                    self.move(0, 0, True)


            if event.type == pygame.QUIT:
                exit()


    def move(self, move_y, move_x, teleport = False):
        if self.game_over():
            return
        
        dino_old_y, dino_old_x = self.find_dino()
        dino_new_y = dino_old_y + move_y
        dino_new_x = dino_old_x + move_x

        #we teleport between portals
        if teleport: 
            portal_exit_y, portal_exit_x = self.find_portal()
            dino_old_y, dino_old_x = self.find_dino()
            self.map[portal_exit_y][portal_exit_x] += 4
            self.map[dino_old_y][dino_old_x] -= 4
            return
        

        #this checks if we are stepping into fire
        if self.map[dino_new_y][dino_new_x] == 2:
            # stepping into fire when walking out of portal
            if self.map[dino_old_y][dino_old_x] == 7:
                self.map[dino_new_y][dino_new_x] += 3
                self.map[dino_old_y][dino_old_x] -= 4
                self.coins += 1
            else:
                self.map[dino_old_y][dino_old_x] -= 2
                self.map[dino_new_y][dino_new_x] += 3
            return

        # stepping into the portal
        if self.map[dino_new_y][dino_new_x] == 3:
            self.map[dino_old_y][dino_old_x] -= 2
            self.map[dino_new_y][dino_new_x] += 4
            return

        # stepping on the exit tile
        if self.map[dino_new_y][dino_new_x] == 6:
            self.map[dino_old_y][dino_old_x] -= 2
            self.map[dino_new_y][dino_new_x] += 2
            return

        # exiting portal
        if self.map[dino_old_y][dino_old_x] == 7:
            if self.map[dino_new_y][dino_new_x] == 1:
                return
            self.map[dino_new_y][dino_new_x] += 4
            self.map[dino_old_y][dino_old_x] -= 4
            self.coins += 1
            return

        # hitting walls
        if self.map[dino_new_y][dino_new_x] == 1:
            return

        # normal stepping while setting tiles on fire... we are not activating special events
        else:
            self.map[dino_old_y][dino_old_x] -= 2
            self.map[dino_new_y][dino_new_x] += 4
            self.coins += 1

        
        

    def find_dino(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in [4, 5, 7, 8]:
                    return (y, x)

    def find_portal(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 3:
                    return (y, x)
                
    def draw_screen(self):
        self.screen.fill((0, 0, 0))
        for y in range(self.height):
            for x in range(self.width):
                tile = self.map[y][x]
                self.screen.blit(self.images[tile], (x * self.scale , y * self.scale))

        text = self.font.render("Coins: " + str(self.coins), False, (255, 0, 0))
        self.screen.blit(text, (25, self.height * self.scale + 10))

        text = self.font.render("F2 = reset", True, (255, 0, 0))
        self.screen.blit(text, (200, self.height * self.scale + 10))

        text = self.font.render("Esc = exit", True, (255, 0, 0))
        self.screen.blit(text, (400, self.height * self.scale + 10))

        text = self.font.render("F = use portal", True, (255, 0, 0))
        self.screen.blit(text, (600, self.height * self.scale + 10))

        if self.game_over():
            text = self.over_font.render("You Died", True, (255, 0, 0))
            text_x = self.scale * self.width / 2 - text.get_width() / 2
            text_y = self.scale * self.height / 2 - text.get_height() / 2
            pygame.draw.rect(self.screen, (0, 0, 0), (text_x, text_y, text.get_width(), text.get_height()))
            self.screen.blit(text, (text_x, text_y))
        
        if self.escaped():
            text = self.over_font.render("Yay! You Escaped Successfully!", True, (255, 0, 0))
            text_x = self.scale * self.width / 2 - text.get_width() / 2
            text_y = self.scale * self.height / 2 - text.get_height() / 2
            pygame.draw.rect(self.screen, (0, 0, 0), (text_x, text_y, text.get_width(), text.get_height()))
            self.screen.blit(text, (text_x, text_y))
        pygame.display.flip()

    def game_over(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 5:
                    return True
        return False
    
    def escaped(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 8:
                    return True
        return False
    
if __name__ == "__main__":
    Ralph()