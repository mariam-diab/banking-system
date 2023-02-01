import random
from datetime import datetime
import time
import threading
from mydatabase import *

class Customer:
    account_locks = {}

    def __init__(self, name, nid, pin, account_number=None):
        self.name = name
        self.nid = nid
        self.pin = pin
        self.account_number = account_number
        if account_number:
            select_sql = "SELECT * FROM customer WHERE account_number=%s"
            select_val = (account_number,)
            mycursor.execute(select_sql, select_val)
            customer_info = mycursor.fetchone()
            if customer_info is not None:
                self.__balance = customer_info[4]
                self.__operations = ast.literal_eval(customer_info[5])
                Customer.account_locks[self.account_number] = threading.Lock()
        else:
            self.account_number = self.generate_bank_account_number()
            self.__balance = 0
            self.__operations = []
            Customer.account_locks[self.account_number] = threading.Lock()

    def deposit(self, amount):
        self.account_locks[self.account_number].acquire()
        now = datetime.now().strftime("on %A, %B %d, %Y, at %I:%M:%S %p")
        if amount > 0:
            self.__balance += amount
            operation = f"A {amount} SAR has been deposited to your account balance {now}"
            self.__operations.append(operation)
            print(f"SUCCESSFUL OPERATION! {operation}.\nYour total balance now is {self.__balance} SAR")
            self.update_database()
        else:
            print("Invalid amount, please try again.")
        self.account_locks[self.account_number].release()
        time.sleep(1)

    def withdraw(self, amount):
        self.account_locks[self.account_number].acquire()
        if not self.__operations:
            print("Your account is still inactive, you did not deposit any money before.")
        elif self.__balance == 0:
            print("Your balance is 0 SAR, you cannot withdraw any amount of money.")
        elif amount > self.__balance:
            print(f"You cannot withdraw this amount, your balance is {self.__balance} SAR.")
        elif amount <= 0:
            print("Invalid amount, please try again.")
        else:
            now = datetime.now().strftime("on %A, %B %d, %Y, at %I:%M:%S %p")
            self.__balance -= amount
            operation = f"A {amount} SAR has been withdrawn from your account balance {now}"
            self.__operations.append(operation)
            print(f"SUCCESSFUL OPERATION! {operation}.\nYour total balance now is {self.__balance} SAR.")
        self.update_database()
        self.account_locks[self.account_number].release()
        time.sleep(1)

    def report(self):
        self.account_locks[self.account_number].acquire()
        if not self.__operations:
            print("Your account is still inactive, you have not performed any previous operations.")
        else:
            for operation in self.__operations:
                print(operation)
        self.account_locks[self.account_number].release()
        time.sleep(3)

    def get_balance(self):
        return self.__balance

    def get_operations(self):
        return self.__operations

    def update_database(self):
        sql = "UPDATE customer SET balance=%s, operations=%s WHERE account_number=%s"
        val = (self.__balance, str(self.__operations), self.account_number)
        try:
            mycursor.execute(sql, val)
            db.commit()
        except Exception as e:
            print("Error:", str(e))
            return

    def generate_bank_account_number(self):
        account_number = str(random.randint(1, 9))
        for i in range(15):
            account_number += str(random.randint(0, 9))

        select_sql = "SELECT * FROM customer WHERE account_number=%s"
        select_val = (account_number,)
        mycursor.execute(select_sql, select_val)
        customer_info = mycursor.fetchone()

        if customer_info is None:
            return account_number
        else:
            return self.generate_bank_account_number()


