# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 09:48:10 2021

@author: fanyak
"""
from sys import exit

opt = None
file_name = None

while opt is None:  
    try:
        key = int(input("1. Place an order\n2. Process an order\nWhat would you like to do? "))
        assert key == 1 or key == 2
        opt = key;
    except AssertionError:
        print("Please select either 1 or 2")
        continue;
    except ValueError:
        print("Please select either 1 or 2")
        continue;
        

if opt == 1:
    file_name = input("How would you like to call this order? ").strip()    
    print("Please place your order below. To stop placing your order, leave the item name empty")
    print("\n********************\n") 
    order = True;
    
    with open('./%s.txt' % file_name, 'w') as f:
        f.write('Item' + "\t" + 'Price' + "\t" +  'Quantity' + "\n")
        while order: 
            item = input("Item: ").strip();
            if item: 
                price = None;
                quantity = None;
                while price is None:
                    try:
                         p = int(input("Price: $"))
                         price = p;
                    except ValueError:
                        print("Please enter a number for the price")
                        continue; 
                while quantity is None:
                    try:
                        q = int(input("Quantity: "))
                        quantity = q;
                    except ValueError:
                        print("Please enter a number for the quantity")
                        continue;
                f.write(str(item) + "\t" + str(price) + "\t" +  str(quantity) + "\n")
                print("\n********************\n")            
            else:
                 print("order saved to file %s.txt.  Exiting application" % file_name)
                 order = False;
                 f.close();
                 exit();
                 
                 
if opt == 2:
    data = None;
    while data is None:
        try:
         file_name = input("What order would you like to process? ")
         with open('./%s.txt' % file_name, 'r') as f:
            data = [order.strip().split('\t') for order in f.readlines()][1:];
            print('Going to the shops and buying everything for you... Please hold');
            for d in data:
                [item, price, quantity] = d;
                total = int(price)*int(quantity)
                print('\tSpending ${} on {}'.format(total,item));
            print("Shopping complete.")   
            f.close()
        except FileNotFoundError:
            print("%s order does not exist." % file_name)
            continue;
            

            
