#implementation of a simple multimedia application that integrates sound,
# image and video elements

import pygame # type: ignore
import sys
import os
import numpy as np  # type: ignore
import io
from pygame import gfxdraw # type: ignore

class SimpleMultimediaApp:
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Simple Multimedia Application")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (100, 100, 255)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        
        # Font
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        # Create media IN-MEMORY (no external files needed)
        self.create_media_in_memory()
        
        # State variables
        self.current_mode = "menu"
        self.sound_playing = False
        self.video_playing = False
        self.video_time = 0
        self.video_frame = 0
        self.clock = pygame.time.Clock()
        
    def create_media_in_memory(self):
        """Create all media content programmatically - NO EXTERNAL FILES NEEDED"""
        
        # 1. CREATE IMAGE IN MEMORY
        self.create_image_in_memory()
        
        # 2. CREATE SOUND IN MEMORY
        self.create_sound_in_memory()
        
        # 3. CREATE VIDEO FRAMES IN MEMORY (as a list of surfaces)
        self.create_video_in_memory()
        
    def create_image_in_memory(self):
        """Create an image surface programmatically"""
        self.image = pygame.Surface((400, 300))
        self.image.fill((240, 240, 255))  # Light blue background
        
        # Draw shapes
        pygame.draw.circle(self.image, self.RED, (100, 100), 40)
        pygame.draw.rect(self.image, self.GREEN, (180, 70, 100, 100))
        pygame.draw.polygon(self.image, self.BLUE, [(320, 100), (280, 180), (360, 180)])
        
        # Add text to image
        text = self.font.render("Sample Image", True, self.BLACK)
        self.image.blit(text, (140, 220))
        
        # Draw a gradient effect
        for i in range(300):
            color_val = 150 + int(100 * i / 300)
            pygame.draw.line(self.image, (color_val, color_val, 255), (0, i), (400, i))
        
    def create_sound_in_memory(self):
        """Create a sound buffer programmatically"""
        try:
            # Create a sine wave sound
            sample_rate = 44100
            duration = 2.0  # seconds
            freq = 440.0  # A4 note
            
            # Generate samples
            n_samples = int(sample_rate * duration)
            buf = np.zeros((n_samples, 2), dtype=np.int16)
            
            max_sample = 2**(16 - 1) - 1
            
            for i in range(n_samples):
                t = float(i) / sample_rate
                
                # Create a chord (multiple frequencies)
                sample = 0.5 * np.sin(2 * np.pi * freq * t)
                sample += 0.3 * np.sin(2 * np.pi * freq * 1.5 * t)  # Fifth
                sample += 0.2 * np.sin(2 * np.pi * freq * 2 * t)    # Octave
                
                # Apply envelope
                envelope = np.exp(-2 * t) * (1 - np.exp(-10 * t))
                sample *= envelope
                
                # Convert to 16-bit integer
                sample_val = int(max_sample * sample)
                buf[i] = [sample_val, sample_val]  # Stereo
            
            # Convert to pygame sound
            self.sound = pygame.sndarray.make_sound(buf)
            
        except:
            # Fallback: create a simple beep using pygame.mixer.Sound
            self.sound = pygame.mixer.Sound(buffer=bytes([128] * 8000))
    
    def create_video_in_memory(self):
        """Create a sequence of frames for video animation"""
        self.video_frames = []
        self.video_duration = 5.0  # 5 seconds
        fps = 30
        
        # Create frames for the video
        for frame_num in range(int(self.video_duration * fps)):
            frame = self.create_video_frame(frame_num, fps)
            self.video_frames.append(frame)
        
        self.total_video_frames = len(self.video_frames)
    
    def create_video_frame(self, frame_num, fps):
        """Create a single video frame"""
        frame = pygame.Surface((400, 300))
        
        # Animated background gradient
        time_val = frame_num / fps
        hue = (np.sin(time_val * 2) + 1) * 128
        
        for y in range(300):
            # Create gradient effect
            r = int(100 + 100 * np.sin(y/50 + time_val))
            g = int(100 + 100 * np.sin(y/30 + time_val*1.5))
            b = int(200 + 55 * np.sin(y/40 + time_val*2))
            pygame.draw.line(frame, (r, g, b), (0, y), (400, y))
        
        # Animated bouncing ball
        ball_radius = 30
        ball_x = 200 + int(150 * np.sin(time_val * 3))
        ball_y = 150 + int(100 * np.cos(time_val * 2))
        
        # Draw ball with gradient
        for r in range(ball_radius, 0, -1):
            color_val = 255 - int(200 * r / ball_radius)
            pygame.draw.circle(frame, (color_val, 100, 100), (ball_x, ball_y), r)
        
        # Rotating square
        square_size = 40
        angle = time_val * 180  # degrees
        points = []
        for i in range(4):
            theta = np.radians(angle + i * 90)
            x = 300 + square_size * np.cos(theta)
            y = 100 + square_size * np.sin(theta)
            points.append((x, y))
        pygame.draw.polygon(frame, (100, 200, 100), points)
        
        # Moving triangle
        tri_x = 100 + int(50 * np.sin(time_val * 4))
        tri_points = [
            (tri_x, 200),
            (tri_x - 30, 250),
            (tri_x + 30, 250)
        ]
        pygame.draw.polygon(frame, (100, 100, 255), tri_points)
        
        # Frame counter
        counter_text = self.small_font.render(f"Frame: {frame_num}", True, self.WHITE)
        frame.blit(counter_text, (10, 10))
        
        # Time display
        time_text = self.small_font.render(f"Time: {time_val:.2f}s", True, self.WHITE)
        frame.blit(time_text, (10, 270))
        
        return frame
    
    def draw_menu(self):
        """Draw the main menu"""
        self.screen.fill(self.WHITE)
        
        # Title with gradient
        title = self.font.render("Simple Multimedia Application", True, self.BLUE)
        title_shadow = self.font.render("Simple Multimedia Application", True, (200, 200, 255))
        self.screen.blit(title_shadow, (self.screen_width//2 - title.get_width()//2 + 2, 52))
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        
        # Draw decorative elements
        pygame.draw.circle(self.screen, (255, 200, 200), (100, 150), 40)
        pygame.draw.rect(self.screen, (200, 255, 200), (self.screen_width - 150, 100, 80, 80))
        
        # Menu options
        options = [
            ("1", "Display Image", "Show generated image"),
            ("2", "Play Sound", "Play generated audio"),
            ("3", "Play Video", "Watch generated animation"),
            ("4", "Exit", "Close application")
        ]
        
        y_offset = 180
        for key, title, desc in options:
            # Draw option box
            option_rect = pygame.Rect(150, y_offset, 500, 70)
            pygame.draw.rect(self.screen, (240, 240, 255), option_rect, border_radius=10)
            pygame.draw.rect(self.screen, self.BLUE, option_rect, 2, border_radius=10)
            
            # Key
            key_text = self.font.render(f"[{key}]", True, self.RED)
            self.screen.blit(key_text, (170, y_offset + 20))
            
            # Title
            title_text = self.font.render(title, True, self.BLACK)
            self.screen.blit(title_text, (230, y_offset + 20))
            
            # Description
            desc_text = self.small_font.render(desc, True, (100, 100, 100))
            self.screen.blit(desc_text, (230, y_offset + 50))
            
            y_offset += 90
    
    def display_image(self):
        """Display the generated image"""
        self.screen.fill(self.WHITE)
        
        title = self.font.render("Image Display Mode", True, self.BLUE)
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 20))
        
        # Display image with border
        img_rect = self.image.get_rect(center=(self.screen_width//2, self.screen_height//2))
        pygame.draw.rect(self.screen, (100, 100, 100), img_rect.inflate(20, 20), border_radius=10)
        self.screen.blit(self.image, img_rect)
        
        # Image info
        info = [
            f"Resolution: {self.image.get_width()}x{self.image.get_height()}",
            "Format: RGB",
            "Generated: Programmatically"
        ]
        
        y_offset = self.screen_height - 100
        for line in info:
            text = self.small_font.render(line, True, self.BLACK)
            self.screen.blit(text, (20, y_offset))
            y_offset += 25
        
        # Instructions
        instr = self.small_font.render("Press ESC to return to menu", True, (100, 100, 100))
        self.screen.blit(instr, (self.screen_width//2 - instr.get_width()//2, self.screen_height - 30))
    
    def play_sound(self):
        """Play the generated sound"""
        self.screen.fill(self.WHITE)
        
        title = self.font.render("Sound Player Mode", True, self.BLUE)
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 20))
        
        # Draw sound visualization
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Draw speaker icon
        pygame.draw.rect(self.screen, (200, 200, 200), (center_x - 60, center_y - 100, 120, 200), border_radius=10)
        
        # Sound waves animation
        if self.sound_playing:
            time_val = pygame.time.get_ticks() / 1000.0
            for i in range(1, 6):
                radius = 50 + i * 20 + 10 * np.sin(time_val * 10 + i)
                pygame.draw.circle(self.screen, (100, 150, 255), (center_x, center_y), int(radius), 2)
        
        # Speaker cones
        pygame.draw.rect(self.screen, (100, 100, 100), (center_x - 30, center_y - 70, 60, 140))
        for y in range(center_y - 60, center_y + 60, 20):
            pygame.draw.line(self.screen, (150, 150, 150), (center_x - 25, y), (center_x + 25, y), 2)
        
        # Status display
        status_box = pygame.Rect(center_x - 100, center_y + 80, 200, 60)
        pygame.draw.rect(self.screen, (240, 240, 240), status_box, border_radius=10)
        pygame.draw.rect(self.screen, self.GREEN if self.sound_playing else self.RED, status_box, 2, border_radius=10)
        
        status = "PLAYING" if self.sound_playing else "STOPPED"
        status_color = self.GREEN if self.sound_playing else self.RED
        status_text = self.font.render(status, True, status_color)
        self.screen.blit(status_text, (center_x - status_text.get_width()//2, center_y + 95))
        
        # Controls
        controls = [
            "SPACE: Play/Pause",
            "S: Stop Sound",
            "R: Restart Sound",
            "ESC: Return to Menu"
        ]
        
        y_offset = self.screen_height - 150
        for control in controls:
            text = self.small_font.render(control, True, self.BLUE)
            self.screen.blit(text, (center_x - text.get_width()//2, y_offset))
            y_offset += 30
    
    def play_video(self):
        """Play the generated video animation"""
        self.screen.fill((50, 50, 50))  # Dark background for video
        
        title = self.font.render("Video Player Mode", True, (255, 255, 200))
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 20))
        
        # Update video time if playing
        if self.video_playing:
            self.video_time += self.clock.get_time() / 1000.0
            if self.video_time > self.video_duration:
                self.video_time = 0
            
            # Calculate current frame
            fps = 30
            self.video_frame = int(self.video_time * fps) % self.total_video_frames
        
        # Display current video frame with border
        video_surface = self.video_frames[self.video_frame]
        video_rect = video_surface.get_rect(center=(self.screen_width//2, self.screen_height//2 - 30))
        
        # Draw video border
        border_color = (0, 200, 0) if self.video_playing else (200, 200, 0)
        pygame.draw.rect(self.screen, border_color, video_rect.inflate(20, 20), 3, border_radius=5)
        
        # Draw play indicator
        if self.video_playing:
            pygame.draw.circle(self.screen, (0, 255, 0), (self.screen_width//2, 70), 8)
        
        self.screen.blit(video_surface, video_rect)
        
        # Video progress bar
        progress_width = 400
        progress_height = 20
        progress_x = self.screen_width//2 - progress_width//2
        progress_y = self.screen_height - 100
        
        # Background of progress bar
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (progress_x, progress_y, progress_width, progress_height), 
                        border_radius=10)
        
        # Progress fill
        if self.video_duration > 0:
            progress = self.video_time / self.video_duration
            fill_width = int(progress_width * progress)
            pygame.draw.rect(self.screen, (0, 200, 0), 
                            (progress_x, progress_y, fill_width, progress_height), 
                            border_radius=10)
        
        # Time display
        time_text = f"{self.video_time:.2f} / {self.video_duration:.2f} seconds"
        time_surface = self.small_font.render(time_text, True, self.WHITE)
        self.screen.blit(time_surface, (self.screen_width//2 - time_surface.get_width()//2, progress_y - 25))
        
        # Frame info
        frame_info = f"Frame: {self.video_frame + 1}/{self.total_video_frames}"
        frame_surface = self.small_font.render(frame_info, True, self.WHITE)
        self.screen.blit(frame_surface, (self.screen_width//2 - frame_surface.get_width()//2, progress_y + 30))
        
        # Controls
        controls = [
            "SPACE: Play/Pause",
            "R: Restart Video",
            "LEFT/RIGHT: Seek Frame",
            "ESC: Return to Menu"
        ]
        
        y_offset = self.screen_height - 40
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, (200, 200, 100))
            x_pos = 20 + i * 200 if i < 2 else 20 + (i-2) * 200
            self.screen.blit(text, (x_pos, y_offset))
    
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # Menu navigation
                if self.current_mode == "menu":
                    if event.key == pygame.K_1:
                        self.current_mode = "image"
                    elif event.key == pygame.K_2:
                        self.current_mode = "sound"
                    elif event.key == pygame.K_3:
                        self.current_mode = "video"
                        self.video_playing = True
                        self.video_time = 0
                    elif event.key == pygame.K_4:
                        return False
                
                # Return to menu from any mode
                if event.key == pygame.K_ESCAPE:
                    if self.current_mode == "sound" and self.sound_playing:
                        self.sound.stop()
                        self.sound_playing = False
                    self.current_mode = "menu"
                    self.video_playing = False
                
                # Sound controls
                if self.current_mode == "sound":
                    if event.key == pygame.K_SPACE:
                        if self.sound_playing:
                            self.sound.stop()
                        else:
                            self.sound.play(-1)  # Loop indefinitely
                        self.sound_playing = not self.sound_playing
                    elif event.key == pygame.K_s:
                        self.sound.stop()
                        self.sound_playing = False
                    elif event.key == pygame.K_r:
                        self.sound.stop()
                        self.sound.play(-1)
                        self.sound_playing = True
                
                # Video controls
                if self.current_mode == "video":
                    if event.key == pygame.K_SPACE:
                        self.video_playing = not self.video_playing
                    elif event.key == pygame.K_r:
                        self.video_time = 0
                        self.video_playing = True
                    elif event.key == pygame.K_LEFT:
                        self.video_time = max(0, self.video_time - 0.1)
                        self.video_frame = int(self.video_time * 30) % self.total_video_frames
                    elif event.key == pygame.K_RIGHT:
                        self.video_time = min(self.video_duration, self.video_time + 0.1)
                        self.video_frame = int(self.video_time * 30) % self.total_video_frames
        
        return True
    
    def run(self):
        """Main application loop"""
        print("=" * 50)
        print("Simple Multimedia Application")
        print("=" * 50)
        print("Features:")
        print("1. Image: Programmatically generated image")
        print("2. Sound: Generated audio with visualization")
        print("3. Video: Real-time animation as video")
        print("=" * 50)
        print("\nControls:")
        print("- Use 1-4 keys to navigate")
        print("- SPACE: Play/Pause")
        print("- ESC: Return to menu")
        print("=" * 50)
        
        while True:
            if not self.handle_events():
                break
            
            # Draw based on current mode
            if self.current_mode == "menu":
                self.draw_menu()
            elif self.current_mode == "image":
                self.display_image()
            elif self.current_mode == "sound":
                self.play_sound()
            elif self.current_mode == "video":
                self.play_video()
            
            pygame.display.flip()
            self.clock.tick(30)  # 30 FPS for smooth video
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = SimpleMultimediaApp()
    app.run()