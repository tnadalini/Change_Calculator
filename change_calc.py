from pickle import FALSE, TRUE
import PySimpleGUI as sg

# 'global' variables
arrBills = [100, 50, 20, 10, 5, 1]
arrCoins = [25, 10, 5, 1]


# set up the output window
layout = [[sg.Text("How much is due? ($)")],
            [sg.Input(key='input_1')],
            [sg.Text("How much is being paid? ($)")],
            [sg.Input(key='input_2')],
            [sg.Text(size=(40,7), key='-OUTPUT-')],
            [sg.Button("Calculate")], [sg.Button("Exit")]
        ]


# Create the window
window = sg.Window("Change_Calculator", layout)


# define functions

#function to calculate change needed
def calc_change():
    # check if inputs are valid
    check = check_inputs()
    if check == TRUE:
        # get float values from check_input
        due = check_input(values['input_1'])
        paid = check_input(values['input_2'])
        change = round((paid - due), 2)

        # if change is < 0, then throw error
        if change < 0:
            window['-OUTPUT-'].update("Not enough payment received!")
            return

        #split change into dollars & cents
        txt = str(change).split(".")

        # calculate coins needed
        coins = calc_coins(int(txt[1]))

        # calculate bills needed
        bills = calc_bills(int(txt[0]))


        # output results
        resultString = "Total Change Due: $" + str(change) + "\n100s:\t" + str(int(bills[0])) + "\t\t" + "Quarters:\t" + str(int(coins[0]))
        resultString += "\n50s:\t" + str(int(bills[1])) + "\t\t" + "Dimes:\t" + str(int(coins[1]))
        resultString += "\n20s:\t" + str(int(bills[2])) + "\t\t" + "Nickels:\t" + str(int(coins[2]))
        resultString += "\n10s:\t" + str(int(bills[3])) + "\t\t" + "Pennies:\t" + str(int(coins[3]))
        resultString += "\n5s:\t" + str(int(bills[4])) + "\n" + "1s:\t" + str(int(bills[5]))
        window['-OUTPUT-'].update(resultString)


# function to calculate coins needed
def calc_coins(val):
    # if there is no coin value, just return 0 coins
    coinResult = [0, 0, 0, 0]

    num = val

    if val == 0:
        return coinResult

    # loop to iterate through list(s) and calculate coins
    i = 0
    while i < len(coinResult):
        y = (num - (num % arrCoins[i])) / arrCoins[i]
        coinResult[i] = y
        num = num - (y * arrCoins[i])
        i += 1

    return coinResult


# function to calc bills needed
def calc_bills(val):
    # if there is no bill value, just return 0 bills
    billResult = [0, 0, 0, 0, 0, 0]

    num = val

    if val == 0:
        return billResult

    # loop to iterate through list(s) and calculate bill
    i = 0
    while i < len(billResult):
        y = (num - (num % arrBills[i])) / arrBills[i]
        billResult[i] = y
        num = num - (y * arrBills[i])
        i += 1

    return billResult


# function to check if inputs are valid numbers; gives warning message upon bad input
def check_inputs():
    # ensure inputs are valid
    checkInput1 = check_input(values['input_1'])
    checkInput2 = check_input(values['input_2'])

    # output errors if needed
    if checkInput1 == -1 and checkInput2 == -1:
        window['-OUTPUT-'].update("Invalid Inputs!\nPlease check both of your input values.")
        return FALSE
    elif checkInput1 == -1:
        window['-OUTPUT-'].update("Invalid Input!\nPlease check your amount due.")
        return FALSE
    elif checkInput2 == -1:
        window['-OUTPUT-'].update("Invalid Input!\nPlease check your amount paid.")
        return FALSE
    else:
        return TRUE


# function to check if given input is a valid int/float
def check_input(val):
    # if the input is an int, immediately return float value
    if val.isdigit():
        return float(val)
    else:
        # check if input can be converted to a float
        try:
            num = float(val)
            return round(num,2)
        # if not, return an error code value
        except ValueError:
            return -1


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    if event == "Calculate":
        calc_change()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()

