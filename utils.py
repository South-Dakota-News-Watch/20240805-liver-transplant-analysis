from bs4 import BeautifulSoup
import pandas as pd

def get_headers(html_file_in):
    with open(html_file_in, 'r') as infile:
        html = infile.read()

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')

    columns = []

    for row in rows:
        cells = row.find_all('td')
        if cells:
            columns.append(cells[0].text)

    return columns


def get_df(datfile_path, **kwargs):
    filepath_stub = datfile_path.split('.DAT')[0]
    html_file = f'{filepath_stub}.htm'
    headers = get_headers(html_file)

    df = pd.read_csv(
        datfile_path,
        sep='\t',
        names=headers,
        low_memory=False,
        na_values=[
            '.',
            'Null or Missing'
        ],
        **kwargs
    )

    return df