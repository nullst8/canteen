from pyzbar import pyzbar
import pymysql as pm
import pyfiglet
from cv2 import cv2

pyfiglet.print_figlet("Canteen App")

conn = pm.connect(host="localhost",
                  user="nullst8",
                  password="mann@2312",
                  db="canteen")
cur = conn.cursor()


def ReadBarcode(image):
    img = cv2.imread(image)
    barcodes = pyzbar.decode(img)

    if not barcodes:
        print("Error Detecting Barcode")

    for barcode in barcodes:
        if barcode.data != "":
            if barcode.data.decode('ascii')[:4] == "N44-":
                admNo = barcode.data.decode('ascii')[4:]
                return admNo
            else:
                print("Barcode Not Recognized!")
        else:
            print("Error Reading Barcode!!")


def CheckUserExists(admNo):
    exists = cur.execute("show tables like 'a{}'".format(admNo))
    return True if exists == 1 else False


def AskInfo(admNo):
    inDebt = False
    nos = int(input("Enter Number of Items to Buy: "))
    for i in range(nos):
        item = input("What Item are You Buying: ")
        amt = input("Enter Amount: ")
        pn = input("Would you like to Pay for it now?(y/n): ")
        inDebt = False if pn[0] == 'y' else True

        if inDebt:
            cur.execute("insert into a{} (item,price) values ('{}',{})".format(
                admNo, item, amt))
            cur.execute("update a{} set debt = debt + {}".format(admNo, amt))
            cur.execute("select debt from a{}".format(admNo))
            q = cur.fetchall()

            for i in q:
                print(i)

            print("done1")
        else:
            cur.execute("insert into a{} (item,price) values ('{}',{})".format(
                admNo, item, amt))
            print("done2")


def CreateEntry(admNo):
    dbInitQuery = "sno int not null auto_increment primary key, item varchar(30) not null,price int not null,debt int"

    if CheckUserExists(admNo):
        AskInfo(admNo)
    else:
        cur.execute("create table a{}({})".format(admNo, dbInitQuery))
        AskInfo(admNo)


a = ReadBarcode("barcode.jpeg")
CreateEntry(a)
