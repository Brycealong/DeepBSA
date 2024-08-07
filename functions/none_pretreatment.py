import os

import numpy as np
import pandas as pd
from tqdm import tqdm


class NonePretreatment(object):

    def __init__(self, file_path, file_name, save_path):
        super(NonePretreatment, self).__init__()
        self.file_path = file_path
        self.file_name = file_name
        self.save_path = save_path

    def run(self, return_path):
        from collections import Counter

        ref_data_path = os.path.join(self.save_path, self.file_name + "_ref.npy")
        mut_data_path = os.path.join(self.save_path, self.file_name + "_mut.npy")
        freq_data_path = os.path.join(self.save_path, self.file_name + "_freq.npy")
        pos_data_path = os.path.join(self.save_path, self.file_name + "_pos.npy")

        data = pd.read_csv(self.file_path, header=None)
        chrome_set = list(Counter(list(data[0])).keys())
        max_chrome = len(chrome_set)
        A_data, a_data, freq_data, position = [], [], [], []  # 保存最后结果

        if return_path:
            return ref_data_path, mut_data_path, freq_data_path, pos_data_path, chrome_set

        for chrome in tqdm(range(int(max_chrome))):
            row_Ap, row_ap = [], []
            row_freq, row_pos = [], []
            chrome_data = data.loc[data[0] == chrome_set[chrome]]
            for _, row in chrome_data.iterrows():
                Ap = np.array(row[4::2])
                ap = np.array(row[5::2])
                Ap[Ap == 0] = 0.0001
                ap[Ap == 0] = 0.0001
                row_Ap.append(Ap)
                row_ap.append(ap)
                row_freq.append(Ap / (ap + Ap))
                row_pos.append(row[1])
            A_data.append(row_Ap)
            a_data.append(row_ap)
            freq_data.append(row_freq)
            position.append(row_pos)

        # print("Lengths of A_data elements:", [len(lst) for lst in A_data])
        # print("Lengths of a_data elements:", [len(lst) for lst in a_data])
        # print("Lengths of freq_data elements:", [len(lst) for lst in freq_data])
        # print("Lengths of position elements:", [len(lst) for lst in position])

        np.save(ref_data_path, np.array(A_data, dtype=object))
        np.save(mut_data_path, np.array(a_data, dtype=object))
        np.save(freq_data_path, np.array(freq_data, dtype=object))
        np.save(pos_data_path, np.array(position, dtype=object))

        return ref_data_path, mut_data_path, freq_data_path, pos_data_path, chrome_set
