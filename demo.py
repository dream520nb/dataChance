# readDir.py
from src.dataChance.ChanceData import BatchChanceData
import time

s = time.time()
BatchChanceData('./test/data', r'./test/output/mp4/',
                3, dir_keep=False, thread_number=4)
d = time.time()
print(d-s)
