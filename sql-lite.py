import mysql.connector
import os
import argparse
from rich.table import Table
from rich.console import Console
from rich.tree import Tree
from rich import print as rprint
from random import randint
csl = Console()

host = ""
user = ""
password = ""
database = ""
def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        csl.print("[bold][green]Connected to the database.[/][/]")
        clear_screen()
        return connection
    except mysql.connector.Error as err:
        print("Error:")
        return None

def command_sql(connection, query):
    try:
        table = Table()
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        color = ['cyan', 'green', 'yellow', 'magenta']
        
        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]
            for column in column_names:
                randColor = randint(0, len(color))
                table.add_column(column,style=str(color[randColor-1]))
            
            for row in rows:
                row_str = [str(item) for item in row]
                table.add_row(*row_str)
               

            console = Console()
            console.print("\nQuery Result :")
            console.print(table)

        cursor.close()
    except mysql.connector.Error as err:
        csl.print(f"\n[red]Error: [/]{err}")

def tree_table(connection):
    try:        
        cursor = connection.cursor()
        query = "show tables"
        cursor.execute(query)
        rows = cursor.fetchall()
        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]
            for column in column_names:
                title = str(column)
                tree = Tree(title)
                
            
            for row in rows:
                row_str = [str(item) for item in row]
                formatted_row_str = ", ".join(row_str)
                value = tree.add(f"[green] {formatted_row_str}")

            rprint(tree)
            return value
    except mysql.connector.Error as err:
        print("Error:")

def banner(host, database, username, connection):
    csl.print(f"Host: [bold][blue]{host}[/][/]")
    csl.print(f"Database: [bold][blue]{database}[/][/]")
    csl.print(f"User: [bold][blue]{username}[/][/]")
    if connection is not None:
        csl.print("\n[bold][green]Connection established[/][/]\n")
    tree_table(connection)

def clear_screen():
    os.system('cls')

def main():
    clear_screen()

    parser = argparse.ArgumentParser(description='Connection to database')
    parser.add_argument('-u', '--username', type=str, help='Nilai username')
    parser.add_argument('-d', '--database', type=str, help='Nilai database')
    parser.add_argument('-host', '--host', type=str, help='Nilai host')

    args = parser.parse_args()

    if args.username is not None and args.database is not None and args.host is not None:
        host = args.host
        user = args.username
        password = input('password :')
        database = args.database

        connection = connect_to_database(host, user, password, database)
    else:
        host = input("Host: ")
        user = input("Username: ")
        password = input("Password: ")
        database = input("Database: ")

        connection = connect_to_database(host, user, password, database)

    banner(host, database, user, connection)
    while True:
        if connection is None:
            print("Connection is not established.")
            break

        command = input("\nExecute Query: ")


        if command.startswith("stop"):
            connection.close()
            print("Connection closed.")
            break
        elif command.startswith("tree"):
            tree = tree_table(connection)
            print(tree)
        else:
            clear_screen()
            banner(host, database, user, connection)
            command_sql(connection, command)
            

if __name__ == "__main__":
    main()
