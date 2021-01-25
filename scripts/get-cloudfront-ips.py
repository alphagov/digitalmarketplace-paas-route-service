#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import json


def main():
    response = urlopen('https://ip-ranges.amazonaws.com/ip-ranges.json').read()
    ranges = json.loads(response)['prefixes']

    return [i['ip_prefix'] for i in ranges if i['service'] == 'CLOUDFRONT']


if __name__ == "__main__":
    print(",".join(main()))
