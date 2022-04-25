import mysql.connector

def DbConnection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="mydatabase"
    )
    return mydb

def PersonInsert(name, age, education_level, language):
    mydb = DbConnection()

    mycursor = mydb.cursor()

    sql = 'INSERT INTO person (name, age, education_level, language) VALUES ("' + name + '", "' + str(age) + '", "' + education_level + '", "' + language + '");'

    mycursor.execute(sql)

    sql = 'SELECT LAST_INSERT_ID();'

    mycursor.execute(sql)
    row = [item[0] for item in mycursor.fetchall()]

    mydb.commit()
    mydb.close()

    print("record inserted: " + str(row[0]))
    return row[0]

def PersonSelect(person_id):
    mydb = DbConnection()

    mycursor = mydb.cursor(dictionary=True)

    sql = 'SELECT * FROM person WHERE person_id = ' + person_id + ';'

    mycursor.execute(sql)

    result = mycursor.fetchone()
    print(result)
    
    mydb.close()
    
    itens = []
    print("record selected: ")
    print(result['name'])

    return result  

def PersonDelete(id):
    mydb = DbConnection()

    mycursor = mydb.cursor()

    sql = 'DELETE FROM person WHERE person_id = ' + id + ';'
    print(sql)

    mycursor.execute(sql)

    mydb.commit()

    print(mycursor.rowcount, "record(s) deleted")
    return []  


def CitySelect(city):
    mydb = DbConnection()

    mycursor = mydb.cursor()

    sql = 'SELECT zone_name FROM time_zone WHERE zone_name LIKE "%' + city + '%" LIMIT 1;'

    mycursor.execute(sql)

    row = [item[0] for item in mycursor.fetchall()]

    mydb.close()

    print("record selected: " + row[0])
    return row[0]    


if __name__=="__main__":
    DataUpdate("Nathalia", 36, "Mestrado", "pt")    
