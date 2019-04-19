from lxml import html
import requests
page = requests.get('https://www.meteoblue.com/en/weather/forecast/week/durgapur_india_1272175')
tree = html.fromstring(page.content)
temp1 = tree.xpath('//div[@class="cell"]/text()')
#temp = tree.xpath('//tr[@title="temperature"]/text()')
print (temp1[7])