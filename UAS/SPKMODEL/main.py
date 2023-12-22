import sys

from colorama import Fore, Style
from models import Base, Smartphone
from engine import engine

from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import NAMA_HP

session = Session(engine)

def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has created!')

class BaseMethod():

    def __init__(self):
        # 1-7 (Kriteria)
        self.raw_weight = {
            'nama': 6,
            'ukuran_layar': 1,
            'memori_internal': 3,
            'kamera_belakang': 2,
            'kapasitas_baterai': 4,
            'harga': 5
        }

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Smartphone)
        return [{
            'name': smartphone.nama,
            'nama': NAMA_HP["".join([x for x in NAMA_HP.keys() if x.lower() in smartphone.nama.lower()])],
            'ukuran_layar': float(smartphone.ukuran_layar.replace(" inch", "")),
            'memori_internal': int(smartphone.memori_internal.replace(" GB", "")),
            'kamera_belakang': int(smartphone.kamera_belakang.replace("MP", "")),
            'kapasitas_baterai': int(smartphone.kapasitas_baterai.replace("mAh", "")),
            'harga': smartphone.harga
        } for smartphone in session.scalars(query)]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]

        nama = [] # max
        ukuran_layar = [] # max
        memori_internal = [] # max
        kamera_belakang = [] # max
        kapasitas_baterai = [] # max
        harga = [] # min

        for data in self.data:
            nama.append(data['nama'])
            ukuran_layar.append(data['ukuran_layar'])
            memori_internal.append(data['memori_internal'])
            kamera_belakang.append(data['kamera_belakang'])
            kapasitas_baterai.append(data['kapasitas_baterai'])
            harga.append(data['harga'])

        max_nama = max(nama)
        max_ukuran_layar = max(ukuran_layar)
        max_memori_internal = max(memori_internal)
        max_kamera_belakang = max(kamera_belakang)
        max_kapasitas_baterai = max(kapasitas_baterai)
        min_harga = min(harga)

        return [{
            'name': data['name'],
            'nama': data['nama']/max_nama, # benefit
            'ukuran_layar': data['ukuran_layar']/max_ukuran_layar, # benefit
            'memori_internal': data['memori_internal']/max_memori_internal, # benefit
            'kamera_belakang': data['kamera_belakang']/max_kamera_belakang, # benefit
            'kapasitas_baterai': data['kapasitas_baterai']/max_kapasitas_baterai, # benefit
            'harga': min_harga/data['harga'], # cost
        } for data in self.data]
 

class WeightedProduct(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight[WP]
        result = {row['name']:
            round(
                row['nama'] ** weight['nama'] *
                row['ukuran_layar'] ** weight['ukuran_layar'] *
                row['memori_internal'] ** weight['memori_internal'] *
                row['kamera_belakang'] ** weight['kamera_belakang'] *
                row['kapasitas_baterai'] ** weight['kapasitas_baterai'] *
                row['harga'] ** (-weight['harga'])
                , 2
            )

            for row in self.normalized_data}
        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1]))

class SimpleAdditiveWeighting(BaseMethod):
    
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight
        result =  {row['name']:
            round(
                row['nama'] * weight['nama'] +
                row['ukuran_layar'] * weight['ukuran_layar'] +
                row['memori_internal'] * weight['memori_internal'] +
                row['kamera_belakang'] * weight['kamera_belakang'] +
                row['kapasitas_baterai'] * weight['kapasitas_baterai'] +
                row['harga'] * -weight['harga']
                , 2
            )
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1]))

def run_saw():
    saw = SimpleAdditiveWeighting()
    print('result:', saw.calculate)

def run_wp():
    wp = WeightedProduct()
    print('result:', wp.calculate)

if len(sys.argv)>1:
    arg = sys.argv[1]

    if arg == 'create_table':
        create_table()
    elif arg == 'saw':
        run_saw()
    elif arg =='wp':
        run_wp()
    else:
        print('command not found')
