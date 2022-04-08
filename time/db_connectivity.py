import mysql.connector

def DataUpdate(name, age, education_level):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="mydatabase"
    )

    mycursor = mydb.cursor()

    sql = 'INSERT INTO person (name, age, education_level) VALUES ("' + name + '", "' + str(age) + '", "' + education_level + '");'

    mycursor.execute(sql)

    mydb.commit()

    print("record inserted")

if __name__=="__main__":
    DataUpdate("Nathalia", 36, "Mestrado")    
