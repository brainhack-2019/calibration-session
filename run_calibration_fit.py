from classifier.data_import import data_import
from classifier.fit_model import fit_model

import numpy as np

_, data, labels = data_import('./calibration.csv', './gesture_order.csv', './samples_data')

model = np.array(fit_model(data, labels))

np.save('./amplifier-online/fitted_model/fitted_model.npy', model)
