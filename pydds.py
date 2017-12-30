
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

class pydds:

    def __init__(self, f_out=1000, f_reload=100, phase_shift=0, phase_bits=32, table_bits=16, sample_bits=16):

        self.pa = pyaudio.PyAudio()

        # setup output buffer
        self.dev_info       = self.pa.get_default_output_device_info()
        self.f_s            = self.dev_info['defaultSampleRate']
        self.f_reload       = float(f_reload)
        buffer_len          = int(round(self.f_s / self.f_reload))
        self.buffer         = np.zeros((buffer_len,), dtype=np.int16)

        # setup phase accumulator
        self.phase_bits     = int(round(phase_bits))
        self.phase_max      = int(round(2**self.phase_bits))
        self.set_phase(phase_shift)

        # setup wave table
        self.table_bits = int(round(table_bits))
        table_len = int(round(2**self.table_bits))
        self.table  = np.zeros(table_len)
        self.sample_absmax = 2**(sample_bits - 1) - 1

        # setup dds generator
        self.phase_acc_shift = self.phase_bits - self.table_bits
        self.load_sine()
        self.set_freq(f_out)
        self.note_off()

        # init pyaudio stream
        self.stream = self.pa.open(format=pyaudio.paInt16, channels=1, frames_per_buffer=self.buffer.size, rate=int(round(self.f_s)), input=False, output=True, stream_callback=self.pyaudio_callback)
        self.stream.start_stream()

    def __del__(self):
        self.close()

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        del self.stream
        del self.pa
        
    

    # parameter modification functions

    def set_freq(self, f_out):
        self.f_out = f_out
        self.tuning_word = int(round((self.f_out / self.f_s) * self.phase_max))

    def set_phase(self, shift):
        self.phase = int(round(float(shift) * self.phase_max)) % self.phase_max

    def note_on(self):
        self.note_is_on = True
        
    def note_off(self):
        self.note_is_on = False

    
    # dds synthesis
        
    def pyaudio_callback(self, in_data, frame_count, time_info, status):
        self.load_buffer()
        return (self.buffer, pyaudio.paContinue)
    
    def load_buffer(self):        
        if self.note_is_on:
            for i in range(self.buffer.size):
                self.buffer[i] = self.table[self.phase >> self.phase_acc_shift]
                self.phase += self.tuning_word
                self.phase %= self.phase_max
        else:
            for i in range(self.buffer.size):
                self.buffer[i] = 0

    # wave table generation functions

    def load_sine(self):
        table = np.empty_like(self.table)
        for i in range(table.size):
            sine_phase = 2 * np.pi * (float(i) / table.size)
            table[i] = int(round(self.sample_absmax * np.sin(sine_phase)))
        self.table = table

    def load_square(self):
        table = np.empty_like(self.table)
        for i in range(table.size):
            if i <= table.size / 2:
                table[i] = self.sample_absmax
            else:
                table[i] = -1 * self.sample_absmax
        self.table = table

    def load_saw(self):
        table = np.empty_like(self.table)
        saw_inc = (2 * self.sample_absmax) / (table.size - 1)
        for i in range(table.size):
            table[i] = int(round((-1 * self.sample_absmax) + i * saw_inc))
        self.table = table

    def load_reverse_saw(self):
        table = np.empty_like(self.table)
        saw_dec = (2 * self.sample_absmax) / (table.size - 1)
        for i in range(table.size):
            table[i] = int(round(self.sample_absmax - i * saw_dec))
        self.table = table

    def load_triangle(self):
        table = np.empty_like(self.table)
        triangle_inc = (2 * self.sample_absmax) / (table.size / 2 - 1)
        for i in range(table.size // 4):
            table[i] = int(round(i * triangle_inc))
        for i in range(table.size // 2):
            table[table.size // 4 + i] = int(round(self.sample_absmax - i * triangle_inc))
        for i in range(table.size // 4):
            table[(3 * table.size) // 4 + i] = int(round(-1 * self.sample_absmax + (i) * triangle_inc))
        self.table = table


    # data array plotting functions

    def plot_table(self):
        plt.plot(range(self.table.size),self.table)
        plt.show()

    def plot_buffer(self):
        plt.plot(range(self.buffer.size),self.buffer)
        plt.show()


