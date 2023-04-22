#! /usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from scipy.io import wavfile

# Source: https://stackoverflow.com/questions/33933842/how-to-generate-noise-in-frequency-range-with-numpy
def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return np.fft.ifft(f).real

def band_limited_noise(min_freq, max_freq, samples=1024, samplerate=1):
    freqs = np.abs(np.fft.fftfreq(samples, 1/samplerate))
    f = np.zeros(samples)
    idx = np.where(np.logical_and(freqs>=min_freq, freqs<=max_freq))[0]
    f[idx] = 1
    return fftnoise(f)

def plot_fft(s, sample_rate, name):
    ps = np.abs(np.fft.fft(s))**2
    time_step = 1/sample_rate
    freqs = np.fft.fftfreq(s.size, time_step)
    idx = np.argsort(freqs)
    plt.figure(figsize=(20,10))
    plt.plot(freqs[idx], ps[idx])
    plt.savefig(name+".svg")
    plt.savefig(name+".png")

def am_modulation(msg, carrier_freq, carrier_ampl, msg_freq, msg_ampl, modulation_idx):
    len_t = len(msg) / msg_freq


def gen_noise_wave():
    sample_rate = 44100
    x = band_limited_noise(200, 20000, 20*sample_rate, sample_rate)
    x = np.int16(x * (2**15 - 1))
    #x = x * 32767

    plot_fft(x, "orig")
    wavfile.write("test.wav", sample_rate, x)


def am_demo():
    duration        = 1 


    msg_ampl        = 50
    msg_rate        = 44100
    modulation_idx  = 1

    carrier_f       = msg_rate * 5
    carrier_ampl    = 1

    sample_rate     = carrier_f * 10  # 10 samples per carrier cycle
    
    msg = msg_ampl * band_limited_noise(4000, 20000, duration*msg_rate, 44100)
    msg_resamp = signal.resample(msg, duration * sample_rate)

    plt.figure(figsize=(20,10))
    plt.plot(msg[0:1000])
    plt.savefig("msg.png")

    plot_fft(msg, msg_rate, "msg_fft")

    plt.figure(figsize=(20,10))
    plt.plot(msg_resamp[0:25 * sample_rate//msg_rate])
    plt.savefig("msg_resamp.png")
    plot_fft(msg_resamp, sample_rate, "msg_resamp_fft")
    
    carrier = carrier_ampl * np.cos(2*np.pi*carrier_f*np.linspace(0, duration, duration*sample_rate))

    am_signal = carrier * (1 + modulation_idx * msg_resamp)

    plot_fft(am_signal, sample_rate, "am_signal_fft")

    plt.figure(figsize=(20,10))
    plt.plot(am_signal[0:25 * sample_rate//msg_rate])
    plt.savefig("am_signal.png")

    diode_out = am_signal * am_signal
#    diode_out[diode_out<0] = 0



    plt.figure(figsize=(20,10))
    plt.plot(diode_out[0:25 * sample_rate//msg_rate])
    plt.savefig("diode_out.png")

    b,a = signal.butter(10, msg_rate/1, btype='low', analog=False, fs=sample_rate)
    msg_out = signal.filtfilt(b,a,diode_out)

#    b,a = signal.butter(10, 100, btype='high', analog=False, fs=sample_rate)
#    msg_out = signal.filtfilt(b,a,msg_out)

    #msg_out = msg_out-np.mean(msg_out)
    #msg_out = msg_out-np.mean(msg_out)

    plt.figure(figsize=(20,10))
    plt.plot(msg_out[0:1000 * sample_rate//msg_rate])
    plt.savefig("msg_out.png")

    msg_out_decim = msg_out[::sample_rate//msg_rate] 
    print(sample_rate//msg_rate)
    print(len(msg_out))
    print(len(msg_out_decim))

    plt.figure(figsize=(20,10))
    plt.plot(msg_out_decim[0:1000])
    plt.savefig("msg_out_decim.png")

    b,a = signal.butter(5, 2000, btype='high', analog=False, fs=msg_rate)
    msg_out_decim_filt = signal.filtfilt(b,a,msg_out_decim)
    #msg_out_decim_filt = signal.lfilter(b,a,msg_out_decim)

    plt.figure(figsize=(20,10))
    plt.plot(msg_out_decim_filt[0:1000])
    plt.savefig("msg_out_decim_filt.png")

    plot_fft(msg_out_decim_filt, msg_rate, "msg_out_decim_filt_fft")

am_demo()
