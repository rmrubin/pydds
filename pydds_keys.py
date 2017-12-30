
from pynput import keyboard as kbd
import pydds as pd
import midi_notes as mn



# dds module functions

def send_note_on(freq):
    dds.set_freq(freq)
    dds.note_on()

def send_note_off():
    dds.note_off()
    


# keyboard press event callback

def on_press(key):
    global pressed
    try:
        if key.char in keymap:              # check for valid key
            freq = keymap[key.char]         # save key's note freq
            if not freq in pressed:         # check for repeat key presses
                pressed.append(freq)        # update keystack with note freq 
                send_note_on(pressed[-1])   # send note for newest key press
        else:
            print('invalid character key: {0}'.format(key.char))
    except AttributeError:                   
        if  key == kbd.Key.esc:             # exit the program by shutting
            print("exiting, bye.")          # down the keyboard listener
            return False
        else:                               
            print('invalid special key: {0}'.format(key))



# keyboard release event callback
        
def on_release(key):
    global pressed
    try:
        if key.char in keymap:                  # check for valid key
            last_key = pressed[-1]              # save last key pressed
            pressed.remove(keymap[key.char])    # remove lifted key from keystack
            try:
                if pressed[-1] != last_key:     # send new note if last key 
                    send_note_on(pressed[-1])   # pressed was lifted 
            except IndexError:                  # send note off if all
                send_note_off()                 # valid keys lifted
    except AttributeError:  # invalid special character
        return True         # keep keyboard listener on
    except ValueError:      # invalid alphanumeric character
        return True         # keep keyboard listener on



# main()

print('synthesizer initializing...')
        
dds = pd.pydds()

# define keymap

keymap = {}
keymap['z'] = "C4"
keymap['s'] = "C#4"
keymap['x'] = "D4"
keymap['d'] = "D#4"
keymap['c'] = "E4"
keymap['v'] = "F4"
keymap['g'] = "F#4"
keymap['b'] = "G4"
keymap['h'] = "G#4"
keymap['n'] = "A4"
keymap['j'] = "A#4"
keymap['m'] = "B4"
keymap[','] = "C5"
keymap['l'] = "C#5"
keymap['.'] = "D5"
keymap[';'] = "D#5"
keymap['/'] = "E5"
keymap['q'] = "F5"
keymap['2'] = "F#5"
keymap['w'] = "G5"
keymap['3'] = "G#5"
keymap['e'] = "A5"
keymap['4'] = "A#5"
keymap['r'] = "B5"
keymap['t'] = "C6"
keymap['6'] = "C#6"
keymap['y'] = "D6"
keymap['7'] = "D#6"
keymap['u'] = "E6"
keymap['i'] = "F6"
keymap['9'] = "F#6"
keymap['o'] = "G6"
keymap['0'] = "G#6"
keymap['p'] = "A6"
keymap['-'] = "A#6"
keymap['['] = "B6"
keymap[']'] = "C7"

# replace note strings with frequency floats

midi_note_freqs = mn.freqs()
midi_note_names = mn.names()

for key in keymap.keys():
    keymap[key] = midi_note_freqs[midi_note_names.index(keymap[key])] 

# create key stack

pressed = [] 

# start key press event listener

print('synthesizer ready.')

with kbd.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# on keyboard listener exit shutdown the dds audio stream

dds.close()
exit()

