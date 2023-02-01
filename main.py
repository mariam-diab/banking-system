from customer_management import *
def menu():
    while True:
        choice = input("Please enter 'i' to sign on, 'o' to open account, 'q' to quit: ").lower()
        if choice == 'i':
            choice = Customer_Management()
            choice.sign_on()
        elif choice == 'o':
            choice = Customer_Management()
            choice.open_account()
        elif choice == 'q':
            print("Thank you for choosing the SNB, see you soon!")
            break
        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":
    menu()