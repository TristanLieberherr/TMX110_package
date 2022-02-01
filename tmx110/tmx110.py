import logging
from pymodbus.client.sync import ModbusTcpClient, ModbusSocketFramer
from pymodbus.constants import Defaults
from pymodbus.interfaces import Singleton
from ctypes import Structure, Union, c_uint16, c_float



class Keys(Singleton):
    RUN     = 0x81
    CAL     = 0x82
    ENTER   = 0x83
    UP      = 0x84
    DOWN    = 0x85
    LEFT    = 0x86
    RIGHT   = 0x87


class ValuesRaw(Structure):
    _fields_ = [("words", c_uint16 * 14)]


class ValuesStruct(Structure):
    _fields_ = [
        ("rate", c_float),
        ("load", c_float),
        ("speed", c_float),
        ("mt", c_float),
        ("rt", c_float),
        ("rt_MINI_CK", c_float),
        ("dt", c_float)
    ]


class ValuesUnion(Union):
    _fields_ = [("raw", ValuesRaw), ("struct", ValuesStruct)]


class StatusBits(Structure):
    _fields_ = [
        ("out_1", c_uint16, 1),
        ("out_2", c_uint16, 1),
        ("low_rate", c_uint16, 1),
        ("high_rate", c_uint16, 1),
        ("low_speed", c_uint16, 1),
        ("high_speed", c_uint16, 1),
        ("low_weigth", c_uint16, 1),
        ("high_weight", c_uint16, 1),
        ("alarme", c_uint16, 1),
        ("total_pulse", c_uint16, 1),
        ("hight_rt", c_uint16, 1),
        ("calibration", c_uint16, 1),
        ("ext_out", c_uint16, 1),
        ("zero_rate", c_uint16, 1),
        ("in_1", c_uint16, 1),
        ("in_2", c_uint16, 1)
    ]


class StatusBitsUnion(Union):
    _fields_ = [
        ("status", c_uint16),
        ("bits", StatusBits)
    ]


class TMX110(ModbusTcpClient):
    def __init__(self, host='127.0.0.1', port=Defaults.Port, framer=ModbusSocketFramer, **kwargs):
        """ Initialize a client instance

        :param host: The host to connect to (default 127.0.0.1)
        :param port: The modbus port to connect to (default 502)
        :param source_address: The source address tuple to bind to (default ('', 0))
        :param timeout: The timeout to use for this socket (default Defaults.Timeout)
        :param framer: The modbus framer to use (default ModbusSocketFramer)

        .. note:: The host argument will accept ipv4 and ipv6 hosts
        """
        super().__init__(host, port, framer, **kwargs)
        ## Constants
        self.__ADDRESS_FLOWRATE         = 0x0000
        self.__ADDRESS_RT               = 0x0001
        self.__ADDRESS_MT               = 0x0002
        self.__ADDRESS_SPEED            = 0x0003
        self.__ADDRESS_STATUS           = 0x0004
        ...
        self.__ADDRESS_LCD1_START       = 0x000F
        self.__ADDRESS_LCD1_END         = 0x0023
        self.__ADDRESS_LCD2_START       = 0x0024
        self.__ADDRESS_LCD2_END         = 0x0037
        self.__ADDRESS_FLOWRATE_FLOAT   = 0x0039
        self.__ADDRESS_LOAD_FLOAT       = 0x003B
        self.__ADDRESS_SPEED_FLOAT      = 0x003D
        self.__ADDRESS_KEYSIM           = 0x0100
        ...
        self.__ADDRESS_ERASE_RT         = 0x0120
        ## Attributes
        self._values_union = ValuesUnion()
        self._status_union = StatusBitsUnion()

    ## Internal methods
    def _read_LCD(self, start, end):
        response = self.read_holding_registers(start, end - start)
        try:
            return "".join([chr(c) for c in response.registers])
        except Exception as e:
            logging.error(e)
            return -1

    ## Read methods
    def read_values(self) -> ValuesStruct:
        response = self.read_holding_registers(self.__ADDRESS_FLOWRATE_FLOAT, 14)
        try:
            for i, word in enumerate(response.registers) :
                self._values_union.raw.words[i] = word
        except Exception as e:
            logging.error(e)
        finally:           
            return self._values_union.struct

    def read_status(self) -> StatusBits:
        response = self.read_holding_registers(self.__ADDRESS_STATUS)
        try:
            self._status_union.status = response.registers[0]
        except Exception as e:
            logging.error(e)
        finally:
            return self._status_union.bits
            
    def read_LCD1(self) -> str:
        return self._read_LCD(self.__ADDRESS_LCD1_START, self.__ADDRESS_LCD1_END)

    def read_LCD2(self) -> str:
        return self._read_LCD(self.__ADDRESS_LCD2_START, self.__ADDRESS_LCD2_END)

    ## Write methods
    def simulate_key(self, key):
        return self.write_register(self.__ADDRESS_KEYSIM, key)

    def erase_RT(self):
        return self.write_register(self.__ADDRESS_ERASE_RT, 1)




    # def write_speed(self, value):
    #     return self.write_register(self.__ADDRESS_SPEED, value)

    # def read_flowrate(self) -> int:
    #     try:
    #         response = self.read_holding_registers(self.__ADDRESS_FLOWRATE)
    #     except:
    #         ...
    #     else: return response.registers[0]

    # def read_RT(self) -> int:
    #     try:
    #         response = self.read_holding_registers(self.__ADDRESS_RT)
    #     except:
    #         ...
    #     else: return response.registers[0]

    # def read_MT(self) -> int:
    #     try:
    #         response = self.read_holding_registers(self.__ADDRESS_MT)
    #     except:
    #         ...
    #     else: return response.registers[0]

    # def read_speed(self) -> int:
    #     try:
    #         response = self.read_holding_registers(self.__ADDRESS_SPEED)
    #     except:
    #         ...
    #     else: return response.registers[0]/100