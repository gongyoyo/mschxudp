#!/usr/bin/env python3
# encoding: utf-8
'''
mschxudp -- ms pinyin user define phrase
'''

import sys
import os

from optparse import OptionParser

__all__ = []
__version__ = 0.1
__date__ = '2017-03-18'
__updated__ = '2017-03-18'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2017 user_name (organization_name)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-d", "--dump", dest="dump", action="store_true", default=False, help="dump the ms pinyin user define phrases", metavar="FILE")
        parser.add_option("-o", "--out", dest="outfile", help="set output[default: %default]", metavar="FILE")

        # set defaults
        parser.set_defaults(outfile="./out.txt")

        # process options
        (opts, args) = parser.parse_args(argv)

        # MAIN BODY #
        
        if opts.dump:
            from mschxudp_file import MschxudpFile;
            for i in args:
                ime = MschxudpFile(i);
                ime.dump();
            return;
            
        
        from mschxudp_file import MschxudpFileBuilder;
        ifb = MschxudpFileBuilder();
        
        while True:
            line = input("Enter a phrase(',pinyin,phrase,candidate,candidate2'):");
            if len(line) <= 1:
                break;
            s = line.split(line[0])[1:5];
            if len(s) < 4:
                break;
            for i in s:
                if len(i) <= 0:
                    break;
            else:
                try:
                    ifb.add_phrase((int(s[2]),int(s[3])), s[0], s[1])
                except:
                    continue
            
        ifb.save(opts.outfile)
        
        print("outfile = %s" % opts.outfile)

    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'mschxudp_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())