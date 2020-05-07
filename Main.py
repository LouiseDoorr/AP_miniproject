import numpy as np
import soundfile as sf
from matplotlib import pyplot as plt
import tkinter as tk
import winsound as ws

notes = {"A4": 440.00, "A4#": 466.16,  # Array containing frequencies of the 4th octave
         "B4": 493.88,
         "C4": 261.63, "C4#": 277.18,
         "D4": 293.66, "D4#": 311.13,
         "E4": 329.63,
         "F4": 349.23, "F4#": 269.99,
         "G4": 392.00, "G4#": 415.00}

fs = 44100  # Samples per second

length = 1  # Length of audio file in seconds

totalSamples = fs * length  # Total amount of samples in audio file
totalSampleArray = np.int(totalSamples)  # Insures that the array is integers

noise = 200  # Amount of noise samples in the beginning of the file

inputSignal = np.r_[np.random.randn(noise), np.zeros(totalSampleArray - noise)]  # Input signal with noise amount of random numbers and the rest being zeros and an array length of totalSamples

time = np.arange(0, totalSamples).T / fs  # Used to plot sinusoid


def karplusStrong(signal, delay, coefficient, allPassCoefficient, sampleSize):
    sampling = np.arange(sampleSize)
    output = np.zeros(sampleSize)
    lowPass = np.zeros(1)   # 
    allPass = np.zeros(2)

    for i in sampling:
        if i < delay:
            tempOutput = signal[i]
        else:
            tempOutput = signal[i] + coefficient * output[i - delay]
        allPassInput = 0.5 * tempOutput + 0.5 * lowPass
        lowPass = tempOutput

        output[i] = allPassCoefficient * (allPassInput - allPass[1]) + allPass[0]
        allPass[0] = allPassInput
        allPass[1] = output[i]

    return output


def plot(signal):
    plt.figure(figsize=(10, 4))
    plt.plot(time, signal, lineWidth=2)
    plt.xlim(time[0], time[int(fs/8)])
    plt.ylim((-10, 10))
    plt.xlabel('$t$ [s]')
    plt.ylabel('$x(t)$ [Pa]')  # if x(t) represents the fluctuations in the air pressure
    plt.show()


def generateNoiseFile(signal, sampleRate):  # Generate a noise file
    sf.write('basic.wav', signal, sampleRate)


def play():
    return ws.PlaySound("basic.wav", ws.SND_FILENAME)


def clicked(freq1, freq2, freq3):
    period1 = fs / freq1  # Samples per period
    period2 = fs / freq2  # Samples per period
    period3 = fs / freq3  # Samples per period

    filterCoefficient = 0.99    # Comb filter coefficient

    combDelay1 = np.int(np.floor(period1 - 0.5))                     # Comb Delay
    fracDelay1 = period1 - combDelay1 - 0.5                          # Fractional delay used to calculate all pass coefficient
    allPassFilterCoefficient1 = (1 - fracDelay1) / (1 + fracDelay1)  # All pass coefficient based on the fractional delay

    combDelay2 = np.int(np.floor(period2 - 0.5))                     # Comb Delay
    fracDelay2 = period2 - combDelay2 - 0.5                          # Fractional delay used to calculate all pass coefficient
    allPassFilterCoefficient2 = (1 - fracDelay2) / (1 + fracDelay2)  # All pass coefficient based on the fractional delay

    combDelay3 = np.int(np.floor(period3 - 0.5))                     # Comb Delay
    fracDelay3 = period3 - combDelay3 - 0.5                          # Fractional delay used to calculate all pass coefficient
    allPassFilterCoefficient3 = (1 - fracDelay3) / (1 + fracDelay3)  # All pass coefficient based on the fractional delay

    # Creates an output signal as a note based on the Karplus Strong method
    outputSignal = karplusStrong(inputSignal, combDelay1, filterCoefficient, allPassFilterCoefficient1, totalSampleArray)
    # Adds another note
    outputSignal += karplusStrong(inputSignal, combDelay2, filterCoefficient, allPassFilterCoefficient2, totalSampleArray)
    # Adds another note
    outputSignal += karplusStrong(inputSignal, combDelay3, filterCoefficient, allPassFilterCoefficient3, totalSampleArray)
    # The three notes combined makes a chord
    generateNoiseFile(outputSignal, fs)  # Generate sound file
    #plot(outputSignal) # When this line is used the sinus wave is plotted before sound is played
    #plot(inputSignal)


window = tk.Tk()
window.title("Karplus guitar")

aMajor = tk.Button(window, text="A Major", bg="white", command=lambda:[clicked(notes["A4"], notes["C4#"], notes["E4"]), play()])
aMajor.grid(column=0, row=0)

bMajor = tk.Button(window, text="B Major", bg="white", command=lambda:[clicked(notes["B4"], notes["D4#"], notes["F4#"]), play()])
bMajor.grid(column=0, row=1)

cMajor = tk.Button(window, text="C Major", bg="white", command=lambda:[clicked(notes["C4"], notes["E4"], notes["G4"]), play()])
cMajor.grid(column=0, row=2)

dMajor = tk.Button(window, text="D Major", bg="white", command=lambda:[clicked(notes["D4"], notes["F4#"], notes["A4"]), play()])
dMajor.grid(column=0, row=3)

eMajor = tk.Button(window, text="E Major", bg="white", command=lambda:[clicked(notes["E4"], notes["G4#"], notes["B4"]), play()])
eMajor.grid(column=0, row=4)

fMajor = tk.Button(window, text="F Major", bg="white", command=lambda:[clicked(notes["F4"], notes["A4"], notes["C4"]), play()])
fMajor.grid(column=0, row=5)

gMajor = tk.Button(window, text="G Major", bg="white", command=lambda:[clicked(notes["G4"], notes["B4"], notes["D4"]), play()])
gMajor.grid(column=0, row=6)

window.mainloop()
