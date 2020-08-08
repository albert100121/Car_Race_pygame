import pygame
import random
import time
from PIL import Image
import os
import sys

#######################################################
# init                                                #
#######################################################
pygame.init()

#init windows size
display_width = 800
display_height = 600
game_window_size = (display_width, display_height)

# Color definitions
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

SCREEN = pygame.display.set_mode(game_window_size)
pygame.display.set_caption("test")
clock = pygame.time.Clock()


#########################################
# read imgs                             #
#########################################
# car_img = pygame.image.load("img/car_me_noback.png")
car_img = pygame.image.load("img/cars/thanos_car.png")
car_en = pygame.image.load("img/cars/car_en_noback.png")
road = pygame.image.load("img/theme/road.png")
thanos = pygame.image.load("img/theme/small_thanos.png")
ironman = pygame.image.load("img/theme/ironman.png")
End = pygame.image.load("img/theme/End.png")
# im = Image.open("img/car_me_noback.png")
im = Image.open("img/cars/thanos_car.png")
im_en = Image.open("img/cars/car_en_noback.png")
car_width, car_height = im.size
en_width, en_height = im_en.size

#########################################
# read highest score                    #
#########################################
if os.path.isfile("highest.txt"):
    high_file = "highest.txt"
    with open(high_file, "r") as High:
        # High_str = High.readline()
        # High_int = int(High_str)
        for line in High:
            High_str = line
        High_int = int(High_str)
        # print(High_int)
else:
    High_int = 0
    High_str = str(High_int)

#########################################
# Class game                            #
#########################################
class Game:
    def __init__(self):
        self.score = 0
        self.playerx = display_width * 0.45
        self.playery = display_height * 0.8
        self.playerx_displacement = 0
        self.PLAYER_LEFT_MOVE = 0
        self.PLAYER_RIGHT_MOVE = 1
        self.VALID_ACTIONS = 2
        self.actions = list([0, 0])

        self.FPS = 60
        self.obstacle_startx = random.randrange(0, display_width)

        # obstacle init position
        self.obstacle_starty = -600
        self.obstacle_speed = 10
        self.obstacle_width = en_width
        self.obstacle_height = en_height

        # stone inti position
        self.stone_speed = 10
        self.stone_width = 50
        self.stone_height = 50
        self.stone_starty = -600
        self.stone_startx = random.randrange(0, display_width)
        # while self.stone_startx >= self.obstacle_startx and self.stone_startx <= self.obstacle_startx + self.obstacle_width:
        while (self.stone_startx >= self.obstacle_startx and self.stone_startx <= self.obstacle_startx + self.obstacle_width) or (self.stone_startx + self.stone_width >= self.obstacle_startx and self.stone_startx +self.stone_width <= self.obstacle_startx + self.obstacle_width):
            self.stone_startx = random.randrange(0, display_width)

        self.draw_stone_flag = False

        # stone mode
        self.stone_flag = False
        self.stone_start_time = 0
        self.stone_num = 1
        # self.stone_collected = []
        self.time_stone_speed = 3
        self.power_stone_speed = -5
        self.space_stone_speed = 0

        # game mode
        self.pause_flag = False
        self.info_flag = True

        self.score = 0
        self.read_high()

    def draw_car(self, x ,y):
        # blit prepare the image to display in background and show once update
        # is called
        SCREEN.blit(car_img, (x,y))

    def draw_car_en(self, x ,y):
        # blit prepare the image to display in background and show once update
        # is called
        SCREEN.blit(car_en, (x,y))
    
    def draw_stone(self, x, y, num):
        stone = pygame.image.load("img/stones/stone%d.png"%num)
        SCREEN.blit(stone, (x, y))
    
    def swap_en(self, num):
        # when score goes high, swap enemy cars
        global car_en
        if os.path.isfile("img/cars/Ene%d.png"%num):
            car_en = pygame.image.load("img/cars/Ene%d.png"%num)
        else:
            car_en = pygame.image.load("img/cars/car_en_noback.png")

    # Read the highest score from the text file ########################
    def read_high(self):
        global High_str
        global High_int    
        if os.path.isfile("highest.txt"):
            high_file = "highest.txt"
            with open(high_file, "r") as High:
                for line in High:
                    High_str = line
                High_int = int(High_str)
        else:
            High_int = 0
            High_str = str(High_int)

    # flip the background road up-side-down ##########################
    def flip_road(self):
        global road
        road = pygame.transform.flip(road, False, True)

    # Show the messages when the car crashes    ######################
    def show_crash_msg(self):
        def text_objects(text, font):
            ts = font.render(text, True, red)
            return ts, ts.get_rect()

        time.sleep(1)
        SCREEN.blit(End, (0,0))
        pygame.display.update()
        time.sleep(2)

        self.game_loop()

    # Show the thanos of inevitable
    def show_thanos(self):
        SCREEN.blit(thanos, (0,0))
        pygame.display.update()
        time.sleep(2)
        self.game_loop()

    # Successfully dodged the enemy
    def things_dodged(self, count):
        # font = pygame.font.SysFont(None, 35)          # Can't compile into exe file if SysFont is None
        font = pygame.font.SysFont('arial', 35)
        text = font.render("Score: "+str(count), True, red)
        SCREEN.blit(text,(50,0))
        info = pygame.font.Font("freesansbold.ttf", 20).render("Info: i", True, white)
        SCREEN.blit(info, (50, 50))

    # Draw the information key on the left top
    def draw_info(self):
        info = pygame.font.Font("freesansbold.ttf", 20).render("Pause: p", True, white)
        SCREEN.blit(info, (50, 75))
        info = pygame.font.Font("freesansbold.ttf", 20).render("Quit: q", True, white)
        SCREEN.blit(info, (50, 100))
        info = pygame.font.Font("freesansbold.ttf", 20).render("Clean High: c", True, white)
        SCREEN.blit(info, (50, 125))
        info = pygame.font.Font("freesansbold.ttf", 20).render("Skip to End: spacebar", True, white)
        SCREEN.blit(info, (50, 150))
    
    # Draw the highest score on the right top of the screen
    def draw_high(self):
        global High_str
        global display_width
        # font = pygame.font.SysFont(None, 35)
        font = pygame.font.SysFont('arial', 35)
        text = font.render("Highest Score: "+ High_str, True, red)
        SCREEN.blit(text,(display_width -250,0))
    
    # Draw the stones I've collected so far
    def draw_collected_stones(self):
        for i in range(1, self.stone_num):
            col = pygame.image.load("img/stones/stone%d.png"%i)
            SCREEN.blit(col,(150+(50*i),0))

    # Define when it's crashed
    def _is_crash(self):
        if self.stone_flag and self.stone_num != 6:
            return False
        if self.playerx  > display_width - car_width or self.playerx  < 0:
            return True

        if self.playery < self.obstacle_starty+self.obstacle_height:
            if self.playerx  > self.obstacle_startx and self.playerx  < self.obstacle_startx + self.obstacle_width or self.playerx + car_width > self.obstacle_startx and self.playerx + car_width < self.obstacle_startx+self.obstacle_width:
                return True

    # Define the situation of touching the stones
    def _touch_stone(self):
        if self.playery < self.stone_starty+self.stone_height:
            if (self.playerx  > self.stone_startx and self.playerx  < (self.stone_startx + self.stone_width)) or (self.playerx + car_width > self.stone_startx and self.playerx + car_width < (self.stone_startx+self.stone_width)):
                self.draw_stone_flag = False
                return True
        return False
    
    # The loop of the game
    def game_loop(self):
        game_exit = False

        self.__init__()

        while not game_exit:
            for event in pygame.event.get():
                # Condition to quit
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    # quit()
                    game_exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # Move left
                        self.actions[self.PLAYER_LEFT_MOVE] = 1
                        self.actions[self.PLAYER_RIGHT_MOVE] = 0
                        self.playerx_displacement = -5
                    elif event.key == pygame.K_RIGHT:
                        # Move right
                        self.actions[self.PLAYER_LEFT_MOVE] = 0
                        self.actions[self.PLAYER_RIGHT_MOVE] = 1
                        self.playerx_displacement = 5
                    elif event.key == pygame.K_SPACE:
                        # Force score = 70 and end the game
                        self.score = 70
                    elif event.key == pygame.K_q:
                        # Force quit
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_c:
                        # Force reset highest score
                        global High_int
                        global High_str
                        with open("highest.txt", "w") as High:
                            High.write("0")
                        High_int = 0
                        High_str = "0"
                    elif event.key == pygame.K_p:
                        # Add the pause key 
                        if self.pause_flag == False:
                            self.pause_flag = True
                        elif self.pause_flag == True:
                            self.pause_flag = False
                    elif event.key == pygame.K_i:
                        # Add the show/hide information key
                        if self.info_flag:
                            self.info_flag = False
                        else:
                            self.info_flag = True
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        # Dont move
                        self.actions[self.PLAYER_LEFT_MOVE] = 0
                        self.actions[self.PLAYER_RIGHT_MOVE] = 0
                        self.playerx_displacement = 0
            self.frame()
        pygame.quit()
        quit()

    def frame(self):
        self.playerx += self.playerx_displacement
        
        # fill the window background with road
        SCREEN.blit(road, (0,0))
        # Calculate the time of the game and flips the road
        f = pygame.time.get_ticks()
        if f % 2 ==0:
            self.flip_road()
        
        # swap car
        if self.score % 10 == 0 :
            num = self.score //10
            self.swap_en(num)

        # self.draw_things(self.obstacle_startx, self.obstacle_starty, self.obstacle_width, self.obstacle_height, black)
        self.draw_car_en(self.obstacle_startx, self.obstacle_starty)
        self.draw_car(self.playerx,self.playery)
        self.things_dodged(self.score)
        self.draw_high()
        self.draw_collected_stones()

        # Time stone and power stone effect
        if self.stone_flag and self.stone_num ==6:
            self.obstacle_starty += self.time_stone_speed       # Slow down the car
        elif self.stone_flag and self.stone_num == 4:
            self.obstacle_starty += self.power_stone_speed      # Move car up
        # elif self.stone_flag and self.stone_num ==2:
        #     self.obstacle_starty += self.space_stone_speed
        else:
            self.obstacle_starty += self.obstacle_speed         # origin car speed

        # if the info is clicked, write out the info
        if self.info_flag:
            self.draw_info()

        # if the enemy is out of the screen, move back up
        if self.obstacle_starty > display_height:
            self.obstacle_starty = 0 - self.obstacle_height
            self.obstacle_startx = random.randrange(0,display_width - self.obstacle_width)
            self.score += 1
            # to increase obstacle speed
            self.obstacle_speed += 0.3      

        # if the car crashes
        if self._is_crash():
            if self.score > High_int:           # save the score
                with open("highest.txt", "w") as High:
                    High.write(str(self.score))
            self.show_crash_msg()               # Show avengers
            self.__init__()



        #####################################################
        # Stone function                                    #
        ##################################################### 
        # draw stone
        # # first version, the stone falls every 10 scores, and doesn't count if caught or not
        # if self.score % 10 == 0 and self.score != 0 and self.score != 70:
        #     self.draw_stone_flag = True
        # if self.draw_stone_flag:
        #     num = self.score//10
        #     self.draw_stone(self.stone_startx, self.stone_starty, num)
        #     self.stone_starty += self.stone_speed

        # second version, which needs to collect the stone
        if self.score % 5 ==0 and self.score != 0 and self.score !=70:      # when score %5 == 0, draw stone
            if not self.draw_stone_flag and not self.stone_flag:            # at that time zone ,no matter touch or not, will keep drawing, so avoid drawing by stone_flag on
                self.draw_stone_flag = True
        if not self.draw_stone_flag:                                        # if not able to draw_stone, move stone back up
            self.stone_starty = 0 - self.stone_height
            # self.stone_startx = random.randrange(0,display_width - self.stone_width)
            # while self.stone_startx >= self.obstacle_startx and self.stone_startx <= self.obstacle_startx + self.obstacle_width:
            while (self.stone_startx >= self.obstacle_startx and self.stone_startx <= self.obstacle_startx + self.obstacle_width) or (self.stone_startx + self.stone_width >= self.obstacle_startx and self.stone_startx +self.stone_width <= self.obstacle_startx + self.obstacle_width):
                self.stone_startx = random.randrange(0, display_width)
        if self.draw_stone_flag and not self._touch_stone():                # start drawing stones, but not at touching moment
            # if self.stone_num in self.stone_collected:
            #     self.stone_num +=1
            self.draw_stone(self.stone_startx, self.stone_starty, self.stone_num)
            self.stone_starty += self.stone_speed
        
        
        # stone reach bottom ############################
        if self.stone_starty > display_height:                              # when stone is over bottom line, 
            self.draw_stone_flag = False
            self.stone_starty = 0 - self.stone_height
            # self.stone_startx = random.randrange(0,display_width - self.stone_width)
            while (self.stone_startx >= self.obstacle_startx and self.stone_startx <= self.obstacle_startx + self.obstacle_width) or (self.stone_startx + self.stone_width >= self.obstacle_startx and self.stone_startx +self.stone_width <= self.obstacle_startx + self.obstacle_width):
                self.stone_startx = random.randrange(0, display_width)

        # stone mode ###################################
        if self.stone_flag:                                 # if stone_flag on, the effects remains 
            def text_objects(text, font):
                ts = font.render(text, True, red)
                return ts, ts.get_rect()
            text = "The End is NEAR!!!"
            large_text = pygame.font.Font("freesansbold.ttf", 75)
            text_surface, text_rect = text_objects(text, large_text)
            text_rect.center = (display_width/2, display_height/2)
            SCREEN.blit(text_surface, text_rect)
        # touch stone #############################################
        if self._touch_stone():
            # need to be the first, in order to erase the stone
            # self.draw_stone_flag = False            # when stone touched, no need to draw stones
            # self.stone_starty = 0 - self.stone_height
            # self.stone_startx = random.randrange(0,display_width - self.stone_width)

            # The space effect ################
            if self.stone_num ==1:
                self.obstacle_startx = 0
                self.obstacle_starty = 300
            # The reality effect #####################
            if self.stone_num ==2:
                self.score += 10    
      

            # The collect stone function
            if not self.stone_flag:                     # self._touch_stone() remains quite a while, in order not to collected too many stones at a time
            # if not self.draw_stone_flag:                     # self._touch_stone() remains quite a while, in order not to collected too many stones at a time
                if self.stone_num ==6:                  # to define which stones to fall
                    # win the game
                    if self.score > High_int:
                        with open("highest.txt", "w") as High:
                            High.write(str(self.score))
                    self.show_thanos()
                    self.__init__()
                elif self.stone_num != 6:
                    self.stone_num += 1
                    # collect stones
                    # print("current",self.stone_num, "collected", self.stone_collected)
                    # if self.stone_num not in self.stone_collected:          
                    #     self.stone_collected.append(self.stone_num)
                
            self.stone_flag = True                  # stone mode flag on, in order not to die
            self.stone_start_time = time.time()

        # if not self.stone_flag:
        #     if self.stone_num == 4:
        #         self.obstacle_speed = 10
        
        if not self._touch_stone():
            if (time.time() - self.stone_start_time) > 3:
                self.stone_flag = False
        
    
        # Show thanos when game ended
        if self.score >= 70:
            if self.score > High_int:
                with open("highest.txt", "w") as High:
                    High.write(str(self.score))
            self.show_thanos()
            self.__init__()
        
        # Game mode
        while self.pause_flag == True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause_flag = False
                    elif event.key == pygame.K_SPACE:
                        # Force score = 70 and end the game
                        self.score = 70
                    elif event.key == pygame.K_q:
                        # Force quit
                        pygame.quit()
                        quit()
                    
            time.sleep(0.1)

            

        pygame.display.update()
        clock.tick(self.FPS) # Frames per second

if __name__ == "__main__":
    g = Game()
    g.game_loop()