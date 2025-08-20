import threading
import pygame
import os
import logging
from config import ALARM_SOUND_PATH

logger = logging.getLogger(__name__)

class Alarm:
    def __init__(self):
        self.is_loaded = False
        self._lock = threading.Lock()
        try:
            if not pygame.mixer.get_init():
                # Initialize with specific format to handle more audio types
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            if ALARM_SOUND_PATH and os.path.exists(ALARM_SOUND_PATH):
                try:
                    pygame.mixer.music.load(ALARM_SOUND_PATH)
                    self.is_loaded = True
                    logger.info(f"Alarm sound loaded successfully: {ALARM_SOUND_PATH}")
                except pygame.error as pe:
                    logger.warning(f"Failed to load alarm sound {ALARM_SOUND_PATH}: {pe}")
                    # Try using a pygame example sound as fallback
                    try:
                        fallback_sound = os.path.join(os.path.dirname(pygame.__file__), 'examples', 'data', 'boom.wav')
                        if os.path.exists(fallback_sound):
                            pygame.mixer.music.load(fallback_sound)
                            self.is_loaded = True
                            logger.info(f"Using fallback alarm sound: {fallback_sound}")
                        else:
                            logger.warning("No fallback alarm sound available")
                    except Exception:
                        logger.warning("Could not load fallback alarm sound")
            else:
                logger.warning(f"Alarm sound file not found: {ALARM_SOUND_PATH}")
        except Exception as e:
            logger.error(f"Failed to initialize alarm: {e}")
            self.is_loaded = False
        self.alarm_thread = None

    def _play(self):
        if not self.is_loaded:
            logger.warning("Alarm sound not loaded, cannot play.")
        try:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            logger.error(f"Alarm playback error: {e}")

    def trigger(self):
        with self._lock:
            if self.alarm_thread is None or not self.alarm_thread.is_alive():
                self.alarm_thread = threading.Thread(target=self._play, daemon=True)
                self.alarm_thread.start()
                logger.info('Alarm triggered')
            else:
                logger.info('Alarm already running, trigger ignored.')

    def stop(self):
        with self._lock:
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