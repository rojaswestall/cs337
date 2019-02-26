import html2text
import urllib.request as url
from bs4 import BeautifulSoup

address = 'https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/?internalSource=hub%20recipe&referringContentType=Search'

response = url.urlopen(address)
soup = BeautifulSoup(response, 'html.parser')

print(soup.find(id="lst_ingredients_1").text)
print(soup.find(id="lst_ingredients_2").text)

for step in soup.select('span[class*="recipe-directions__list--item"]'):
    print(step.text)
