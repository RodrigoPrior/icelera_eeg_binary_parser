import argparse
import icelera


parser = argparse.ArgumentParser(
    prog='iceleracli',
    description='Parse iCelera binary eeg output file to csv.',
    usage='python iceleracli -f <binary file>'
    )

parser.add_argument('-f', dest='inputFile', help='specify binary file')

args = parser.parse_args()

if not args.inputFile:
    parser.print_help()
    exit(0)

icelera.parse(fname=args.inputFile)
