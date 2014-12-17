import optparse
import icelera

parser = optparse.OptionParser('usage %prog -f <binary file>')

parser.add_option(
    '-f', dest='inputFile', type='string',
    help='specify binary file')

(options, args) = parser.parse_args()
inputFile = options.inputFile

if (inputFile is None):
    print parser.usage
    exit(0)

icelera.parse(fname=inputFile)
