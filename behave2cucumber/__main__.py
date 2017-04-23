import sys
import json
import getopt
import logging
from pprint import pprint

from .__init__ import convert

# Global Parameters
_name = "behave2cucumber"
_debug = logging.WARNING

# Logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-10.10s]  %(message)s")
shortFormatter = logging.Formatter("[%(levelname)-8.8s]  %(message)s")
log = logging.getLogger()
log.setLevel(_debug)
fileHandler = logging.FileHandler("{0}/{1}.log".format("./", _name))
fileHandler.setFormatter(logFormatter)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(shortFormatter)
log.addHandler(fileHandler)
log.addHandler(consoleHandler)


options = {
    "short": "hd:i:o:rf",
    "long": [
        "help", "debug=", "infile=", "outfile=", "remove-background", "format-duration"
    ],
    "descriptions": [
        "Print help message",
        "Set debug level",
        "Specify the input JSON",
        "Specify the output JSON, otherwise use stdout",
        "Remove background steps from output",
        "Format the duration"
    ]
}


def usage():
    """Print out a usage message"""

    global options
    l = len(options['long'])
    options['shortlist'] = [s for s in options['short'] if s is not ":"]

    print("python -m behave2cucumber [-h] [-d level|--debug=level]")
    for i in range(l):
        print("    -{0}|--{1:20} {2}".format(options['shortlist'][i], options['long'][i], options['descriptions'][i]))


def main(argv):
    """Main"""
    global options

    opts = None
    try:
        opts, args = getopt.getopt(argv, options['short'], options['long'])
    except getopt.GetoptError:
        usage()
        exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            exit()
        elif opt in ("-d", "--debug"):
            try:
                arg = int(arg)
                log.debug("Debug level received: " + str(arg))
            except ValueError:
                log.warning("Invalid log level: " + arg)
                continue

            if 0 <= arg <= 5:
                log.setLevel(60 - (arg*10))
                log.critical("Log level changed to: " + str(logging.getLevelName(60 - (arg*10))))
            else:
                log.warning("Invalid log level: " + str(arg))

    infile = None
    outfile = None
    remove_background = False
    duration_format = False

    for opt, arg in opts:
        if opt in ("-i", "--infile"):
            log.info("Input File: " + arg)
            infile = arg
        if opt in ("-o", "--outfile"):
            log.info("Output File: " + arg)
            outfile = arg
        if opt in ("-r", "--remove-background"):
            log.info("Remove Background: Enabled")
            remove_background = True
        if opt in ("-f", "--format-duration"):
            log.info("Format Duration: Enabled")
            duration_format = True

    if infile is None:
        log.critical("No input JSON provided.")
        usage()
        exit(3)

    with open(infile) as f:
        cucumber_output = convert(json.load(f),
                                  remove_background=remove_background,
                                  duration_format=duration_format)

    if outfile is not None:
        with open(outfile, 'w') as f:
            json.dump(cucumber_output, f, indent=4, separators=(',', ': '))
    else:
        pprint(cucumber_output)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(0)
    except EOFError:
        sys.exit(0)
    # except:
    #     sys.exit(0)