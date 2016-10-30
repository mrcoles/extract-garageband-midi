#!/usr/bin/env python3

from __future__ import print_function, division, unicode_literals

import os
import re


DEFAULT_OUTPUT = os.path.expanduser('~/Desktop/extracted.mid')

LOOPS_DIRECTORY = os.path.expanduser('~/Library/Audio/Apple Loops/User Loops/SingleFiles')

RE_MIDI = re.compile(r'MTrk(.*)CHS', re.DOTALL)


# Test your result
# ----------------
#
# Turns out Mac OSX no longer plays MIDI files, install this to test.
#
# ```
# brew install timidity
# timidity your_file.mid
# ```
#


def convert_file(infile, outfile):
    """
    infile - read binary in file of GarageBand .aif loop file
    outfile - write binary out file
    """
    content = infile.read()

    start_token = _bytes_token('MTrk')
    end_token = _bytes_token('CHS')

    start_index = content.find(start_token)
    end_index = content.find(end_token)

    # via http://www.ccarh.org/courses/253/handout/smf/
    header_chunk = (
        # indicate that this is a MIDI file.
        b'MThd'
        # length of the header chunk
        b'\x00\x00\x00\x06'
        # format (single track file format is 0)
        b'\x00\x00'
        # number of track chunks
        b'\x00\x01'
        # unit of time for delta timing (larger number is faster,
        # you can fiddle with this value to get different speeds)
        b'\x02\x08'
    )

    track_chunk = content[start_index:end_index]

    outfile.write(header_chunk + track_chunk)


def _bytes_token(val):
    return bytes(val, 'utf-8')


def list_loops_dir():
    fnames = [fname for fname in os.listdir(LOOPS_DIRECTORY) if fname.endswith('.aif')]
    count = len(fnames)
    print('\n## Found {} loop file{}{}\n'.format(
        count, '' if count == 1 else 's', ':' if count else '.')
    )
    for fname in fnames:
        print("  '{}'".format(os.path.join(LOOPS_DIRECTORY, fname)))

    if fnames:
        print('\nCopy-paste the path to any of these files to this command, to '
              'extract a .mid file.\n')


## Main

def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser(
        description='Extract the MIDI file from a GarageBand .aif loop file'
    )
    parser.add_argument('--list', '-l', action='store_true', default=False,
                        help=('List the contents of the Garageband '
                              'loops directory. Use this to find the path '
                              'to your extracted loop file.'))
    parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'),
                        default=sys.stdin,
                        help='Path to Garageband .aif loop file')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('wb'),
                        default=None,
                        help='Path to output .mid file')
    args = parser.parse_args()

    if args.list:
        list_loops_dir()
        return

    if args.outfile is None:
        outfile = open(DEFAULT_OUTPUT, 'wb')
    else:
        outfile = args.outfile

    convert_file(args.infile, outfile)


if __name__ == '__main__':
    main()
