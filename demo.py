# readDir.py
from src.dataChance.ChanceData import BatchChanceData
import time

s = time.time()
BatchChanceData('./test/data', r'./test/dataout',
                5, dir_keep=False, thread_number=2)
d = time.time()
print(d-s)
