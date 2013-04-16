from optparse import OptionParser
import os
def run():
    print "running"

    parser = OptionParser()
    cwd = os.getcwd()
    parser.add_option('-d', "--destdir", dest="dest", default="%s/build" % os.getcwd(), help="Destination Directory for the zenpack. [%default]")
    (opts, args) = parser.parse_args()

    # Making sure all mandatory options appeared.
    mandatory = ['dest']
    for m in mandatory:
        if not opts.__dict__[m]:
            print "mandatory option is missing\n"
            parser.print_help()
            exit(-1)
    
