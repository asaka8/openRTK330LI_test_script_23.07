from socket import *
import os,sys
import time
import psutil
import serial
import sys
import struct
import hashlib
import re


# if len(sys.argv) < 3:
#     print('para wrong')
# com_set = sys.argv[1]

# baud_set = sys.argv[2]

class Decode:
    def __init__(self):
        self.com_set = 'COM8'
        self.baud_set = 460800

    def calc_crc(self, payload):
        '''
        Calculates 16-bit CRC-CCITT
        '''
        crc = 0x1D0F
        for bytedata in payload:
            crc = crc ^ (bytedata << 8)
            i = 0
            while i < 8:
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc = crc << 1
                i += 1

        crc = crc & 0xffff
        crc_msb = (crc & 0xFF00) >> 8
        crc_lsb = (crc & 0x00FF)
        return [crc_msb, crc_lsb]

    def packet_cmd(self, cmd_type,cmd_len,cmd_data):
        packet = []
        packet.extend(bytes(cmd_type, 'utf-8'))
        packet.append(cmd_len)
        if cmd_len > 0:
            packet.extend(cmd_data)
        final_packet = packet 
        cmd_packet = [0x55,0x55] + final_packet + self.calc_crc(final_packet)
        cmd_hex = []
        for ele in cmd_packet:
            cmd_hex.append( hex(ele) )
        # print('list',cmd_hex)
        return bytes(cmd_packet)

    def data_parse(selfm, data,cmd):
        parse_state = 0
        get_data = []
        len = 0
        get_len = 0
        for ele in data:
            if parse_state == 0:
                if ele == 0x55:
                    parse_state = 1
                    continue
            if parse_state == 1:
                if ele == 0x55:
                    parse_state = 2
                    continue
            if parse_state == 2:
                if ele == ord(cmd[0]):
                    parse_state = 3
                    continue
                else:
                    parse_state = 0
                    continue
            if parse_state == 3:
                if ele == ord(cmd[1]):
                    parse_state = 4
                    # print('--------------------------')
                    continue
                else:
                    parse_state = 0
                    continue
                    
            if parse_state == 4:
                len = ele
                # print('len = {0}'.format(ele))
                parse_state = 5
                continue
            if parse_state == 5:
                if get_len < len:
                    get_len+= 1
                    get_data.append(ele)
                    continue
                else:
                    return get_data
                    continue

    def get_md5_from_chip_id(self, chip_id):
        hash_md5 = hashlib.md5(bytes(chip_id))
        md5 = hash_md5.hexdigest()
        tmp = re.findall(r'.{2}', md5)
        md5_list = [int(ele, 16) for ele in tmp]
        key = list('Aceinna')
        key_list = [ord(ele) for ele in key] + [0x00]
        new_data = md5_list + key_list 

        hash_md5 = hashlib.md5(bytes(new_data))
        md5 = hash_md5.hexdigest()
        tmp = re.findall(r'.{2}', md5)
        md5_list = [int(ele, 16) for ele in tmp]

        # print(md5_list)
        return md5_list


    def start_decode(self):
        python_serial = serial.Serial(self.com_set,int(self.baud_set),timeout=0.01)
        while True:
            user_cmd = 'gI0'
            cmd_type = user_cmd[0:2]  # bytes(user_cmd[0:2], 'utf-8')
            cmd_len = 0
            cmd_data = None

            user_cmd_packet_all = self.packet_cmd(cmd_type,cmd_len,cmd_data)
            data = python_serial.read_all()
            # print('packet',user_cmd_packet_all)
            python_serial.write(user_cmd_packet_all)
            if cmd_len == 0:
                respose_to_parse = user_cmd[0:2]

            else:
                respose_to_parse = user_cmd[3:5]
            time.sleep(1)

            while True:
                data = python_serial.read_all()
                if len(data) > 0:
                    #print(data)                        
                    data_get = self.data_parse(data,respose_to_parse)
                    if data_get != None :
                        # print(bytes(data_get))
                        md5_data = self.get_md5_from_chip_id(data_get)
                        
                        cmd_type = 'uP'
                        cmd_len = 16 + 4
                        cmd_data = [62,0,0,0] + md5_data
                        user_cmd_packet_all = self.packet_cmd(cmd_type,cmd_len,cmd_data)
                        python_serial.write(user_cmd_packet_all)
                        #data_get_hex = [("%02x" % ele) for ele in data_get  ]
                        time.sleep(2)
                        cmd_type = 'sC'
                        cmd_len = 0
                        cmd_data = None
                        user_cmd_packet_all = self.packet_cmd(cmd_type,cmd_len,cmd_data)
                        # print(user_cmd_packet_all)
                        python_serial.write(user_cmd_packet_all)                    

                    break
            break
        python_serial.close()


D = Decode()
D.start_decode()