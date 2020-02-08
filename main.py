import mysql.connector
import time

# initial connection to database
mydb = mysql.connector.connect(
  user="root",
  host="localhost",
  # my password commented out for submission
  passwd="",
  database="cse4701s19_project2"
)
mycursor = mydb.cursor()

# printed so the user knows the program is still running
def another_choice():
  print('----ENTER ANOTHER CHOICE OR 0 TO QUIT----')

# given a user entered name, and initial balance, function will create an account in the database
def create_acct():
  sql = "INSERT INTO account (name_on_account, balance) VALUES (%s, %s)"
  name = input("NAME ON ACCOUNT: ")
  balance = input("ENTER INITIAL BALANCE: ")
  mycursor.execute(sql, (name, balance))
  mydb.commit()
  print("----", mycursor.rowcount, "RECORD INSERTED----")
  print('----ACCOUNT SUCCESSFULLY CREATED----')
  print('')

# given a user entered account_no, function will return the details of the account
def check_balance():
  acct_no = input("ENTER ACCOUNT NUMBER: ")
  mycursor.execute("SELECT * FROM account WHERE account_no =" + acct_no + ";")
  balance_info = mycursor.fetchall()
  # check if account_no is valid
  if len(balance_info) == 0:
    print("ACCOUNT NUMBER ENTERED IS INVALID")
  else:
    for x in balance_info:
      print("ACCOUNT NUMBER: ", x[0])
      print("NAME ON ACCOUNT: ", x[1])
      print("BALANCE OF ACCOUNT: ", x[2])
      print("ACCOUNT OPENED ON: ", x[3], "\n")

# Ask the bank teller for account number. 
# Show the account details (number, name, balance, and account open date), lock the account for update. 
# Then ask the teller to enter deposit amount. 
# Update balance on the account and release the lock. 
# Show new balance.
def deposit():
  acct_no = input("ENTER ACCOUNT NUMBER: ")
  mycursor.execute("SELECT * FROM account WHERE account_no =" + acct_no + " FOR UPDATE;")
  account_details = mycursor.fetchall()
  # check if account_no is valid
  if len(account_details) == 0:
    print("ACCOUNT NUMBER ENTERED IS INVALID")
  else:
    for x in account_details:
      print("ACCOUNT NUMBER: ", x[0])
      print("NAME ON ACCOUNT: ", x[1])
      print("BALANCE OF ACCOUNT: ", x[2])
      print("ACCOUNT OPENED ON: ", x[3], "\n")
 
    deposit_amt = input("ENTER DEPOSIT AMOUNT : ")
    mycursor.execute("UPDATE account SET balance = balance + " + deposit_amt + " WHERE account_no =" + acct_no + ";")
    mydb.commit()

    mycursor.execute("SELECT balance FROM account WHERE account_no =" + acct_no + ";")
    new_balnce = mycursor.fetchall()
    for x in new_balnce:
      print ("NEW BALANCE : ", x[0])  

# Ask for the account number. 
# Show the account details and lock the account for update. 
# Ask for the withdrawal amount. Update balance on the account and release the lock. 
# Show new balance. Display error if balance is insufficient for withdrawal.

def withdraw():
  acct_no = input("ENTER ACCOUNT NUMBER: ")
  mycursor.execute("SELECT * FROM account WHERE account_no =" + acct_no + " FOR UPDATE;")
  account_details = mycursor.fetchall()
  # check if account_no is valid
  if len(account_details) == 0:
    print("ACCOUNT NUMBER ENTERED IS INVALID")
  else:
    for x in account_details:
      print("ACCOUNT NUMBER: ", x[0])
      print("NAME ON ACCOUNT: ", x[1])
      print("BALANCE OF ACCOUNT: ", x[2])
      print("ACCOUNT OPENED ON: ", x[3], "\n")
    
    withdrawal_amt = input("ENTER WITHDRAWAL AMOUNT : ")
    # withdraw if sufficient funds
    if float(withdrawal_amt) <= account_details[0][2]:
      mycursor.execute("UPDATE account SET balance = balance - " + withdrawal_amt + " WHERE account_no =" + acct_no + ";")
      mydb.commit()
      mycursor.execute("SELECT balance FROM account WHERE account_no =" + acct_no + ";")
      new_balnce = mycursor.fetchall()
      for x in new_balnce:
        print ("NEW BALANCE : ", x[0])
    else:
      print("BALANCE IS INSUFFICENT FOR WITHDRAWAL")

# Ask for the source account number. 
# Show account details and lock the source account. 
# Ask for target account number. Show details and lock the target account. 
# Ask for the transfer amount. Withdraw amount from source account. 
# Display error message in case of insufficient balance. 
# Make your program go to sleep for 10 seconds to simulate network congestion. 
# Deposit the amount into the target account, and go to sleep for 10 seconds again. 
# Commit the transaction and show confirmation of transfer.
def transfer():
  # FETCH SOURCE ACCOUNT NUMBER STEP
  srce_acct_no = input("ENTER SOURCE ACCOUNT NUMBER: ")
  mycursor.execute("SELECT * FROM account WHERE account_no =" + srce_acct_no + " FOR UPDATE;")
  srce_account_details = mycursor.fetchall()
  # check if account_no is valid
  if len(srce_account_details) == 0:
    print("SOURCE ACCOUNT NUMBER ENTERED IS INVALID")
  else:
    for x in srce_account_details:
      print("SOURCE ACCOUNT NUMBER: ", x[0])
      print("NAME ON ACCOUNT: ", x[1])
      print("BALANCE OF ACCOUNT: ", x[2])
      print("ACCOUNT OPENED ON: ", x[3], "\n")
      # FETCH TARGET ACCOUNT NUMBER STEP
      trgt_acct_no = input("ENTER TARGET ACCOUNT NUMBER: ")
      mycursor.execute("SELECT * FROM account WHERE account_no =" + trgt_acct_no + " FOR UPDATE;")
      trgt_account_details = mycursor.fetchall()
      # check if account_no is valid
      if len(trgt_account_details) == 0:
        print("TARGET ACCOUNT NUMBER ENTERED IS INVALID")
      else:
        for x in trgt_account_details:
          print("TARGET ACCOUNT NUMBER: ", x[0])
          print("NAME ON ACCOUNT: ", x[1])
          print("BALANCE OF ACCOUNT: ", x[2])
          print("ACCOUNT OPENED ON: ", x[3], "\n")

        # TRANSFER STEP
        transfer_amt = input("ENTER TRANSFER AMOUNT : ")
        # withdraw from source account if sufficient funds
        if float(transfer_amt) <= srce_account_details[0][2]:
          mycursor.execute("UPDATE account SET balance = balance - " + transfer_amt + " WHERE account_no =" + srce_acct_no + ";")
          # sleep program for 10 seconds
          time.sleep(10)
          # deposit into target account
          mycursor.execute("UPDATE account SET balance = balance + " + transfer_amt + " WHERE account_no =" + trgt_acct_no + ";")
          # sleep program for 10 more seconds
          time.sleep(10)
          # commit transaction to database
          mydb.commit()
          print("----TRANSFER SUCCESSFULLY COMPLETED----")
          # confirmation of transfer
          mycursor.execute("SELECT balance FROM account WHERE account_no =" + srce_acct_no + ";")
          srce_balance_info = mycursor.fetchall()
          for x in srce_balance_info:
            print("NEW BALANCE OF SOURCE ACCOUNT: ", x[0])
          mycursor.execute("SELECT balance FROM account WHERE account_no =" + trgt_acct_no + ";")
          trgt_balance_info = mycursor.fetchall()
          for x in trgt_balance_info:
            print("NEW BALANCE OF TARGET ACCOUNT: ", x[0])
        else:
          print("SOURCE ACCOUNT BALANCE IS INSUFFICENT FOR WITHDRAWAL")  




# main function to run banking program
def main():
  contin = True
  while contin:
    print("MAIN MENU\n","1 -- CREATE ACCOUNT\n", "2 -- CHECK BALANCE\n", "3 -- DEPOSIT\n","4 -- WITHDRAW\n", "5 -- TRANSFER\n","0 -- QUIT")
    choice = input("ENTER YOUR CHOICE: ")
    if choice == '1':
      create_acct()
      # program still active so user enters another choice
      another_choice()
    elif choice == '2':
      check_balance()
      # program still active so user enters another choice
      another_choice()
    elif choice == '3':
      deposit()
      # program still active so user enters another choice
      another_choice()
    elif choice == '4':
      withdraw()
      # program still active so user enters another choice
      another_choice()
    elif choice == '5':
      transfer()
      # program still active so user enters another choice
      another_choice()
    elif choice == '0':
      contin = False 
    else:
      #invalid choice entered by user
      print('!!!!THAT IS NOT A VALID CHOICE!!!!')
  # user quit program with choice 0
  print('****PROGRAM IS DONE RUNNING****')
  # close connection to mysql database
  mydb.close()

if __name__ == "__main__" :
  main()



