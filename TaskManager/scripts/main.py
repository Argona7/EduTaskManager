from argparse import ArgumentParser
from  DataBase.DB import *
def main():
    parser = ArgumentParser(description="Создание базы данных для указаннного года ")
    parser.add_argument('year', type=int , help='Год для создании ьазы данных')
    args = parser.parse_args()

    print(args.year)


if __name__ == "__main__":
    main()