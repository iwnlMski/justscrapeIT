import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='Mski',
    password='Sqldb2k21.',
    database='mydatabase',
)

cursor = mydb.cursor()
# cursor.execute('ALTER TABLE offers CHANGE skills skills LONGTEXT')
# cursor.execute('DELETE FROM offers WHERE id > 0')
# mydb.commit()


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


def create_table_for_language(language):
    sql_create_table = f'CREATE TABLE {language} (technology VARCHAR(255), count INT)'
    cursor.execute(sql_create_table)


def select_offers_with_language(language):
    sql_select_by_lang = 'SELECT skills FROM offers WHERE skills LIKE %s'
    val_search_lang = ("%"+language+"%", )
    cursor.execute(sql_select_by_lang, val_search_lang)
    return cursor.fetchall()


def get_tech_from_offer(results):
    for tech in results:
        yield tech


def filter_by_language(language):
    try:
        create_table_for_language(language)
    except mysql.connector.errors.ProgrammingError:
        print("already exists")
    offers_with_language = select_offers_with_language(language)
    offer_gen = get_tech_from_offer(offers_with_language)
    for offer in offer_gen:
        yield offer


def skill_in_table(skill, language):
    sql = f'SELECT * FROM {language} WHERE technology = \'{skill}\''
    print(sql)
    cursor.execute(sql)
    return True if cursor.fetchall() else False


def get_skill_count(skill, language):
    sql = f'SELECT count FROM {language} WHERE technology = \'{skill}\''
    cursor.execute(sql)
    count = cursor.fetchall()
    return int(count[0][0])


def increment_skill_counter(skill, language):
    incr_count = get_skill_count(skill, language) + 1
    sql = f'UPDATE {language} SET count = {incr_count} WHERE technology = \'{skill}\''
    cursor.execute(sql)


def create_skill_record(skill, language):
    sql = f'INSERT INTO {language} (technology, count) VALUES (\'{skill}\', {1})'
    cursor.execute(sql)


def check_for_not_allowed_signs(word):
    if '\'' in word:
        return word.replace('\'', '')
    else:
        return word


def create_table_with_tech_for_lang(language):
    skill_set_gen = filter_by_language(language)
    for skill_set in skill_set_gen:
        for skill in skill_set[0].split(', '):
            skill = check_for_not_allowed_signs(skill)
            if skill_in_table(skill, language):
                increment_skill_counter(skill, language)
            else:
                create_skill_record(skill, language)
    mydb.commit()


def delete_table_of_skills(language):
    try:
        sql = f'DROP TABLE {language}'
        cursor.execute(sql)
    except mysql.connector.errors.ProgrammingError:
        print('No such table')