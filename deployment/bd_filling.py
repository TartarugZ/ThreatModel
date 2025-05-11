import argparse
from sqlalchemy import create_engine
import test_filling
from functions import ubi_parsing, vul_parsing

# Конфигурация по умолчанию
DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword'
}


def vul_parse(engine):
    vul_parsing.download_vul_file()
    vul_parsing.parse_vulnerabilities(engine)
    vul_parsing.parse_software_types_and_vul_types(engine)
    vul_parsing.connect_vul_soft_vul_type(engine)


def ubi_parse(engine):
    ubi_parsing.download_ubi_file()
    ubi_parsing.parse_device_types(engine)
    ubi_parsing.parse_ubi_threats(engine)
    ubi_parsing.connect_treat_device_type(engine)


def data_base_fill(
        host: str,
        port: int,
        database: str,
        user: str,
        password: str
):

    try:
        SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
        #  Парсинг и внесение данных об угрозах информационной безопасности (УБИ) и объектах воздействия (ОВ)
        ubi_parse(engine)
        #  Парсинг и внесение данных об уязвимостях
        vul_parse(engine)
        # Негативные последствия (НП)
        test_filling.negative(engine)
        # Способы реализации (СР)
        test_filling.realization(engine)
        # Устройства (УСТ)
        test_filling.devices(engine)
        # Связь УСТ с НП
        test_filling.device_result(engine)
        # Связь УСТ с УБИ
        test_filling.device_threat(engine)
        # Связь УСТ с СР
        test_filling.device_realization(engine)
        #  Виды воздействия (ВВ)
        test_filling.impact_types(engine)
        #  Интерфейсы (ИНТ)
        test_filling.interface_fill(engine)
        # Связь ИНТ и СР
        test_filling.interface_realization_fill(engine)
        # Связь ОВ и ИНТ
        test_filling.device_type_interface(engine)
        #  Тактики и техники (Т)
        test_filling.tactic_and_technique(engine)
        # Связь УСТ с Т
        test_filling.device_scenario(engine)
        # Название организации
        test_filling.organization_fill(engine)
        # Виды нарушителей
        test_filling.intruders(engine)
        # Критерии инсайдера
        test_filling.insider_criteria_fill(engine)
        # Связь УСТ между собой
        test_filling.device_connection(engine)
        # Связь уязвимостей и УСТ
        test_filling.device_vul(engine)
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

    data_base_fill(
        host=args.host,
        port=args.port,
        database=args.database,
        user=args.user,
        password=args.password
    )


if __name__ == "__main__":
    main()
