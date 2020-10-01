import sqlite3
import sys, os
import datetime
from datetime import timedelta, date
from datetime import datetime as dt


conn = sqlite3.connect('library.db')


def main_menu():
    os.system('clear')
    print("Welcome,")
    print("1- Find an item in the library\n")
    print("2- Borrow an item from the library\n")
    print("3- Return a borrowed item\n")
    print("4- Donate an item to the library\n")
    print("5- Find an event in the library\n")
    print("6- Register for an event in the library\n")
    print("7- Volunteer for the library\n")
    print("8- Ask for help from a librarian\n")

    choice = input("Please enter the option number to start: \n")
    exec_menu(choice)
    return

def exec_menu(choice):    
    if choice == '1':
        findItem()
    elif choice == '2':
        borrowItem()
    elif choice == '3':
        returnItem()
    elif choice == '4':
        donateItem()
    elif choice == '5':
        findEvent()
    elif choice == '6':
        registerEvent()
    elif choice == '7':
        volunteer()
    elif choice == '8':
        askHelp()
    else:
        print("\nError: Please enter one of the given options\n")
        main_menu()
    return


#Find an item in the library
def findItem():
    mycursor = conn.cursor()
    mytitle = input("Please enter the title of item you want to find:\n")
    mycursor.execute("SELECT * FROM Item WHERE title= ?", (mytitle,))
    rows=mycursor.fetchall()
    if rows:
        print("We do have the following items : ")
        for row in rows:
          print("item ID = " + str(row[0]) + ", title = " + str(row[1]) + ", availability = " + str(row[8]) + ", shelf_num = "+ str(row[4])+"\n")

    else:
        category = input("Unfortunately, we cannot find the mateched item. Please select the type of item you want to find: \n 1.Books-non fiction \n 2.Books-fiction \n 3.Journal \n 4.Magazine \n 5.Movie \n 6.Music \n 7.Others\n")

        if category == '1':
            c = 'Books-non fiction'
        if category == '2':
            c = 'Books-fiction'
        if category == '3':
            c = 'Journal'
        if category == '4':
            c = 'Magazine'
        if category == '5':
            c = 'Movie'
        if category == '6':
            c = 'Music'
        if category == '7':
            c = 'Others'

        if category == '1' or category == '2':
            authorf = input("Please enter the author's first name of the book:\n")
            authorl = input("Please enter the author's last name of the book:\n")
            mycursor.execute ("SELECT i.item_id, i.title, a.first_name, a.last_name, i.availability, i.shelf_num FROM Item i, items_of_author o, Books b, Author a WHERE i.item_id=b.item_id AND i.item_id=o.item_id AND o.author_id=a.author_id AND a.first_name= ? AND a.last_name= ? AND i.cat_name = ?", (authorf, authorl, c))
            rows = mycursor.fetchall()
            if rows:
              print("We do have the following items : ")
              for row in rows:
                print("item ID = " + str(row[0]) + ", title = " + str(row[1]) + ", availability = " + str(row[4]) + ", shelf_num = "+ str(row[5])+"\n")
            else:
              print("Unfornataly, there is no matched author, but we do have the following items that are matching the category: ")
              mycursor.execute ("SELECT * FROM Item WHERE cat_name = ?", (c,))
              rows = mycursor.fetchall()
              if rows:
                for row in rows:
                  print("item ID = " + str(row[0]) + ", title = " + str(row[1]) + ", availability = " + str(row[8]) + ", shelf_num = "+ str(row[4])+"\n")
              else:
                print("There is no matched item. Please retry.")
                findItem()

        elif category == '3' or category == '4':
            pubn = input("Please enter the publisher's name :\n")
            mycursor.execute ("SELECT i.item_id, i.title, p2.Publisher_name, i.availability, i.shelf_num FROM Item i, items_of_Publisher o, Periodicals p1, Publisher p2 WHERE i.item_id=p1.item_id AND  i.item_id=o.item_id AND o.publisher_id=p2.publisher_id AND p2.Publisher_name= ? AND i.cat_name = ?", (pubn,c))
            rows = mycursor.fetchall()
            if rows:
                for row in rows:
                    print("item ID = " + str(row[0]) + ", title = " + str(row[1]) + ", availability = " + str(row[3]) + ", shelf_num = "+ str(row[4])+"\n")
            else:
                print("Unfornataly, we cannot find the publisher, but we do have the following items that are matching the category: ")
                mycursor.execute ("SELECT * FROM Item WHERE cat_name = ?", (c,))
                rows = mycursor.fetchall()
                if rows:
                  for row in rows:
                    print("item ID = " + str(row[0]) + ", title = " + str(row[1]) + ", availability = " + str(row[8]) + ", shelf_num = "+ str(row[4])+"\n")
                else:
                  print("We cannot find the publisher. Please retry.")
                  findItem()

        elif category =='5' or  category =='6':
            artistn = input("Please enter the artist's name:\n")
            mycursor.execute ("SELECT i.item_id, i.title, a2.Artist_name, i.availability, i.shelf_num  FROM Item i, items_of_Artist o, Audiovisuals a1, Artist a2 WHERE i.item_id=a1.item_id AND i.item_id=o.item_id AND o.artist_id=a2.artist_id AND a2.Artist_name= ? AND i.cat_name = ?", (artistn,c))
            rows = mycursor.fetchall()
            if rows:
                for row in rows:
                    print("item ID = " + str(row[0]) + ", title = " + str(row[1]) + ", availability = " + str(row[3]) + ", shelf_num = "+ str(row[4])+"\n")
            else:
                pn = input("We cannot find the artist. Please try to enter the producer's name:\n")
                mycursor.execute ("SELECT i.item_id, i.title, p.Producer_name, i.availability, i.shelf_num FROM Item i, items_of_Producer o, Audiovisuals a, Producer p WHERE i.item_id=a.item_id AND i.item_id=o.item_id AND o.producer_id=p.producer_id AND p.Producer_name= ? AND i.cat_name = ?", (pn,c))
                rows = mycursor.fetchall()
                if rows:
                    for row in rows:
                        print("item ID = " + str(row[0]) + ", title = " + str(row[1]) + ", availability = " + str(row[3]) + ", shelf_num = "+ str(row[4])+"\n")
                else:
                    print("Unfornataly, we cannot find either of the artist nor the producer, but we do have the following items that are matching the category: ")
                    mycursor.execute ("SELECT * FROM Item WHERE cat_name = ?", (c,))
                    rows = mycursor.fetchall()
                    if rows:
                      for row in rows:
                        print("item ID = " + str(row[0]) + ", title = " + str(row[1]) + ", availability = " + str(row[8]) + ", shelf_num = "+ str(row[4])+"\n")
                    else:
                      print("We cannot find either of the artist nor the producer. Please retry.")
                      findItem()
        else:
          mycursor.execute ("SELECT * FROM Item WHERE cat_name = ?", (c,))
          rows = mycursor.fetchall()
          if rows:
              print("We do have the following items : ")
              for row in rows:
                  print("item ID = " + str(row[0]) + ", title = " + str(row[1]) + ", availability = " + str(row[8]) + ", shelf_num = "+ str(row[4])+"\n")
          else:
              print("There is no matched item. Please retry.")
              findItem()

    mycursor.close()
    back = input("Do you wish to go back? Y/N  \n")
    if back in ('Y', 'y', 'Yes', 'yes'):
      main_menu()
    else:
      return

#Borrow an item from the library    
def borrowItem():
    mycursor = conn.cursor()
    myid = input("Please enter your Person ID:\n")
    mycursor.execute("SELECT * FROM Person WHERE Person_id= ?", (myid,))
    resultp = mycursor.fetchone()
    if resultp is None:
        print("There is no matched ID. Please try again")
        borrowItem()   
    if resultp[14] == 0:
        print("Unable to borrow, you have an overdue book has not returned")
        mycursor.close()
        back = input("Do you wish to go back? Y/N  \n")
        if back in ('Y', 'y', 'Yes', 'yes'):
          main_menu()
        else:
          return
    if resultp[14] == 1:
        itemId = input("Please enter the item ID you want to borrow:\n")
        mycursor.execute("SELECT * FROM Item WHERE item_id= ?", (itemId,))
        results = mycursor.fetchone()
        if results is None:
            print("There is no matched ID. Please try again")
            borrowItem()  
        elif results[4]==0:
            print('This book is too hot, we no longer have a collection, please wait for someone to return it')
            back = input("Do you wish to go back? Y/N  \n")
            if back in ('Y', 'y', 'Yes', 'yes'):
              main_menu()
            else:
              return
        else:
            mycursor.execute('UPDATE Person SET allow_borrow = 0 WHERE person_id = ?', (myid,))
            mycursor.execute('UPDATE Item SET availability = 0 AND borrow_date = ? AND due_date = ? AND person_id = ? WHERE item_id = ? ', (date.today(), date.today() + timedelta(days=10), myid, itemId))
            print('You have succesfully borrowed %s' % results[1])
            conn.commit()
            mycursor.close()
            back = input("Do you wish to go back? Y/N  \n")
            if back in ('Y', 'y', 'Yes', 'yes'):
              main_menu()
            else:
              return
        
#Return a borrowed item
def returnItem():
    mycursor = conn.cursor()
    itemId = input("Please enter the item ID you want to return:\n")
    mycursor.execute("SELECT * FROM Item WHERE item_id= ?", (itemId,))
    results = mycursor.fetchone()
    if results is None:
      print("There is no matched ID. Please try again")
      returnItem()
    else:
      myid = input("Please enter your Person ID:\n")
      mycursor.execute("SELECT * FROM Person WHERE person_id= ?", (myid,))
      resultp = mycursor.fetchone()
      if resultp is None:
            print("There is no matched ID. Please try again")
            returnItem()   
      if resultp[14] == 0:
            mycursor.execute('UPDATE Person SET allow_borrow = 1 WHERE person_id = ?', (myid,))
      
      if dt.strptime(results[7], '%Y-%m-%d').date()<date.today(): #passed the due date, fines is required
        print('This book passed the due date, $'+ str(((date.today()-dt.strptime(results[7], '%Y-%m-%d').date()).days)*2) + ' fine is required')
            
        #fineamount, #finepayed
        mycursor.execute('INSERT INTO Fines_on VALUES (?,?,?,?,?)', (date.today(),myid, date.today(),((date.today()-dt.strptime(results[7], '%Y-%m-%d').date()).days)*2, 0))

      print('You have succesfully returned %s' % results[1])
      conn.commit()
      mycursor.close()
      back = input("Do you wish to go back? Y/N  \n")
      if back in ('Y', 'y', 'Yes', 'yes'):
        main_menu()
      else:
        return
    
    
#Donate an item to the library
def donateItem():
    mycursor = conn.cursor()

    # Retrieve largest item_id in database
    SQLRetrieval = ("SELECT MAX(item_id)" "FROM Item")
    mycursor.execute(SQLRetrieval)
    results = mycursor.fetchone()
    newItem_id = results[0][0] + str(int(results[0][1]) + 1)
    mycursor.close()

    print("Create a profile for a new item")
    category = input("Please select the type of the item you are gonna donate: \n 1.Books-non fiction \n 2.Books-fiction \n 3.Journal \n 4.Magazine \n 5.Movie \n 6.Music \n 7.Others\n")

    if category == '1':
        c = 'Books-non fiction'
    if category == '2':
        c = 'Books-fiction'
    if category == '3':
        c = 'Journal'
    if category == '4':
        c = 'Magazine'
    if category == '5':
        c = 'Movie'
    if category == '6':
        c = 'Music'
    if category == '7':
        c = 'Others'

    title = input("Please enter title: ")
    pid = input("Please enter your person ID: ")
    desc = input("Please enter the description: ")
    condition = input("Please enter the condition: \n 1.Excellent\n 2.Good \n 3.Average \n 4.Poor \n")
    if condition == '1':
        cond = 'Excellent'
    if condition == '2':
        cond = 'Good'
    if condition == '3':
        cond = 'Average'
    if condition == '4':
        cond = 'Poor'
    
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM Person WHERE Person_id= ?", (pid,))
    resultp = mycursor.fetchone()
    
    SQLCommand = ("INSERT INTO New_items(new_id, new_title, cat_name, person_id, desc, condition) VALUES (?,?,?,?,?,?)")
    Values = [newItem_id,title,c,pid,desc,cond]
    
    mycursor.execute(SQLCommand,Values)
    conn.commit() #commit any pending transactions to the database
    print("The profile for item " + str(newItem_id) + "(id) " + title +  " was created.\n")
    mycursor.close()
    
    back = input("Do you wish to go back? Y/N  \n")
    if back in ('Y', 'y', 'Yes', 'yes'):
      main_menu()
    else:
      return

#Find an event in the library
def findEvent():
    mycursor = conn.cursor()
    myeventName = input("Please enter the event name:\n")
    mycursor.execute("SELECT * FROM Event WHERE event_name= ?", (myeventName,))
    row=mycursor.fetchone()
    if row:
        print("Event name : " + str(row[0]) + ", event type : " + str(row[1]) + ", description:" + str(row[2]) + ", date: " + str(row[3]) +", time : "+ str(row[4]) + ", audience = "+ str(row[5]) + ", has_food = "+ str(row[6])+ ", room_number = "+ str(row[7])+"\n")
    else:
        etype = input("Unfortunately, we cannot find the mateched event. Please select the type of item you want to find: \n 1.Book related events\n 2.Art shows \n 3.Film screenings \n 4.Workshops \n 5.Networking \n 6.Others \n")

        if etype == '1':
            et = 'Book related events'
        if etype == '2':
            et = 'Art shows'
        if etype == '3':
            et = 'Film screenings'
        if etype == '4':
            et = 'Workshops'
        if etype == '5':
            et = 'Networking'
        if etype == '6':
            et = 'Others'

        mycursor.execute ("SELECT * FROM Event WHERE event_type = ?", (et,))
        rows = mycursor.fetchall()
        if rows:
            print("We do have the following events : ")
            for row in rows:
                print("Event name : " + str(row[0]) + ", event type : " + str(row[1]) + ", description:" + str(row[2]) + ", date: " + str(row[3]) +", time : "+ str(row[4]) + ", audience = "+ str(row[5]) + ", has_food = "+ str(row[6])+ ", room_number = "+ str(row[7])+"\n")
        else:
          print("Invalid input. Please retry.")
          findEvent()
    mycursor.close()
    back = input("Do you wish to go back? Y/N  \n")
    if back in ('Y', 'y', 'Yes', 'yes'):
      main_menu()
    else:
      return

#Register for an event in the library
def registerEvent():
    mycursor = conn.cursor()
    myeventname = input("Please enter the event name:\n")
    mypersonId = input("Please enter your person id:\n")

    SQLCommand = ("INSERT INTO Register(event_name, person_id) VALUES (?,?)")
    Values = [myeventname, mypersonId]
    
    mycursor.execute(SQLCommand,Values)
    conn.commit() #commit any pending transactions to the database
    print("The event " + str(myeventname) + " and you (ID: " + mypersonId +  ") was successfully registered.\n")
    mycursor.close()
    back = input("Do you wish to go back? Y/N  \n")
    if back in ('Y', 'y', 'Yes', 'yes'):
      main_menu()
    else:
      return

#Volunteer for the library
def volunteer():
    mycursor = conn.cursor()
    #Search for volunteer positions
    volType = input("Please enter the the volunteer type you are interested:\n 1.Adult literacy tutoring \n 2.Adult numeracy tutoring \n 3.Home deliver library materials \n 4.Teen volunteers \n 5.Others\n")
    if volType == '1':
            vt = 'Adult literacy tutoring'
    if volType == '2':
            vt = 'Adult numeracy tutoring'
    if volType == '3':
            vt = 'Home deliver library materials'
    if volType == '4':
            vt = 'Teen volunteers'
    if volType == '5':
            vt = 'Others'
    mycursor.execute ("SELECT * FROM Volunteer_options WHERE vol_type= ?", (vt,))
    rows = mycursor.fetchall()
    if rows:
        for row in rows:
            print("\n volunteer name = " + str(row[0]) + ", type = " + str(row[1]) + ", activity = " + str(row[2]) + ", hours per week = "+ str(row[3])+"\n")
    if rows is None:
        print("There is no position for this type. Please retry.")
        volunteer()
    
    #Sign up for the volunteer  
    signup = input("Are you interested about any of the volunteer activity? Y/N  \n ")
    if signup in ('Y', 'y', 'Yes', 'yes'):
      mypersonId = input("Please enter your person id:\n")
      vol_name = input("Please enter the volunteer name:\n")
      SQLCommand = ("INSERT INTO Volunteer(person_id, vol_name) VALUES (?,?)")
      Values = [mypersonId, vol_name]
    
      mycursor.execute(SQLCommand,Values)
      conn.commit() #commit any pending transactions to the database
      print("You (ID: " + mypersonId +  ") was successfully registered as the volunteer of " + str(vol_name)+ "\n")
      mycursor.close()

    back = input("Do you wish to go back? Y/N \n")
    if back in ('Y', 'y', 'Yes', 'yes'):
      main_menu()
    else:
      return

#Ask for help from a librarian
def askHelp():
    mycursor = conn.cursor()
    # Retrieve largest help_id in database
    SQLRetrieval = ("SELECT MAX(help_id) FROM Help")
    mycursor.execute(SQLRetrieval)
    results = mycursor.fetchone()
    newHelp_id = int(results[0]) + 1
    mycursor.close()
   
    mypersonId = input("Please enter your person id:\n")
    htype = input("What kind of help do you need:\n 1- Research/finding items \n 2. Citation help \n 3. Writing help \n 4. Event/workshop help \n 5. Others\n")

    if htype == '1': helpType = 'Research/finding items'
    elif htype == '2': helpType = 'Citation help'
    elif htype == '3': helpType = 'Writing help'
    elif htype == '4': helpType = 'Event/workshop help'
    else: helpType = 'Others'

    urgent = input("Is it urgent? 0/1 \n")
    while urgent != '1' and urgent != '0': 
      print("invalid input. Please retry")
      urgent = input("Is it urgent? 0/1 \n")

    desc = input("Please write a description: \n")
    
    mycursor = conn.cursor()
    SQLCommand = ("INSERT INTO Help(help_id, help_type, help_desc, is_urgent, person_id) VALUES (?,?,?,?,?)")
    Values = [newHelp_id, helpType, desc, int(urgent), mypersonId]
    
    mycursor.execute(SQLCommand,Values)
    conn.commit() #commit any pending transactions to the database
    print("Your (ID= "+ str(mypersonId) + ") request (ID= " + str(newHelp_id) + ") has been recorded and our librarian will come and help \n")

    mycursor.close()
    back = input("Do you wish to go back? Y/N  \n")
    if back in ('Y', 'y', 'Yes', 'yes'):
      main_menu()
    else:
      return



### Main ###
main_menu()

conn.close()

