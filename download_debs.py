import requests
import re 
import os


pattern = re.compile(r'<a href="(.*?)">(.*?)</a>')
res = requests.get('http://packages.deepin.com/deepin/pool/non-free/d/deepin-wine/')
text = res.text.split('\n')
for item in text:
    if 'href' in item:
        #print(pattern.findall(item))
        name, url = pattern.findall(item)[0]
        if len(name) < 6:
            #print(name) 
            continue

        url = 'http://packages.deepin.com/deepin/pool/non-free/d/deepin-wine/' + url 
        print(url)
        os.system(f'wget {url}')

        #print(name, url, name == url)





