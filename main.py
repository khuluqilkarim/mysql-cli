# C:/Python311/python.exe

import mysql.connector
import os
from prettytable import PrettyTable
from colorama import init, Fore

init(autoreset=True)

def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print(Fore.GREEN + "Connected to the database." + Fore.RESET)
        clear_screen()
        return connection
    except mysql.connector.Error as err:
        print(Fore.RED + "Error:" + Fore.RESET, err)
        return None

def show_tables(connection):
    try:
        cursor = connection.cursor()
        query = f"SHOW tables"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]
            table = PrettyTable(column_names)
            
            for row in rows:
                table.add_row([Fore.YELLOW + str(cell) + Fore.RESET for cell in row])
            
            print(table)
        
        cursor.close()
    except mysql.connector.Error as err:
        print(Fore.RED + "Error:" + Fore.RESET, err)

def commandSql(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]
            table = PrettyTable(column_names)
            
            for row in rows:
                table.add_row(row)
            
            print(Fore.YELLOW + "Query Result" + Fore.RESET)
            print(table)
        
        cursor.close()
    except mysql.connector.Error as err:
        print(Fore.RED + "Error:" + Fore.RESET, err)

def benner(host, database, username,connection):
    print(f"Host: {Fore.BLUE}{host}{Fore.RESET}")
    print(f"Database: {Fore.BLUE}{database}{Fore.RESET}")
    print(f"User: {Fore.BLUE}{username}{Fore.RESET}")
    if connection != None:
        print(Fore.GREEN + "\nConnection established\n\n" + Fore.RESET)

def clear_screen():
    os.system('cls')

def main():
    clear_screen()
    host = input("Host: ")
    user = input("Username: ")
    password = input("Password: ")
    database = input("Database: ")

    connection = connect_to_database(host, user, password, database)
    benner(host, database, user,connection)
    show_tables(connection)
    while True:
        if connection is None:
            print(Fore.RED + "Connection is not established." + Fore.RESET)
            break

        command = input("\nExecute Query: ")

        if command.startswith(".tables"):
            show_tables(connection)
        elif command.startswith(".stop"):
            connection.close()
            print(Fore.YELLOW + "Connection closed." + Fore.RESET)
            break
        else:
            commandSql(connection, command)

if __name__ == "__main__":
    main()
