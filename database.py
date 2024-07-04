from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select, ForeignKey, delete, exists
from models import UserSchema
from sqlalchemy.exc import IntegrityError

from config import DB_HOST, DB_USER, DB_NAME, DB_PASS, DB_PORT

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(url=DATABASE_URL, echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class Users(Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str]
    hashed_password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


class Vacancies(Model):
    __tablename__ = "vacancies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int]
    name: Mapped[str]
    city: Mapped[str]
    salary_from: Mapped[int]
    salary_to: Mapped[int]
    url: Mapped[str]
    experience: Mapped[str]
    search: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


async def create_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.drop_all)


async def reg_user(user: UserSchema):
    async with new_session() as session:
        try:
            new_user = Users(login=user.login, hashed_password=user.password, email=user.email)
            session.add(new_user)
            await session.flush()
            await session.commit()
        except IntegrityError:
            return "Already Exist"
        return new_user.id


async def get_users():
    async with new_session() as session:
        query = select(Users)
        result = await session.execute(query)
        return result.scalars().all()


async def write_vacancies(vac, search, user_id):
    async with new_session() as session:
        if vac["salary"] == None:
            salary_from = 0
            salary_to = 0
        else:
            if vac["salary"]["from"] == None:
                salary_from = 0
                salary_to = vac["salary"]["to"]
            elif vac["salary"]["to"] == None:
                salary_from = vac["salary"]["to"]
                salary_to = 0
            else:
                salary_from = vac["salary"]["from"]
                salary_to = vac["salary"]["to"]
        try:
            vacancy = Vacancies(vacancy_id=int(vac["id"]),
                                name=vac["name"],
                                city=vac["area"]["name"],
                                salary_from=salary_from,
                                salary_to=salary_to,
                                url=vac["alternate_url"],
                                experience=vac["experience"]["id"],
                                search=search,
                                user_id=user_id)
            session.add(vacancy)
            await session.flush()
            await session.commit()
        except IntegrityError:
            print("Уже есть")


async def get_user_vacancies(id):
    async with new_session() as session:
        query = select(Vacancies).where(Vacancies.user_id == id)
        result = await session.execute(query)
        return result.scalars().all()


async def get_id(email: str):
    async with new_session() as session:
        query = select(Users.id).where(Users.email == email)
        result = await session.execute(query)
        return result.scalars().all()

async def delete_vacancies(id):
    async with new_session() as session:
        query = delete(Vacancies).where(Vacancies.user_id == id)
        await session.execute(query)
        await session.flush()
        await session.commit()