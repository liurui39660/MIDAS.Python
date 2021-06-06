# MIDAS.Python

Python implementation of the [MIDAS algorithm](https://github.com/Stream-AD/MIDAS).

## Demo

1. Open a terminal at the root `MIDAS.Python/`
1. `set PYTHONPATH=src` (Windows) or `PYTHONPATH=src` (Linux/macOS)
    - Because this is where the MIDAS package is
1. `python example/Demo.py`

It runs on `data/darpa_processed.csv`, using MIDAS-F with default parameters as in the C++ version, and will export anomaly scores to `temp/Score.txt`.

## Requirement

- MIDAS Cores
  - `numpy`
  - `numba`: JIT compilation
- `example/Demo.py`
  - `pyprojroot`: Detect project root
  - `sklearn`: ROC-AUC
  - `tqdm`: Show progress

## Note 

Preliminary tests show the ROC-AUC difference of this version and the C++ version is less than 1e-7.   

I tried to include some optimizations, but it is still order-of-magnitude times slower than the C++ version, e.g., 97ms vs. 5s for the `NormalCore`.  
Therefore, this python implementation should only be used for understanding the high-level concepts of the algorithm.  
For production environments or research projects, it is highly suggested to use our fully-optimized [C++ version in the master branch](https://github.com/Stream-AD/MIDAS).

## Customization

### Switch Cores

Uncomment the desired core at `example/Demo.py:15-17` and comment out the rest.

### Custom Dataset + `Demo.py`

You need to prepare two files:

- Data file
  - A header-less csv format file of shape `[N,3]`
  - Columns are sources, destinations, timestamps
  - Replace the path at `example/Demo.py:9` 
  - E.g. `data/DARPA/darpa_processed.csv`
- Label file
  - A header-less csv format file of shape `[N,1]`
  - The corresponding label for data records
    - 0 means normal record
    - 1 means anomalous record
  - Replace the path at `example/Demo.py:10`
  - E.g. `data/DARPA/darpa_ground_truth.csv`

### Custom Dataset + Custom Runner

1. Include `MIDAS.NormalCore`, `MIDAS.RelationalCore` or `MIDAS.FilteringCore`
1. Instantiate cores with required parameters
1. Call `Call()` on individual data records, it returns the anomaly score for the input record

## Citation

If you use this code for your research, please consider citing our arXiv preprint

```bibtex
@misc{bhatia2020realtime,
    title={Real-Time Streaming Anomaly Detection in Dynamic Graphs},
    author={Siddharth Bhatia and Rui Liu and Bryan Hooi and Minji Yoon and Kijung Shin and Christos Faloutsos},
    year={2020},
    eprint={2009.08452},
    archivePrefix={arXiv},
    primaryClass={cs.LG}
}

```

or our AAAI paper


```bibtex
@inproceedings{bhatia2020midas,
    title="MIDAS: Microcluster-Based Detector of Anomalies in Edge Streams",
    author="Siddharth {Bhatia} and Bryan {Hooi} and Minji {Yoon} and Kijung {Shin} and Christos {Faloutsos}",
    booktitle="AAAI 2020 : The Thirty-Fourth AAAI Conference on Artificial Intelligence",
    year="2020"
}
```
