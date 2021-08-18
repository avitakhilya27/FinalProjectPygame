import pygame
## pengaturan tampilan game
# mengatur ukuran layar
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Maintain Independece"

# mengatur warna background (RGB code)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

#menginisialisasi gambar yang ditampilkan
kalah_image = pygame.image.load('asset/gameover.png')
kalah_image = pygame.transform.scale(kalah_image, (300, 100))
menang_image = pygame.image.load('asset/merdeka.jpg')
menang_image = pygame.transform.scale(menang_image, (280, 280))

# menambahkan suara
pygame.mixer.init()
start_sound = pygame.mixer.Sound('sound effect/start.mp3')
langkah_sound = pygame.mixer.Sound('sound effect/langkah.ogg')
gameover_sound = pygame.mixer.Sound('sound effect/gameover.ogg')
finish_sound = pygame.mixer.Sound('sound effect/finish.mp3')

# frame rate = mengatur jumlah frame per second
clock = pygame.time.Clock()

#penerapan object oriented progamming
class Game:
    TICK_RATE = 60

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # menampilkan screen
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):
        is_game_over = False
        direction = 0
        did_win = False
        start_sound.play()

        player_character = PlayerCharacter('asset/player.png', 275, 550, 50, 50)

        enemy_1 = EnemyCharacter('asset/musuh1.png', 20, 450, 50, 50)
        enemy_1.SPEED += level_speed

        enemy_2 = EnemyCharacter('asset/musuh2.png', self.width - 40, 300, 50, 50)
        enemy_2.SPEED += level_speed

        enemy_3 = EnemyCharacter('asset/musuh3.png', 20, 100, 50, 50)
        enemy_3.SPEED += level_speed

        enemy_4 = EnemyCharacter('asset/musuh4.png', self.width - 20, 25, 45, 45)
        enemy_4.SPEED += level_speed

        Flag = GameObject('asset/flag.png', 275, -15, 60, 60)
        game_font = pygame.font.Font('04B_19.ttf', 20)

        # perulangan untuk mengupdate game
        while not is_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                        langkah_sound.play()
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                        langkah_sound.play()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                        langkah_sound.play()
                print(event)

            # memanggil karakter
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image,(0, 0))

            player_character.move(direction, self.height)
            player_character.draw(self.game_screen)
            Flag.draw(self.game_screen)

            enemy_1.move(self.width)
            enemy_1.draw(self.game_screen)

            if level_speed > 2 :
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)
            if level_speed > 4 :
                enemy_3.move(self.width)
                enemy_3.draw(self.game_screen)
            if level_speed > 5:
                enemy_4.move(self.width)
                enemy_4.draw(self.game_screen)

            #jika bertabrakan
            if player_character.detection_collison(enemy_1):
                is_game_over = True
                did_win = False
                self.game_screen.blit(kalah_image, (150, 250))
                gameover_sound.play()
                pygame.display.update()
                clock.tick(1)
                break
            if player_character.detection_collison(enemy_2):
                is_game_over = True
                did_win = False
                self.game_screen.blit(kalah_image, (150, 250))
                gameover_sound.play()
                pygame.display.update()
                clock.tick(1)
                break
            if player_character.detection_collison(enemy_3):
                is_game_over = True
                did_win = False
                self.game_screen.blit(kalah_image, (150, 250))
                gameover_sound.play()
                pygame.display.update()
                clock.tick(1)
                break
            if player_character.detection_collison(enemy_4):
                is_game_over = True
                did_win = False
                self.game_screen.blit(kalah_image, (150, 250))
                gameover_sound.play()
                pygame.display.update()
                clock.tick(1)
                break
            if player_character.detection_collison(Flag):
                is_game_over = True
                did_win = True
                self.game_screen.blit(menang_image, (150, 150))
                finish_sound.play()
                pygame.display.update()
                clock.tick(1)
                break

            pygame.display.update()
            clock.tick(self.TICK_RATE)

        if did_win: #jika menang, game akan berulang, jika kalah, game berakhir
            self.run_game_loop(level_speed + 1.0)
        else:
            return


class GameObject:
    def __init__(self, image_path, x, y, width, height):
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

        # load karakter pada game
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos)) #blit untuk menambahkan karakter objek

class PlayerCharacter(GameObject):

    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0 :
            self.y_pos += self.SPEED
        if self.y_pos >= max_height - 50:
            self.y_pos = max_height - 50

    def detection_collison(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height: #jika posisi pemain diatas enemy, game berlanjut
            return False
        elif self.y_pos + self.height < other_body.y_pos: #jika posisi pemain dibawah enemy, game berlanjut
            return False
        if self.x_pos > other_body.x_pos + other_body.width: #jika posisi pemain dikanan enemy, game lanjut
            return False
        elif self.x_pos + self.width < other_body.x_pos: #jika posisi pemain dikiri enemy, game lanjut
            return False

        return True


class EnemyCharacter(GameObject):

    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40 :
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

pygame.init()
new_game = Game('asset/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)


#keluar dari game
pygame.quit()
quit()

