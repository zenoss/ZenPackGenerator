#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

from colorama import init, Fore, Back, Style

OUTPUT_COLORS = True


def colored(color, text, style=Style.BRIGHT):
    global OUTPUT_COLORS
    if OUTPUT_COLORS:
        text = color + Style.BRIGHT + text + Style.NORMAL + Fore.RESET
    return text


def red(text):
    return colored(Fore.RED, text)


def green(text):
    return colored(Fore.GREEN, text)


def blue(text):
    return colored(Fore.CYAN, text)


def purple(text):
    return colored(Fore.MAGENTA, text)


def yellow(text):
    return colored(Fore.YELLOW, text)


def grey(text):
    return colored(Fore.BLACK, text, style=Style.DIM)


def debug(logger, msg, prefix=True, colored=True):
    string = str(msg)
    if prefix:
        prefix = " >>> "
        prefix = prefix if not colored else grey(prefix)
        string = prefix + string
    logger.debug(string)


def info(logger, msg, prefix=True, colored=True):
    string = str(msg)
    if prefix:
        prefix = " [*] "
        prefix = prefix if not colored else prefix.replace("*", green("*"))
        string = prefix + string
    logger.info(string)


def warn(logger, msg, prefix=True, colored=True):
    string = str(msg)
    if prefix:
        prefix = " [*] "
        prefix = prefix if not colored else prefix.replace("*", yellow("*"))
        string = prefix + string
    logger.warn(string)


def error(logger, msg, prefix=True, colored=True):
    string = str(msg)
    if prefix:
        prefix = " !!! "
        prefix = prefix if not colored else red(prefix)
        string = prefix + string
    logger.error(string)


def critical(logger, msg, prefix=True, colored=True):
    string = str(msg)
    if prefix:
        prefix = " !!! "
        prefix = prefix if not colored else purple(prefix)
        string = prefix + string
    logger.error(string)


def log(severity, msg, prefix=" " * 5, colored=None):
    string = str(msg)
    if prefix:
        prefix = " !!! "
        if colored:
            try:
                prefix = colored(prefix)
            except:
                pass
        string = prefix + string
    logger.log(severity, string)
