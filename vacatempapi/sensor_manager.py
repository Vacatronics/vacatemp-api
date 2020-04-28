import time
import threading
import os
import pathlib
from datetime import datetime
from .sensor import TempSensor


class TempSensorManager(threading.Thread):
    '''Classe para gerenciar os sensores disponíveis no sistema.'''
    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensors = []
        self._is_running = False
        self._period = 1800
        self.db = db

    def init(self):
        '''Classe para inicializar o módulo de leitura one-wire.'''
        os.system('modprobe w1-gpio-cl m1="gdt:4"')
        os.system('modprobe w1-therm')

    def list_sensors(self):
        '''Lista todos os sensores disponíveis no sistema.'''
        self.init()
        devices_dir = pathlib.Path('/sys/bus/w1/devices')
        self.sensors = []
        for sensor in devices_dir.glob('**/28-*'):
            # Verifica se sensores estão cadastrados no banco ou não
            # E insere caso não estejam
            if self.db:
                sdb = self.db.sensors.find_one({'_id': sensor.name})
                if not sdb:
                    self.db.sensors.insert_one({
                        '_id': sensor.name, 
                        '_created': datetime.now(), 
                        '_updated': datetime.now()
                })
            self.sensors.append(TempSensor(sensor.name))


    def run(self):
        '''Rotina para ler os sensores a cada minuto.'''
        self._is_running = True
        last_read = datetime(1900, 1, 1)
        while self._is_running:
            if (datetime.now() - last_read).total_seconds() > self._period:
                # Hora de ler 
                for sensor in self.sensors:
                    try:
                        if sensor.read_temp() and self.db:
                            # Salva no banco
                            self.db.temperatures.insert_one({
                                'sensor': sensor._id, 
                                'temperature': sensor.temperature,
                                '_created': datetime.now(),
                                '_updated': datetime.now()
                            })
                    except:
                        # TODO: Deveriamos logar isso, mas vamos deixar 
                        # sem nada por enquanto.
                        pass
                # Atualize data ultima leitura
                last_read = datetime.now()
            time.sleep(0.1)
            
    def stop(self):
        self._is_running = False
