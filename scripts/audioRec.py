
import pyaudio
import wave
import keyboard

def get_index(p):
    
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev['name'] == 'Microsoft Sound Mapper - Input':
            dev_index = dev['index']
            return dev_index

def stream(duration = 1.3 , sr = 44100, format = pyaudio.paInt32, channels = 1, chunk = 1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=format,channels=channels,rate=sr,input=True,frames_per_buffer=chunk)
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
   
    recording = True
    print('Press Enter to Start Recording')
    keyboard.wait('enter')
    stream = p.open(format=format,channels=channels,rate=sr,input=True,frames_per_buffer=chunk, input_device_index=7)
    frames = []
    while recording:
        print("Recording... Hold space to end recording")
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

