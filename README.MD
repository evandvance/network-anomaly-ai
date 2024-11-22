# Anomaly Based Intrusion Detection

## The Data

The data used for this model can be found at <https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset?select=Wednesday-workingHours.pcap_ISCX.csv>

Due to its size and Githubs policys, it will not be included in this repo. It is accessed in the code from a folder named data.

The details of curration of the captures used is found at <https://www.unb.ca/cic/datasets/ids-2017.html> as well as the raw captures used to create the csvs

## Setup

With pip installed run

`pip install -r requirements.txt`

from the base directory of this repo.

With using conda

```sh
conda create --name ids-ai python=3.10
conda activate ids-ai
conda config --set pip_interop_enabled True
conda install --yes --file requirements.txt
pip install nfstream
```
