from typing import List
import os.path as path

class Cart:
    def __init__(self, multiplier):
        self.items = []
        self.multiplier = multiplier
    def add_to_cart(self,item):
        self.items.append(item)
    def remove_item(self,index):
        self.items.remove(self.items[index])
    def total(self):
        return self.calculate_total()
    def calculate_total(self):
        total = 0.0
        for item in self.items:
            total = total + float(item.price)
        return total
    def get_items(self):
        return self.items
    def clear_cart(self):
        self.items.clear()
    def total_in_marks(self):
        return self.total() * self.multiplier
    def show_cart_str(self):
        final_str = f"{'':=^30}"+"\n" + f"{' Cart ':=^30}\n"
        i = 0
        for item in self.items:
            formatted_price = f"{float(item.price):.2f}"
            final_str = final_str + f"{i+1} - {item.name:.<30}..{formatted_price:.>8}\n"
            i = i + 1
        formatted_total = f"{self.total():.2f}"
        formatted_marks = f"{self.total_in_marks():.2f}"
        final_str = final_str + f"{'':=^30}\n" + f"{'Total (D)': <10}" + f"{formatted_total: >9}" + f"\n{'Total (M):': <10}" + f"{formatted_marks: >9}" + f"\n{'':=^30}" + "\n"
        return final_str
    def csv_string(self):
        serialized = self.multiplier.to_string() + "\n"
        for item in self.items:
            serialized = serialized + item.csv_string()
        return serialized

class Item:
    def __init__(self,section,aisle,name,price):
        self.section = section
        self.aisle = aisle
        self.name = name
        self.price = price
    def string_to_item(str):
        split = str.split()
        return Item(split[0],split[1],split[2],split[3])
    def to_string(self):
        price_str = ''
        try:
            price_str = f"{float(self.price):.2f}"
        except:
            price_str = self.price
        string = f"{self.section: <16}" + f"{self.aisle: <20}" + f"{self.name: <35}" + f"{price_str: >8}"
        return string
    def csv_string(self):
        return f"{self.section},{self.aisle},{self.name},{self.price}\n"

class ItemsDB:
    def __init__(self, filepath):
        self.items = FileIO.csv_items_to_list(filepath)
        self.sections = ItemsDB.get_sections(self.items)
        self.ailes = ItemsDB.get_aisles(self.items)
    
    def filter_section(self,section):
        return self.filter_section(self.items,section)
    def filter_section(items,section):
        filtered = [item for item in items if item.section.lower().find(section.strip().lower()) != -1]
        return filtered
    
    def filter_aisle(self,aisle):
        return self.filter_aisle(self.items,aisle)
    def filter_aisle(items,aisle):
        filtered = [item for item in items if item.aisle.lower().find(aisle.strip().lower()) != -1]
        return filtered
    
    def filter_name(self,item_name):
        return self.filter_name(self.items, item_name)
    def filter_name(items,item_name):
        filtered = [item for item in items if item.name.lower().find(item_name.strip().lower()) != -1]
        return filtered

    def filter_price_range(self,low,high):
        if low == 0 and high == 0:
            # both nonexistent
            return self.items
        elif low == 0 and high != 0:
            # high only
            filtered = [item for item in self.items if float(item.price) < float(high) ]
            return filtered
        elif high == 0 and low != 0:
            # low only
            filtered = [item for item in self.items if float(item.price) > float(low) ]
            return filtered
        else:
            filtered = [item for item in self.items if (float(item.price) > float(low) and float(item.price) < float(high)) ]
            return filtered
    def filter_price_range(items,low,high):
        if low == 0 and high == 0:
            # both nonexistent
            return items
        elif low == 0 and high != 0:
            # high only
            filtered = [item for item in items if float(item.price) < float(high) ]
            return filtered
        elif high == 0 and low != 0:
            # low only
            filtered = [item for item in items if float(item.price) > float(low) ]
            return filtered
        else:
            filtered = [item for item in items if (float(item.price) > float(low) and float(item.price) < float(high)) ]
            return filtered

    def get_sections(items):
        sections = []
        for item in items:
            if item.section not in sections:
                sections.append(item.section)
        return sections
    def get_aisles(items):
        aisles = []
        for item in items:
            if item.aisle not in aisles:
                aisles.append(item.aisle)
        return aisles
    
    def add(self,item):
        self.items.append(item)

    def to_string(self):
        string = ''
        for item in self.items:
            string = string + item.to_string()
        
        return string

class FileIO:
    def csv_items_to_list(filepath):
        db = []
        file = open(filepath,'r')
        line = file.readline()
        while(line != ''):
            split = line.split(',')
            clean_price = split[3].strip()
            db.append(Item(split[0],split[1],split[2],clean_price))
            line = file.readline()
        file.close()
        return db

    def get_profile(filepath):
        file = open(filepath,'r')
        line = file.readline()
        file.close()
        return line.split(',')
    
    def save_to_txt(string,filepath):
        file = open(filepath, 'w')
        file.write(string)
        file.close()
    def cart_to_txt(cart, filepath):
        file = open(filepath, 'w')
        file.write(cart.csv_string())
        file.close()

class ShopperProfile:
    def __init__(self, name, curr_balance):
        self.name = name
        self.balance = curr_balance
    
    def update_balance(self, new_balance):
        self.balance = new_balance

    def build_from_str(line):
        split_line = line.split(',')
        profile = ShopperProfile(split_line[0], split_line[1])
        return profile
    
    def build_from_txt(filename):
        file = open(filename, 'r')
        line = str(file.readline())
        file.close()
        if line == '': return ShopperProfile.build_from_input()
        profile = ShopperProfile.build_from_str(line)
        return profile
    
    def build_from_input():
        name = input("Enter name: ")
        bal = input("Enter current balance: ")
        profile = ShopperProfile(name, bal)
        return profile
    
    def save_to_txt(profile):
        file = open("profile.txt", 'w')
        file.write(str(profile.name) + ',' + str(profile.balance))
        file.close()

class ConsoleInterface:
    main_menu = {
        "i": "Show (i)tems",
        "s": "(S)earch",
        "r": "(R)eset filters",
        "c": "(C)art",
        "q": "(Q)uit !! LOSE ALL PROGRESS !!"
    }
    cart_menu = {
        "a": "(A)dd item to cart",
        "v": "(V)iew cart",
        "r": "(R)emove item from cart",
        "c": "(C)lear cart",
        "p": "(P)urchase items",
        "b": "(B)ack"
    }
    search_menu = {
        "i": "Show (i)tems",
        "s": "by (s)ection",
        "a": "by (a)isle",
        "n": "by (n)ame",
        "p": "by (p)rice",
        "b": "(b)ack"
    }
    
    def __init__(self,db,cart,profile):
        self.db = db
        self.curr_list = db.items
        self.cart = cart
        self.profile = profile
    
    # --- Cart --- #
    def cart_interface(self):
        self.show_cart_options()
        usr_input = input("Select an option: ")
        usr_input = usr_input.lower()
        while (usr_input != "b"):
            self.cart_handler(usr_input)
            self.show_cart_options()
            usr_input = input("Select an option: ")
            usr_input = usr_input.lower()
    def show_cart_options(self):
        print(f"{'':-^30}")
        print(f"{' Cart Options ':-^30}\n")
        for key in self.cart_menu.keys():
            print(f"{key}: {self.cart_menu[key]}\n")
        print(f"{'':-^30}\n")
        print("\n")
    def cart_handler(self,usr_input):
        usr_input = usr_input.lower()
        match usr_input:
            case "a":
                self.add_to_cart()
            case "v":
                self.show_cart()
            case "r":
                self.remove_from_cart()
            case "c":
                self.clear_cart()
            case "p":
                self.purchase()
            case _:
                print("Invalid input. Try again.\n")
    def clear_cart(self):
        self.cart.clear_cart()
    def add_to_cart(self):
        self.display_items_indexed()
        length = len(self.curr_list)
        usr_input = input("Which item do you want? Type its number: ")
        try:
            usr_input = int(usr_input)
        except:
            print("Invalid input. Must be a non-negative number. Try again.\n")
            return
        if(usr_input > length):
            print("Number is too high. Try Again.\n")
            return
        elif(usr_input < 1):
            print("Number is too low. Try again.\n")
            return
        item_added = self.curr_list[usr_input - 1]
        self.cart.add_to_cart(item_added)
        formatted_item_price = f"{float(item_added.price):.2f}"
        print(f"Item added: {item_added.name: <30} {formatted_item_price: >8}\n")
    def show_cart(self):
        print(self.cart.show_cart_str())
    def remove_from_cart(self):
        self.show_cart()
        cart_items = self.cart.get_items()
        length = len(cart_items)
        usr_input = input("Which item do you want to remove? Type its number: ")
        try:
            usr_input = int(usr_input)
        except:
            print("Invalid input. Must be a non-negative number. Try again.\n")
            return
        if(usr_input > length):
            print("Number is too high. Try Again.\n")
            return
        elif(usr_input < 1):
            print("Number is too low. Try again.\n")
            return
        index = int(usr_input) - 1
        item_removed = cart_items[index]
        self.cart.remove_item(index)
        print(f"Item removed: {item_removed.name}\n")
    def purchase(self):
        purchase_ui = PurchaseInterface(self.profile,self.cart)
        purchase_ui.purchase_ui()

    # --- Search --- #
    def search(self):
        self.show_search_menu()
        usr_input = input("Select an option: ")
        usr_input = usr_input.lower()
        while (usr_input != "b"):
            self.search_handler(usr_input)
            self.show_search_menu()
            usr_input = input("Select an option: ")
            usr_input = usr_input.lower()   
    def show_search_menu(self):
        print(f"{'':-^30}")
        print(f"{' Search Options ':-^30}\n")
        for key in self.search_menu.keys():
            print(f"{key}: {self.search_menu[key]}\n")
        print(f"{'':-^30}\n")
        print("\n")
    def search_handler(self,usr_input):
        usr_input = usr_input.lower()
        match usr_input:
            case "i":
                self.display_items()
            case "s":
                self.section_search()
            case "a":
                self.aisle_search()
            case "n":
                self.name_search()
            case "p":
                self.price_search()
            case _:
                print("Invalid input. Try again.\n")
    def section_search(self):
        print("\n")
        usr_input = input("Type any term in the Section titles ('o' for options): ")
        usr_input = usr_input.lower()
        while(usr_input == "o"):
            self.print_section_options()
            usr_input = input("Type any term in the Section titles ('o' for options): ")
        self.curr_list = ItemsDB.filter_section(self.curr_list,usr_input)
        print(f"{'NEW LIST':-^30}")
        self.display_items() 
    def print_section_options(self):
        print("\n")
        for section in self.sections:
            print(f"- {section}\n")
        print("\n") 
    def aisle_search(self):
        print("\n")
        usr_input = input("Type any term in the Aisle titles ('o' for options): ")
        usr_input = usr_input.lower()
        while(usr_input == "o"):
            self.print_section_options()
            usr_input = input("Type any term in the Aisle titles ('o' for options): ")
        self.curr_list = ItemsDB.filter_aisle(self.curr_list,usr_input)
        print(f"{'NEW LIST':-^30}")
        self.display_items()
    def print_aisle_options(self):
        print("\n")
        for aisle in self.aisle:
            print(f"- {aisle}\n")
        print("\n")
    def name_search(self):
        print("\n")
        usr_input = input("Type any term in the name of the item: ")
        usr_input = usr_input.lower()
        self.curr_list = ItemsDB.filter_name(self.curr_list,usr_input)
        print(f"{'NEW LIST':-^30}")
        self.display_items()
    def price_search(self):
        print("\n")
        try:
            low = float(input("Type any low end price (or 0 for none): "))
            high = float(input("Type any high end price (or 0 for none): "))
        except:
            print("Invalid input. It must be only a reasonable number, with a decimal if you want.\nTry again.")
            return
        self.curr_list = ItemsDB.filter_price_range(self.curr_list,low,high)
        print(f"{'NEW LIST':-^30}")
        self.display_items()

    # --- Menu --- #
    def menu(self):
        self.show_main_options()
        usr_input = input("Select an option: ")
        usr_input = usr_input.lower()
        while (usr_input != "q"):
            self.main_input_handler(usr_input)
            self.show_main_options()
            usr_input = input("Select an option: ")
            usr_input = usr_input.lower()          
    def show_main_options(self):
        print(f"{'':-^30}")
        print(f"{' Options ':-^30}\n")
        for key in self.main_menu.keys():
            print(f"{key}: {self.main_menu[key]}\n")
        print(f"{'':-^30}\n")
        print("\n")
    def main_input_handler(self,usr_input):
        usr_input = usr_input.lower()
        match usr_input:
            case "i":
                self.display_items()
            case "s":
                self.search()
            case "r":
                self.reset_filters()
            case "c":
                self.cart_interface()
            case _:
                print("Invalid input. Try again.")
    
    # --- Other --- # 
    def display_items_indexed(self):
        print("\n")
        print(f"{'':-^30}")
        i = 1
        for item in self.curr_list:
            print(f"{i}: {item.to_string()}")
            i = i + 1
        print(f"{'':-^30}")
        print("\n")
    def display_items(self):
        print("\n")
        print(f"{'':-^30}")
        for item in self.curr_list:
            print(f"{item.to_string()}\n")
        print(f"{'':-^30}")
        print("\n")
    def reset_filters(self):
        self.curr_list = self.db.items

class PurchaseInterface:
    def __init__(self, profile, cart):
        self.cart = cart
        self.profile = profile
    
    purchase_options = {
        "v": "(V)iew bill",
        "c": "(C)omplete purchase",
        "b": "(B)ack"    
    }
    
    def purchase_ui(self):
        self.show_purchase_options()
        usr_input = input("Select an option: ")
        usr_input = usr_input.lower()
        while (usr_input != "b"):
            self.handler(usr_input)
            self.show_purchase_options()
            usr_input = input("Select an option: ")
            usr_input = usr_input.lower()
    
    def handler(self,usr_input):
        usr_input = usr_input.lower()
        match usr_input:
            case "v":
                self.view_bill()
            case "c":
                self.complete()
            case _:
                print("Invalid input. Try again.")

    def show_purchase_options(self):
        print(f"{'':-^30}")
        print(f"{' Search Options ':-^30}\n")
        for key in self.purchase_options.keys():
            print(f"{key}: {self.purchase_options[key]}\n")
        print(f"{'':-^30}\n")
        print("\n")

    def view_bill(self):
        print(self.cart.show_cart_str())
        balance_formatted = f"{float(self.profile.balance):.2f}"
        print(f"Balance before: {balance_formatted: >10}")
        balance_after = f"{float(self.profile.balance) - float(self.cart.total_in_marks()):.2f}"
        print(f"Balance after:  {balance_after: >10}")

    def complete(self):
        balance = float(self.profile.balance)
        if self.cart.total_in_marks() < float(balance):
            formatted_balance = f"{balance: .2f}"
            balance_after = balance - self.cart.total_in_marks()
            formatted_balance_after = f"{balance_after: .2f}"
            reciept = self.cart.show_cart_str() + f"{'':=^30}\n" + f"{'Balance before (M)': <10}" + f"{formatted_balance: >9}" + f"\n{'Balance after:': <10}" + f"{formatted_balance_after: >9}\n"
            self.profile.balance = balance_after
            FileIO.save_to_txt(reciept, './saves/last_receipt.txt')
            print(reciept)
            self.cart.clear_cart()
            ShopperProfile.save_to_txt(self.profile)
            print("Purchase completed.")
        else:
            print("Insufficient funds. Could not complete purchase.")

def main():
    # --- Create Profile ---
    if path.exists('./saves/profile.txt'): 
        curr_usr = ShopperProfile.build_from_txt('./saves/profile.txt')
    else:
        curr_usr = ShopperProfile.build_from_input()

    # --- Create Dataframe ---
    db = ItemsDB('./saves/items_COC.csv')
    # --- Menu Loop ---
    cart = Cart(float(input("Ask the DM (What is today's inflation multiplier?): ")))
    console = ConsoleInterface(db,cart,curr_usr)
    console.menu()
    # save current profile before leaving with new balance

main()