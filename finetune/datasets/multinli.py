import os
import logging
from pathlib import Path

import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from finetune import Entailment
from finetune.datasets import Dataset

logging.basicConfig(level=logging.DEBUG)

FILENAME = "multinli.dev.csv"
DATA_PATH = os.path.join('Data', 'Entailment', FILENAME)


class MultiNLI(Dataset):

    def __init__(self, filename=None, **kwargs):
        super().__init__(filename=(filename or DATA_PATH), **kwargs)

    def download(self):
        """
        Download Stanford Sentiment Treebank to enso `data` directory
        """
        path = Path(self.filename)
        if path.exists():
            return

        path.parent.mkdir(parents=True, exist_ok=True)

        remote_url = "https://s3.amazonaws.com/enso-data/multinli.dev.csv"

        response = requests.get(remote_url)
        open(DATA_PATH, 'wb').write(response.content)



if __name__ == "__main__":
    # Train and evaluate on SST
    dataset = MultiNLI(nrows=1000).dataframe
    model = Entailment(verbose=True)
    trainX1, testX1, trainX2, testX2, trainY, testY = train_test_split(
        dataset.x1, dataset.x2, dataset.target, test_size=0.3, random_state=42
    )
    model.fit(trainX1, trainX2, trainY)
    accuracy = np.mean(model.predict(testX1, testX2) == testY)
    print('Test Accuracy: {:0.2f}'.format(accuracy))
