# -*- coding: utf-8 -*- 
'''
    This program will log Audio amplitude over frequncy in sqllite table.
    Tokens and Keys should be added before runing the program.
    Copyright (C) 2017 contributed by Pritam Pan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
 '''    

import pyaudio
import wave
import scipy.io.wavfile as wavfile
import numpy as np
#import pylab as pl
import time
import datetime
import threading
import sys
import os
###########################################################################
## Class Decibel
###########################################################################

class Decibel ():

    ###############
    def CurrentTime(self):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        return st

    def InputDevices(self):
        dev = []
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
        for i in range (0,numdevices):
                if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                        print "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name')
                        dev.append(p.get_device_info_by_host_api_device_index(0,i).get('name'))
        return dev

    def RecordSound(self,fl='sample.wav',id=0):
        CHUNK = 2048
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 1
        WAVE_OUTPUT_FILENAME = fl

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=id)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def CalculateDecibel(self,fl='sample.wav'):
        rate, data = wavfile.read(fl)

        p = 20*np.log10(np.abs(np.fft.rfft(data[:2048, 0])))
        f = np.linspace(0, 500,  500)
        #f = np.fft.fftfreq(len(np.abs(np.fft.fft(data[:2048, 0]))))
        #f = np.fft.fftfreq(500,1)

        #print abs(p).min(),abs(p).max()
        #print tuple(p)
        #print(abs(f * rate).min(), abs(f * rate).max())
        #print type(p),type(f)
            
        #print p
        #print max(f),len(f)
        return tuple(p)

if __name__ == "__main__":
    d = Decibel()
    # list audio devices
    d.InputDevices()
    # record a audio sample from default 0 device
    d.RecordSound()
    #calculate and print outuput value
    print(d.CalculateDecibel())
