
import board
import digitalio
import audioio
import neopixel
import time
import array
import math


pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.01)
# enable the speaker
spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True

audiofiles = ["rimshot.wav"]

SAMPLERATE = 8000
jingle = [392, 659, 587, 523, 392, 392, 392, 392, 659, 587, 523, 440, 0,
          440, 698, 659, 587, 493,   0, 784, 784, 698, 587, 659, 0,
          392, 659, 587, 523, 392,   0, 392, 659, 587, 523, 440, 440,
          440, 698, 659, 587, 784, 784, 784, 784, 880, 784, 698, 587, 523, 784,
          659, 659, 659, 659, 659, 659, 784, 523, 587, 659, 0,
          698, 698, 698, 698, 698, 659, 659, 659, 659, 659, 587, 587, 659, 587, 784,
          659, 659, 659, 659, 659, 659, 784, 523, 587, 659, 0,
          698, 698, 698, 698, 698, 659, 659, 659, 659, 
          784, 784, 698, 587, 523, 0]
jlength = [1, 1, 1, 1, 3, 0.5, 0.5, 1, 1, 1, 1, 3, 1, 
           1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1,
           1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
           1, 1, 2, 1, 1, 2, 1, 1, 1.5, 0.5, 3, 1,
           1, 1, 1.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 1, 2, 2,
           1, 1, 2, 1, 1, 2, 1, 1, 1.5, 0.5, 3, 1,
           1, 1, 1.5, 0.5, 1, 1, 1, 0.5, 0.5,
           1, 1, 1, 1, 4, 30]
XY = map(list, zip(jingle, jlength))

def play_file(filename):
    wave_file = open(filename, "rb")
    with audioio.WaveFile(wave_file) as wave:
        with audioio.AudioOut(board.A0) as audio:
            audio.play(wave)
            while audio.playing:
                pass

def play_tones(arr):
    cflag = 0
    audio = audioio.AudioOut(board.A0)
    for note, l in XY:
        if cflag == 0:
            pixels.fill((255, 0, 0))
            cflag = 1
        else:
            pixels.fill((0, 255, 0))
            cflag = 0
        if note != 0:
            length = SAMPLERATE // (note)
            sine_wave = array.array("H", [0] * length)
            for i in range(length):          
                sine_wave[i] = int(math.sin(math.pi * 2 * i / 18)
                                   * (2 ** 15) + 2 ** 15)                       
            sine_wave_sample = audioio.RawSample(sine_wave)
            audio.play(sine_wave_sample, loop=True)
        time.sleep(l*0.4)
    audio.play(sine_wave_sample, loop=False)
    
audio = audioio.AudioOut(board.A0)        
while True:
    cflag = 0
    for note, l in XY:
        if cflag == 0:
            pixels.fill((255, 0, 0))
            cflag = 1
        else:
            pixels.fill((0, 255, 0))
            cflag = 0
        if note != 0:
            length = SAMPLERATE // (note)
            sine_wave = array.array("H", [0] * length)
            for i in range(length):          
                sine_wave[i] = int(math.sin(math.pi * 2 * i / 18)
                                   * (2 ** 15) + 2 ** 15)                       
            sine_wave_sample = audioio.RawSample(sine_wave)
            audio.play(sine_wave_sample, loop=True)
        time.sleep(l*0.4)
    audio.play(sine_wave_sample, loop=False)
    
    while True:
        if cflag == 0:
            pixels.fill((255, 0, 0))
            cflag = 1
            time.sleep(0.5)
        else:
            pixels.fill((0, 255, 0))
            cflag = 0
            time.sleep(0.5)
