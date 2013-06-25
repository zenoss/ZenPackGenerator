#!/usr/bin/env python
# test_pep8_conformance.py
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

import os
import sys
import unittest

from mock import mock_open, patch, call, MagicMock
import pep8


class WriteTemplatesBase(unittest.TestCase):

    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        # assume this file lives in git_repo/zpg/tests
        current_file = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_file)
        top_folder = os.path.dirname(current_folder)
        filepaths = []
        for root, folders, files in os.walk(top_folder):
            filepaths.extend(
                (os.path.join(root, f)
                 for f in files
                 if f[-3:] == ".py"
                 if f[:5] != "test_"))
        results = pep8style.check_files(filepaths)
        errors = str(results.total_errors)
        msgs = [
            "Found %s code style errors (and warnings)." % errors,
        ]
        self.assertEqual(results.total_errors, 0, "\n".join(msgs))
