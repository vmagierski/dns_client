#!/usr/bin/env python3
import os
import struct
import myutils

'''
    +---------------------+
    |        Header       |
    +---------------------+
    |       Question      | the question for the name server
    +---------------------+
    |        Answer       | RRs answering the question
    +---------------------+

     no Authority or Additional records yet
'''


class DNS_Message:
    def __init__(self, hostname, header=None, question=None, answer=None):
        self.header = Header()
        print('created header: ')
        print(self.header.to_bytes())
        print('header msg id: ')
        print(self.header.msg_id)

        self.question = self._construct_question_section(hostname)
        self.answer = answer

    def to_bytes(self):
        return self.header.to_bytes() + self.question

    def _construct_question_section(self, name):
        QName = self._construct_QName(name)
        QType = 1  # 2 bytes, value of 1 represents A record Type
        QClass = 1  # 2 bytes, value of 1 represents Internet

        question_section_bytes = QName
        question_section_bytes += struct.pack('>hh', QType, QClass)
        return question_section_bytes

    def _construct_QName(self, name):
        '''

            _construct_QName(self, www.mydomain.com):

            =>
            Then, encode each part separately, with the leading byte representing the length 
            of the following letters:

            0x03 0x77 0x77 0x77                             (for "length of 3" followed by "www")
            0x08 0x6D 0x79 0x64 0x6F 0x6D 0x61 0x69 0x6E    (for "length of 8" followed my "mydomain")
            0x03 0x63 0x6F 0x6D                             (for "length of 3" followed by "com")
            Finally, add a closing byte of 0x00 to signify the end of the domain string.


        resource: https://ecs-network.serv.pacific.edu/past-courses/2015-fall-ecpe-170/lab/lab-network-inter
        '''

        parts = name.split(".")
        QName = bytearray()

        for p in parts:
            QName += bytes([len(p)])
            QName += bytearray(p, 'utf-8')

        QName += b'\x00'
        return bytes(QName)


class Header:
    def __init__(self,
             msg_id=os.urandom(2),    # 2 byte random header id
             QR='0',                  # 1 bit, 0 if query, 1 if response
             OPCODE='0000',           # 4 bits, value of 0 represents standard query
             AA='0',                  # 1 bit. valid in responses only, represents authoritative answer
             TC='0',                  # 1 bit. truncation
             RD='1',                  # 1 bit, recursion desired
             RA='0',                  # 1 bit, recursion available ( valid in responses only)
             Reserved='000',          # 3 bits, unused, set to 0
             RCODE='0000',            # 1 byte, identifies response type (ignored in requests)
             QDCount=1,               # Each Count variable is 2 bytes
             ANCount=0,
             NSCount=0,
             ARCount=0):

        self.msg_id = msg_id
        self.QR = QR
        self.OPCODE = OPCODE
        self.AA = AA
        self.TC = TC
        self.RD = RD
        self.RA = RA
        self.Reserved = Reserved
        self.RCODE = RCODE
        self.QDCount = QDCount
        self.ANCount = ANCount
        self.NSCount = NSCount
        self.ARCount = ARCount

    def from_bytes(self, byte_data):
        # Unpack/convert from network to host order?
        self.msg_id = byte_data[0:2]
        flags = byte_data[2:4] 

        flags_as_string_of_ones_and_zeros = ''

        for b in flags:
            for i in range(0,8):
                current = '1' if myutils.is_set(i, b) else '0'
                flags_as_string_of_ones_and_zeros += current

        self.QR = myutils.is_set(0, flags[0])
        self.OPCODE = flags_as_string_of_ones_and_zeros[1:5]
        self.AA = flags_as_string_of_ones_and_zeros[5]
        self.TC = flags_as_string_of_ones_and_zeros[6]
        self.RD = flags_as_string_of_ones_and_zeros[7]
        self.RA = flags_as_string_of_ones_and_zeros[8]
        self.Reserved = flags_as_string_of_ones_and_zeros[8:11]
        self.RCODE = flags_as_string_of_ones_and_zeros[11:16]

        self.QDCount = byte_data[5:7]
        self.ANCount = byte_data[7:9]
        self.NSCount = byte_data[9:11]
        self.ARCount = byte_data[11:13]
        return self

    def to_bytes(self):
        flags = int(self.QR +
                    self.OPCODE +
                    self.AA +
                    self.TC +
                    self.RD +
                    self.RA +
                    self.Reserved +
                    self.RCODE,
                    2)


        header_bytes = self.msg_id
        flags_as_bytes = struct.pack('>h', flags)
        header_bytes += flags_as_bytes
        header_bytes += struct.pack('>hhhh',
                                    self.QDCount,
                                    self.ANCount,
                                    self.NSCount,
                                    self.ARCount
                                    )
        return header_bytes


#class Resource_Record:
#    def __init__(self,
#                 name,
#                 rr_type,
#                 rr_class,
#                 ttl,
#                 rlength,
#                 rdata
#                 ):
#        
#        '''
#NAME	The name being returned e.g. www or ns1.example.net If the name is in the same domain as the question then typically only the host part (label) is returned, if not then a FQDN is returned.
#TYPE	The RR type, for example, SOA or AAAA
#CLASS	The RR class, for instance, Internet, Chaos etc.
#TTL	The TTL in seconds of the RR, say, 2800
#RLENGTH	The length of RR specific data in octets, for example, 27
#RDATA	The RR specific data (see Binary RR Formats below) whose length is defined by RDLENGTH, for instance, 192.168.254.2
#        '''
#

class DNS_Response:
    def __init__(self, raw_data):
        header = Header().from_bytes(raw_data[0:12]) # header is first 12 bytes of response

    def parse_data(self, data):
        '''
            takes a binary string of data and p
        '''
