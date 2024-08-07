import os
import gzip
from tqdm import tqdm
import pandas as pd


class Record(object):
    """
    One line information in vcf file
    """

    def __init__(self, line, sample_num):
        info = line.split("\t")
        self.line = line
        self.CHROM = info[0]
        self.POS = info[1]
        self.ID = info[2]
        self.REF = info[3]
        self.ALT = info[4]
        self.QUAL = info[5]
        self.FILTER = info[6]
        self.INFO = [{pair_lst[0]: pair_lst[1] if len(pair_lst) > 1 else ""} for pair_lst in
                     [pair.split("=") for pair in info[7].split(";")]]
        self.FORMAT = info[8].split(":")
        self.sample_num = sample_num
        self.GT = []
        for i in self.sample_num:
            GT_value = info[i].split(":")
            GT_dict = {}
            for g in range(len(GT_value)):
                GT_dict[self.FORMAT[g]] = GT_value[g]
            self.GT.append(GT_dict)


class VCF(object):
    """
    VCF class, read VCF, write VCF, get VCF information
    """

    def __init__(self, vcf, samples):
        self.header = []
        # read .gz file if necessary
        root, ext = os.path.splitext(vcf)
        if ext == ".gz":
            self.reader = gzip.open(vcf, 'rt')
        else:
            self.reader = open(vcf, 'rt')
        # self.reader = open(uncompress_vcf, 'r')
        self.line = self.reader.readline().strip()
        while self.line.startswith('##'):
            self.header.append(self.line)
            self.line = self.reader.readline().strip()
        head = self.line.split("\t")
        self.sample_num = []
        for s in samples:
            try:
                self.sample_num.append(head.index(s))
            except ValueError:
                print(f"{s} not in header")

    def __iter__(self):
        return self

    def __next__(self):
        self.line = self.reader.readline().strip()
        if self.line != "":
            self.record = Record(self.line, self.sample_num)
            return self.record
        else:
            self.reader.close()
            raise StopIteration()

    def reader_close(self):
        self.reader.close()


class VCF2Excel(object):
    def __init__(self, file_path, file_name, excel_dir, selected_chromosomes, selected_samples):
        super(VCF2Excel, self).__init__()
        self.file_path = file_path
        self.file_name = file_name
        self.excel_dir = excel_dir
        # self.filtered_vcf_dir = filtered_vcf_dir
        self.selected_chromosomes = selected_chromosomes
        self.selected_samples = selected_samples

    def run(self):
        # # Create filtered VCF path
        # filtered_vcf = os.path.join(self.filtered_vcf_dir, f"{self.file_name}_filtered.vcf.gz")
        #
        # with open(self.file_path, "r") as vcf:
        #     lines = vcf.readlines()
        #
        #     # extract the header line (starts with a #CHROM)
        #     header_line = [line.strip()[1:].split("\t") for line in lines if line.startswith("#CHROM")]
        #
        #     # create a df from the remaining lines
        #     data_lines = [line.strip().split("\t") for line in lines if not line.startswith("#")]
        #
        #     df = pd.DataFrame(data=data_lines, columns=header_line)
        #
        #
        #
        # # index the VCF file
        # subprocess.run(f"bcftools index -f {self.file_path}", shell=True, check=True)
        # # Filter the VCF file if necessary
        # if len(self.selected_chromosomes) != 0:
        #     if len(self.selected_samples) != 0:
        #         temp_vcf = os.path.join(self.filtered_vcf_dir, f"{self.file_name}_filtered_temp.vcf.gz")
        #         chrom_filter_cmd = f"bcftools view -r {','.join(self.selected_chromosomes)} -Oz -o {temp_vcf} {self.file_path}"
        #         subprocess.run(chrom_filter_cmd, shell=True, check=True)
        #         sample_filter_cmd = f"bcftools view -s {','.join(self.selected_samples)} -Oz -o {filtered_vcf} {temp_vcf}"
        #         subprocess.run(sample_filter_cmd, shell=True, check=True)
        #         os.remove(temp_vcf)
        #     else:
        #         chrom_filter_cmd = f"bcftools view -r {','.join(self.selected_chromosomes)} -Oz -o {filtered_vcf} {self.file_path}"
        #         subprocess.run(chrom_filter_cmd, shell=True, check=True)
        #     vcf_path_to_use = filtered_vcf
        # elif len(self.selected_samples) != 0:
        #     sample_filter_cmd = f"bcftools view -s {','.join(self.selected_samples)} -Oz -o {filtered_vcf} {self.file_path}"
        #     subprocess.run(sample_filter_cmd, shell=True, check=True)
        #     vcf_path_to_use = filtered_vcf
        # else:
        #     vcf_path_to_use = self.file_path

        # Process the VCF file and convert it to Excel
        vcf = VCF(self.file_path, self.selected_samples)
        data = []
        for r in tqdm(vcf, desc="vcf to excel"):
            if r.CHROM in self.selected_chromosomes:
                if ',' not in r.ALT:
                    try:
                        row = [str(r.CHROM), int(r.POS), r.REF, r.ALT]
                        for i in r.GT:
                            row.append(int(i["AD"].split(",")[0]))
                            row.append(int(i["AD"].split(",")[1]))
                        data.append(row)
                    except:
                        pass

        df = pd.DataFrame(data)
        chrom_set = df[0].unique().tolist()
        print("Keeping chromosomes: ", chrom_set)
        print("Keeping bi-allelic SNPs...")
        save_path = os.path.join(self.excel_dir, self.file_name + ".csv")
        df.to_csv(save_path, header=False, index=False)

        return save_path
