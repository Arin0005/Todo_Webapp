import re

print("\nCalculator")
print("To Exit type 'Quit' \n")

prev_equation = 0 # will hold the result of previous equation
run = True

def start_calculation():
    global run # here the global run value is considered
    global prev_equation

    if prev_equation == 0:
        # if there is no calculation done then it  takes new input
        equation = input("Enter the Equation :")
    else:
        # if there is a calculation done in the past then it holds that value
        equation = input(str(prev_equation))


    if equation == 'Quit':
        print("Closing Calculator")
        run = False #here run is local variable and to quit the process it need to be global and run variable is overwritten

    else:
        equation = re.sub('[a-zA-Z,.:()""]','',equation)

        if prev_equation == 0:
            print("Current Equation is :",equation)
            prev_equation = eval(equation)
        else:
            print("Answer to previous equation was :",prev_equation)
            prev_equation = eval(str(prev_equation) + equation)



while run:
    start_calculation()
