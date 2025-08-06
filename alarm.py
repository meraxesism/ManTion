import threading
import pygame
import os
import logging
from config import ALARM_SOUND_PATH

pygame.mixer.init()

def play_alarm():
    def _play():
        try:
            if not os.path.exists(ALARM_SOUND_PATH):
                logging.error(f"Alarm sound file not found: {ALARM_SOUND_PATH}")
                return
            pygame.mixer.music.load(ALARM_SOUND_PATH)
            pygame.mixer.music.play()
        except Exception as e:
            logging.error(f"Alarm playback error: {e}")
    threading.Thread(target=_play, daemon=True).start()
    logging.info('Alarm triggered')