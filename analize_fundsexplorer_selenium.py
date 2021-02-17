from selenium import webdriver
import time
import json

driver = webdriver.Chrome(
    executable_path=r"./chromedriver.exe"
)
driver.get("https://www.fundsexplorer.com.br/rendimentos-e-amortizacoes")
time.sleep(5)
table = driver.find_element_by_id('table-incomes-amortizations')
trs = table.find_elements_by_tag_name('tr')
data = []
for tr in trs:
    tds = tr.find_elements_by_tag_name('td')
    if len(tds) == 10:
        [codigo, nome_fundo, fechamento, valor_cota, yield_1_mes, yield_12_meses, tipo, periodo_referencia, data_base, data_pag] = tds
        if ',' in yield_1_mes.text and ',' in yield_12_meses.text:
            fechamento_value = float(fechamento.text.replace(',', '.'))
            if fechamento_value > 0:
                valor_cota_value = float(valor_cota.text.replace(',', '.'))
                yield_1_mes_value = float(yield_1_mes.text.replace(',', '.'))
                yield_12_meses_value = float(yield_12_meses.text.replace(',', '.'))
                porcentagem_value = (valor_cota_value/fechamento_value)*100
                data.append({
                    'codigo': codigo.text,
                    'fechamento': fechamento_value,
                    'valor_cota': valor_cota_value,
                    'porcentagem_formatted': "%.2f" % round(porcentagem_value, 2) + '%',
                    'porcentagem': valor_cota_value/fechamento_value,
                    'yield_1_mes': yield_1_mes_value,
                    'yield_12_meses': yield_12_meses_value
                })
data.sort(key=lambda x: x.get('porcentagem'))
print(json.dumps(data, indent=4, sort_keys=True))
driver.close()