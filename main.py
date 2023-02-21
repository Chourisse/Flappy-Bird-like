import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition de la fenêtre de jeu
window_width = 288
window_height = 512
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Chargement des images
background_image = pygame.image.load("background.png").convert()
bird_image = pygame.image.load("bird.png").convert_alpha()
pipe_image = pygame.image.load("pipe.png").convert_alpha()

# Définition des constantes de jeu
gravity = 0.25
bird_speed = 5
pipe_speed = 3
pipe_gap = 150
pipe_frequency = 150

# Définition de la classe Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0
 
    def update(self):
        self.velocity += gravity
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = -bird_speed

# Définition de la classe Pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
    def update(self):
        self.rect.x -= pipe_speed

# Création des groupes de sprites
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Création du personnage principal
bird = Bird(50, 200)
all_sprites.add(bird)

# Boucle de jeu principale
running = True
clock = pygame.time.Clock()
score = 0
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    # Génération des obstacles
    if random.randint(1, pipe_frequency) == 1:
        pipe_x = window_width
        pipe_y = random.randint(-200, 0)
        top_pipe = Pipe(pipe_x, pipe_y)
        bottom_pipe = Pipe(pipe_x, pipe_y + pipe_image.get_height() + pipe_gap)
        all_sprites.add(top_pipe)
        all_sprites.add(bottom_pipe)
        pipes.add(top_pipe)
        pipes.add(bottom_pipe)

    # Mise à jour des sprites
    all_sprites.update()

    # Vérification des collisions
    if pygame.sprite.spritecollide(bird, pipes, False):
        running = False

    # Suppression des pipes hors de l'écran
    for pipe in pipes:
        if pipe.rect.x < -pipe_image.get_width():
            pipes.remove(pipe)
            all_sprites.remove(pipe)
            score += 1

    # Affichage des sprites
    window.blit(background_image, (0, 0))
    all_sprites.draw(window)

    # Affichage du score
    font = pygame.font.Font(None, 36)
    text = font.render(str(score), True, (255, 255, 255))
    window.blit(text, (10, 10))

    # Actualisation de l'écran
    pygame.display.flip()

    # Pause de 60 images par seconde
    clock.tick(60)
