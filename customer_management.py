from customer import *
class Customer_Management():
    def sign_on(self):
        account_number = input("Please enter your bank account number: ")
        pin = input("Please enter your pin: ")
        sql = "SELECT * FROM customer WHERE account_number=%s AND pin=%s"
        val = (account_number, pin)
        mycursor.execute(sql, val)
        customer_data = mycursor.fetchone()
        if customer_data is None:
            print("Invalid account number or pin, please try again!")
            return
        customer = Customer(customer_data[1], customer_data[2], customer_data[4], customer_data[0])
        print(f"Welcome {customer.name}! What do you want to do?")
        while True:
            process = input("1: Deposit \n2: Withdraw \n3: Report \n4: Log out \nEnter the number of the process: ")
            if process == '1':
                amount = int(input("Enter the amount of money you want to deposit: "))
                customer.deposit(amount)
            elif process == '2':
                amount = int(input("Enter the amount of money you want to withdraw: "))
                customer.withdraw(amount)
            elif process == '3':
                customer.report()
            elif process == '4':
                print("Thank you for choosing the SNB, see you soon!")
                break
            else:
                print("Invalid process, please try again.")
        time.sleep(2)

    def open_account(self):
        name = input("Please enter your name: ").upper()
        while not self.check_valid_input(name, "name"):
            print("Invalid name, please enter only letters.")
            name = input("Please enter your name: ").upper()

        nid = input("Please enter your National ID: ")
        while not self.check_valid_input(nid, "nid"):
            print("Invalid National ID, please enter 9 digits.")
            nid = input("Please enter your National ID: ")
        sql = "SELECT * FROM customer WHERE nid = %s"
        val = (nid,)
        mycursor.execute(sql, val)
        results = mycursor.fetchall()
        if results:
            print("You already have an account, you are not allowed to have another.")
            return

        pin = input("Please enter a 4-digit pin: ")
        while not self.check_valid_input(pin, "pin"):
            print("Invalid pin, please enter 4 digits.")
            pin = input("Please enter a 4-digit pin: ")

        customer = Customer(name, nid, pin)
        print(f"Thank you {name}, your account has been created successfully! Your bank account number is {customer.account_number}")
        sql = "INSERT INTO customer (account_number, name, nid, pin, balance, operations) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (customer.account_number, customer.name, customer.nid, customer.pin, customer.get_balance(), str(customer.get_operations()))
        mycursor.execute(sql, val)
        db.commit()
        time.sleep(2)

    def check_valid_input(self, input, type):
        if type == "name":
            if input.isalpha():
                return True
            else:
                return False
        elif type == "pin":
            if input.isdigit() and len(input) == 4:
                return True
            else:
                return False
        elif type == "nid":
            if input.isdigit() and len(input) == 9:
                return True
            else:
                return False
        else:
            return False

