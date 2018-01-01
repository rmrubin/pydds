#!/usr/bin/env python

"""mono.py: PyDDS Monophonic ADSR Synthesis Module
"""

import time as tm
import numpy as np
import matplotlib.pyplot as plt
import pyaudio

__version__     = "0.2.1"
__status__      = "Development"

__author__      = "Randy Rubin"
__copyright__   = "Copyright 2018, Randy Rubin"
__license__     = "MIT"


class DDS:

    _TAB_INDEX_BITS = 16
    _PHASE_ACC_BITS = 32
    _SAMPLE_BITS = 16
    _ENV_VAL_BITS = 16

    _TAB_LEN = int(round(2**_TAB_INDEX_BITS))
    _PHASE_ACC_MAX = int(round(2**_PHASE_ACC_BITS)) - 1
    _PHASE_ACC_SHIFT = _PHASE_ACC_BITS - _TAB_INDEX_BITS  
    _SAMPLE_ABSMAX = int(round(2**(_SAMPLE_BITS - 1))) - 1
    _ENV_VAL_ABSMAX = int(round(2**_ENV_VAL_BITS)) - 1


    def __init__(self, VERBOSE=False,
                OUT_BUF_UPDATE_MS=5,
                amp_ratio=0.25,
                freq_hz=440,
                phase_ratio=0,
                attack_ms=50,
                decay_ms=100,
                sustain_ratio=0.5,
                release_ms=333,
                cancel_ms=3,
                retrigger=False,
                recycle=True,
                decimation=False,
                bit_depth=False):
        
        self._start_time = tm.time()
        self.VERBOSE = VERBOSE

        self._verbose("Initializing synthesis module...")

        self.OUT_BUF_UPDATE_MS = OUT_BUF_UPDATE_MS
        self._init_pyaudio()

        self.set_amp_ratio(amp_ratio) 
        self.set_freq_hz(freq_hz)
        self.set_phase_ratio(phase_ratio)
        self.set_attack_ms(attack_ms) 
        self.set_decay_ms(decay_ms)
        self.set_sustain_ratio(sustain_ratio) 
        self.set_release_ms(release_ms) 
        self.set_cancel_ms(cancel_ms) 
        self.ena_retrigger() if retrigger else self.dis_retrigger() 
        self.ena_recycle() if recycle else self.dis_recycle()
        self.set_decimation(decimation) if decimation else self.dis_decimation()
        self.set_bit_depth(bit_depth) if bit_depth else self.dis_bit_depth() 

        self._load_all_tabs()
        self.sel_sin() 
        self.note_off()
        
        self._verbose("Synthesis module initialization complete.")


    def __del__(self):
        self.close()


    def _timestamp(self):
        return tm.time()-self._start_time

    def _verbose(self, msg):
        if self.VERBOSE:
            print("{:.3f} {}".format(self._timestamp(), msg))

        
    def _init_pyaudio(self):
        self._verbose("Setup audio device interface...")
        self._pa = pyaudio.PyAudio()
        self._DEV_INFO = self._pa.get_default_output_device_info()
        self._SAMPLE_RATE_HZ = int(round(self._DEV_INFO['defaultSampleRate']))
        out_buf_len = int(round(self._SAMPLE_RATE_HZ * (self.OUT_BUF_UPDATE_MS / 1000)))
        self._out_buf = np.zeros(out_buf_len, dtype=np.int16)
        self._verbose("Audio device interface is ready.")

    def _pyaudio_callback(self, in_data, frame_count, time_info, status):
        self._load_out_buf()
        return (self._out_buf, pyaudio.paContinue)
    
    def _load_out_buf(self):        
        out_buf = np.empty_like(self._out_buf)
        for i in range(self._out_buf.size):
            if (self._env_state == 'a' or self._env_state == 'd'
                    or self._env_state == 's' or self._env_state == 'r'
                    or self._env_state == 'c'):
                out_buf[i] = self._tab_wav[self._phase_acc >> self._PHASE_ACC_SHIFT]
                out_buf[i] = int(round(out_buf[i] * self._amp_ratio))
            else:
                out_buf[i] = 0
            self._phase_acc += self._tuning_freq
            self._phase_acc %= self._PHASE_ACC_MAX
        self._out_buf = out_buf    


    # interface functions

    def start(self):
        self._stream = self._pa.open(format=pyaudio.paInt16, channels=1, frames_per_buffer=self._out_buf.size,
                rate=self._SAMPLE_RATE_HZ, input=False, output=True, stream_callback=self._pyaudio_callback)
        self._stream.start_stream()
        self._stream_up = True

    def stop(self):
        if self._stream_up:
            self._stream.stop_stream()
            self._stream_up = False

    def close(self):
        self.stop()  
        self._stream.close()
        self._pa.terminate()
        
    def sel_sin(self):
        self._tab_wav = self._TAB_SIN

    def sel_sqr(self):
        self._tab_wav = self._TAB_SQR

    def sel_saw(self):
        self._tab_wav = self._TAB_SAW

    def sel_rev_saw(self):
        self._tab_wav = self._TAB_REV_SAW

    def sel_tri(self):
        self._tab_wav = self._TAB_TRI

    def note_on(self):
        self._env_state = 'a'
        
    def note_off(self):
        self._env_state = 'i'
    
    def set_amp_ratio(self, amp):
        self._amp_ratio = amp
        
    def set_freq_hz(self, freq):
        self._freq_hz = freq
        self._tuning_freq = int(round(
                (self._freq_hz / self._SAMPLE_RATE_HZ) * self._PHASE_ACC_MAX))    

    def set_phase_ratio(self, phase):
        self._phase_acc = int(round(phase * self._PHASE_ACC_MAX)) % self._PHASE_ACC_MAX

    def set_attack_ms(self, attack):
        return

    def set_decay_ms(self, decay):
        return

    def set_sustain_ratio(self, sustain):
        return

    def set_release_ms(self, release):
        return

    def set_cancel_ms(self, cancel):
        return

    def ena_retrigger(self):
        return
        
    def dis_retrigger(self): 
        return

    def ena_recycle(self):
        return

    def dis_recycle(self):
        return

    def set_decimation(self,decimation):
        return

    def dis_decimation(self):
        return

    def set_bit_depth(self,bit_depth):
        return

    def dis_bit_depth(self): 
        return


    # wave and envelope lookup tables

    def _load_sin(self):
        self._verbose("Generating sine wave table...")
        self._TAB_SIN = np.empty(self._TAB_LEN, dtype=np.int16)
        for i in range(self._TAB_SIN.size):
            sine_phase = 2 * np.pi * (float(i) / self._TAB_SIN.size)
            self._TAB_SIN[i] = int(round(self._SAMPLE_ABSMAX * np.sin(sine_phase)))
        self._verbose("Sine wave table loaded.")

    def _load_sqr(self):
        self._verbose("Generating square wave table...")     
        self._TAB_SQR = np.empty(self._TAB_LEN, dtype=np.int16)
        for i in range(self._TAB_SQR.size):
            if i <= self._TAB_SQR.size / 2:
                self._TAB_SQR[i] = self._SAMPLE_ABSMAX
            else:
                self._TAB_SQR[i] = -1 * self._SAMPLE_ABSMAX
        self._verbose("Square wave table loaded.")

    def _load_saw(self):
        self._verbose("Generating saw wave table...")
        self._TAB_SAW = np.empty(self._TAB_LEN, dtype=np.int16)
        saw_inc = (2 * self._SAMPLE_ABSMAX) / (self._TAB_SAW.size - 1)
        for i in range(self._TAB_SAW.size):
            self._TAB_SAW[i] = int(round((-1
                    * self._SAMPLE_ABSMAX) + i * saw_inc))
        self._verbose("Saw wave table loaded.")

    def _load_rev_saw(self):
        self._verbose("Generating reverse saw wave table...")  
        self._TAB_REV_SAW = np.empty(self._TAB_LEN, dtype=np.int16)
        saw_dec = (2 * self._SAMPLE_ABSMAX) / (self._TAB_REV_SAW.size - 1)
        for i in range(self._TAB_REV_SAW.size):
            self._TAB_REV_SAW[i] = int(round(self._SAMPLE_ABSMAX - i * saw_dec))
        self._verbose("Reverse saw wave table loaded.")

    def _load_tri(self):
        self._verbose("Generating triangle wave table...")     
        self._TAB_TRI = np.empty(self._TAB_LEN, dtype=np.int16)
        tri_inc = (2 * self._SAMPLE_ABSMAX) / (self._TAB_TRI.size / 2 - 1)
        for i in range(self._TAB_TRI.size // 4):
            self._TAB_TRI[i] = int(round(i * tri_inc))
        for i in range(self._TAB_TRI.size // 2):
            self._TAB_TRI[self._TAB_TRI.size // 4 + i] = int(round(self._SAMPLE_ABSMAX - i * tri_inc))
        for i in range(self._TAB_TRI.size // 4):
            self._TAB_TRI[(3 * self._TAB_TRI.size) // 4 + i] = int(round(-1 * self._SAMPLE_ABSMAX + (i) * tri_inc))
        self._verbose("Triangle wave table loaded.")

    def _load_exp(self):
        self._verbose("Generating exponential ramp table...")     
        tab_exp = np.empty(self._TAB_LEN, dtype=np.float64)
        exp_multiplier = self._ENV_VAL_ABSMAX**(1 / tab_exp.size)
        tab_exp[0] = exp_multiplier
        for i in range(1, tab_exp.size):
            tab_exp[i] = tab_exp[i-1] * exp_multiplier 
        tab_exp = np.rint(tab_exp)
        self._TAB_EXP = np.empty(tab_exp.size, dtype=np.uint16)
        self._TAB_EXP = tab_exp.astype(np.uint16)
        self._verbose("Exponential ramp table loaded.")
    
    def _load_all_tabs(self):
        self._verbose("Loading lookup tables...")
        self._load_sin()
        self._load_sqr()
        self._load_saw()
        self._load_rev_saw()
        self._load_tri()
        self._load_exp()
        self._verbose("Lookup tables ready.") 


# data array plotting functions

    def plot_tab(self, tab_name):
        if tab_name == "SIN" or tab_name == "SINE":
            tab = self._TAB_SIN
        elif tab_name == "SQR" or tab_name == "SQUARE":
            tab = self._TAB_SQR
        elif tab_name == "SAW":
            tab = self._TAB_SAW
        elif (tab_name == "REV_SAW" or tab_name == "REV SAW"
                  or tab_name == "REVSAW" or tab_name == "REVERSE_SAW"
                  or tab_name == "REVERSE SAW" or tab_name == "REVERSESAW"):
            tab = self._TAB_REV_SAW 
        elif tab_name == "TRI" or tab_name == "TRIANGLE":
            tab = self._TAB_TRI
        elif tab_name == "EXP" or tab_name == "EXPONENTIAL":
            tab = self._TAB_EXP
        else:
            return "TableNameError"
        plt.plot(range(tab.size),tab)
        plt.show()

    def plot_buf(self):
        plt.plot(range(self.out_buf.size),out_buf.buffer)
        plt.show(block=False)

