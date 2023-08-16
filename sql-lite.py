import mysql.connector
import os
import argparse
from rich.table import Table
from rich.console import Console
from rich.tree import Tree
from rich import print as rprint
from random import randint
import itertools
import threading
import time
import sys

csl = Console()
class LoadingAnimation:
    def __init__(self):
        self.done_event = threading.Event()
        self.done_event.clear()

    def animate(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done_event.is_set():
                break
            sys.stdout.write('\rloading  ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('')
        clear_screen()


host = ""
user = ""
password = ""
database = ""
def connect_to_database(host, user, password, database,loading_obj):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        csl.print("[bold][green]Connected to the database.[/][/]")
        loading_obj.done_event.set()
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
def help_display():
    csl.print("sql-lite 1.0 (https://github.com/khuluqilkarim/mysql-cli)")
    print("Usage: sql-lite [Options] {target specification}")
    print("TARGET SPECIFICATION:")
    print("  -u <input username> username from database")
    print("  -d <input databse_name> database name's")
    print("  -host <input host/URL> host/URL from database")
    csl.print("\nEXAMPLES:\n  [purple]sql-lite -u root -d example -host localhost[/]")
def banner(host, database, username, connection):
    csl.print(f"Host: [bold][blue]{host}[/][/]")
    csl.print(f"Database: [bold][blue]{database}[/][/]")
    csl.print(f"User: [bold][blue]{username}[/][/]")
    if connection is not None:
        csl.print("\n[bold][green]Connection established[/][/]\n")
    tree_table(connection)

def banner_loading(host, database, username):
    clear_screen()
    csl.print(f"Host: [bold][blue]{host}[/][/]")
    csl.print(f"Database: [bold][blue]{database}[/][/]")
    csl.print(f"User: [bold][blue]{username}[/][/]")
    
    csl.print("\n[bold][red]Waiting for Connection established[/][/]\n")

def clear_screen():
    os.system('cls')

def main():
    clear_screen()

    parser = argparse.ArgumentParser(description='Connection to database', add_help=False)
    parser.add_argument('-u', '--username', type=str, help='Value for username')
    parser.add_argument('-d', '--database', type=str, help='Value for database')
    parser.add_argument('-host', '--host', type=str, help='Value for host')
    parser.add_argument('-h', '--help-info', action='store_true', help='Display help information')

    args = parser.parse_args()

    if args.help_info:
        help_display()
        return
    elif args.username is not None and args.database is not None and args.host is not None:
        host = args.host
        user = args.username
        password = input('password: ')
        database = args.database
        banner_loading(host, database, user)
        loading = LoadingAnimation()
        t = threading.Thread(target=loading.animate)
        t.start()
        
        connection = connect_to_database(host, user, password, database,loading)
        t.join()
    else:
        host = input("Host: ")
        user = input("Username: ")
        password = input("Password: ")
        database = input("Database: ")
        banner_loading(host, database, user)
        loading = LoadingAnimation()
        t = threading.Thread(target=loading.animate)
        t.start()
        
        connection = connect_to_database(host, user, password, database,loading)
        t.join()

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


