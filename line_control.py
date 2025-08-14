import logging

logger = logging.getLogger(__name__)

class LineController:
    def __init__(self):
        self.running = True

    def stop_line(self):
        if self.running:
            logger.warning("Assembly line STOP triggered by gesture (fist)")
            # TODO: Integrate with PLC / relay here
            self.running = False

    def start_line(self):
        if not self.running:
            logger.info("Assembly line START triggered by gesture (open palm)")
            # TODO: Integrate with PLC / relay here
            self.running = True

    def is_running(self) -> bool:
        return self.running
