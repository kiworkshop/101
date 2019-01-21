import requests
import bs4

url = 'https://cafe.naver.com/ArticleList.nhn?search.clubid=10050146&search.menuid=155&search.boardtype=L'
response = requests.get(url)
bs = bs4.BeautifulSoup(response.text, 'html.parser')
table = bs.select('#main-area > div:nth-child(5) > table')[0]
rows = table.tbody.find_all('tr')

rows = [row for index, row in enumerate(rows) if index % 2 == 0]
for row in rows:
    post_no = row.find('div', attrs={'class': 'inner_number'}).get_text()
    post_title = row.find('a', attrs={'class': 'article'}).get_text().strip()
    post_author = row.find('a', attrs={'class': 'm-tcol-c'}).get_text()
    post_date = row.find('td', attrs={'class': 'td_date'}).get_text()
    print(post_no, post_title, post_author, post_date)