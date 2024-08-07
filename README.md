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
### Models

Please download [this directory](https://drive.google.com/drive/folders/1t-UBBbp1V83j4jv8_htW3BwhGzYX9QLK?usp=drive_link) entirely and put it at the same location with `main.py`.

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

```
python main.py --i wheat-vcf/ALL.vcf.gz \
				--m DL K ED4 SNP SmoothG SmoothLOD Ridit \
				--p 1 \
				--p1 15 \
				--chromosomes chr1 chr2 chr3 \
				--samples Mutant123 Wild123 \
				--s Tri-kernel-smooth \
        --w 0.75
        --t 0
```

## Outputs
The program will output a directory called `Results`. Files inside are like below.
```
├── 0-DL-Tri-kernel-smooth-0.75-0.1250.png
├── 0-DL-Tri-kernel-smooth-0.75-0.1250.pdf
├── 0-DL-Tri-kernel-smooth-0.75-0.1250.csv
├── ...
```
- `0-DL-Tri-kernel-smooth-0.75-0.1250.csv` : columns in this order.
  + **QTL**: Identifier for the Quantitative Trait Locus.
  + **Chr**: Chromosome where the QTL is located.
  + **Left**: Left boundary of the QTL interval.
  + **Peak**: Peak position of the QTL.
  + **Right**: Right boundary of the QTL interval.
  + **Value**: Smoothed data of the peak position.
- `0-DL-Tri-kernel-smooth-0.75-0.1250.png`



+ **POS** - The position on the chromosome in nt 
+ **REF** - The reference allele at that position 
+ **ALT** - The alternate allele 
+ **DP.HIGH** - The read depth at that position in the high bulk 
+ **AD_REF.HIGH** - The allele depth of the reference allele in the high bulk 
+ **AD_ALT.HIGH** - The alternative allele depth in the high bulk  
+ **SNPindex.HIGH** - The calculated SNP-index for the high bulk 
+ Same as above for the low bulk 
+ **REF_FRQ** - The reference allele frequency as defined above 
+ **deltaSNP** - The $\Delta$(SNP-index) as defined above

+ `SNPindex.filt.tsv` : SNPs filtered with user-specified or default thresholds. One column `tricubeDeltaSNP` is added, which represents the smoothed deltaSNP values.
+ `allchr.png` : delta SNP index for all chromosomes
  - **dots** : variant
  - **<span style="color: red; ">RED line</span>** : smoothed delta SNP-index
  ![allchr](https://github.com/Brycealong/QTL-analysis/blob/main/images/allchr.png)
+ `chr1.png` : delta SNP index for one chromosome. Same for other chromosomes.
  ![6a](https://github.com/Brycealong/QTL-analysis/blob/main/images/6A.png)
+ `distribution.png`: distribution of reference allele frequency, read depths of each sample and SNP index of each sample. Adjust your thresholds using this graph.
  ![dis](https://github.com/Brycealong/QTL-analysis/blob/main/images/distribution.png)
+ `analysis.log`: log how many SNPs are filtered out on each parameter.



## Citation
- Hiroki Takagi, Akira Abe, Kentaro Yoshida, Shunichi Kosugi, Satoshi Natsume, Chikako Mitsuoka, Aiko Uemura, Hiroe Utsushi, Muluneh Tamiru, Shohei Takuno, Hideki Innan, Liliana M. Cano, Sophien Kamoun, Ryohei Terauchi (2013).  [QTL-seq: rapid mapping of quantitative trait loci in rice by whole genome resequencing of DNA from two bulked populations](https://doi.org/10.1111/tpj.12105). Plant journal 74:174-183.
- Mansfeld, B.N. and Grumet, R. (2018), QTLseqr: An R Package for Bulk Segregant Analysis with Next-Generation Sequencing. The Plant Genome, 11: 180006. https://doi.org/10.3835/plantgenome2018.01.0006
