import pygame

class Sound:
    def __init__(self, game) -> None:
        self.game = game
        pygame.mixer.init()
        self.path = 'random_projects/raycast attempt 2/resources/sound/'
        self.shotgun_sound = pygame.mixer.Sound(f'{self.path}shotgun.wav')
        self.npc_pain = pygame.mixer.Sound(f'{self.path}npc_pain.wav')
        self.npc_death = pygame.mixer.Sound(f'{self.path}npc_death.wav')
        self.npc_attack = pygame.mixer.Sound(f'{self.path}npc_attack.wav')
        self.player_pain = pygame.mixer.Sound(f'{self.path}player_pain.wav')

        # self.theme = pygame.mixer.music.load(f'{self.path}theme.mp3')
        self.theOnlyThingTheyFearIsYou = pygame.mixer.music.load(f'{self.path}better_theme.mp3')

    def play_theme(self):
        pygame.mixer.music.play(-1)