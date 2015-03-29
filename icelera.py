import numpy as np
import struct
import pandas as pd


def parse(fname, headersize=1530):
    """
    parse icelera eeg binary file to csv
    fname = file name
    headersize = header size (default position byte 1530)
    """
    infile = open(fname, "rb")
    try:
        # deal with header
        infile.seek(0)

        # read bin data
        header_types = '395s 8s 8s ' + \
            '4s 4s 4s 16s 4s 15s '*23 + \
            '4s 4s 4s 16s 4s 6s'
        header = struct.unpack(header_types, infile.read(1530))
        filesize = infile.read()

        # set variables with header data
        total_time_measure = int(header[1])  # total measure time in sec.
        freq = int(header[5])  # frequency values
        freq_bytes = freq * 2  # frequency in bytes
        channels_total = int(header[2])  # total number of channels
        channels = [x.strip(' ') for x in header[6::6]]  # probe name no spaces

        # position head to binary data
        infile.seek(headersize)

        # initialize variables
        seconds = np.empty([0, freq])
        final = np.empty([0, channels_total])

        # start processing
        for i in range(len(filesize)/freq_bytes):
            data = infile.read(freq_bytes)
            bloco = np.asarray([struct.unpack('h'*freq, data)])
            seconds = np.append(seconds, bloco, axis=0)

        # transpose array to 24 columns
        for c in np.arange(seconds.shape[0])[::channels_total]:
            final = np.vstack((final, seconds[0+c:channels_total+c].T))

        # load np array do pd dataframe
        df = pd.DataFrame(final, columns=channels)
        # insert time
        # TODO: fix default date 18/11/2014...probably recover from header
        # TODO: fix 3906U (256Hz) freq rate...calc based in header freq
        df['time'] = pd.date_range(
            '18/11/2014',
            periods=freq*total_time_measure, freq='3906U')
        # convert to timeseries
        df = df.set_index(['time'])
        # save data to csv file
        df.to_csv(fname + '.csv')
        print ('csv saved:', final.shape[0],
               'lines', final.shape[1], 'columns')

    finally:
        infile.close
