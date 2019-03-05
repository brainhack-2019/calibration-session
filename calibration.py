from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier, DummyCppAmplifier
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

amps = TmsiCppAmplifier.get_available_amplifiers()
#amps = DummyCppAmplifier.get_available_amplifiers()
amp = TmsiCppAmplifier(amps[0])

amp.sampling_rate = 128

amp.start_sampling()
gains = np.array(amp.current_description.channel_gains)
offsets = np.array(amp.current_description.channel_offsets)

def samples_to_microvolts(samples):
    return samples * gains + offsets

channels = amp.current_description.channel_names
channels = np.array(channels)
channels = channels.reshape((1,channels.shape[0]))
channels = channels[:, [0, 1, 3, 4, 6, 7, 9, 10, 31]]
channels = channels[0]
signal = np.zeros((16, 9))
    
cnt = 0
while True:
    cnt += 1
    packet = amp.get_samples(16)
    samples = samples_to_microvolts(packet.samples)
    samples = samples[:, [0, 1, 3, 4, 6, 7, 9, 10, 31]]

    signal = np.vstack((signal, samples))

    if signal.shape[0] > 11000:
	
        frame = pd.DataFrame(data=signal, columns=channels)
        frame.to_csv('calibration.csv', sep = ',')
        print('saved')
        break


#signal = signal[16:]

#s0 = signal[:, 0] -  np.mean(signal[:, 0])
#s1 = signal[:, 1] -  np.mean(signal[:, 1])

#plt.plot(s0 - s1, label='offset corrected')
#plt.legend()
#plt.show()

