import os
import pygame

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.music_folder = music_folder
        
        if os.path.exists(self.music_folder):
            self.playlist = [f for f in os.listdir(self.music_folder) if f.endswith(('.mp3', '.wav'))]
        else:
            self.playlist = []
            
        self.current_index = 0
        self.is_playing = False

    def load_track(self):
        if self.playlist:
            track_path = os.path.join(self.music_folder, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)

    def play(self):
        if self.playlist:
            if not self.is_playing:
                self.load_track()
                pygame.mixer.music.play()
                self.is_playing = True
            else:
                pygame.mixer.music.unpause() # Better than play() for resuming

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.is_playing = False
            self.play()

    def prev_track(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.is_playing = False
            self.play()

    def get_current_track_name(self):
        return self.playlist[self.current_index] if self.playlist else "No Tracks Found"

    def get_progress(self):
        pos = pygame.mixer.music.get_pos()
        return max(0, pos // 1000)