import pygame # type: ignore
import pygame.midi # type: ignore

#initialize 
pygame.init()
pygame.midi.init()

screen = pygame.display.set_mode((800, 500))   
pygame.display.set_caption("MIDI Piano")
font = pygame.font.Font(None, 48)

try:
    midi_out = pygame.midi.Output(0)
except:
    midi_out = None

# Extended piano keys - 2 octaves (21 keys)
keys = [
    (pygame.K_z, 48, "Z"), (pygame.K_x, 50, "X"), (pygame.K_c, 52, "C"), 
    (pygame.K_v, 53, "V"), (pygame.K_b, 55, "B"), (pygame.K_n, 57, "N"), 
    (pygame.K_m, 59, "M"),
    (pygame.K_a, 60, "A"), (pygame.K_s, 62, "S"), (pygame.K_d, 64, "D"), 
    (pygame.K_f, 65, "F"), (pygame.K_g, 67, "G"), (pygame.K_h, 69, "H"), 
    (pygame.K_j, 71, "J"),
    (pygame.K_q, 72, "Q"), (pygame.K_w, 74, "W"), (pygame.K_e, 76, "E"), 
    (pygame.K_r, 77, "R"), (pygame.K_t, 79, "T"), (pygame.K_y, 81, "Y"), 
    (pygame.K_u, 83, "U")
]

active_notes = []
current_message = "Press keyboard keys to play notes"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            for key, note, letter in keys:
                if event.key == key and note not in active_notes:
                    active_notes.append(note)
                    current_message = f"Playing: {letter} (Note {note})"
                    if midi_out:
                        midi_out.note_on(note, 127)
        
        if event.type == pygame.KEYUP:
            for key, note, letter in keys:
                if event.key == key and note in active_notes:
                    active_notes.remove(note)
                    if midi_out:
                        midi_out.note_off(note, 127)
                    
                    if not active_notes:
                        current_message = "Press keyboard keys to play notes"
    
    screen.fill((0, 0, 0))
    
    # Draw instructions
    instr = font.render(current_message, True, (255, 255, 255))
    screen.blit(instr, (50, 30))
    
    quit_text = font.render("Press ESC to exit", True, (255, 255, 255))
    screen.blit(quit_text, (50, 70))
    
    # Draw piano keys in 3 rows 
    # Row 1: Low octave (Z-X-C-V-B-N-M)
    for i, (key, note, letter) in enumerate(keys[0:7]):
        color = (255, 0, 0) if note in active_notes else (200, 200, 200)
        pygame.draw.rect(screen, color, (50 + i*80, 120, 60, 80))
        
        # Show letter on keyboard
        letter_text = font.render(letter, True, (0, 0, 0))
        screen.blit(letter_text, (70 + i*80, 150))
    
    # Row 2: Middle octave (A-S-D-F-G-H-J)
    for i, (key, note, letter) in enumerate(keys[7:14]):
        color = (255, 0, 0) if note in active_notes else (255, 255, 255)
        pygame.draw.rect(screen, color, (50 + i*80, 220, 60, 80))
        
        letter_text = font.render(letter, True, (0, 0, 0))
        screen.blit(letter_text, (70 + i*80, 250))
    
    # Row 3: High octave (Q-W-E-R-T-Y-U)
    for i, (key, note, letter) in enumerate(keys[14:21]):
        color = (255, 0, 0) if note in active_notes else (200, 200, 255)
        pygame.draw.rect(screen, color, (50 + i*80, 320, 60, 80))
        
        letter_text = font.render(letter, True, (0, 0, 0))
        screen.blit(letter_text, (70 + i*80, 350))
    
    pygame.display.flip()

if midi_out:
    midi_out.close()
pygame.midi.quit()
pygame.quit()