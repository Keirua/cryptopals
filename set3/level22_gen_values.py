from level21_mt19937 import mt32
from random import randint
import time

# Generates 32 random numbers with mt32 algorithms, with a random seed.
# The filename contains the seed value

time.sleep(randint(0, 10))
random_seed = int(time.time())

mt = mt32(random_seed)

with open(str("mt32/") + str(random_seed)+'.mt32', 'w') as f:
	for i in range (32):
		time.sleep(randint(0, 3))
		f.write(str(mt.extract_number()) + "\n")

f.close()
