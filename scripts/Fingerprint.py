import numpy as np
import librosa
from hashlib import sha1

def fingerprint(audio_path, sr = 44100):
    #Reads audio file
    audio, _ = librosa.load(audio_path, sr=sr, mono=True)
    
    # Applies Simple Fourier Transform
    stft = librosa.stft(audio, n_fft=2048, hop_length=512)
    
    
    # Finds Local Maximums and makes it 1D
    peaks = librosa.util.localmax(np.abs(stft))
    peaks = peaks.flatten()
    
    #Finds The indexes of the local maximums(peaks)
    peakIndex = []
    for i in range(0, len(peaks)):
        if peaks[i] and i >= len(peakIndex):
            peakIndex.append(i)
    #Splits the peaks array into subsections from one peak to the next
    peakSections = np.split(peaks, peakIndex)

    #Fingerprints every subssection
    fingerprints = []
    for j in peakSections:
        # Cria a fingerprint a partir dos picos
        fingerprint = sha1(j.tobytes()).hexdigest()
        fingerprints.append(fingerprint)
    
    return fingerprints

def compare(fingerprint1, fingerprint2):
    close = 0
    #Sorts the fingerprints for faster searching
    fingerprint1 = np.sort(fingerprint1)
    fingerprint2 = np.sort(fingerprint2)
    #Compares both fingerprints and returns closeness percentage
    if len(fingerprint1) <= len(fingerprint2):
        for i in range(len(fingerprint1) - 1):
            if fingerprint1[i] == fingerprint2[i]:
                close += 1
        return (close/len(fingerprint1))*100
    else:
        for i in range(len(fingerprint2) - 1):
            if fingerprint1[i] == fingerprint2[i]:
                close += 1  
        return (close/len(fingerprint2))*100 
    
def main():
    fingerprint1 = fingerprint('audio/make1.wav')
    fingerprint2 = fingerprint('audio/make4.wav')
    close = compare(fingerprint1, fingerprint2)
    print(close)

if __name__ == "__main__":
    main()