from bs4 import BeautifulSoup
import requests

url="https://fiis.com.br/anual/"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "html.parser")
#table = soup.find("table", attrs={"id": "table-incomes-amortizations"})
listFi = soup.find("ul", attrs={"id": "items"})
for item in listFi:
    title = item.find('span')
    if (not isinstance(title, int)):
        name = title.contents[0]
        print(name)
        table = item.find('table')
        print(table.find_all('tbody'))