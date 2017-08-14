import argparse
parser = argparse.ArgumentParser(description='This is a PyMOTW sample program')
# parser.add_argument("echo", help="echo the string you use here")
# parser.add_argument(
#    "square", help="display a square of a given number", type=int)
parser.add_argument('-a', action="store_true", default=False)
parser.add_argument('-b', action="store", dest="b")
parser.add_argument('-c', action="store", dest="c", type=int)

print(parser.parse_args(['-a', '-b', 'val', '-c', '3']))
print(parser.parse_args(['-a', '-b', 'val', '-c3']))
args = parser.parse_args()

# print(args.echo)
# print(args.square**2)
