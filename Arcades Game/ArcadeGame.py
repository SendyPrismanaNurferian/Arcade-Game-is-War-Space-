import sys
import random
import pygame
from pygame.locals import *

pygame.init()

'''IMAGES GAMES'''
player_ship = 'playership.png'
enemy_ship = 'enemyship.png'
ufo_ship = 'UFOship.png'
player_bullet = 'enembull.png'
enemy_bullet = 'enembull1.png'
ufo_bullet = 'enembull2.png'

''''SOUNDS or SONGS GAMES'''
fire_sound = pygame.mixer.Sound('fireship.wav')
explosion_sound = pygame.mixer.Sound('low_epl.wav')
go_sound = pygame.mixer.Sound('go.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')
back_sound = pygame.mixer.music.load('Backsound.mp3')
war_sound = pygame.mixer.Sound('epicsong.mp3')
game_over_music = pygame.mixer.Sound('illusory.mp3')

pygame.mixer.init()

screen = pygame.display.set_mode((0,0), FULLSCREEN)
s_width, s_height = screen.get_size()

clock = pygame.time.Clock()
FPS = 60

background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()
ufobullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

sprite_group = pygame.sprite.Group()

pygame.mouse.set_visible(False)

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([x,y])
        self.image.fill('white')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1
        self.rect.x += 1
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10, 0)
            self.rect.x = random.randrange(-400, s_width)

class Particle(Background):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(0, s_height)
        self.image.fill('grey')
        self.vel = random.randint(3,8)

    def update(self):
        self.rect.y += self.vel
        if self.rect.y > s_height:
            self.rect.y = random.randrange(0, s_height)
            self.rect.x = random.randrange(0, s_width)

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('Black')
        self.alive = True
        self.count_to_life = 0
        self.activate_bullet = True
        self.alpha_duration = 0

    def update(self):
        if self.alive:
            self.image.set_alpha(50)
            self.alpha_duration += 1
            if self.alpha_duration > 170:
                self.image.set_alpha(255)
            mouse = pygame.mouse.get_pos()
            self.rect.x = mouse[0] - 20
            self.rect.y = mouse[1] + 40
        else:
            self.alpha_duration = 0
            epl_x = self.rect.x + 50
            epl_y = self.rect.y + 50
            explosion = Explosion(epl_x, epl_y)
            explosion_group.add(explosion)
            sprite_group.add(explosion)
            pygame.time.delay(20)
            self.rect.y = s_height + 200
            self.count_to_life += 1
            if self.count_to_life > 100:
                self.alive = True
                self.count_to_life = 0
                self.activate_bullet = True
    
    def shoot(self):
        if self.activate_bullet:
            bullet = PlayerBullet(player_bullet)
            mouse = pygame.mouse.get_pos()
            bullet.rect.x = mouse[0] + 35
            bullet.rect.y = mouse[1] 
            playerbullet_group.add(bullet)
            sprite_group.add(bullet)

    def dead(self):
        self.alive = False
        self.activate_bullet = False

class Enemy(Player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(80, s_width-80)
        self.rect.y = random.randrange(-500, 0)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(80, s_width-50)
            self.rect.y = random.randrange(-2000, 0)
        self.shoot()

    def shoot(self):
        if self.rect.y in (0, 30, 70, 300, 700):
            enemybullet = EnemyBullet(enemy_bullet)
            enemybullet.rect.x = self.rect.x + 15
            enemybullet.rect.y = self.rect.y + 60
            enemybullet_group.add(enemybullet)
            sprite_group.add(enemybullet)

class ufo(Player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = -200
        self.rect.y = 200
        self.move = 1
    
    def update(self):
        self.rect.x += self.move
        if self.rect.x > s_width + 200:
            self.move *= -1
        elif self.rect.x < -200:
            self.move *= -1
        self.shoot()

    def shoot(self):
        if self.rect.x % 50 == 0:
            ufobullet = EnemyBullet(ufo_bullet)
            ufobullet.rect.x = self.rect.x + 120
            ufobullet.rect.y = self.rect.y + 125
            ufobullet_group.add(ufobullet)
            sprite_group.add(ufobullet) 

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('Black')

    def update(self):
        self.rect.y -= 15
        if self.rect.y < 0:
            self.kill()

class EnemyBullet(PlayerBullet):
    def __init__(self, img):
        super().__init__(img)
        self.image.set_colorkey('White')

    def update(self):
        self.rect.y += 3
        if self.rect.y > s_height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img_list = []
        for i in range(1,6):
            img = pygame.image.load(f'ep{i}.png').convert()
            img.set_colorkey('Black')
            img = pygame.transform.scale(img, (120, 120))
            self.img_list.append(img)
        self.index = 0
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count_delay = 0

    def update(self):
        self.count_delay += 1
        if self.count_delay >= 12:
            if self.index < len(self.img_list) - 1:
                self.count_delay = 0
                self.index += 1
                self.image = self.img_list[self.index]
        if self.index >= len(self.img_list) - 1:
            if self.count_delay >= 12:
                self.kill()

class Games:
    def __init__(self):
        self.count_hit = 0
        self.count_hit2 = 0
        self.lifes = 5
        self.score = 0
        self.init_create = True
        self.game_over_sound_delay = 0
    
        self.startgame_screen()

    def startgame_text(self):
        font = pygame.font.SysFont('Calibri-Bold', 70)
        text = font.render("WAR OF SPACE", True, 'Blue')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)

        font2 = pygame.font.SysFont('Calibri', 20)
        text2 = font2.render("Project From M4$ $3ÑÐÝ", True, 'Red')
        text2_rect = text.get_rect(center=(s_width/2, s_height/2+80))
        screen.blit(text2, text2_rect)

        font3 = pygame.font.SysFont('Calibri-Bold', 20)
        text3 = font3.render("Tekan ENTER untuk Bermain", True, 'White')
        text3_rect = text.get_rect(center=(s_width/2, s_height/2+150))
        screen.blit(text3, text3_rect)

    def startgame_screen(self):
        pygame.mixer.Sound.stop(game_over_music)
        pygame.mixer.Sound.play(war_sound)
        self.lifes = 5
        sprite_group.empty()
        while True:
            screen.fill('Black')
            self.startgame_text()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        self.run_game()

            pygame.display.update()

    def pausegame_text(self):
        font = pygame.font.SysFont('Calibri-Bold', 50)
        text = font.render("PAUSED", True, 'White')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)
    
    def pausegame_screen(self):
        self.init_create = False
        while True:
            self.pausegame_text()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_SPACE:
                        self.run_game()

            pygame.display.update()

    def gameover_text(self):
        font = pygame.font.SysFont('Calibri-Bold', 50)
        text = font.render("GAME OVER", True, 'RED')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)        

    def gameover_screen(self):
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(game_over_sound)
        while True:
            screen.fill('Black')
            self.gameover_text()
            self.game_over_sound_delay += 1
            if self.game_over_sound_delay > 1000:
                pygame.mixer.Sound.play(game_over_music)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.startgame_screen()

            pygame.display.update()        
    
    def create_background(self):
        for i in range(20):
            x = random.randint(1,6)
            background_image = Background(x,x)
            background_image.rect.x = random.randrange(0, s_width)
            background_image.rect.y = random.randrange(0, s_height)
            background_group.add(background_image)
            sprite_group.add(background_image)

    def create_particles(self):
        for i in range(100):
            x = 1
            y = random.randint(1,7)
            particle = Particle(x, y)
            particle_group.add(particle)
            sprite_group.add(particle)

    def create_player(self):
        self.player = Player(player_ship)
        player_group.add(self.player)
        sprite_group.add(self.player)
    
    def create_enemy(self):
        for i in range(10):
            self.enemy = Enemy(enemy_ship)
            enemy_group.add(self.enemy)
            sprite_group.add(self.enemy)

    def create_ufo(self):
        for i in range(1):
            self.ufo = ufo(ufo_ship)
            ufo_group.add(self.ufo)
            sprite_group.add(self.ufo)

    def playerbullet_hit_enemy(self):
        hit = pygame.sprite.groupcollide(enemy_group, playerbullet_group, False
        , True)
        for i in hit:
            self.count_hit += 1
            if self.count_hit == 2:
                self.score += 10
                epl_x = i.rect.x + 20
                epl_y = i.rect.y + 40
                explosion = Explosion(epl_x, epl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-3000, -100)
                self.count_hit = 0
                pygame.mixer.Sound.play(explosion_sound)

    def playerbullet_hit_ufo(self):
        hit = pygame.sprite.groupcollide(ufo_group, playerbullet_group, False 
        , True)
        for i in hit:
            self.count_hit2 += 1
            if self.count_hit2 == 4:
                self.score += 30
                epl_x = i.rect.x + 80
                epl_y = i.rect.y + 130
                explosion = Explosion(epl_x, epl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = -100
                i.rect.y = 50              
                self.count_hit2 = 0
                pygame.mixer.Sound.play(explosion_sound)

    
    def enemybullet_hit_player(self):
        if self.player.image.get_alpha() == 255:
            hit = pygame.sprite.spritecollide(self.player, enemybullet_group, True)
            if hit:
                self.lifes -= 1
                self.player.dead()
                pygame.mixer.Sound.play(explosion_sound)
                if self.lifes < 0:
                    self.gameover_screen()

    def ufobullet_hit_player(self):
        if self.player.image.get_alpha() == 255:
            hit = pygame.sprite.spritecollide(self.player, ufobullet_group, True)
            if hit:
                self.lifes -= 1
                self.player.dead()
                pygame.mixer.Sound.play(explosion_sound)
                if self.lifes < 0:
                    self.gameover_screen()
    
    def player_enemy_crashed(self):
        if self.player.image.get_alpha() == 255:
            hit = pygame.sprite.spritecollide(self.player, enemy_group, False)
            if hit:
                for i in hit:
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-3000, -100)
                    self.lifes -= 1
                    self.player.dead()
                    pygame.mixer.Sound.play(explosion_sound)
                    if self.lifes < 0:
                        self.gameover_screen()

    def player_ufo_crashed(self):
        if self.player.image.get_alpha() == 255:
            hit = pygame.sprite.spritecollide(self.player, ufo_group, False)
            if hit:
                for i in hit:
                    i.rect.x = -200
                    self.lifes -= 1
                    self.player.dead()
                    pygame.mixer.Sound.play(explosion_sound)
                    if self.lifes < 0:
                        pygame.display.update()
                        pygame.quit()
                        sys.exit()

    def create_lifes(self):
        self.lifes_img = pygame.image.load(player_ship)
        self.lifes_img = pygame.transform.scale(self.lifes_img, (20,20))
        n = 0
        for i in range(self.lifes):
            screen.blit(self.lifes_img, (0+n, s_height-720))
            n += 80

    def create_score(self):
        score = self.score
        font = pygame.font.SysFont('Calibri', 30)
        text = font.render("Score: "+str(score), True, 'green')
        text_rect = text.get_rect(center=(s_width-100, s_height-700))
        screen.blit(text, text_rect)

    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()

    def run_game(self):
        pygame.mixer.Sound.stop(war_sound)
        pygame.mixer.Sound.play(go_sound)
        pygame.mixer.music.play(-1)
        if self.init_create:
            self.create_background()
            self.create_particles()
            self.create_player()
            self.create_enemy()
            self.create_ufo()
        while True:
            screen.fill('Black')
            self.playerbullet_hit_enemy()
            self.playerbullet_hit_ufo()
            self.enemybullet_hit_player()
            self.ufobullet_hit_player()
            self.player_enemy_crashed()
            self.player_ufo_crashed()
            self.run_update()
            pygame.draw.rect(screen, 'Black', (0,0,s_width,25))
            self.create_lifes()
            self.create_score()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    pygame.mixer.Sound.play(fire_sound)
                    self.player.shoot()
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                    if event.key == K_SPACE:
                        self.pausegame_screen()

            pygame.display.update()
            clock.tick(FPS)

def main():
    game = Games()
    
if __name__ == '__main__':
    main()