from urllib.request import urlopen
import json
import config

class Storage:
    def __init__(self):
        self._storage_companies = []
        self._apikey = config.apikey
        print('Хранилище проиницилизировано')

    def get_company_api(self,company):
        url = (f"https://financialmodelingprep.com/api/v3/profile/{company}/?apikey={self._apikey}")
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    def upload_storage(self):
        def get_companies_api():
            url = (f"https://financialmodelingprep.com/api/v3/stock/list?apikey={self._apikey}")
            response = urlopen(url)
            data = response.read().decode("utf-8")
            return json.loads(data)
        self._storage_companies = get_companies_api()
        print("Данные в хранилище загружены")


    def get_companies_data(self,company):
        try:
            chosenDict = next(item for item in self._storage_companies if item["symbol"] == company)
            return f"Компания - {chosenDict['name']} Цена - {chosenDict['price']} Биржа - {chosenDict['exchange']}"
            
        except StopIteration:
            return "Ввели неправильную компанию"
