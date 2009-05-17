import scikits.audiolab as al
import numpy as np

fps = 30.0
nband = 256
fft_size = 2**11
bandsize = fft_size/(2*nband)
w = al.sndfile('loop.wav', 'read')
sr = w.get_samplerate()
ns = w.get_nframes()
s = w.read_frames(ns)
binsize = int(sr/fps)
nbins = int(ns/binsize)
window = 2*binsize
tmp = np.zeros(window+len(s), dtype=np.float32)
tmp[binsize:-binsize] = s[:,0] #might want to avg channels?
s = tmp
ffts = np.zeros((nbins, nband), dtype=np.float32)
print nbins
for i in xrange(nbins):
    tmp = s[i*binsize:i*binsize+window]
    clip = (window-fft_size)/2
    tmp = tmp[clip:-clip] * np.hanning(fft_size)
    tmp2 = np.zeros(nband, dtype=np.float32)
    fft_tmp = np.fft.fft(tmp)[:fft_size/2].real**2
    for j in xrange(nband):
        tmp2[j] = np.log(np.average(fft_tmp[j*bandsize:(j+1)*bandsize]))
    ffts[i] = tmp2


bpm = 120.0
bps = bpm/60.0
fpb = fps/bps
tsig = 4#/4
nbars = 3
