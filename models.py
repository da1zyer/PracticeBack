from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

experiences = {
    "no": "noExperience",
    "1_3": "between1And3",
    "3_6": "between3And6",
    "6": "moreThan6"
}


class VacancySchema(BaseModel):
    text: str
    experience: str
    salary: int
    only_with_salary: bool
    user_id: int


metadata = MetaData()


class UserSchema(BaseModel):
    login: str = Field(default=None)
    password: str = Field(default=None)
    email: EmailStr = Field(default=None)


class UserSchemaLogin(BaseModel):
    password: str = Field(default=None)
    email: EmailStr = Field(default=None)


Users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("login", String),
    Column("hashed_password", String),
    Column("email", String, unique=True)
)

Vacancies = Table(
    "vacancies",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("vacancy_id", Integer),
    Column("name", String),
    Column("city", String),
    Column("salary_from", Integer),
    Column("salary_to", Integer),
    Column("url", String),
    Column("experience", String),
    Column("search", String),
    Column("user_id", Integer, ForeignKey("users.id")),
)
