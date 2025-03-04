import pandas
from tabulate import tabulate
# this one makes a decorated statements
def make_statement(statement, decoration, lines=1):
    """This one makes a decorated statement, defaults to a single line
    :parameter statement, decoration, lines(optional)
    :return nothing!
    """
    res=""
    lines = int(lines)
    for i in range(0, lines):
        if i == int(lines / 2):
            res=res+f"{decoration * 3} {statement} {decoration * 3}\n"
        else:
            res+=decoration * (len(statement) + 8) +"\n"
    return res
def instruction():
    make_statement("Instruction","ℹ️")
    print("""
    
For each ticket holder enter ...
- Their name
- Their age
- The payment method (cash / credit)

THe program will record the ticket sale and calculate the ticket cost (and the profit).

Once you have either sold all of the tickets or entered the exit code ('xxx'), the program will display the ticket
sales information and write the data to a text file.

It will also choose one lucky ticket holder who wins the draw (their ticket is free).

    """)

def not_blank(question):
    """ check if the input is blank to make sure the return of this function is not blank"""
    print(question,end="")
    while True:
        response = input()
        if response == "":
            print("Sorry, this can't be blank...")
            continue
        return response


def yes_no(question):
    while True:
        response = input(question).lower()
        if response == "yes" or response == "y":
            return True
        if response == "no" or response == "n":
            return False
        print("""Please enter either "yes"(y) or "no"(n) """)


def string_checker(question, valid_ans_list=("yes", "no"), num_letters=1):
    """ This function check what user wants from the list showed by checking if they input the specific amount of letter(s) or full letter(s) of a valid option on the list"""
    while True:
        response = input(question).lower()
        for item in valid_ans_list:
            if response == item or response == item[:num_letters]:  # i[:j] means taking the element from first index 0 to before index j.
                return item
        print(f"Please choose a valid answer from {valid_ans_list}")


def num_check(question, num_type, exitcode):
    """ This function checking and make sure that it returns a valid integer or float"""
    print(question,end="")
    if num_type == "integer" or num_type == "int":
        num_type = int
        value_error_announcement = "please enter an integer (ie: a number which does not have a decimal part)."
        lesser_announcement = "please enter an integer that is more than 0"
    else:
        num_type = float
        value_error_announcement = "please enter a number"
        lesser_announcement = "please enter a number that is more than 0"

    while True:
        try:
            response = input()
            if response=="":
                return ""
            response=num_type(response)
            if response <= 0:
                print(lesser_announcement)
                continue
            if exitcode:
                return response
            return
        except ValueError:
            print(value_error_announcement)


# def int_check(question,name):
#     """ This function check if their age are available to buy a ticket and output their name with the result, ie: "A is too young"""
#     print(question,end="")
#     while True:
#         try:
#             response = int(input())
#             if response < 12:
#                 print(f"Sorry you are too young for this movie")
#                 return False
#             elif response > 120:
#                 print(f"?? That looks like a typo (too old)")
#                 return False
#             elif response >=12 and response<16:
#                 # First return element is for the if condition in main to see if the program should continue because users age is in valid boundary
#                 # Second element return the index/position of their ticket type in the list in main: 0 for children, 1 for adult, 2 for senior
#                 return True , 0
#             elif response >=16 and response<65:
#                 return True, 1
#             elif response >=65 and response<121:
#                 return True, 2
#         except ValueError:
#             print("<Please enter an integer>")

def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)

def get_expenses(exp_type,default_item_quanity=1):
    """:return the frame for pandas""" 
    all_item_name=[]
    all_item_quanity=[]
    all_item_cost=[]

    # expenses dict
    data_dict={
        "Item":all_item_name,
        "Amount":all_item_quanity,
        "$ / Item":all_item_cost
    }
    while True:
        response=not_blank("Item name: ")
        if response!="xxx":
            # name of item
            all_item_name.append(response)
            item_quanity=num_check("How many: ", "int", True)
            # numer of item
            if item_quanity=="":
                item_quanity=default_item_quanity
            all_item_quanity.append(item_quanity)
            # cost of item
            item_cost=num_check("Price for one: ","float",True)
            all_item_cost.append(item_cost)
            continue
        if len(all_item_name)== 0 and exp_type=="variable":
            print(f"Oops - you have not entered anything.\nYou need at least one item.")
            continue
        break

    # make pandas
    expense_frame = pandas.DataFrame(data_dict)
    # calculate subtotal
    subtotal = expense_frame['Cost'].sum()
    return expense_frame, subtotal
#main is here
# product_name = not_blank("Product name: ")
quanity_made = num_check("Quantity being made: ", "interger", True)
variable_expense=get_expenses("variable",quanity_made)

print()

print("Getting Variable Costs...")
variable_pandas=variable_expense[0]
variable_subtotal=variable_expense[1]

print("Getting Fixed Costs...")
fixed_expense = get_expenses("fixed")
print()
fixed_pandas = fixed_expense[0]
fixed_subtotal=fixed_expense[1]


# Temporary output area fo easy testing

print("=== Variable Expenses ==")
print(variable_pandas)
print(f"Fixed Subtotal: ${fixed_subtotal:.2f}")

print()
total_expenses = variable_subtotal + fixed_subtotal
print(f"Total Expenses: ${total_expenses:.2f}")
