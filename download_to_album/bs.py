import bs4 as bs
import urllib.request

sauce = urllib.request.urlopen('https://www.youtube.com/watch?v=Qyclqo_AV2M&list=PLmo4pBukfRoN8SB5RKvfiY9CTl9pI_IFc').read()

soup = bs.BeautifulSoup(sauce, 'lxml')

link_text = []
f = open('linky.txt', 'w')

for a in soup.find_all('a', href=True):
    if a.get_text(strip=True):
        if 'watch' in str(a['href']) and 'index' in str(a['href']):
            link = 'https://www.youtube.com' + str(a['href'])
            print(link)
            link_text.append(a['href'])
            f.write(link)
            f.write('\n')
print(len(link_text))
