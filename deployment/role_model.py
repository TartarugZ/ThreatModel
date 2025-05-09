from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import argparse
from typing import Optional

# Конфигурация по умолчанию (можно редактировать напрямую)
DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword'
}

# SQL-скрипт для создания ролей и назначения прав
SQL_SCRIPT = """
-- Создание роли admin_ib
CREATE ROLE admin_ib NOLOGIN;

-- Создание роли engineer_ib
CREATE ROLE engineer_ib NOLOGIN;

-- Создание роли user_creator
CREATE ROLE user_creator NOLOGIN  CREATEROLE;

-- Назначение прав для роли admin_ib
-- Права на чтение, добавление, изменение и удаление для всех таблиц, кроме User
GRANT SELECT, INSERT, UPDATE, DELETE ON Vulnerability TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON SoftwareTypeVulnerability TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON InsiderCriteria TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON InsiderCriteriaType TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON Intruder TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceTypeIntruder TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON Interface TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceTypeInterface TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON InterfaceRealizationWay TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON RealizationWay TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceIp TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceImpactType TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON ImpactType TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON Organization TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON OrganizationResponsibility TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON Threat TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceTypeThreat TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceType TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON VulnerabilitySoftware TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON VulnerabilityTypeVulnerability TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON VulnerabilityType TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON Tactic TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON Technique TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON Device TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON Worker TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON WorkerInsiderCriteria TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceScenario TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceVulnerability TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceThreat TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceNegativeResult TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON NegativeResult TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceRealization TO admin_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceConnection TO admin_ib;

-- Назначение прав для роли engineer_ib
-- Права на чтение для всех таблиц, кроме User
GRANT SELECT ON Vulnerability TO engineer_ib;
GRANT SELECT ON SoftwareTypeVulnerability TO engineer_ib;
GRANT SELECT ON InsiderCriteria TO engineer_ib;
GRANT SELECT ON InsiderCriteriaType TO engineer_ib;
GRANT SELECT ON Intruder TO engineer_ib;
GRANT SELECT ON DeviceTypeIntruder TO engineer_ib;
GRANT SELECT ON Interface TO engineer_ib;
GRANT SELECT ON DeviceTypeInterface TO engineer_ib;
GRANT SELECT ON InterfaceRealizationWay TO engineer_ib;
GRANT SELECT ON RealizationWay TO engineer_ib;
GRANT SELECT ON DeviceIp TO engineer_ib;
GRANT SELECT ON DeviceImpactType TO engineer_ib;
GRANT SELECT ON ImpactType TO engineer_ib;
GRANT SELECT ON Organization TO engineer_ib;
GRANT SELECT ON OrganizationResponsibility TO engineer_ib;
GRANT SELECT ON Threat TO engineer_ib;
GRANT SELECT ON DeviceTypeThreat TO engineer_ib;
GRANT SELECT ON DeviceType TO engineer_ib;
GRANT SELECT ON VulnerabilitySoftware TO engineer_ib;
GRANT SELECT ON VulnerabilityTypeVulnerability TO engineer_ib;
GRANT SELECT ON VulnerabilityType TO engineer_ib;
GRANT SELECT ON Tactic TO engineer_ib;
GRANT SELECT ON Technique TO engineer_ib;
GRANT SELECT ON Device TO engineer_ib;
GRANT SELECT ON Worker TO engineer_ib;
GRANT SELECT ON WorkerInsiderCriteria TO engineer_ib;
GRANT SELECT ON DeviceScenario TO engineer_ib;
GRANT SELECT ON DeviceVulnerability TO engineer_ib;
GRANT SELECT ON DeviceThreat TO engineer_ib;
GRANT SELECT ON DeviceNegativeResult TO engineer_ib;
GRANT SELECT ON NegativeResult TO engineer_ib;
GRANT SELECT ON DeviceRealization TO engineer_ib;
GRANT SELECT ON DeviceConnection TO engineer_ib;

-- Права на чтение, добавление, изменение и удаление для таблиц, содержащих "Device" в названии
GRANT SELECT, INSERT, UPDATE, DELETE ON Device TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceTypeIntruder TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceTypeInterface TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceIp TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceImpactType TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceTypeThreat TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceType TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceScenario TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceVulnerability TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceThreat TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceNegativeResult TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceRealization TO engineer_ib;
GRANT SELECT, INSERT, UPDATE, DELETE ON DeviceConnection TO engineer_ib;

-- Назначение полных прав на таблицу User для роли user_creator
GRANT SELECT, INSERT, UPDATE, DELETE ON "User" TO user_creator;

-- Предоставление прав на использование последовательностей (sequences) для admin_ib
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO admin_ib;

-- Предоставление прав на использование последовательностей для engineer_ib (для таблиц с "Device")
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO engineer_ib;

-- Предоставление прав на использование последовательностей для user_creator
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO user_creator;

-- Предоставление user_creator прав на назначение ролей admin_ib и engineer_ib
GRANT admin_ib TO user_creator WITH ADMIN OPTION;
GRANT engineer_ib TO user_creator WITH ADMIN OPTION;
"""


def create_engine_connection(
        host: str,
        port: int,
        database: str,
        user: str,
        password: str
) -> Optional[any]:
    """
    Функция для создания подключения к базе данных PostgreSQL с использованием SQLAlchemy.
    Возвращает объект Engine или None в случае ошибки.
    """
    try:
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_string)
        print("Успешное подключение к базе данных!")
        return engine
    except SQLAlchemyError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None


def parse_arguments():
    """
    Парсинг аргументов командной строки.
    """
    parser = argparse.ArgumentParser(description='Создание ролей и назначение прав в PostgreSQL с SQLAlchemy')
    parser.add_argument('--host', type=str, default=DEFAULT_CONFIG['host'], help='Хост базы данных')
    parser.add_argument('--port', type=int, default=DEFAULT_CONFIG['port'], help='Порт базы данных')
    parser.add_argument('--database', type=str, default=DEFAULT_CONFIG['database'], help='Имя базы данных')
    parser.add_argument('--user', type=str, default=DEFAULT_CONFIG['user'], help='Имя пользователя')
    parser.add_argument('--password', type=str, default=DEFAULT_CONFIG['password'], help='Пароль')

    return parser.parse_args()


def execute_sql_script(engine: any):
    """
    Выполнение SQL-скрипта для создания ролей и назначения прав.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text(SQL_SCRIPT))
            connection.commit()  # Явный коммит транзакции
            print("Роли admin_ib и engineer_ib успешно созданы, права назначены.")
    except SQLAlchemyError as e:
        print(f"Ошибка выполнения SQL-скрипта: {e}")
        connection.rollback()


def main():
    # Парсинг аргументов из командной строки
    args = parse_arguments()

    # Создание подключения к базе данных
    engine = create_engine_connection(
        host=args.host,
        port=args.port,
        database=args.database,
        user=args.user,
        password=args.password
    )

    # Выполнение SQL-скрипта
    if engine:
        try:
            execute_sql_script(engine)
        finally:
            engine.dispose()
            print("Соединение закрыто.")


if __name__ == "__main__":
    main()
