import html2text
import urllib2
from bs4 import BeautifulSoup

response = urllib2.urlopen('https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/?internalSource=hub%20recipe&referringContentType=Search')
soup = BeautifulSoup(response, 'html.parser')

print(soup.find(id="lst_ingredients_1").text)
print(soup.find(id="lst_ingredients_2").text)

for step in soup.select('span[class*="recipe-directions__list--item"]'):
    print step.text
