import json
import sqlite3

connection = sqlite3.connect("./Speak.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS message (id INTEGER PRIMARY KEY, chat_id INTEGER, role TEXT,"
    "content TEXT, audio BLOB, date DATETIME DEFAULT CURRENT_TIMESTAMP)"
)
connection.close()


def get_all_chats():
    connection = sqlite3.connect("Speak.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM chat")
    chats = cursor.fetchall()
    connection.close()
    return chats


def insert_chat(name):
    connection = sqlite3.connect("Speak.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO chat (name) VALUES (?)", (name,))
    connection.commit()
    connection.close()
    # return chat_id
    return cursor.lastrowid


def insert_message(chat_id, role, content, audio):
    connection = sqlite3.connect("Speak.db")
    cursor = connection.cursor()
    content_json = json.dumps(content)
    cursor.execute(
        "INSERT INTO message (chat_id, role, content, audio) VALUES ( ?, ?, ?, ?)",
        (chat_id, role, content_json, audio),
    )
    connection.commit()
    connection.close()


# det all messages by chat id and sort by datetime in descending order


def get_messages_by_chat_id(chat_id):
    connection = sqlite3.connect("Speak.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM message WHERE chat_id = ? ORDER BY date DESC", (chat_id,)
    )
    messages = cursor.fetchall()
    connection.close()
    return messages
