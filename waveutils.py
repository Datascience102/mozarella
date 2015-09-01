import struct
import wave

def wav_encode(chunk_raw):
    return b''.join([struct.pack('h', value) for value in chunk_raw])
    
def wav_save(chunk, filename, channels=1, rate=44100):
    if isinstance(chunk, list):
        chunk = wav_encode(chunk)
     
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(2)
    waveFile.setframerate(rate)
    waveFile.writeframes(chunk)
    waveFile.close()