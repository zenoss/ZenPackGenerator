#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#


# ForeMock and StyleMock were added to allow for setup to run when
#  Colorama is not installed.
class ForeMock(object):
    """Mocked up interface for colorama.Fore"""
    RESET = ""
    RED = ""
    GREEN = ""
    CYAN = ""
    MAGENTA = ""
    YELLOW = ""
    BLACK = ""


class StyleMock(object):
    """Mocked up interface for colorama.Style"""
    NORMAL = ""
    BRIGHT = ""
    DIM = ""

# During setup.py, zpg is imported to capture the version of zpg.  But,
#  if colorama is not already installed, then setup will fail.  Duck
#  typing below to prevent failure to install in the absence of the
#  colorama package.
try:
    from colorama import Fore, Style
except ImportError:
    Fore = ForeMock()
    Style = StyleMock()

OUTPUT_COLORS = True


def disable_color():
    """Disables color output"""
    global OUTPUT_COLORS
    global Fore
    global Style
    OUTPUT_COLORS = False
    Fore = ForeMock()
    Style = StyleMock()


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
