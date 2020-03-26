import pathlib


class TempSensor:
    '''Classe para realizar a leitura de temperatura de um sensor DS18B20.

    :args:
        _id: ID único do sensor
    '''
    def __init__(self, _id):
        self._id = _id
        self._temp = 0.0

    def __read_temp_file(self):
        '''Carrega todas linhas do arquivo criado pelo sensor.'''
        # Caminho para o arquivo
        devices_dir = pathlib.Path('/sys/bus/w1/devices')
        sensor_file = devices_dir / self._id / 'w1_slave'
        # Le todas as linhas
        f = open(sensor_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        '''Read temperature from 1-Wire sensor'''
        lines = self.__read_temp_file()
        # Uma leitura válida possui a string "YES" no final da primeira linha
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.1)
            lines = self.__read_temp_file()
        # A segunda linha contém a temperatura lida
        # após o texto t=
        tindex = lines[1].find('t=')
        if tindex == -1:
            return False
        temp_string = lines[1].strip()[tindex+2:]
        self._temp = float(temp_string) / 1000.0
        return True

    @property
    def temperature(self):
        return self._temp

    @property
    def temperature_fahrenheit(self):
        return (self._temp * 9 / 5) + 32.0

    @property
    def temperature_kelvin(self):
        return self._temp + 273.15

    def __str__(self):
        return f'Sensor {self._id} ({self.temperature} ºC)'

    def __repr__(self):
        return self.__str__()
