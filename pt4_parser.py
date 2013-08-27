import sys
import struct

def parse(filename):
    with open(filename, 'rb') as input:
        header = input.read(212)
        capture_data_mask = ord(header[158])
        #print hex(capture_data_mask)
        _ = input.read(272 - 212)
        status = input.read(60)
        _ = input.read(1024 - 272 - 60)

        data =  input.read()
        offset = 0
        unpacker = struct.Struct('hH')
        error_counter = 0
        for i in xrange(len(data)/unpacker.size):
            current_byte, voltage_byte = unpacker.unpack_from(data, i * unpacker.size)
            if current_byte == 0x8001 or voltage_byte == 0xffff:
                continue
            coarse_measurement = current_byte & 0x01
            current_ticks = current_byte & 0xfffe
            if coarse_measurement:
                current_ma = current_ticks * .250
            else:
                current_ma = current_ticks * .001
            voltage_ticks = voltage_byte & 0xfffc
            voltage_v = voltage_ticks * .000125

            print '%.4f,%.3f' % (i * .0002, round(current_ma * voltage_v, 3))



if __name__ == "__main__":
    parse(sys.argv[1])
