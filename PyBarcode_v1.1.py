# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:39:59 2017
@author: Phani Atmakur

PyBarcode - Python Barcode Labels Printing.
"""
import sys, os, win32print, cx_Oracle, re


printer_name = win32print.GetDefaultPrinter ()
db_con = cx_Oracle.connect('username', 'password', 'server address - (IP) or hostname')
cursor = db_con.cursor()

print ">_________________________________________________________<"
print "| PYBARCODE VER.1.1. {Py2.7}                              |"
print "| PyBarcode reads user input, fetches data from database  |"
print "| and prints a barcode with respective identifiers on it. |"
print "|_________________________________________________________|" 
print "\n"



#Reads input from user.
#----------------------
def read_scannerdata():
    #keyboard_input = str(raw_input())
    print "*********************************************************"
    print "Enter ID or scan a barcode:"
    print "*********************************************************"
    keyboard_input = str(raw_input())
    print "---------"
    print "ID: " + keyboard_input.upper()
    feedto_printer(get_data(keyboard_input.upper()), keyboard_input)


#Retrieves data from Oracle database.
#------------------------------------
def get_data(data):
    ids = []
    query = "SELECT * \
             FROM   ITEMS \
             WHERE  INVENTORY_ID =:sub_query"

    sub_query = "SELECT * FROM DELIVERIES WHERE REQUEST_NUMBER=:REQUEST_NUMBER"

    cursor.execute(sub_query, {'REQUEST_NUMBER':data})
    for row in cursor:
        ids.append(row[0])
        

    cursor.execute(query, {'sub_query':ids[0]})
    for item in cursor:
        ids.append(item[0]) 
    
    return ids


#Prints data to a barcode along with identifiers.
#------------------------------------------------
def feedto_printer(req_data, keyboard_input):
    print "DATA    : %r " % req_data
    if req_data == [None]:
        print "INVALID INPUT (OR) BARCODE SCANNED.\nPLEASE TRY AGAIN."
        #print "*********************************************************"
        print "\n"
        read_scannerdata()

    else:
        print "NHI     : " + req_data[0], "\nNAME    : " + req_data[1]
        print "\n"
        #print "*********************************************************"

        barcode = str(req_data[0])
        name = str(req_data[1])
    
        # Barcode printer data feed format
        DATA1 = 'N' + '\n' \
        + 'MD25' + '\n' \
        + 'B300,60,0,1,2,2,50,B,"' + name[:12] + '"' + '\n' \
        + 'A310,01,0,3,2,2,N,"' + barcode + '"' + '\n' \
        + 'P1' + '\n'

        DATA = '^XA' + '\n' \


        DATA3 = '^XA' + '\n' \

        # Writing a log file for tracking workstations, latte numbers, nhi and datetime

        if sys.version_info >= (3,):
            raw_data = bytes (DATA, "utf-8")
        else:
            raw_data = DATA
    
        hPrinter = win32print.OpenPrinter (printer_name)
        try:
            hJob = win32print.StartDocPrinter (hPrinter, 1, (DATA, None, "RAW"))
            try:
                win32print.StartPagePrinter (hPrinter)
                win32print.WritePrinter (hPrinter, raw_data)
                win32print.EndPagePrinter (hPrinter)
            finally:
                win32print.EndDocPrinter (hPrinter)
        finally:
            win32print.ClosePrinter (hPrinter)
            read_scannerdata()
     
read_scannerdata()