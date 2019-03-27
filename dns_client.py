#!/usr/bin/env python3
import socket
import argparse
import os
from DNS.DNS import *


def main():
  parser = argparse.ArgumentParser(description="Basic DNS client lookup implemented by me")
  parser.add_argument('--hostname', help='the hostname to lookup')
  parser.add_argument('--forwarder', help='the dns server to forward the request to')
  args = parser.parse_args()

  hostname = args.hostname
  forwarder = args.forwarder

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  dns_request = DNS_Request('www.example.com')

  dns_request = dns_request.to_bytes()

  PORT = 53

  try:
    print('sending following request:')
    print(dns_request)
    sent = sock.sendto(dns_request, (forwarder, PORT))
    print('sent')

    # receive data
    data = sock.recvfrom(512)
    print('received {!r}'.format(data))
    

  finally:
    print('closing socket')
    sock.close()



if __name__ == "__main__":
  main()
