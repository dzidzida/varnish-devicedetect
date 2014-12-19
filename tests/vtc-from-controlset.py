#!/usr/bin/env python
"""
Parse the list of manually classified User-Agent strings and
prepare a varnishtest test case that verifies the correct classification.

Author: Lasse Karstensen <lkarsten@varnish-software.com>, July 2012
"""

HEADER="""varnishtest "automatic test of control set"
server s1 {
       rxreq
       txresp
} -start
varnish v1 -vcl+backend {
        include "${projectdir}/../devicedetect.vcl";
        sub vcl_deliver {
            call devicedetect;
            set resp.http.X-UA-Device = req.http.X-UA-Device;
        }
} -start

client c1 {"""
TAILER="""}
client c1 -run
"""

def main():
    print HEADER
    for line in open("../controlset.txt"):
        line = line.strip()
        if line.startswith("#") or len(line) == 0:
            continue
        assert "\"" not in line

        classid, uastring = line.split("\t", 1)

        print "\ttxreq -hdr \"User-Agent: %s\"" % uastring
        print "\trxresp"
        print "\texpect resp.http.X-UA-Device == \"%s\"\n" % classid
    print TAILER

if __name__ == "__main__":
    main()
