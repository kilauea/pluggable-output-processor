#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Output processor for `cmake`
#
# Copyright (c) 2013 Alex Turbov <i.zaufi@gmail.com>
#
# Pluggable Output Processor is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pluggable Output Processor is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import outproc
import re
import shlex

_SUCCESS_RE = re.compile('^-- (Check|Looking|Performing Test|Detecting).*-{1,2} (works|done|found|Success)$')
_SUCCESS2_RE = re.compile('^-- Found .*:\s.*$')
_FAILURE_RE = re.compile('^-- .* - not found$')
_FATAL_RE = re.compile('^CMake Error.*')


class Processor(outproc.Processor):

    def __init__(self, config, binary):
        super().__init__(config, binary)
        self.success = config.get_color('success-test', 'green+bold')
        self.failure = config.get_color('fail-test', 'red+bold')
        self.fatal = config.get_color('fatal-error', 'red+bold')


    def _colorize(self, color, line):
        return color + line + self.config.reset_color


    def handle_line(self, line):
        if _SUCCESS_RE.match(line) or _SUCCESS2_RE.match(line):
            return self._colorize(self.success, line)
        if _FAILURE_RE.match(line):
            return self._colorize(self.failure, line)
        if _FATAL_RE.match(line):
            return self._colorize(self.fatal, line)
        return line