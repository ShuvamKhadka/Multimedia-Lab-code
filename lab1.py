import numpy as np # type: ignore
import sounddevice as sd # type: ignore

# Configuration
sample_rate = 44100
duration = 2
t = np.linspace(0, duration, int(sample_rate * duration))
frequency = 440.0

# Base sound for manipulation
sine_wave = np.sin(2 * np.pi * frequency * t)

print("=== AUDIO SYNTHESIS ===")
# Synthesis techniques
sd.play(sine_wave, sample_rate)
sd.wait()
print("✓ Sine wave")

sd.play(np.sign(sine_wave), sample_rate)
sd.wait()
print("✓ Square wave")

sd.play(2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1, sample_rate)
sd.wait()
print("✓ Triangle wave")

print("=== AUDIO MANIPULATION ===")
# Manipulation techniques
sd.play(sine_wave * 0.3, sample_rate)  # Volume reduction
sd.wait()
print("✓ Volume change (quiet)")

sd.play(sine_wave[::2], sample_rate//2)  # Speed change
sd.wait()
print("✓ Speed change (fast)")

sd.play(sine_wave[::-1], sample_rate)  # Reverse
sd.wait()
print("✓ Reverse audio")

# Fade effect
fade_samples = int(0.5 * sample_rate)
fade_in = np.linspace(0, 1, fade_samples)
faded = sine_wave.copy()
faded[:fade_samples] *= fade_in
sd.play(faded, sample_rate)
sd.wait()
print("✓ Fade effect")
print("Lab completed! Covered both synthesis AND manipulation.")