from bs4 import BeautifulSoup, SoupStrainer
# import urllib.request
# with urllib.request.urlopen('https://saintlad.com/make-a-web-crawler/') as response:
#    html = response.read()
#    print(html)
#    #soup = BeautifulSoup(html)
# #print(soup.prettify())    
writefile = open('output.txt', 'a')
import urllib.request
response =  urllib.request.urlopen('https://en.wikibooks.org/wiki/Java_Programming')
allTheLinks = []
for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
   if link.has_attr('href'):
      if link['href'][1:5]=='wiki':
         if('Help:' not in link['href']):

            allTheLinks.append('https://en.wikibooks.org'+link['href'])
count = 0
for x in allTheLinks:
   print(count)
   if (count>18 and count<107):
      #print(x)

      detailed_response =  urllib.request.urlopen(x)
      detailed_soup = BeautifulSoup(detailed_response)
      #print(detailed_soup.prettify)

      p_tags = []
      next = firstElem.nextSilbing
      while next.name != "h2":
         p_tags.append(next)
         next = next.nextSibling

   count += 1


#-------
# html = response.read()
# soup = BeautifulSoup(html)
#
# #s=str(soup.prettify)
# s = str(soup)
#
# print(s)
#
# writefile.write('Once upon a time in a Galaxy far far away')
# try:
#    writefile.write(str(s))
#
#
# except UnicodeEncodeError:
#    for c in s:
#       try:
#          writefile.write(c)
#          print(c, end='')
#       except UnicodeEncodeError:
#          print('?', end='')
#
#
# writefile.write('Hail Lord Vader')
# writefile.close()
