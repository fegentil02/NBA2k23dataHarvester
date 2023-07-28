
import pyaudio
import numpy as np
import tempfile
import wave
import keyboard


def stream(duration = 1.2 , sr = 44100, format = pyaudio.paInt32, channels = 1, chunk = 1024):
    p = pyaudio.PyAudio()
    dev_index = 0
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
            dev_index = dev['index']
    
    stream = p.open(format=format,channels=channels,rate=sr,input=True,input_device_index = dev_index,frames_per_buffer=chunk)
    frames = []
    for i in range(0, int(sr /chunk * duration)):
        data = stream.read(chunk)    
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open('temp.wav', 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(sr)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return

def record(duration = 1, sr = 44100, format = pyaudio.paInt32, channels = 1, chunk = 1024, fileName = "output.wav"):
    p = pyaudio.PyAudio()
    dev_index = 0
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
            dev_index = dev['index']
    recording = True
    print('Press Enter to Start Recording')
    keyboard.wait('enter')
    stream = p.open(format=format,channels=channels,rate=sr,input=True,input_device_index = dev_index,frames_per_buffer=chunk)
    frames = []
    while recording:
        print("Recording...")
        for i in range(0, int(sr /chunk * duration)):
            data = stream.read(chunk)    
            frames.append(data)
        if keyboard.is_pressed('space'):
            recording = False
    print("Done Recording")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(fileName, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(sr)
    wf.writeframes(b''.join(frames))
    wf.close()
    return       


def main():
    record()


if __name__ == "__main__":
    main()

