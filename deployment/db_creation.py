import psycopg2
import argparse
from sqlalchemy import create_engine
from data_base.db_model import create_db

# Конфигурация по умолчанию
DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword'
}


def create_database(
        host: str,
        port: int,
        database: str,
        user: str,
        password: str
):

    try:
        SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
        create_db(engine)
        print("Успешное подключение к базе данных!")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")


def parse_arguments():

    parser = argparse.ArgumentParser(description='Подключение к базе данных PostgreSQL')
    parser.add_argument('--host', type=str, default=DEFAULT_CONFIG['host'], help='Хост базы данных')
    parser.add_argument('--port', type=int, default=DEFAULT_CONFIG['port'], help='Порт базы данных')
    parser.add_argument('--database', type=str, default=DEFAULT_CONFIG['database'], help='Имя базы данных')
    parser.add_argument('--user', type=str, default=DEFAULT_CONFIG['user'], help='Имя пользователя')
    parser.add_argument('--password', type=str, default=DEFAULT_CONFIG['password'], help='Пароль')

    return parser.parse_args()


def main():
    args = parse_arguments()

    create_database(
        host=args.host,
        port=args.port,
        database=args.database,
        user=args.user,
        password=args.password
    )


if __name__ == "__main__":
    main()
