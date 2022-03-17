import time
import struct
import io
import csv
from unittest import result
from Test_Logger import TestLogger
from Test_Cases import Test_Section
from Test_Cases import Test_Case
from Test_Cases import Code
from Test_Cases import Condition_Check
from openRTK330LI_decode import Decode

# user input command
INPUT_pG = [0x70, 0x47]
INPUT_gV = [0x67, 0x56]
INPUT_gB = [0x67, 0x42]
INPUT_uP = [0x75, 0x50]
INPUT_uB = [0x75, 0x42]
INPUT_sC = [0x73, 0x43]
INPUT_rD = [0x72, 0x44]
INPUT_cA = [0x63, 0x41]

# user uart output data
OUTPUT_s1 = [0x73, 0x31]
OUTPUT_i1 = [0x69, 0x31]
OUTPUT_g1 = [0x67, 0x31]
OUTPUT_o1 = [0x6F, 0x31]
OUTPUT_y1 = [0x79, 0x31]

# user uart output data
OUTPUT_s1_RATE_HZ = 1
OUTPUT_i1_RATE_HZ = 50
OUTPUT_g1_RATE_HZ = 1
OUTPUT_o1_RATE_HZ = 1
OUTPUT_y1_RATE_HZ = 1

LONG_TERM_TEST_CNT = 10000

# Add test scripts here
class Test_Scripts:
    uut = None

    def __init__(self, device):
        Test_Scripts.uut = device
        self.decode = Decode()
    
    def _message_no_payload_test(self, message_type):
        message = []
        message += message_type
        message += [0x0]
        
        response = Test_Scripts.uut.sensor_command(message)
        
        if response:
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False,struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0]

    def _rd_field_test(self, message_type):        
        FIELDS_NUM = 10
        message = []
        message += message_type

        packet_len = 1 + 2 * FIELDS_NUM
        message.append(packet_len)
        message.append(FIELDS_NUM)        
        
        for i in  range(FIELDS_NUM):
            message += list(struct.pack('>H', i + 8))

        response = Test_Scripts.uut.sensor_command(message)
              
        if response:
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False, 0, struct.unpack('<H', bytes(message_type))[0]
    
            
    def _wr_field_test(self, message_type):
        FIELDS_NUM = 10
        message = []
        message += message_type

        packet_len = 1 + 4 * FIELDS_NUM
        message.append(packet_len)
        message.append(FIELDS_NUM)        
        
        for i in  range(FIELDS_NUM):
            message += list(struct.pack('>H', i + 8))
            message += list(struct.pack('>H', i + 1))
 
        response = Test_Scripts.uut.sensor_command(message)
        #print(response)
              
        if response:
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False, 0, struct.unpack('<H', bytes(message_type))[0]
        
    def _rd_eeprom_test(self, message_type, start_address, word_read_num):
        message = []
        message += message_type
        message_len = 3
        message.append(message_len)
        start_address_list = struct.pack('>H', start_address)
        message += start_address_list
        message.append(word_read_num)
        
        response = Test_Scripts.uut.sensor_command(message)
        
        if response:
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False, 0, struct.unpack('<H', bytes(message_type))[0]
            
    def _wr_eeprom_test(self, message_type, start_address, word_write_num, data_write = []):
        message = []
        message += message_type
        message_len = 3 + word_write_num * 2
        message.append(message_len)
        start_address_list = struct.pack('>H', start_address)
        message += start_address_list
        message.append(word_write_num)
        message += data_write
        
        response = Test_Scripts.uut.sensor_command(message)
        
        if response:
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False,struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0]
                
    def get_hardware_version_test(self):
        message = []
        message_type = INPUT_pG
        message_len = 0x00        
        
        message += message_type
        message.append(message_len)
        response = Test_Scripts.uut.sensor_command(message)
        if response:
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False,struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0]
    
    def get_software_version_test(self):
        message = []
        message_type = INPUT_gV
        message_len = 0x00        
        
        message += message_type
        message.append(message_len)
        response = Test_Scripts.uut.sensor_command(message)
        if response:
            print(response)
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False,struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0]        
    
    def set_one_user_parameter_test(self):
        message = []
        message_type = INPUT_uP
        message_len = 8        
        
        message += message_type
        message.append(message_len)
        parameter_id = 4
        
        message += list(struct.pack('>I', parameter_id))
        
        parameter_value = 50
        message += list(struct.pack('>f', parameter_value))
        
        
        response = Test_Scripts.uut.sensor_command(message)
        if response:
            print(response)
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False,struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0] 
    
    def save_user_parameters(self):
        return self._message_no_payload_test(INPUT_sC)

    def restore_default_parameters(self):
        result = self._message_no_payload_test(INPUT_rD)
        Test_Scripts.uut.UART_close()
        time.sleep(0.01)
        self.decode.start_decode()  # decode the openrtk after restore
        print('openrtk has been decode')
        time.sleep(0.01)
        Test_Scripts.uut.UART_open()
        return result
    
    def get_continuous_user_parameters(self):
        message = []
        message_type = INPUT_gB
        message_len = 0x02        
        
        message += message_type
        message.append(message_len)
        
        start_parameter_id = 0
        end_parameter_id = 18
        message.append(start_parameter_id)
        message.append(end_parameter_id)
        
        response = Test_Scripts.uut.sensor_command(message)
        if response:
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False,struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0]    

    def set_user_parameters_same_category(self):
        message = []
        message_type = INPUT_uB
        message_len = 5        
        
        message += message_type
        message.append(message_len)
        
        start_parameter_id = 2
        message.append(start_parameter_id)
        
        for i in range(4):
            message.append(i)
        
        response = Test_Scripts.uut.sensor_command(message)
        if response:
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False,struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0]           

    def set_car_speed(self):
        message = []
        message_type = INPUT_cA
        message_len = 4        
        
        message += message_type
        message.append(message_len)
        
        speed_val = 80.0
        message+= list(struct.pack('<f', speed_val))        
        
        response = Test_Scripts.uut.sensor_command(message)
        if response:
            if(response[0] == bytes(message_type)):
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False,struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0]
    
    def _packet_rate_check(self, message_type, rateHz):
        check_ok_times = 0
        time_delta = 1.2 / rateHz
        
        for i in range(5):
            time.sleep(0.2)
            response = Test_Scripts.uut.read_response(message_type)
            if response:
                t0 = time.time()
                response = Test_Scripts.uut.read_response(message_type)
                if response:
                    t2 = time.time() - t0
                    #print(t2, time_delta)
                    if t2 < time_delta:
                        check_ok_times += 1
                    else:
                        break
                else:
                    break
            else:
                break
        

        if response:
            if check_ok_times == 5:
                return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
            else:
                return False,struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0] 

        
    def corrIMU_data_packet_test(self):
        return self._packet_rate_check(OUTPUT_s1, OUTPUT_s1_RATE_HZ)
        
    def gnss_solution_data_packet_test(self):
        return self._packet_rate_check(OUTPUT_g1, OUTPUT_g1_RATE_HZ)
        
    def ins_solution_data_packet_test(self):
        return self._packet_rate_check(OUTPUT_i1, OUTPUT_i1_RATE_HZ)

    def odometer_data_packet_test(self):
        return self._packet_rate_check(OUTPUT_o1, OUTPUT_o1_RATE_HZ)
        
    def status_data_packet_test(self):
        return self._packet_rate_check(OUTPUT_y1, OUTPUT_y1_RATE_HZ)

    def long_term_test(self):
        message = []
        message_type = INPUT_pG
        message_len = 0x00        
        
        message += message_type
        message.append(message_len)
        
        error_cnt = 0
        success_cnt = 0
        
        for i in range(LONG_TERM_TEST_CNT):
            response = Test_Scripts.uut.sensor_command(message)
            #print(response)
            if response is None or (response and response[0] != bytes(message_type)):
                error_cnt += 1
                break
            else:
                success_cnt+=1
                if success_cnt % 100 == 0 or success_cnt == LONG_TERM_TEST_CNT:
                    print('success_cnt:', success_cnt) 
                
                
        if error_cnt == 0:
            return True, struct.unpack('<H', response[0])[0], struct.unpack('<H', bytes(message_type))[0]
        else:
            return False,0, struct.unpack('<H', bytes(message_type))[0]  


#################################################

class Test_Environment:

    def __init__(self, device):
        self.scripts = Test_Scripts(device)
        self.test_sections = []

    # Add test scetions & test scripts here
    def setup_tests_(self):
        section1 = Test_Section("user output command verification")
        self.test_sections.append(section1)        
        section1.add_test_case(Code("corrIMU data packet test",   self.scripts.corrIMU_data_packet_test))
        section1.add_test_case(Code("gnss solution data packet test",   self.scripts.gnss_solution_data_packet_test))
        section1.add_test_case(Code("ins solution data packet test",   self.scripts.ins_solution_data_packet_test))
        section1.add_test_case(Code("status data packet test",   self.scripts.status_data_packet_test))
        section1.add_test_case(Code("odometer car speed packet test", self.scripts.odometer_data_packet_test))

        section2 = Test_Section("user input command verification")
        self.test_sections.append(section2)        
        section2.add_test_case(Code("get hardware version test",   self.scripts.get_hardware_version_test))
        section2.add_test_case(Code("get software version test",   self.scripts.get_software_version_test))
        section2.add_test_case(Code("set one parameter test",   self.scripts.set_one_user_parameter_test)) 
        section2.add_test_case(Code("save user parameters test",   self.scripts.save_user_parameters)) 
        section2.add_test_case(Code("get continuous user parameters test",   self.scripts.get_continuous_user_parameters))
        section2.add_test_case(Code("get user parameters of the same category test",   self.scripts.set_user_parameters_same_category))
        section2.add_test_case(Code("restore default parameters test",   self.scripts.restore_default_parameters))
        section2.add_test_case(Code("set car speed test",   self.scripts.set_car_speed))

        section3 = Test_Section("long term packet test verification")
        self.test_sections.append(section3)
        section3.add_test_case(Code("long term packet test", self.scripts.long_term_test))

    def setup_tests(self):
        section1 = Test_Section("user input command verification")
        self.test_sections.append(section1)        
        section1.add_test_case(Code("set one parameter test",   self.scripts.set_one_user_parameter_test)) 
        section1.add_test_case(Code("save user parameters test",   self.scripts.save_user_parameters)) 
        # section1.add_test_case(Code("restore default parameters test",   self.scripts.restore_default_parameters))
        
    def run_tests(self):
        for section in self.test_sections:
            section.run_test_section()

    def print_results(self):
        print("\tTest Results::")
        for section in self.test_sections:
            print("\t\tSection " + str(section.section_id) + ": " + section.section_name + "\r\n")
            for test in section.test_cases:
                id = str(section.section_id) + "." + str(test.test_id)
                result_str = "\t\t\tPassed --> " if test.result['status'] else "\t\t\tFailed --x "
                print(result_str + id + " " + test.test_case_name + "\t\t"+ "Expected: "+ test.result['expected'] + " Actual: "+  test.result['actual'] + "\r\n")

    def _create_csv(self, file_name, fieldnames):
        with open(file_name, 'w+') as out_file:
            writer = csv.DictWriter(out_file, fieldnames = fieldnames)
            writer.writeheader()

    def log_results(self, file_name):
        logger = TestLogger(file_name)
        field_names = ['id', 'test_name', 'expected', 'actual', 'status']
        logger.create(field_names)
        for section in self.test_sections:
            for test in section.test_cases:
                logger.write_log(test.result)
