NOME_DO_CANDIDATO = 'Moisés Rodrigues Alves'
EMAIL_DO_CANDIDATO = 'moisesinho_ra@hotmail.com'

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import sleep
from tkinter import E
from typing import Dict, List, Tuple

import requests

import input_logic
import year
MAIN_FOLDER = Path(__file__).parent.parent


def request_journals(start_date, end_date):
    url = 'https://engine.procedebahia.com.br/publish/api/diaries'

    r = requests.post(url, data={"cod_entity": '50', "start_date": start_date,
                                 "end_date": end_date})
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 400:
        sleep(10)
        return request_journals(start_date, end_date)
    return {}


def download_jornal(edition, path):
    url = 'http://procedebahia.com.br/irece/publicacoes/Diario%20Oficial' \
          '%20-%20PREFEITURA%20MUNICIPAL%20DE%20IRECE%20-%20Ed%20{:04d}.pdf'.format(int(edition))
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        with open(path, 'wb') as writer:
            writer.write(r.content)
        return edition, path
    return edition, ''


def download_mutiple_jornals(editions, paths):
    threads = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for edition, path in zip(editions, paths):
            threads.append(executor.submit(download_jornal, edition, path))

        results = []
        for task in as_completed(threads):
            results.append(task.result())

    results = [[r for r in results if r[0] == e][0] for e in editions]
    return [r[1] for r in results]


class JournalDownloader:
    def __init__(self):
        self.pdfs_folder = MAIN_FOLDER / 'pdfs'
        self.jsons_folder = MAIN_FOLDER / 'out'

        self.pdfs_folder.mkdir(exist_ok=True)
        self.jsons_folder.mkdir(exist_ok=True)

    def get_day_journals(self, year: int, month: int, day: int) -> List[str]:
        # TODO: get all journals of a day, returns a list of JSON paths

        date = f'{year}-{month}-{day}' # YYYY-MM-DD
        type(date)
        editions = request_journals(date, date)
        
        list_return=list()
        for a in range(0, len(editions['diaries'])):

               

            edition = editions['diaries'][a]['edicao']
            file_name = editions['diaries'][a]['arquivo']
            
            list_return.append(self.dump_json())
            download_jornal(edition, file_name)
            print(f'nº{a}\n\n')


    def get_month_journals(self, year: int, month: int) -> List[str]:
        # TODO: get all journals of a month, returns a list of JSON paths

        date_ini = f'{year}-{month}-{1}' # YYYY-MM-DD
        date_end = f'{year}-{month}-{year.days_in_monts(year, month)}'

        editions = request_journals(date_ini, date_end)
        
        list_return=list()
        for a in range(0, len(editions['diaries'])):

               

            edition = editions['diaries'][a]['edicao']
            file_name = editions['diaries'][a]['arquivo']
            list_return.append(self.dump_json())
            download_jornal(edition, file_name)
            print(f'nº{a}\n\n')


    def get_year_journals(self, year: int) -> List[str]:
        # TODO: get all journals of a year, returns a list of JSON paths
        # date = f'{year}-{month}-{day}' # YYYY-MM-DD
        date_init = f'{year}-{1}-{1}'
        date_end = f'{year}-{12}-{year.is_leap(year)}'
        editions = request_journals(date_init, date_end)
        
        list_return=list()
        for a in range(0, len(editions['diaries'])):

               

            edition = editions['diaries'][a]['edicao']
            file_name = editions['diaries'][a]['arquivo']
            list_return.append(self.dump_json())
            download_jornal(edition, file_name)
            print(f'nº{a}\n\n')


    @staticmethod
    def parse(response: Dict) -> List[Tuple[str, str]]:
        # TODO: parses the response and returns a tuple list of the date and edition
        pass

    def download_all(self, editions: List[str]) -> List[str]:
        # TODO: download journals and return a list of PDF paths. download in `self.pdfs_folder` folder
        #  OBS: make the file names ordered. Example: '0.pdf', '1.pdf', ...
        error = False
        i = 0
        journals = list()
        while not error:
            try:
                print(i, '...')
                print(download_jornal(i, self.pdfs_folder))
                i += 1
            except error:
                error = True
                print("End")

        print(journals)
        pass

    def dump_json(self, pdf_path: str, edition: str, date: str) -> str:
        if pdf_path == '':
            return ''
        output_path = self.jsons_folder / f"{edition}.json"
        data = {
            'path': str(pdf_path),
            'name': str(edition),
            'date': date,
            'origin': 'Irece-BA/DOM'
        }
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data,
                                  indent=4, ensure_ascii=False))
        return str(output_path) 



def main():
    Journal = JournalDownloader()
    Journal.get_day_journals(year=2017, month=7, day=10)
    # menu[2](self, 10)
    # Journal.download_all(self, 10)
    # download_mutiple_jornals(20, Journal.pdfs_folder)
    # while True:
    # j = request_journals('2021-01-20', '2021-02-21')

    # for i in range(len(j['diaries'])):
    #     print(j['diaries'][i]['extra'])

if __name__ == "__main__":
    main()
        
