import sqlite3
import config
import datetime

now = datetime.datetime.now()

class DBConnection:
    def __init__(self):
        self.conn = sqlite3.connect(f'{config.DIR}database.db', check_same_thread=False)
        self.c = self.conn.cursor()

    def create_tables(self):
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS goods (name Text, info TEXT, price_first INT, price_second INT, link_photo TEXT, main TEXT, id_goods INTEGER PRIMARY KEY)")

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS group_msg (id_user id, date_msg TEXT)")

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS setting (id INT, notification TEXT, notifical_day TEXT, promo TEXT, promo_day INT, promo_date TEXT, salse_promo INT)")

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS zakaz (id INT, grind TEXT, method TEXT, Weight TEXT, Quantity TEXT, orderr TEXT, price INT, id_coffe INT, id_order INTEGER PRIMARY KEY, basket TEXT, comment TEXT, promo TEXT)")

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS profile (id INT, phone TEXT, FIO TEXT, nova_poshta TEXT, adrees TEXT, city TEXT, last_zakaz TEXT, promo_profile TEXT)")

    def show_tablese(self, id):
        return self.c.execute(f"SELECT * FROM setting WHERE id='{id}'").fetchone()

    def show_all_profile(self):
        return self.c.execute(f"SELECT * FROM profile").fetchall()

    def update_promo(self, change, id):
        self.c.execute(f'UPDATE profile SET promo_profile=(?) WHERE id = (?)',
                       [change, id])
        self.conn.commit()

    def add_tables(self, id, notification, notifical_day, promo, promo_day, promo_date, salse_promo):
        self.c.execute(
            'INSERT INTO setting(id, notification, notifical_day, promo, promo_day, promo_date, salse_promo) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (id, notification, notifical_day, promo, promo_day, promo_date, salse_promo)
        )
        self.conn.commit()

    def add_group(self, id, date):
        self.c.execute(
            'INSERT INTO group_msg(id_user, date_msg) VALUES (?, ?)',
            (id, date)
        )
        self.conn.commit()

    def show_group(self, id):
        return self.c.execute(f"SELECT * FROM group_msg WHERE id_user='{id}'").fetchone()

    def show_me_method(self, id):
        return self.c.execute(f"SELECT * FROM zakaz WHERE id_order='{id}'").fetchone()


    def promo(self, promo, promo_day, salse):
        id = 1
        promo_date = now.strftime("%Y-%m-%d")
        self.c.execute(f'UPDATE setting SET promo=(?), promo_day=(?), promo_date=(?), salse_promo=(?) WHERE id = (?)',
                       [promo, promo_day, promo_date, salse, id])
        self.conn.commit()

    def update_notifical_day(self, cahnge, id):
        self.c.execute(f'UPDATE setting SET notifical_day=(?) WHERE id = (?)',
                       [cahnge, id])
        self.conn.commit()

    def update_notification(self, cahnge, id):
        self.c.execute(f'UPDATE setting SET notification=(?) WHERE id = (?)',
                       [cahnge, id])
        self.conn.commit()

    def show_user(self, id):
        return self.c.execute(f"SELECT * FROM profile WHERE id='{id}'").fetchone()

    def add_user(self, id, phone, FIO, nova_poshta, adrees, city, last_zakaz, promo_profile):
        self.c.execute(
            'INSERT INTO profile(id, phone, FIO, nova_poshta, adrees, city, last_zakaz, promo_profile) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (id, phone, FIO, nova_poshta, adrees, city, last_zakaz, promo_profile)
        )
        self.conn.commit()

    def delete_profile(self, id_):
        self.c.execute(f"DELETE FROM profile WHERE id='{id_}'")
        self.conn.commit()

    def update_nova_poshta(self, id, phone, FIO, nova_poshta, city):
        self.c.execute(f'UPDATE profile SET phone=(?), FIO=(?), nova_poshta=(?), city=(?)  WHERE id = (?)', [phone, FIO, nova_poshta, city, id])
        self.conn.commit()

    def update_last_zakaz(self, id):
        last_zakaz = now.strftime("%Y-%m-%d")
        self.c.execute(f'UPDATE profile SET last_zakaz=(?) WHERE id = (?)', [last_zakaz, id])
        self.conn.commit()

    def update_pickup(self, id, phone, FIO, city):
        self.c.execute(f'UPDATE profile SET phone=(?), FIO=(?), city=(?)  WHERE id = (?)', [phone, FIO, city, id])
        self.conn.commit()

    def update_delivery(self, id, phone, FIO, adrees, city):
        self.c.execute(f'UPDATE profile SET phone=(?), FIO=(?), adrees=(?), city=(?) WHERE id = (?)', [phone, FIO, adrees, city, id])
        self.conn.commit()

    def update_orderr(self, id, orderr):
        self.c.execute(f'UPDATE zakaz SET orderr=(?) WHERE id_order = (?)', [orderr, id])
        self.conn.commit()

    def delete_from_basket(self, id_):
        self.c.execute(f"DELETE FROM zakaz WHERE id_order='{id_}'")
        self.conn.commit()

    def show_order(self, id):
        return self.c.execute(f"SELECT * FROM zakaz WHERE id='{id}' and basket='{'False'}'").fetchall()


    def show_basket(self, id):
        return self.c.execute(f"SELECT * FROM zakaz WHERE id='{id}' and basket='{'True'}'").fetchall()

    def show_id_order(self, id):
        # print(id, grind, method, Weight, Quantity, order, price, id_coffee, basket)
        # return self.c.execute(f"SELECT * FROM zakaz WHERE id='{id}' and grind='{grind}' and method='{method} 'and Weight='{Weight}' and Quantity='{Quantity}' and orderr='{order}' and price='{price}' and id_coffe='{id_coffee}' and basket='{basket}'").fetchone()
        return self.c.execute(
            f"SELECT * FROM zakaz WHERE id='{id}'").fetchall()

    def update_basket(self, change, id_order):
        self.c.execute(f'UPDATE zakaz SET basket=(?) WHERE id_order = (?)', [change, id_order])
        self.conn.commit()


    def show_weight(self, id):
        return self.c.execute(f"SELECT * FROM zakaz WHERE id_order='{id}'").fetchone()

    def show_order_one(self, id_goods):
        return self.c.execute(f"SELECT * FROM goods WHERE id_goods='{id_goods}'").fetchone()

    def add(self, main, name, info, price_first, price_second, link_photo):
        self.c.execute(
        'INSERT INTO goods(name, info, price_first, price_second, link_photo, main) VALUES (?, ?, ?, ?, ?, ?)',
        (name, info, price_first, price_second, link_photo, main))
        self.conn.commit()

    def add_order(self, id, grind, method, Weight, Quantity, order, price, id_coffee, basket, comment, promo):
        self.c.execute(
            'INSERT INTO zakaz(id, grind, method, Weight, Quantity, orderr, price, id_coffe, basket, comment, promo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (id, grind, method, Weight, Quantity, order, price, id_coffee, basket, comment, promo)
        )
        self.conn.commit()
        return self.c.lastrowid

    def show_price_coffe(self, id):
        return self.c.execute(f"SELECT * FROM goods WHERE id_goods='{id}'").fetchone()

    def show_goods(self, goods):
        return self.c.execute(f"SELECT * FROM goods WHERE main='{goods}'").fetchall()

    def show_all_goods(self):
        return self.c.execute(f"SELECT * FROM goods").fetchall()

    def show_my_order(self, id_order):
        return self.c.execute(f"SELECT * FROM zakaz WHERE id_order='{id_order}'").fetchone()

    def updateGrind(self, grind, id_order):
        self.c.execute(f'UPDATE zakaz SET grind=(?) WHERE id_order = (?)', [grind, id_order])
        self.conn.commit()

    def updateMethod(self, change, id_order):
        self.c.execute(f'UPDATE zakaz SET method=(?) WHERE id_order = (?)', [change, id_order])
        self.conn.commit()

    def updateComment(self, change, id_order):
        self.c.execute(f'UPDATE zakaz SET comment=(?) WHERE id_order = (?)', [change, id_order])
        self.conn.commit()

    def updateWeight(self, change, id_order):
        self.c.execute(f'UPDATE zakaz SET Weight=(?) WHERE id_order = (?)', [change, id_order])
        self.conn.commit()

    def updateQuantili(self, change, id_order):
        print(change, id_order)
        self.c.execute(f'UPDATE zakaz SET Quantity=(?) WHERE id_order = (?)', [change, id_order])
        self.conn.commit()

    def updateprice_in_order(self, change, id_order):
        self.c.execute(f'UPDATE zakaz SET price=(?) WHERE id_order = (?)', [change, id_order])
        self.conn.commit()

    def show_data(self):
        return self.c.execute(f"SELECT * FROM profile WHERE last_zakaz != '{'None'}'").fetchall()

    def __del__(self):
        self.c.close()
        self.conn.close()


    # def addUser(self, m):
    #     if [] == self.c.execute('SELECT * FROM USERS WHERE ID = (?)',[m.chat.id]).fetchall():
    #         self.c.execute(f'INSERT INTO USERS VALUES (?, ?, ?)', [m.chat.id, 0, m.text[7:]])
    #         if m.chat.last_name != None:
    #             name = f'{m.chat.first_name} {m.chat.last_name}'
    #         else:
    #             name = m.chat.first_name
    #         self.c.execute(f'INSERT INTO PROFILE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    #                        [m.chat.id, m.chat.username, name, None, None, 0.0000000000, 0, 0,0,None,0])
    #         self.conn.commit()
    #
    # def updateName(self, id,name):
    #     self.c.execute(f'UPDATE PROFILE SET FIRSTNAME=(?) WHERE ID = (?)', [name, id])
    #     self.conn.commit()
    #
    # def updateGetCount(self, username):
    #     self.c.execute(f'UPDATE PROFILE SET GET_COUNT=(GET_COUNT+1) WHERE USERNAME = (?)',[username])
    #     self.conn.commit()
    #
    # def getProfile(self, username=None, id=None):
    #     if username != None:
    #         return self.c.execute(f'SELECT * FROM PROFILE WHERE USERNAME = (?)', [username]).fetchone()
    #     if id != None:
    #         return self.c.execute(f'SELECT * FROM PROFILE WHERE ID = (?)', [id]).fetchone()
    #
    # def updateUsername(self, id, username):
    #     self.c.execute(f'UPDATE PROFILE SET USERNAME=(?) WHERE ID = (?)', [username, id])
    #     self.conn.commit()
    #
    # def updatePhoto(self, id, photo):
    #     self.c.execute(f'UPDATE PROFILE SET PHOTO=(?) WHERE ID = (?)', [photo, id])
    #     self.conn.commit()
    #
    # def updateAvatar(self, id, photo):
    #     self.c.execute(f'UPDATE PROFILE SET PHOTO_LOGO=(?) WHERE ID = (?)', [photo, id])
    #     self.conn.commit()
    #
    # def getProfiles(self):
    #     return self.c.execute(f'SELECT * FROM PROFILE').fetchall()
    #
    # def getUser(self, id):
    #     table = self.c.execute('SELECT * FROM USERS WHERE ID = (?)',[id]).fetchone()
    #     return table
    #
    # def skipEducation(self, id):
    #     self.c.execute('UPDATE USERS SET EDUCATION=1 WHERE ID = (?)',[id])
    #     self.conn.commit()
    #
    # def createDeal(self, seller, buyer, cur, amount, description, status):
    #     data = datetime.today()
    #     self.c.execute('INSERT INTO DEALS VALUES (NULL, ?,?,?,?,?,?,?)', [seller, buyer, amount,cur, description, status, data.strftime("%d %m %Y")])
    #     self.conn.commit()
    #     return self.c.lastrowid
    #
    # def deleteDeal(self, deal_id):
    #     self.c.execute('DELETE FROM DEALS WHERE ID = (?) AND STATUS = "FREEZE"', [deal_id])
    #     self.c.execute('DELETE FROM DEALS WHERE ID = (?) AND STATUS = "WAIT"', [deal_id])
    #     self.conn.commit()
    #
    # def updateDeal(self, status, deal_id):
    #     self.c.execute('UPDATE DEALS SET STATUS=(?) WHERE ID = (?)', [status,deal_id])
    #     self.conn.commit()
    #
    # def getActiveDeals(self, id):
    #     return self.c.execute('SELECT * FROM DEALS WHERE SELLER == (?) AND STATUS == "INPROCESS" OR BUYER = (?) AND STATUS == "INPROCESS" ', [id,id]).fetchall()
    #
    # def getDeal(self, deal_id):
    #     return self.c.execute('SELECT * FROM DEALS WHERE ID = (?)', [deal_id]).fetchone()
    #
    # def getSellCount(self, id):
    #     return self.c.execute('SELECT * FROM DEALS WHERE SELLER = (?) AND STATUS = "DONE"',[id]).fetchall()
    #
    # def getBuyCount(self, id):
    #     return self.c.execute('SELECT * FROM DEALS WHERE BUYER = (?) AND STATUS = "DONE"', [id]).fetchall()
    #
    # def getWaitDeals(self, id):
    #     return self.c.execute('SELECT * FROM DEALS WHERE BUYER = (?) AND STATUS = "WAIT"', [id]).fetchall()
    #
    #
    # def getAllDealsCount(self, id):
    #     deal = len(self.c.execute('SELECT * FROM DEALS WHERE BUYER = (?) AND STATUS = "DONE"', [id]).fetchall())
    #     count = deal + len(self.c.execute('SELECT * FROM DEALS WHERE SELLER = (?) AND STATUS = "DONE"',[id]).fetchall())
    #     return count


# db = DBConnection()
# db.create_tables()
# row = db.show_data()
# print(row)
# info = '<b>Farm:</b> Inzovu\n' \
#                '<b>Variety:</b> Bourbon, Typica\n' \
#                '<b>Processing:</b> Washed\n' \
#                '<b>Taste:</b> Honey, red currant, cherry\n\n' \
#                '<b>Price:</b>\n' \
#                '250 gr - 171 uah\n' \
#                '1 kg - 603 uah'
# db.add('Filter Roast', '🇷🇼 RWANDA 1 Espresso', info, 171, 603, 'https://i.ibb.co/FW7J4Dt/1.png')
#
# print(db.show_goods('Filter Roast'))
