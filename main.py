from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from parser import vacancies_parser
from models import VacancySchema, UserSchema, UserSchemaLogin
from database import create_tables, reg_user, get_users, get_id, delete_tables, get_user_vacancies, delete_vacancies
from auth.jwt_handler import sign_jwt
from auth.jwt_bearer import jwtBearer

origins = [
    "http://127.0.0.1:5500",  # Live Server VSCode
    "https://da1zyer.github.io",  # Github Pages
    "null"  # Простое открытие
]


@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   yield
   await delete_tables()  # Заменить на что-то типа print("Offline"), если хочется, чтобы база сохранялась после
                          # отключения


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/vacancies", dependencies=[Depends(jwtBearer())])  # Получение вакансий по параметрам
async def get_vacancies(query: VacancySchema):
    return await vacancies_parser(query)


@app.post("/signup")  # Регистрация
async def user_signup(user: UserSchema):
    reg = await reg_user(user)
    if reg == "Already Exist":
        return "Already Exist"
    return sign_jwt(user.email)


async def check_user(user: UserSchemaLogin):  # Проверка Email и пароля
    users = await get_users()
    for i in users:
        if i.email == user.email and i.hashed_password == user.password:
            return True
    return False


@app.post("/login")  # Вход
async def user_login(user: UserSchemaLogin):
    if await check_user(user):
        return sign_jwt(user.email)
    else:
        return "error"


@app.get("/users")  # Все пользователи
async def get_all_users():
    return await get_users()


@app.get("/getuserid")  # Id пользователя по Email
async def get_user_id(email: str):
    return await get_id(email)


@app.get("/getuservacs", dependencies=[Depends(jwtBearer())])  # Вакансии конкретного пользователя
async def get_user_vacs(id: int):
    return await get_user_vacancies(id)


@app.delete("/deletevacs", dependencies=[Depends(jwtBearer())])  # Удалить вакансии пользователя
async def get_user_vacs(id: int):
    return await delete_vacancies(id)


