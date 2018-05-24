#!/usr/bin/env python
"""This script takes in a JSON output Gitlab CI and updates the record in NS1."""
import json
import sys
import os
from nsone import NSONE


def main():
    ref_config = json.load(sys.stdin)
    ns1_api_key = os.getenv("NS1_API_KEY")
    if ns1_api_key is None:
        print "Failed to load API Key"
        sys.exit(999)
    ns1 = NSONE(apiKey=ns1_api_key)
    try:
        zone = ns1.loadZone(ref_config['zone'])
    except Exception:
        print "Exception: Failed on Zone load. Zone does not exist?"
        sys.exit(999)
    try:
        api_record = zone.loadRecord(ref_config['domain'], ref_config['type'])
    except Exception:
        print "Exception: Failed to load record. Record does not exist!"
        print "Creating a new record..."
        kwargs = {k: v for k, v in ref_config.iteritems() if k in ('answers', 'filters', 'ttl')}
        zone.add_CNAME(ref_config['domain'], **kwargs)
        sys.exit()
    try:
        kwargs = {k: v for k, v in ref_config.iteritems() if k in ('answers', 'filters', 'ttl')}
        api_record.update(**kwargs)
        print "Update successful"
    except Exception:
        sys.exit(123)
    sys.exit()

if __name__ == '__main__':
    main()
