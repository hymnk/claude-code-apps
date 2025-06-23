#!/usr/bin/env python3
"""
FPS AIM Training Game
Resolution: 1280x960
Time: 60 seconds
Scoring: Based on distance from target center
"""

import pygame
import math
import random
import time
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
FPS = 60
GAME_TIME = 60  # seconds

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Target settings
TARGET_RADIUS = 30
TARGET_CENTER_RADIUS = 8
TARGET_INNER_RADIUS = 15
TARGET_OUTER_RADIUS = 30

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = TARGET_RADIUS
        self.hit = False
        self.hit_time = 0
        
    def draw(self, screen):
        """Draw the target with concentric circles"""
        if not self.hit:
            # Outer ring (red)
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), TARGET_OUTER_RADIUS, 3)
            # Middle ring (white)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), TARGET_INNER_RADIUS, 2)
            # Center dot (red)
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), TARGET_CENTER_RADIUS)
            # Center dot inner (white)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), TARGET_CENTER_RADIUS - 3)
        else:
            # Hit effect - brief flash
            if time.time() - self.hit_time < 0.2:
                pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), TARGET_OUTER_RADIUS)
    
    def is_clicked(self, click_x, click_y):
        """Check if the target was clicked"""
        distance = math.sqrt((click_x - self.x) ** 2 + (click_y - self.y) ** 2)
        return distance <= TARGET_OUTER_RADIUS
    
    def get_hit_score(self, click_x, click_y):
        """Calculate score based on distance from center"""
        distance = math.sqrt((click_x - self.x) ** 2 + (click_y - self.y) ** 2)
        
        if distance <= TARGET_CENTER_RADIUS:
            return 100  # Bullseye
        elif distance <= TARGET_INNER_RADIUS:
            # Inner ring: 60-80 points based on distance
            return max(60, 80 - int((distance - TARGET_CENTER_RADIUS) * 2))
        elif distance <= TARGET_OUTER_RADIUS:
            # Outer ring: 10-50 points based on distance
            return max(10, 50 - int((distance - TARGET_INNER_RADIUS) * 2))
        else:
            return 0  # Miss
    
    def move_to_random_position(self):
        """Move target to a random position on screen"""
        margin = TARGET_OUTER_RADIUS + 10
        self.x = random.randint(margin, WINDOW_WIDTH - margin)
        self.y = random.randint(margin, WINDOW_HEIGHT - margin)
        self.hit = False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("FPS AIM Trainer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.state = "start"  # start, playing, finished
        self.start_time = 0
        self.score = 0
        self.hits = 0
        self.total_clicks = 0
        self.hit_scores = []
        
        # Target
        self.target = Target(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r and self.state == "finished":
                    self.restart_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos[0], event.pos[1])
        
        return True
    
    def handle_click(self, x, y):
        """Handle mouse clicks"""
        if self.state == "start":
            # Check if clicked on center target to start game
            if self.target.is_clicked(x, y):
                self.start_game()
        
        elif self.state == "playing":
            self.total_clicks += 1
            
            if self.target.is_clicked(x, y):
                # Hit!
                hit_score = self.target.get_hit_score(x, y)
                self.score += hit_score
                self.hits += 1
                self.hit_scores.append(hit_score)
                self.target.hit = True
                self.target.hit_time = time.time()
                
                # Move target to new position after short delay
                self.target.move_to_random_position()
    
    def start_game(self):
        """Start the game"""
        self.state = "playing"
        self.start_time = time.time()
        self.score = 0
        self.hits = 0
        self.total_clicks = 0
        self.hit_scores = []
        self.target.move_to_random_position()
    
    def restart_game(self):
        """Restart the game"""
        self.state = "start"
        self.target.x = WINDOW_WIDTH // 2
        self.target.y = WINDOW_HEIGHT // 2
        self.target.hit = False
    
    def update(self):
        """Update game logic"""
        if self.state == "playing":
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= GAME_TIME:
                self.state = "finished"
    
    def draw_start_screen(self):
        """Draw the start screen"""
        self.screen.fill(DARK_GRAY)
        
        # Title
        title = self.big_font.render("FPS AIM TRAINER", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "Click the center target to start",
            "You have 60 seconds to hit as many targets as possible",
            "Accuracy matters - closer to center = higher score",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, LIGHT_GRAY)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 40))
            self.screen.blit(text, text_rect)
        
        # Draw center target
        self.target.draw(self.screen)
        
        # Click to start text
        start_text = self.font.render("CLICK TARGET TO START", True, YELLOW)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
        self.screen.blit(start_text, start_rect)
    
    def draw_game_screen(self):
        """Draw the game screen"""
        self.screen.fill(BLACK)
        
        # Draw target
        self.target.draw(self.screen)
        
        # Draw UI
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, GAME_TIME - elapsed_time)
        
        # Timer
        timer_text = self.font.render(f"Time: {remaining_time:.1f}s", True, WHITE)
        self.screen.blit(timer_text, (10, 10))
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 50))
        
        # Hits
        hits_text = self.font.render(f"Hits: {self.hits}/{self.total_clicks}", True, WHITE)
        self.screen.blit(hits_text, (10, 90))
        
        # Accuracy
        accuracy = (self.hits / self.total_clicks * 100) if self.total_clicks > 0 else 0
        accuracy_text = self.font.render(f"Accuracy: {accuracy:.1f}%", True, WHITE)
        self.screen.blit(accuracy_text, (10, 130))
        
        # Crosshair at mouse position
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(self.screen, WHITE, 
                        (mouse_pos[0] - 10, mouse_pos[1]), 
                        (mouse_pos[0] + 10, mouse_pos[1]), 2)
        pygame.draw.line(self.screen, WHITE, 
                        (mouse_pos[0], mouse_pos[1] - 10), 
                        (mouse_pos[0], mouse_pos[1] + 10), 2)
    
    def draw_end_screen(self):
        """Draw the end screen with final score"""
        self.screen.fill(DARK_GRAY)
        
        # Game Over
        game_over = self.big_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(game_over, game_over_rect)
        
        # Final Score
        final_score = self.big_font.render(f"FINAL SCORE: {self.score}", True, YELLOW)
        score_rect = final_score.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(final_score, score_rect)
        
        # Statistics
        accuracy = (self.hits / self.total_clicks * 100) if self.total_clicks > 0 else 0
        avg_score = sum(self.hit_scores) / len(self.hit_scores) if self.hit_scores else 0
        
        stats = [
            f"Targets Hit: {self.hits}",
            f"Total Clicks: {self.total_clicks}",
            f"Accuracy: {accuracy:.1f}%",
            f"Average Hit Score: {avg_score:.1f}",
            f"Hits per Second: {self.hits / GAME_TIME:.1f}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, LIGHT_GRAY)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 350 + i * 30))
            self.screen.blit(text, text_rect)
        
        # Performance rating
        if accuracy >= 80 and avg_score >= 80:
            rating = "EXCELLENT!"
            color = GREEN
        elif accuracy >= 60 and avg_score >= 60:
            rating = "GOOD"
            color = YELLOW
        elif accuracy >= 40 and avg_score >= 40:
            rating = "FAIR"
            color = ORANGE
        else:
            rating = "NEEDS PRACTICE"
            color = RED
        
        rating_text = self.big_font.render(rating, True, color)
        rating_rect = rating_text.get_rect(center=(WINDOW_WIDTH // 2, 550))
        self.screen.blit(rating_text, rating_rect)
        
        # Restart instruction
        restart_text = self.font.render("Press R to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        """Main draw function"""
        if self.state == "start":
            self.draw_start_screen()
        elif self.state == "playing":
            self.draw_game_screen()
        elif self.state == "finished":
            self.draw_end_screen()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()