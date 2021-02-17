from selenium import webdriver
import time
import json
import pandas as p
from ExcelFactory import XlsFactory

driver = webdriver.Chrome(
    executable_path=r"./chromedriver.exe"
)
driver.get("https://fiis.com.br/anual/")
time.sleep(12)
table = driver.find_element_by_id('items')
items = table.find_elements_by_tag_name('li')
close_modal = driver.find_element_by_id('popup-x')
close_modal.click()
time.sleep(2)
modal_container_close = driver.find_element_by_class_name('modal__close')
modal_container_close.click()
time.sleep(2)
rows_data = []

for item in items:
    print(str(items.index(item)) + '/' + str(len(items)))
    try:
        code = item.find_element_by_class_name('ticker')
        name = item.find_element_by_class_name('name')
        item.click()
        time.sleep(2)
        table = item.find_element_by_tag_name('table')
        tbody = table.find_element_by_tag_name('tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        cols_data = []
        for row in rows:
            cols = row.find_elements_by_tag_name('td')
            if len(cols) == 3:
                [year, dividend_yield, yield_share] = cols
                dividend_yield_value = float(dividend_yield.text.replace('%', '').replace(',', '.'))
                yield_share_value = float(yield_share.text.replace('R$ ', '').replace(',', '.'))
                cols_data.append({
                    'year': int(year.text),
                    'dividend_yield': dividend_yield_value,
                    'yield_share': yield_share_value
                })
        value = {
            'code': code.text,
            'name': name.text,
            'data': cols_data
        }
        rows_data.append(value)
    except Exception as e:
        print(str(items.index(item)) + '/' + str(len(items)) + ' - Exception')

# data.sort(key=lambda x: x.get('porcentagem'))
XlsFactory.create_csv(f'{str(time.time())}-fiis.xls', 'fiis', rows_data)
df = p.DataFrame(rows_data)
df.to_excel('pandas_xls.xlsx')
# print(json.dumps(rows_data, indent=2, sort_keys=True))
driver.close()