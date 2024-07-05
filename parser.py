import requests
from models import VacancySchema
from database import write_vacancies

access_token = "APPLLVI1F7343UFG4U5T0NU85VVSP7NVJVGO7HSR1C6A73G04R3SF2C7VP1QMTKC"


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
            if page == 200:
                break
            for i in response:
                await write_vacancies(i, options.text, options.user_id)
    return "done"
