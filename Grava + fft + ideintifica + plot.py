from __future__ import division
import pyaudio
import wave
from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi, argmax
from scipy.io.wavfile import read,write

def buscaNota(vet_f, vet_Y):
    #argmax elemento relativo ao maior valor no vetor
    maior = argmax(vet_Y)
    f_nota = vet_f[maior]
    return f_nota

def transformada(y,Fs):
    #arange cria vetor: [0..(tam//2)-1] para o eixo frequencia
    frq = (arange(tam//2))/timp
    #calcula a fft e normaliza em relacao ao numero de amostras
    Y = fft(y)/tam 
    Y = abs(Y[arange(tam//2)]) #seleciona a 1a metade dos elementos para plot (matriz quadrada)
    #da pra fazer com numpy.array se precisar

    plot(frq,Y,'r') 
    xlabel('Freq (Hz)')
    ylabel('|Y (freq)|')
    
    return frq,Y

#Lista de notas: 12 semitons por oitava (36 semitons)
#4a oitava ("N" = regiao sem nota) (24 regioes por oitava) 
notasLista =  ["C4", "N", "C#4", "N", "D4", "N", "D#4", "N", "E4", "N", "F4", "N", "F#4", "N", "G4", "N", "G#4", "N", "A4", "N", "A#4", "N", "B4", "N"]
#5a oitava
notasLista += ["C5", "N", "C#5", "N", "D5", "N", "D#5", "N", "E5", "N", "F5", "N", "F#5", "N", "G5", "N", "G#5", "N", "A5", "N", "A#5", "N", "B5", "N"]
#6a oitava (23 regioes)
notasLista += ["C6", "N", "C#6", "N", "D6", "N", "D#6", "N", "E6", "N", "F6", "N", "F#6", "N", "G6", "N", "G#6", "N", "A6", "N", "A#6", "N", "B6"]

#Referencias dos limites das notas/semitons e regioes sem nota
#4a oitava
notasRef =  [510, 536, 541, 567, 574, 5900, 609, 635, 646, 672, 685, 711, 726, 752, 770, 796, 817, 843, 867, 893, 919, 945, 974, 1000]
#5a oitava
notasRef += [1026, 1066, 1088, 1128, 1154, 1194, 1224, 1264, 1298, 1338, 1376, 1416, 1459, 1499, 1547, 1587, 1641, 1681, 1740, 1780, 1844, 1884, 1955, 1995]
#6a oitava
notasRef += [2070, 2116, 2194, 2240, 2326, 2372, 2466, 2512, 2614, 2670, 2770, 2816, 2936, 2982, 3112, 3158, 3299, 3345, 3497, 3543, 3706, 3752, 3928, 3974]

#constantes para gravacao
FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "file.wav"

#taxa de amostragem
Fs = 44100;

#inicia gravacao pela PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=Fs, input=True,
                frames_per_buffer=CHUNK)
print ("Gravando...")
frames = []

#transfere para mem
for i in range(0, int(Fs / CHUNK * RECORD_SECONDS)):
    dt = stream.read(CHUNK)
    frames.append(dt)

stream.stop_stream()
stream.close()
audio.terminate()
print ("Gravacao concluida")
 
#grava em disco
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(Fs)
waveFile.writeframes(b''.join(frames))
waveFile.close()

#leitura
rate,data=read(WAVE_OUTPUT_FILENAME)
#trabalhando com o canal esquerdo
y=data[:,0]

#tamanho do arquivo em seg (div pela taxa de amostragem)
tam=len(y)
timp=tam/44100.
#cria vetor com tamanho de amostras pra representar o tempo (inicio, fim, num de elementos)
t=linspace(0,timp,tam)

#Cria grafico amplitude (y) X tempo (t)
subplot(2,1,1)
plot(t,y)
xlabel('Time')
ylabel('Amplitude')
subplot(2,1,2)
#Extrai e plota o dominio de frequencia por FFT
x,y = transformada(y,Fs)
nota = buscaNota(x,y)


#Identificacao da nota
#Inicializacao dos limites do vetor notasRef
bottom = 0
top    = 71

#Se tiver dentro dos limites
#Loop para repartir e achar a nota -- O(log(n))
if nota < notasRef[bottom]:
    print "Ops, nao foi boa nota (fora dos limites de uma flauta soprano:" + str("%.2f" % nota) + "Hz)"
    print "Nota mais proxima: " + notasLista[bottom] + " com range " + str(notasRef[bottom]) + "Hz ~ " + str(notasRef[bottom+1]) + "Hz"
elif nota > notasRef[top-1]:
    print "Ops, nao foi boa nota (fora dos limites de uma flauta soprano:" + str("%.2f" % nota) + "Hz)"
    print "Nota mais proxima: " + notasLista[top-1] + " com range " + str(notasRef[top-1]) + "Hz ~ " + str(notasRef[top]) + "Hz"
else:
    middle = 36//2

    while middle != bottom:
        if nota < notasRef[middle]:
            top = middle
            middle = top//2
        else:
            bottom = middle
            middle = (top + middle)//2
    if notasLista[bottom] == "N":
        print "Ops, nao foi boa nota (" + str("%.2f" % nota) + "Hz)"
        if (nota - notasRef[bottom]) > (notasRef[bottom+1] - nota):
            notaProx = bottom+1
        else:
            notaProx = bottom-1
        print "Nota mais proxima: " + notasLista[notaProx] + " com range " + str(notasRef[notaProx]) + "Hz ~ " + str(notasRef[notaProx+1]) + "Hz"
            
    else:
        print "A nota com frequencia " + str("%.2f" % nota) + "Hz eh um " + notasLista[bottom]


#plot
show()
