#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests


def main():
    response = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json')
    ranges = json.loads(response.content)['prefixes']

    return [i['ip_prefix'] for i in ranges if i['service'] == 'CLOUDFRONT']


if __name__ == "__main__":
    print(",".join(main()))
