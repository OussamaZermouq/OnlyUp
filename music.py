import pygame


class Music:
    def __init__(self,index):
        pygame.mixer.init()
        pygame.mixer.music.load(f"Assets/Music/song{index}.mp3")

    def stop(slef):
        pygame.mixer.music.stop()

    def run(self):
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
