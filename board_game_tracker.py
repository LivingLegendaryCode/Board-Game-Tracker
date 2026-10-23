# Board Game Tracker — Jarrell Warren
import os
from getpass import getpass

# imports 
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Connect to MySQL Database
def create_connection(hostName, Uid, pwd, dbName, port):
    conn = None
    try:
        conn = mysql.connector.connect(
            host = hostName,#End
            user = Uid,#UserID
            password = pwd,#password
            database = dbName,#Database Name
            port = port, #Port
        )
        print("Connection DB successful")
    except Error as e:
        print(f"Error: {e}")
    return conn

# Create Table in Database
def create_table(conn):
    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute("""CREATE TABLE IF NOT EXISTS boardgame (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gamename VARCHAR(20) NOT NULL,
            maxplayers INT NOT NULL,
            result VARCHAR(50),
            gameduration DATETIME,
            maxscore INT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
        print("Table Created")
    except Error as e:
        print(f"Error: {e}")

# Output Data
def outputData(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM boardgame")#sql
        result = cursor.fetchall()
        for row in result:
            print(row)
    except Error as e:
        print(f"Error: {e}")

# Add Game
def addGame(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        gamename = input("Enter Game: ")
        gamename = gamename.strip()
        if not gamename or len(gamename) > 20:# error handling for game name
            print("Game name must contain 1–20 characters.")
            return
        maxplayers = int(input("Enter Max Number Players: "))
        result = input(" Game Result: ")
        maxscore = int(input(" Max Score: "))
        if maxplayers < 1 or maxscore < 0 or len(result) > 50:
            print("Players must be positive, score nonnegative, and result at most 50 characters.")
            return
        start_time = datetime.now()
        
        sql = "INSERT INTO boardgame (gamename, maxplayers, result, maxscore, gameduration) VALUES (%s, %s, %s, %s, %s)"#Class code
        val = (gamename, maxplayers, result, maxscore, start_time)
        cursor.execute(sql, val)
        conn.commit()
        print("Game Added")
    except ValueError:
        print("Players and score must be whole numbers.")
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")

# Delete Game
def deleteGame(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        game = input("Delete Game: ")
        if input(f"Delete all records named {game!r}? Type yes: ").strip().lower() != 'yes':
            print('Delete cancelled.')
            return
        sql = "DELETE FROM boardgame WHERE gamename = %s"
        val = (game,)
        cursor.execute(sql, val)
        conn.commit()
        print(f"{cursor.rowcount} game record(s) deleted.")
    except Error as e:
        print(f"Error: {e}")

# Main Function
def main():
    try:
        port = int(os.getenv('DB_PORT', '3306'))
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print('DB_PORT must be a number from 1 to 65535.')
        return
    password = os.getenv('DB_PASSWORD')
    if password is None:
        password = getpass('MySQL password: ')
    conn = create_connection(
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_USER', 'boardgame_user'),
        password,
        os.getenv('DB_NAME', 'board_game_tracker'),
        port,
    )
    if conn is not None:
        create_table(conn)
        while True:
            print("\nJarrell Warren Boardgames Menu:\n")
            print("o = Output Data")
            print("a = Add Game")
            print("d = Delete Game")
            print("q = Quit")
            choice = input("Enter your choice: o,a,d,q: ").strip().lower()
            if choice == "o":
                outputData(conn)
            elif choice == "a":
                addGame(conn)
            elif choice == "d":
                deleteGame(conn)
            elif choice == "q":
                break
            else:
                print("Invalid choice. Choices are: o,a,d,q")
        conn.close()
    else:
        print("Connection Failed")

if __name__ == "__main__":
    main()
