
"""
Define Your variables
"""

# Web URL
web_url = 'https://www.rxlist.com/pharmacy/dallas-tx_pharmacies.htm'
# HTML class where data is located
class_loc ='tabcontent'
# specific HTML tag holding the data 
spec_loc = 'p'

import requests
from bs4 import BeautifulSoup
import csv

# creating the function
def website_script(web_url, class_loc, spec_loc): 
    r = requests.get(web_url)
    # test connection is working and should get "Response [200]" --- 
    print(r.status_code) 
    # prints content - not useful but verify if the website is working
    print(r.content)

    # use beautifulsoup
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup.title)

    # define the HTML location of the data 
    s = soup.find('div', class_=class_loc)
    # within the HTML location where exactly is the data stored
    content = s.find_all(spec_loc)
    
    empty_list = []
    count = 1
    for x in content:
        d = {}
        d['Data Number'] = f'Count {count}'
        d['Data information'] = x.text
        count += 1
        empty_list.append(d)
    # file will be saved in directory you are working in 
    filename = 'extracted_data_2.csv'
    with open(filename, 'w', newline='') as f:
        w = csv.DictWriter(f,['Data Number','Data information'])
        w.writeheader()
     
        w.writerows(empty_list)



## Calling the function
website_script(web_url, class_loc, spec_loc)


    