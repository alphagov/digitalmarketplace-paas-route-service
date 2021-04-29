#!/usr/local/bin/python3.6

"""A simple supervisord event listener to relay process output to supervisor's stdout
Copied from https://github.com/coderanger/supervisor-stdout and modified to remove the prefix
Copyright (c) 2012, Noah Kantrowitz
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the Noah Kantrowitz nor the names of its contributors may
  be used to endorse or promote products derived from this software without
  specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Noah Kantrowitz BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from __future__ import print_function
import sys


def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def main():
    while 1:
        write_stdout('READY\n')  # transition from ACKNOWLEDGED to READY
        line = sys.stdin.readline()   # read header line from stdin
        headers = dict([x.split(':') for x in line.split()])
        data = sys.stdin.read(int(headers['len']))  # read the event payload
        write_stdout('RESULT %s\n%s' % (len(data.encode("utf-8")), data))  # transition from READY to ACKNOWLEDGED


def event_handler(event, response):
    response = response.decode()
    _, data = response.split('\n', 1)
    print(data.strip())


if __name__ == '__main__':
    main()
