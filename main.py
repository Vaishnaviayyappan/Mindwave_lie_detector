# main.py

import pygame
import socket
import json
import time
import random
import threading
import sys
from config import *

class MindWaveDataCollector(threading.Thread):
    """
    Connects to BlueMuse and collects EEG data in a separate thread.
    """
    def __init__(self, host, port):
        super().__init__(daemon=True) # Daemon thread will exit when main program exits
        self.host = host
        self.port = port
        self.sock = None
        self.is_connected = False
        self.latest_data = {"attention": 0, "meditation": 0}
        self.lock = threading.Lock()

    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.is_connected = True
            print("Successfully connected to BlueMuse.")

            buffer = ""
            while self.is_connected:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:
                    break
                buffer += data
                
                # Process each complete JSON line
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line:
                        try:
                            packet = json.loads(line)
                            # We are interested in 'eSense' data
                            if 'eSense' in packet:
                                with self.lock:
                                    self.latest_data['attention'] = packet['eSense'].get('attention', 0)
                                    self.latest_data['meditation'] = packet['eSense'].get('meditation', 0)
                        except json.JSONDecodeError:
                            continue # Ignore malformed packets

        except ConnectionRefusedError:
            print("Connection refused. Is BlueMuse running and connected to the headset?")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.sock:
                self.sock.close()
            self.is_connected = False
            print("Disconnected from BlueMuse.")

    def get_data(self):
        """Thread-safe way to get the latest data."""
        with self.lock:
            return self.latest_data.copy()

class LieDetectorApp:
    def __init__(self):
        pygame.init()
        self.width, self.height = 700, 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("NeuroSky Lie Detector - Oddball Paradigm")
        self.clock = pygame.time.Clock()
        
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        self.data_collector = MindWaveDataCollector(HOST, PORT)
        self.results_log = []

    def run(self):
        self.data_collector.start()
        time.sleep(2) # Give the connection a moment to establish

        if not self.data_collector.is_connected:
            print("Could not connect to data source. Exiting.")
            pygame.quit()
            return

        self._run_experiment()
        self._show_results()
        self._wait_to_close()

        self.data_collector.is_connected = False # Signal thread to stop
        self.data_collector.join()
        pygame.quit()

    def _run_experiment(self):
        """Runs the main card-flashing experiment."""
        random.shuffle(DECK)
        self.screen.fill((20, 20, 30))
        start_text = self.font_medium.render(f"Think of this card: {SECRET_CARD}", True, (255, 255, 100))
        self.screen.blit(start_text, (self.width // 2 - start_text.get_width() // 2, 50))
        start_inst = self.font_small.render("Press SPACE when ready", True, (200, 200, 200))
        self.screen.blit(start_inst, (self.width // 2 - start_inst.get_width() // 2, 120))
        pygame.display.flip()

        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_start = False

        for i, card in enumerate(DECK):
            # --- Show a fixation cross ---
            self.screen.fill((20, 20, 30))
            cross_text = self.font_large.render("+", True, (200, 200, 200))
            self.screen.blit(cross_text, (self.width // 2 - 15, self.height // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(INTER_STIMULUS_INTERVAL)

            # --- Show the card and record response ---
            self.screen.fill((30, 30, 40))
            card_text = self.font_large.render(card, True, (255, 255, 255))
            self.screen.blit(card_text, (self.width // 2 - card_text.get_width() // 2, self.height // 2 - 50))
            pygame.display.flip()
            
            # Record attention data for the duration the card is shown
            attention_readings = []
            start_time = time.time()
            while time.time() - start_time < CARD_DISPLAY_TIME / 1000.0:
                data = self.data_collector.get_data()
                attention_readings.append(data['attention'])
                pygame.time.wait(50) # Sample every 50ms

            # Process the readings
            if attention_readings:
                avg_attention = sum(attention_readings) / len(attention_readings)
                is_significant = avg_attention > ATTENTION_THRESHOLD
            else:
                avg_attention = 0
                is_significant = False

            self.results_log.append({
                'card': card,
                'avg_attention': avg_attention,
                'is_significant': is_significant
            })

    def _show_results(self):
        """Displays the final analysis of the experiment."""
        self.screen.fill((20, 20, 30))
        title_text = self.font_medium.render("Experiment Analysis", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 30))

        secret_responses = [r for r in self.results_log if r['card'] == SECRET_CARD]
        other_responses = [r for r in self.results_log if r['card'] != SECRET_CARD]

        if secret_responses:
            secret_attention = secret_responses[0]['avg_attention']
            secret_text = self.font_small.render(f"Response to Secret Card ('{SECRET_CARD}'):", True, (255, 255, 255))
            self.screen.blit(secret_text, (50, 100))
            secret_val_text = self.font_small.render(f"Average Attention: {secret_attention:.2f}", True, (255, 255, 100))
            self.screen.blit(secret_val_text, (70, 130))

        if other_responses:
            other_avg = sum(r['avg_attention'] for r in other_responses) / len(other_responses)
            other_text = self.font_small.render(f"Average Response to Other Cards:", True, (255, 255, 255))
            self.screen.blit(other_text, (50, 180))
            other_val_text = self.font_small.render(f"Average Attention: {other_avg:.2f}", True, (180, 180, 180))
            self.screen.blit(other_val_text, (70, 210))

        # Simple conclusion logic
        conclusion = ""
        conclusion_color = (180, 180, 180)
        if secret_responses and other_responses:
            if secret_attention > other_avg * 1.2: # Arbitrary factor for a significant difference
                conclusion = f"Conclusion: Significant response detected for '{SECRET_CARD}'."
                conclusion_color = (100, 255, 100)
            else:
                conclusion = f"Conclusion: No significant response detected for '{SECRET_CARD}'."
                conclusion_color = (255, 100, 100)

        conclusion_text = self.font_medium.render(conclusion, True, conclusion_color)
        self.screen.blit(conclusion_text, (50, 280))

        inst_text = self.font_small.render("Press any key to exit.", True, (150, 150, 150))
        self.screen.blit(inst_text, (50, self.height - 50))
        
        pygame.display.flip()

    def _wait_to_close(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False

if __name__ == "__main__":
    app = LieDetectorApp()
    app.run()
