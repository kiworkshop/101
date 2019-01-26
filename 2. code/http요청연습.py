import requests
from selenium import webdriver

#url = 'https://www.devex.com/api/public/search/articles?page%5Bsize%5D=20'
url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
driver = webdriver.Chrome('./chromedriver')
driver.get(url)
id_input = driver.find_element_by_xpath('//*[@id="id"]')
id_input.send_keys('zzangy92')
pw_input = driver.find_element_by_xpath('//*[@id="pw"]')
pw_input.send_keys('asdasd')
login_btn = driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input')
login_btn.click()


## bs = bs4.BeautifulSoup(response.text, 'html.parser')
## table = bs.select('#main-area > div:nth-child(5) > table')[0]
## rows = table.tbody.find_all('tr')

##rows = [row for index, row in enumerate(rows) if index % 2 == 0]
##for row in rows:
 ##   post_no = row.find('div', attrs={'class': 'inner_number'}).get_text()
 ##   post_title = row.find('a', attrs={'class': 'article'}).get_text().strip()
 ##   post_author = row.find('a', attrs={'class': 'm-tcol-c'}).get_text()
 ##  post_date = row.find('td', attrs={'class': 'td_date'}).get_text()
 ##   print(post_no, post_title, post_author, post_date)