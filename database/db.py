import sqlite3


def create_database():
    try:
        # Создание подключения к базе данных SQLite3
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()

        # Создание таблицы "Пользователи"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY
            )
        ''')

        # Создание таблицы "Каналы"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Channels (
                channel_id INTEGER PRIMARY KEY,
                channel_name TEXT NOT NULL,
                channel_link TEXT
            )
        ''')

        # Создание таблицы "Подписки"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Subscriptions (
                subscription_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                channel_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES Users (user_id),
                FOREIGN KEY (channel_id) REFERENCES Channels (channel_id)
            )
        ''')

        # Создание таблицы "Messages"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Messages (
                channel_id INTEGER,
                text TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (channel_id) REFERENCES Channels (channel_id)
            )
        ''')

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        print("База данных успешно создана.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")


def add_user(user_id):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute('INSERT INTO Users (user_id) VALUES (?)', (user_id,))

    conn.commit()
    conn.close()


def add_channel_and_subscription(user_id, channel_id, channel_link, channel_name):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Channels WHERE channel_id = ?', (channel_id,))
    existing_channel = cursor.fetchone()

    if not existing_channel:
        cursor.execute('INSERT INTO Channels (channel_id, channel_name, channel_link) VALUES (?, ?, ?)', (channel_id, channel_name, channel_link))

    cursor.execute('''
            SELECT * 
            FROM Subscriptions 
            WHERE user_id = ? AND channel_id = ?
        ''', (user_id, channel_id))
    existing_subscription = cursor.fetchone()

    if not existing_subscription:
        cursor.execute('INSERT INTO Subscriptions (user_id, channel_id) VALUES (?, ?)', (user_id, channel_id))
    else:
        conn.commit()
        conn.close()
        return False

    conn.commit()
    conn.close()
    return True


def remove_subscription(user_id, channel_id):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    cursor.execute('''
                SELECT * 
                FROM Subscriptions 
                WHERE user_id = ? AND channel_id = ?
            ''', (user_id, channel_id))
    existing_subscription = cursor.fetchone()

    if existing_subscription:
        cursor.execute('DELETE FROM Subscriptions WHERE user_id = ? AND channel_id = ?', (user_id, channel_id))

    cursor.execute('SELECT * FROM Subscriptions WHERE channel_id = ?', (channel_id,))
    remaining_subscriptions = cursor.fetchall()

    if not remaining_subscriptions:
        cursor.execute('DELETE FROM Channels WHERE channel_id = ?', (channel_id,))

    conn.commit()
    conn.close()


def get_all_channel_links():
    try:
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()

        cursor.execute('SELECT channel_link FROM Channels')
        channel_links = cursor.fetchall()

        conn.close()

        channel_links = [link[0] for link in channel_links]

        return channel_links
    except sqlite3.Error as e:
        return []


def get_subscribed_users(channel_id):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT user_id
        FROM Subscriptions
        WHERE channel_id = ?
    ''', (channel_id,))
    subscribed_users = cursor.fetchall()

    conn.close()

    subscribed_users = [user[0] for user in subscribed_users]

    return subscribed_users


def get_user_subscribed_channels(user_id):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Channels.channel_id, Channels.channel_name, Channels.channel_link
        FROM Channels
        INNER JOIN Subscriptions ON Channels.channel_id = Subscriptions.channel_id
        WHERE Subscriptions.user_id = ?
    ''', (user_id,))
    subscribed_channels = cursor.fetchall()

    conn.close()

    subscribed_channels_dict = {}
    for channel_id, channel_name, channel_link in subscribed_channels:
        subscribed_channels_dict[channel_id] = [channel_name, channel_link]

    return subscribed_channels_dict


def get_channel_id_by_name(channel_name):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    cursor.execute('SELECT channel_id FROM Channels WHERE channel_name = ?', (channel_name,))
    channel_id = cursor.fetchone()

    conn.close()

    if channel_id:
        return channel_id[0]
    else:
        return None


def check_channel_exists(channel_id):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Channels WHERE channel_id = ?', (channel_id,))
    existing_channel = cursor.fetchone()

    conn.close()

    if existing_channel:
        return True
    else:
        return False


def get_channel_link_by_id(channel_id):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    cursor.execute('SELECT channel_link FROM Channels WHERE channel_id = ?', (channel_id,))
    channel_link = cursor.fetchone()

    conn.close()

    if channel_link:
        return channel_link[0]
    else:
        return None


def add_message(channel_id, text):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    # Добавление сообщения в таблицу
    cursor.execute('''
            INSERT INTO Messages (channel_id, text)
            VALUES (?, ?)
        ''', (channel_id, text))

    conn.commit()
    conn.close()


def delete_message(message_id):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    # Удаление сообщения из таблицы
    cursor.execute('DELETE FROM Messages WHERE message_id = ?', (message_id,))

    conn.commit()
    conn.close()


def get_message_text(message_id):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    # Получение текста сообщения по его ID
    cursor.execute('SELECT text FROM Messages WHERE message_id = ?', (message_id,))
    message_text = cursor.fetchone()

    conn.close()

    if message_text:
        return message_text[0]
    else:
        return None


create_database()