import pandas as pd
from spk_model import WeightedProduct

class Smartphone():

    def __init__(self) -> None:
        self.smartphone = pd.read_csv('smartphone_202310311831.csv')

    def get_recs(self, kriteria):
        wp = WeightedProduct(self.smartphone.to_dict(orient="records"), kriteria)
        return wp.calculate

