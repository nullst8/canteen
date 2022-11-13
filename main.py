from pyzbar import pyzbar
import pymysql as pm
import pyfiglet
from cv2 import cv2

pyfiglet.print_figlet("canteen app")

conn = pm.connect(host="localhost",
                  user="nullst8",
                  password="mann@2312",
                  db="canteen")
cur = conn.cursor()


def ReadBarcode(image):
    img = cv2.imread(image)
    barcodes = pyzbar.decode(img)

    if not barcodes:
        print("err detecting barcode")

    for barcode in barcodes:

        if barcode.data != "":
            if barcode.data.decode('ascii')[:4] == "N44-":
                admNo = barcode.data.decode('ascii')[4:]
                return admNo
            else:
                print("barcode not recognized!")
        else:
            print("err reading barcode!!")


def CheckUserExists(admNo):
    exists = cur.execute("show tables like 'a{}'".format(admNo))
    return True if exists == 1 else False


def CreateEntry(admNo):
    dbInitQuery = "sno int not null auto_increment primary key, item varchar(30) not null,price int not null,debt int"
    if CheckUserExists(admNo):
        pass
    else:
        cur.execute("create table a{}({})".format(admNo, dbInitQuery))


# a = ReadBarcode("barcode.jpeg")
# print(a)

CreateEntry(30120)
