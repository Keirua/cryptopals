from level21_mt19937 import mt32
from random import randint

random_seed = 42

def get_values_by_seed(seed):
	mt = mt32(seed)
	return [mt.extract_number() for i in range(32)]

def compare(actual, expected):
	for i in range(32):
		if (actual[i] != expected[i]):
			return False
	return True

def get_expected_values(filename):
	with open(filename, 'r') as f:
		data = [int(l) for l in f]
	return data

expected_values = get_expected_values("mt32/1508440814.mt32")
expected_values = get_values_by_seed(10023)

def compare_by_seed(seed, expected):
	mt = mt32(seed)
	for i in range(32):
		if(mt.extract_number() != expected_values[i]):
			return False
	return True

for seed in range (0, 1 << 32):
	if (compare_by_seed(seed, expected_values)):
		print("{} is the seed's value".format(seed))
		break;
	if (seed % 1000 == 0):
		print("{}".format(seed))