from pylab import plot, show, title, xlabel, ylabel, subplot, savefig, fft, arange, ifft, sin, linspace, pi
from scipy.io.wavfile import read,write

def plotSpectru(y,Fs):
 n = len(y) 
 k = arange(n)
 T = n/Fs
 frq = k/T #
 frq = frq[range(n/2)] 

 Y = fft(y)/n 
 Y = Y[range(n/2)]
 
 plot(frq,abs(Y),'r') 
 xlabel('Freq (Hz)')
 ylabel('|Y(freq)|')

Fs = 44100;  

rate,data=read('Do1.wav')
y=data[:,1]
lungime=len(y)
timp=len(y)/44100.
t=linspace(0,timp,len(y))

subplot(2,1,1)
plot(t,y)
xlabel('Time')
ylabel('Amplitude')
subplot(2,1,2)
plotSpectru(y,Fs)
show()
