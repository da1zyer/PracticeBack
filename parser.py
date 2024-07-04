from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json
from models import VacancySchema
from database import write_vacancies


access_token = "APPLLVI1F7343UFG4U5T0NU85VVSP7NVJVGO7HSR1C6A73G04R3SF2C7VP1QMTKC"

# def make_url(job, salary: int, page=0):
#     url = "https://hh.ru/search/vacancy?"
#     url += "text="
#     for i in job.split():
#         url += i + "+"
#     url = url[:-1] + "&page=" + str(page)
#     if salary > 0:
#         url += "&salary={salary}&only_with_salary=true".format(salary=salary)
#     return url


# def short_url(url):
#     return url.split("?")[0]


# def vacancies_parser(job, salary):
#     vac = []
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(options=options)
#     driver.get(make_url(job=job, salary=salary))
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     pages = soup.find_all("span", class_="pager-item-not-in-short-range")
#     try:
#         pages_count = int(pages[-1].find("span").get_text())
#     except IndexError:
#         pages_count = 1
#     vacancies = soup.find_all("span", class_="serp-item__title-link-wrapper")
#     for i in range(0, pages_count):
#         driver.get(make_url(job=job, page=i, salary=salary))
#         time.sleep(20)
#         soup = BeautifulSoup(driver.page_source, "html.parser")
#         vacancies = soup.find_all("span", class_="serp-item__title-link-wrapper")
#         for item in vacancies:
#             link = item.find("a")["href"]
#             if "adsrv" not in link:
#                 vac.append(short_url(link))
#     return vac


def make_vacancy_url(text, experience, salary, only_with_salary, page, per_page=10, search_field="name"):
    url = "https://api.hh.ru/vacancies?"
    url += "page={page}&".format(page=page)
    url += "per_page={per_page}&".format(per_page=per_page)
    url += "text={text}&".format(text=text)
    url += "experience={experience}&".format(experience=experience)
    url += "salary={salary}&".format(salary=salary)
    url += "only_with_salary={only_with_salary}&".format(only_with_salary=only_with_salary)
    url += "search_field={search_field}&".format(search_field=search_field)
    return url


async def vacancies_parser(options: VacancySchema):
    headers = {"Authorization": "Bearer {token}".format(token=access_token)}
    vaca = []
    page = 0
    while True:
        url = make_vacancy_url(text=options.text,
                               experience=options.experience,
                               salary=options.salary,
                               only_with_salary=options.only_with_salary,
                               page=page)
        response = requests.get(url, headers=headers).json()["items"]
        if len(response) == 0:
            break
        else:
            page += 1
            #Изменить на 200
            if page == 200:
                break
            for i in response:
                await write_vacancies(i, options.text, options.user_id)
    return "done"
