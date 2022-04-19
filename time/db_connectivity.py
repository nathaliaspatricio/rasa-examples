import mysql.connector

def DbConnection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="mydatabase"
    )
    return mydb

def PersonInsert(name, age, education_level):
    mydb = DbConnection()

    mycursor = mydb.cursor()

    sql = 'INSERT INTO person (name, age, education_level) VALUES ("' + name + '", "' + str(age) + '", "' + education_level + '");'

    mycursor.execute(sql)

    sql = 'SELECT LAST_INSERT_ID();'

    mycursor.execute(sql)
    row = [item[0] for item in mycursor.fetchall()]

    mydb.commit()
    mydb.close()

    print("record inserted: " + str(row[0]))
    return row[0]


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
    DataUpdate("Nathalia", 36, "Mestrado")    
