import psycopg2


class DB:
    def __init__(self, database, host, user, password):
        conn = psycopg2.connect(database=database, host=host, user=user, password=password)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                (id int unique,
                                username text unique,
                                karma int)
                                 ''')
        cursor.close()
        self.connection.commit()

    def create_new_user(self, user_id, username):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users (id, username, karma)
                VALUES (%d, '%s', 0)
                ON CONFLICT (id) DO NOTHING''' % (user_id, username, user_id))
        self.connection.commit()

    def get_user_id(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username='%s'" % username)
        user_id = cursor.fetchone()
        if user_id is None:
            return 0
        else:
            return id[0]


class KarmaModel:
    def __init__(self, connection):
        self.connection = connection

    def get_current_karma(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT karma FROM users WHERE id = %d" % user_id)
        karma = cursor.fetchone()[0]
        return karma

    def add_karma(self, user_id, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %d" % user_id)
        user = cursor.fetchone()
        if user is None:
            cursor.execute("INSERT INTO users VALUES (%d, '%s', 1)" % (user_id, username))
        else:
            karma = int(user[2]) + 1
            cursor.execute("UPDATE users SET karma=%d WHERE id=%d" % (karma, user_id))
        self.connection.commit()

    def reduce_karma(self, user_id, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '%s'" % username)
        user = cursor.fetchone()
        karma = -1
        if user is None:
            cursor.execute("INSERT INTO users VALUES (%d, '%s', -1)" % (user_id, username))
        else:
            karma = int(user[2]) - 1
            cursor.execute("UPDATE users SET karma=%d WHERE id=%d" % (karma, user_id))
        self.connection.commit()
        if karma < -99:
            return 2
        else:
            return 1

    def get_top20(self, is_ascending):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = int(cursor.fetchone()[0])
        if count == 0:
            return "There is no users in database"
        else:
            top_list = "Top people with positive karma: "
            if is_ascending:
                query = "SELECT * FROM users ORDER BY karma LIMIT 20"
            else:
                query = "SELECT * FROM users ORDER BY karma DESC LIMIT 20"
            cursor.execute(query)
            top20 = cursor.fetchall()
            i = 1
            for user in top20:
                top_list += "\n" + str(int(i + 1)) + ". @" + "[" + str(user[1]) + "]" + " with " + str(
                    user[2]) + " karma"
                i += 1
            return top_list