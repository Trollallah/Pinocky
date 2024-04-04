import pygame.display

from scripts.utilities.scale import scale_singleton as scale


class GameTimer:
    """Measures time passed since game start, but excluding any time passed while game paused."""
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        # Timer Stuff
        self.time_start = 0
        self.current_time_ms = 0
        self.current_time_s = 0
        self.is_time_paused = False
        self.pause_time_start = 0
        self.pause_time_end = 0
        self.total_pause_time = 0
        self.first_loop = True
        # Timer display
        self.text_size = 72
        if scale.scale:
            self.text_size *= 2
        self.timer_text = ""
        self.font = pygame.font.SysFont('arial', self.text_size, bold=False, italic=False)
        self.text_surf = self.font.render("Test", False, 'black')
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.midtop = (self.display_surface.get_width() // 2, 0)

    def pause_time(self):
        """
        Pauses game and adds time to be used in time paused calculation.
        :return:
        """
        if not self.is_time_paused:
            self.pause_time_start = pygame.time.get_ticks()
            self.is_time_paused = True
        else:
            self.pause_time_end = pygame.time.get_ticks()

    def calculate_time_paused(self):
        """
        Calculates time that has elapsed since pause began.
        :return:
        """
        self.total_pause_time += (self.pause_time_end - self.pause_time_start)

    def draw_last_time(self):
        """
        Draws last good game time during paused session.
        :return:
        """
        self.text_surf = self.font.render(self.timer_text, False, 'black')
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.midtop = (self.display_surface.get_width() // 2, 0)
        self.display_surface.blit(self.text_surf, self.text_rect)

    def draw_time(self):
        """
        Draws current time without paused session included.
        :return:
        """
        self.current_time_ms = pygame.time.get_ticks() - self.total_pause_time - self.time_start
        self.current_time_s = self.current_time_ms // 1000
        self.format_time_text()
        self.text_surf = self.font.render(self.timer_text, False, 'black')
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.midtop = (self.display_surface.get_width() // 2, 0)
        self.display_surface.blit(self.text_surf, self.text_rect)

    def format_time_text(self):
        """
        Formats current time to read m:ss
        :return:
        """
        temp = self.current_time_s
        minutes, seconds = divmod(temp, 60)
        self.timer_text = f"{minutes}:{seconds:02d}"
