from pyzbar import pyzbar
import pyfiglet
from cv2 import cv2

pyfiglet.print_figlet("canteen app")


def ReadBarcode(image):
    img = cv2.imread(image)
    barcodes = pyzbar.decode(img)

    if not barcodes:
        print("err detecting barcode")

    for barcode in barcodes:

        if barcode.data != "":
            if barcode.data.decode('ascii')[:4] == "N44-":
                print("your admission number is:{}".format(
                    barcode.data.decode('ascii')[4:]))
            else:
                print("barcode not recognized!")
        else:
            print("err reading barcode!!")


# selImg = input(r"enter img path: ")
# ReadBarcode(selImg)
ReadBarcode("barcode.jpeg")
# ReadBarcode("not.png")
