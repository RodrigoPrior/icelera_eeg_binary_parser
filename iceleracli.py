import argparse
import icelera


parser = argparse.ArgumentParser(
    prog='iceleracli',
    description='Convert EEG timeseries (csv file) to entropy by time window.',
    usage='python entropycli -f <binary file>'
    )

parser.add_argument('-f', dest='inputFile', help='specify binary file')

args = parser.parse_args()

if not args.inputFile:
    parser.print_help()
    exit(0)

icelera.parse(fname=args.inputFile)
