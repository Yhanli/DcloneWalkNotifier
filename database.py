import sqlite3
import stat


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


"""
(chat_id, sub_regions, sub_hc, sub_ladder, sub_progress) VALUES (?,?,?,?,?)",
            (
                user.chat_id,
                user.regions,
                user.hc,
                user.ladder,
                user.progress,
            ),
            """


class DcloneDB:
    def __init__(self) -> None:
        self.DB = sqlite3.connect(
            "data.db",
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        self.DB.row_factory = dict_factory
        self.c = self.DB.cursor()

        self.init_db()

    # User DB control
    def put_user(self, user):
        c = self.c
        c.execute(
            f"INSERT INTO user (chat_id) VALUES (?)",
            (user.chat_id,),
        )
        self.DB.commit()

    def get_user(self, id):
        c = self.c
        c.execute(f"SELECT * FROM user WHERE chat_id=?", (id,))
        return c.fetchone()

    def delete_user(self, id):
        c = self.c
        c.execute(f"DELETE FROM user WHERE chat_id=?", (id,))
        self.DB.commit()

    def update_user(self, user):
        c = self.c
        c.execute(
            f"UPDATE user SET sub_regions=?, sub_hc=?, sub_ladder=?, sub_progress=? WHERE chat_id=?",
            (
                user.region,
                user.hc,
                user.ladder,
                user.progress,
                user.chat_id,
            ),
        )
        self.DB.commit()

    def is_existing_user(self, id):
        c = self.c
        c.execute(f"SELECT * FROM user WHERE chat_id=?", (id,))
        if c.fetchone():
            return True
        return False

    def get_subscribed_users(self, status):
        c = self.c
        c.execute(
            f"""SELECT * FROM user  
                        WHERE sub_regions LIKE "%{status.region}%" 
                        AND sub_hc LIKE "%{status.hc}%" 
                        AND sub_ladder LIKE "%{status.ladder}%" 
                        AND sub_progress LIKE "%{status.progress}%"
                    """
        )
        users = c.fetchall()
        return [int(user["chat_id"]) for user in users]

    # Status DB control
    def put_status(self, status):
        c = self.c
        c.execute(
            f"INSERT INTO status (region, hc, ladder, progress, timestamp) VALUES (?,?,?,?,?)",
            (
                status.region,
                status.hc,
                status.ladder,
                status.progress,
                status.time,
            ),
        )
        self.DB.commit()

    def find_status(self, region, hc, ladder):
        c = self.c
        c.execute(
            f"SELECT * FROM status WHERE region=? and hc=? and ladder=? ORDER BY timestamp DESC",
            (region, hc, ladder),
        )
        return c.fetchone()

    def is_existing_status(self, status):
        c = self.c
        c.execute(
            f"SELECT * FROM status WHERE region=? and hc=? and ladder=? and progress=? ORDER BY timestamp DESC",
            (status.region, status.hc, status.ladder, status.progress),
        )

        old_status = c.fetchone()
        if old_status:
            if status.progress == str(old_status["progress"]):
                return True
        return False

    def init_db(self):
        c = self.c
        c.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'user'"
        )
        if c.fetchone() is None:
            print("initialize user db")
            c.execute(
                """
                    CREATE TABLE user
                (
                        id integer PRIMARY KEY,
                        chat_id text NOT NULL,
                        sub_regions text DEFAULT "1|2|3" NOT NULL,
                        sub_hc text DEFAULT "2" NOT NULL,
                        sub_ladder text DEFAULT "1" NOT NULL,
                        sub_progress text DEFAULT "4|5|6" NOT NULL,
                        subbed integer DEFAULT 1 NOT NULL
                    )      
            """
            )
            self.DB.commit()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'status'"
        )
        if c.fetchone() is None:
            print("initialize status db")
            c.execute(
                """
                    CREATE TABLE status
                (
                        id integer PRIMARY KEY,
                        region integer NOT NULL,
                        hc integer NOT NULL,
                        ladder integer NOT NULL,
                        progress integer NOT NULL,
                        timestamp integer NOT NULL
                    )
            """
            )
            self.DB.commit()

    def terminate(self):
        self.DB.close()
