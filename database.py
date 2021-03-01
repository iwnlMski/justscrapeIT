import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='Mski',
    password='Sqldb2k21.',
    database='mydatabase',
)

cursor = mydb.cursor()
# cursor.execute('ALTER TABLE offers CHANGE skills skills LONGTEXT')


def initialize_table():
    try:
        cursor.execute(
            'CREATE TABLE offers ('
            'id INT AUTO_INCREMENT PRIMARY KEY,'
            ' link VARCHAR(255),'
            ' title VARCHAR(255),'
            ' company VARCHAR(255),'
            ' salary VARCHAR(255),'
            ' location VARCHAR(255),'
            ' skills VARCHAR(1023))'
        )
    except mysql.connector.errors.ProgrammingError:
        return "Already initialized"


def offer_not_exists(link):
    sql = 'SELECT * FROM offers WHERE link=%s'
    link = (link, )
    cursor.execute(sql, link)
    if not cursor.fetchall():
        return True
    else:
        return False


def add_to_database(data):
    sql = 'INSERT INTO offers (link, title, company, salary, location, skills) VALUES (%s, %s, %s, %s, %s, %s)'
    val = (data['link'], data['title'], data['company'], data['salary'], data['location'], data['skills'])
    cursor.execute(sql, val)
    mydb.commit()