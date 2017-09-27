import argparse
parser = argparse.ArgumentParser()
parser.add_argument('numbers', type=int, nargs='+')
args = parser.parse_args()
print args