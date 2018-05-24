#!/usr/bin/env python
"""This script takes in output Gitlab CI in the form of a Json Object and queries NS1 for validity and match of the DNS record and contents of it's answers."""
import json
import sys
import os
import traceback
from nsone import NSONE


def scrub_record(record):
    """Take a json object recieved from NS1 and scrub it for items that conflict."""
    general_scrub_list = ['use_client_subnet', 'feeds', 'meta', 'regions', 'networks', 'link', 'id', 'override_ttl', 'tier']
    meta_scrub_list = ['id', 'feeds']
    for x in general_scrub_list:
        if x in record:
            del record[x]
    for g in record['answers']:
        for x in meta_scrub_list:
            if x in g:
                del g[x]


def validate(config, api_record):
    """Validate for all entries both the generic and the answer meta data from both Reference Config and API downloaded configurations"""
    scrub_record(config)
    scrub_record(api_record)
    general_components = ['zone', 'domain', 'ttl', 'type']
    for x in general_components:
        if config[x] != api_record[x]:
            return False
    filter_k = lambda k: k['filter'][0]
    if sorted(config.get('filters', []), key=filter_k) != sorted(api_record.get('filters',[]), key=filter_k):
        return False
    filter_k = lambda k: k['answer'][0]
    if sorted(config.get('answers', []), key=filter_k) != sorted(api_record.get('answers',[]), key=filter_k):
        return False
    return True

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
        sys.exit(123)
    try:
        if not validate(ref_config, api_record.data):
            print "Configs mismatch. Push configs again."
            sys.exit(123)
        else:
            print "Configs match, no overrite needed"
    except Exception:
        print "Exception thrown upon validation. Check data structure is valid."
        sys.exit(123)

if __name__ == '__main__':
    main()
