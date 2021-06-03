
import re
import requests
from bs4 import BeautifulSoup as bs

def main(url):
    # requestsによってhtmlソースを取得
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')

    # codeのtagを抽出
    code_soup = soup.find_all(class_="company-code")
    code_list = []
    for code in code_soup:
        # print(code.text)
        code_list.append(code.text)

    # 企業名のtagを抽出
    company_soup = soup.find_all(class_="company-name")
    company_list = []
    for company in company_soup:
        # print(company.text)
        company_list.append(company.text)

    # 国名のtagを抽出
    country_soup = soup.find_all(class_="responsive-hidden")
    country_list = []
    for country in country_soup:
        # print(country.text)
        country_list.append(country.text)
    
    return code_list, company_list, country_list

total_code_list = []
total_company_list = []
total_country_list = []
for i in range(1,4):
    url = "https://companiesmarketcap.com/page/" + str(i)
    code_list, company_list, country_list = main(url)
    total_code_list.extend(code_list)
    total_company_list.extend(company_list)
    total_country_list.extend(country_list)

# エスケープ文字の除去
for i in range(len(total_company_list)):
    total_company_list[i] = re.sub('\W', '', total_company_list[i])

# 欠損値の除去
total_company_list.pop(115)
total_code_list.pop(115)
total_country_list = [s for s in total_country_list if '\n' not in s]
total_country_list.pop(115)

# for i in range(len(total_code_list)):
#     print(total_code_list[i], total_company_list[i], total_country_list[i])



