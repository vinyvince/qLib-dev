#!/usr/bin/python

import argparse
import os
import subprocess

# Declare global variable name
args = None

def build_cmd():
    for f in files():
        if os.path.isdir(f):
            debug('Processing: ' + f)
            if f[-len(args.extension):] == args.extension:
                otl = f[:-len(args.extension)] + '.otl'
                print 'Building:', otl
                try:
                    output = subprocess.check_output(['hotl', '-C', f, otl],
                            stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    print 'ERROR: The build process of {0} failed.'.format(otl)
                    print e.output
                    break
                except OSError as e:
                    print 'ERROR: The build process of {0} failed.'.format(otl)
                    print '{0} ({1})'.format(e.strerror, e.errno)
                    break

def extract_cmd():
    for f in files():
        if os.path.isfile(f):
            debug('Processing: ' + f)
            if f[-4:] == '.otl':
                dir = f[:-4] + args.extension
                print 'Extracting:', f
                try:
                    output = subprocess.check_output(['hotl', '-X', dir, f],
                            stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    print 'ERROR: The extraction process of {0} failed.'.format(f)
                    print e.output
                    break
                except OSError as e:
                    print 'ERROR: The extraction process of {0} failed.'.format(f)
                    print '{0} ({1})'.format(e.strerror, e.errno)
                    break

def clean_cmd():
    for f in files():
        if args.source:
            if os.path.isdir(f):
                debug('Processing: ' + f)
                if f[-len(args.extension):] == args.extension:
                    print 'Deleting:', f
                    try:
                        output = subprocess.check_output(['rm', '-r', f],
                                stderr=subprocess.STDOUT)
                    except subprocess.CalledProcessError as e:
                        print 'ERROR: Removing {0} failed.'.format(otl)
                        print e.output
                        break
                    except OSError as e:
                        print 'ERROR: Removing {0} failed.'.format(otl)
                        print '{0} ({1})'.format(e.strerror, e.errno)
                        break
        else:
            if os.path.isfile(f):
                debug('Processing: ' + f)
                if f[-4:] == '.otl':
                    dir = f[:-4] + args.extension
                    print 'Deleting:', f
                    try:
                        output = subprocess.check_output(['rm', f],
                                stderr=subprocess.STDOUT)
                    except subprocess.CalledProcessError as e:
                        print 'ERROR: Removing {0} failed.'.format(f)
                        print e.output
                        break
                    except OSError as e:
                        print 'ERROR: Removing {0} failed.'.format(f)
                        print '{0} ({1})'.format(e.strerror, e.errno)
                        break

def files():
    for a in args.file:
        yield a
        if os.path.isdir(a):
            for d in os.walk(a):
                if not args.recursive and d[0] != a:
                    break
                for f in d[1] + d[2]:
                    yield os.path.join(d[0],f)

def debug(msg):
    """
    Print debug messages
    """
    if args.debug:
        print "DEBUG:", msg

def parse_args():
    """
    Parse command line arguments.
    """

    common_args = argparse.ArgumentParser(add_help=False)
    common_args.add_argument('-D', '--debug', action='store_true',
            help='Print debug messages')

    otl_args = argparse.ArgumentParser(add_help=False)
    otl_args.add_argument('file', type=str, nargs='*', default='.',
            help='File and/or directory to process ["%(default)s"]')
    otl_args.add_argument('-x','--extension', type=str, default='_OTL',
            help='File extension of extracted OTL directories ["%(default)s"]')
    otl_args.add_argument('-R', '--recursive', action='store_true',
            help='Descend into sub-directories')

    main_parser = argparse.ArgumentParser(parents=[common_args],
            description='Command line tool to manage qLib.')

    subparsers = main_parser.add_subparsers(dest='command', help='Supported commands')

    build_parser = subparsers.add_parser('build', parents=[common_args, otl_args],
            help='Builds OTLs from extracted dir structures',
            description='Builds OTLs from extracted dir structures.')
    extract_parser = subparsers.add_parser('extract', parents=[common_args, otl_args],
            help='Extracts OTLs into dir structures',
            description='Extracts OTLs into dir structures.')
    clean_parser = subparsers.add_parser('clean', parents=[common_args, otl_args],
            help='Removes OTLs or OTL sources',
            description='Removes OTLs or OTL sources.')

    clean_parser.add_argument('-s', '--source', action='store_true',
            help='Deletes sources instead of built OTLs')

    global args
    args = main_parser.parse_args()

    debug(args)

# Main
parse_args()

{'build': build_cmd,
'extract': extract_cmd,
'clean': clean_cmd,
}[args.command]()
