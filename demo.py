# readDir.py
from src.dataChance.ChanceData import BatchChanceData
import time

s = time.time()
BatchChanceData('./test/data', r'./test/output/pdf/',
                3, dir_keep=False, thread_number=1)
d = time.time()
print(d-s)
