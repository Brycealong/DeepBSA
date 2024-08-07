# deepbsa User Guide

## Table of contents
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Outputs](#outputs)



## Dependencies
### Python libraries
- pandas 
- matplotlib 
- statsmodels 
- tensorflow 
- pyinstaller 
- tqdm

#### Installation using conda

Create an environment (optional). 
```
conda create -n deepbsa
conda activate deepbsa
conda install -c conda-forge python
```
Then install the packages using conda.
```
conda install -c conda-forge pandas matplotlib statsmodels tensorflow pyinstaller tqdm
```

### Clone this repository

Change directory to where you want to place this repo and use 
```
git clone https://github.com/Brycealong/DeepBSA.git
```
to clone the repo. The default name of folder is `DeepBSA`.

### Models

Please download [this directory](https://drive.google.com/drive/folders/1t-UBBbp1V83j4jv8_htW3BwhGzYX9QLK?usp=drive_link) entirely and place it in the repo directory you just cloned.



## Usage

```
python main.py -h

usage: main.py [-h] --i I [--m M [M ...]] [--p P] [--p1 P1] [--p2 P2] [--p3 P3] [--chromosomes CHROMOSOMES [CHROMOSOMES ...]]
               [--samples SAMPLES [SAMPLES ...]] [--s S] [--w W] [--t T]

options:
  -h, --help            show this help message and exit
  --i I                 The input file path(vcf/csv).
  --m M [M ...]         List of algorithms to use(DL/K/ED4/SNP/SmoothG/SmoothLOD/Ridit) used. Default is DL.
  --p P                 Whether to pretreatment data(1[True] or 0[False]). Default is True.
  --p1 P1               Pretreatment step 1: Number of read thread, the SNP whose number lower than it will be filtered. Default is 0.
  --p2 P2               Pretreatment step 2: Chi-square test(1[True] or 0[False]). Default is 1[True].
  --p3 P3               Pretreatment step 3: Continuity test(1[True] or 0[False]). Default is 1[True].
  --chromosomes CHROMOSOMES [CHROMOSOMES ...]
                        List of chromosomes to select.
  --samples SAMPLES [SAMPLES ...]
                        List of samples to select.
  --s S                 The function to smooth the result(Tri-kernel-smooth/LOWESS/Moving Average), Defalut is LOWESS
  --w W                 Windows size of LOESS. The number is range from 0-1. 0 presents the best size for minimum AICc. Default is
                        0(auto).
  --t T                 The threshold to find peaks(float). Default is 0(auto)

```

### Example:

Move inside the directory.
```bash
cd DeepBSA
```

We have put the vcf file inside the directory under the path `wheat-vcf/ALL.vcf.gz`.

```bash
python main.py --i wheat-vcf/ALL.vcf.gz \
               --m DL K ED4 SNP SmoothG SmoothLOD Ridit \
               --p 1 \
               --p1 15 \
               --chromosomes chr1 chr2 chr3 \
               --samples Mutant123 Wild123 \
               --s Tri-kernel-smooth \
               --w 0.75 \
               --t 0
```
This example is:
- testing on all the algorithms
- with pretreatment
- minimum read number `15`
- choosing SNPs from `chr1`, `chr2` and `chr3`
- choosing bulks `Mutant123` and `Wild123`
- using smooth function `Tri-kernel-smooth`
- window size fraction `0.75`
- auto calculate threshold for each algorithm

## Outputs

The program will output multiple directories named `Excel_Files`, `NoPretreatment`, `Pretreated_Files`, some `__pycache__` and `Results`. Inside `Results`: 
```
Results
├── ALL
    ├──15-DL-Tri-kernel-smooth-0.75-0.1250.png
    ├──15-DL-Tri-kernel-smooth-0.75-0.1250.pdf
    ├──15-DL-Tri-kernel-smooth-0.75-0.1250.csv
    ├──...
```

The program can be rerun on different datasets, and each run will create a new folder inside the `Results` directory in the format `Results/{basename_of_file}/`. For example, we have `wheat-vcf/ALL.vcf.gz`, so the directory is named `ALL`. **Therefore, it is essential that the VCF files have unique basenames to avoid conflicts**.

Naming convention: `{read_number}-{func_name}-{smooth_func}-{smooth_window_size}-{threshold}.pdf`

- `read_number`: `--p1`
- `func_name`: `--m`
- `smooth_func`: `--s`
- `smooth_window_size`: `--w` (`auto` if set to 0)
- `threshold`: `--t` (auto calculated if set to 0)

results:

- `0-DL-Tri-kernel-smooth-0.75-0.1250.csv` : columns in this order.

  + **QTL**: Identifier for the Quantitative Trait Locus.
  + **Chr**: Chromosome where the QTL is located.
  + **Left**: Left boundary of the QTL interval.
  + **Peak**: Peak position of the QTL.
  + **Right**: Right boundary of the QTL interval.
  + **Value**: Smoothed data of the peak position.
- `0-DL-Tri-kernel-smooth-0.75-0.1250.png`

  - **dots** : variant

  - **<span style="color: orange; ">orange line</span>** : smoothed data

  - **<span style="color: blue; ">blue dashed line</span>** : threshold

![0-DL-Tri-kernel-smooth-0.75-0.1250](https://github.com/Brycealong/DeepBSA/blob/main/Results/0-DL-Tri-kernel-smooth-0.75-0.1250.png)

- `0-DL-Tri-kernel-smooth-0.75-0.1250.pdf` : same as png.

Same as above for other methods.



## Citation
- Li, Zhao, et al. "DeepBSA: A deep-learning algorithm improves bulked segregant analysis for dissecting complex traits." *Molecular Plant* 15.9 (2022): 1418-1427.
- Dong, Jianke, et al. "QTL analysis for low temperature tolerance of wild potato species Solanum commersonii in natural field trials." *Scientia Horticulturae* 310 (2023): 111689.
