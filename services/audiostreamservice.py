import pyaudio
import audioop
FORMAT = pyaudio.paInt16
NOISE_THRESH = 2**10
class AudioStreamService:
    def __init__(self, **kwargs):
        self.audio = pyaudio.PyAudio()
        self.sample_counter = 0
        self.time = 0
        self.recording = []
        self.format = kwargs.get('format', pyaudio.paInt16)
        self.channels = kwargs.get('channels', 1)
        self.rate = kwargs.get('rate', 44100)
        self.chunk_size = kwargs.get('chunk_size', 1024)
        self.noise_thresh = kwargs.get('threshold', NOISE_THRESH)
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                      rate=self.rate, input=True, frames_per_buffer = self.chunk_size)
                      
    def noise_cancel(self, sample):
        return sample
        if abs(sample) < self.noise_thresh:
            return 0
        return sample
        
    def read_raw_chunk(self):
        self.sample_counter += self.chunk_size
        self.time += self.chunk_size / float(self.rate)
        size = max(self.chunk_size, self.stream.get_read_available())
        chunk =  self.stream.read(size)
        self.recording.append(chunk)
        return chunk
        
    def read_processed_chunk(self):
        data = self.read_raw_chunk()
        return [self.noise_cancel(audioop.getsample(data, 2, x)) for x in range(0, self.chunk_size)]
    
    def dispose(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
    def encode(self, chunk_raw):
        return b''.join([struct.pack('h', value) for value in chunk_raw])
    
    def save(self, filename):
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(audio.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(b''.join([self.encode(r) for r in self.recording]))
        waveFile.close()