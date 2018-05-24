# Requires influxdb, python-ldap and dnspython packages
import dns.resolver
import ldap
from influxdb import InfluxDBClient, exceptions
import subprocess, logging, time
import os

delay = 10

def check_auth(ip_of_ldap_server,username,password):
    try:
        conn = ldap.initialize('ldap://%s' % (ip_of_ldap_server))
        conn.protocol_version = 3
        conn.simple_bind_s(username,password)
        return True
    except dns.exception.DNSException:
        print "DNS Query failed"
        return False
    except ldap.INVALID_CREDENTIALS:
        print "Failed to authenticate"
        return False
    except ldap.SERVER_DOWN:
        print "Unable to reach LDAP Server"
        return False

def get_ldap_server():
    resolver = dns.resolver.Resolver()
    resolver.nameservers=["10.124.0.2"]
    ans = resolver.query("<FQDN YOU WANT TO LOOKUP>", "A")
    return ans[0]

def main():
    #host = os.environ.get('TELEGRAF_HOST')
    #port = os.environ.get('TELEGRAF_PORT')
    #dbname = os.environ.get('TELEGRAF_DB')
    #datacenter = os.environ.get('DATACENTER')
    host = "<INFLUXDB HOST>"
    port = "8086"
    dbname = "iacpl"

    client = InfluxDBClient(host=host, database=dbname, port=port)

    while True:
        result = check_auth(get_ldap_server(),"<yourusername>@your.domain","<yourpassword>")
        print result
        json_body = [{
            "measurement": "ldap_auth_successful",
            "tags": {
                "server": "<FQDN of TESTED SERVER>",
                "bu": "csg"
                },
            "fields": {
                "auth_successful": result
                }
        }]
        client.write_points(json_body)
        #print "sleep for 1min"
        time.sleep(delay)

if __name__ == '__main__':
    main()