import threading
import pygame
import os
import logging
from config import ALARM_SOUND_PATH

logger = logging.getLogger(__name__)

class Alarm:
    def __init__(self):
        self.is_loaded = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            if ALARM_SOUND_PATH and os.path.exists(ALARM_SOUND_PATH):
                pygame.mixer.music.load(ALARM_SOUND_PATH)
                self.is_loaded = True
            else:
                logger.warning(f"Alarm sound file not found: {ALARM_SOUND_PATH}")
        except Exception as e:
            logger.error(f"Failed to initialize alarm: {e}")
            self.is_loaded = False
        self.alarm_thread = None

    def _play(self):
        if not self.is_loaded:
            logger.warning("Alarm sound not loaded, cannot play.")
            return
        try:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            logger.error(f"Alarm playback error: {e}")

    def trigger(self):
        if self.alarm_thread is None or not self.alarm_thread.is_alive():
            self.alarm_thread = threading.Thread(target=self._play, daemon=True)
            self.alarm_thread.start()
            logger.info('Alarm triggered')

    def stop(self):
        try:
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception:
            pass

    def __del__(self):
        try:
            if pygame.mixer.get_init():
                pygame.mixer.quit()
        except Exception:
            pass