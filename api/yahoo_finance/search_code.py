
import requests
from bs4 import BeautifulSoup as bs

def main(url):
    # requestsによってhtmlソースを取得
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')

    # codeのtagを抽出
    code_soup = soup.find_all(class_="txtcenter")
    code_list = []
    for code in code_soup:
        a = code.find("a")
        try:
            if a.text != "掲示板":
                # print(a.text)
                code_list.append(a.text)
        except AttributeError:
            pass

    # 企業名のtagを抽出
    company_soup = soup.find_all(class_="normal yjSt")
    company_list = []
    for company in company_soup:
        # print(company.text)
        company_list.append(company.text)
    
    return code_list, company_list

total_code_list = []
total_company_list = []
for i in range(1,6):
    url = "https://info.finance.yahoo.co.jp/ranking/?kd=4&tm=d&vl=a&mk=1&p=" + str(i)
    code_list, company_list = main(url)
    total_code_list.extend(code_list)
    total_company_list.extend(company_list)

# for i in range(len(total_code_list)):
    # print(total_code_list[i], total_company_list[i])

