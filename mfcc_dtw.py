import librosa

y1, sr1 = librosa.load('amostras/do_normal1.wav')
y2, sr2 = librosa.load('amostras/do_alto1.wav')

#%pylab inline
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pl.subplot(1, 3, 1)
mfcc1 = librosa.feature.mfcc(y1, sr1)
librosa.display.specshow(mfcc1)

pl.subplot(1, 3, 2)
mfcc2 = librosa.feature.mfcc(y2, sr2)
librosa.display.specshow(mfcc2)

from dtw import dtw

dist, cost, acc, path = dtw(mfcc1.T, mfcc2.T, dist=lambda mfcc1, mfcc2: pl.norm(mfcc1 - mfcc2, ord=1))
print 'Normalized distance between the two sounds:', dist

plt.subplot(1, 3, 3)
plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.xlim((-0.5, cost.shape[0]-0.5))
plt.ylim((-0.5, cost.shape[1]-0.5))
plt.show()
