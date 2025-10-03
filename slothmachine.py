import random

# ---- Game Settings ----
MAX_LINES = 3      # Maximum number of lines a user can bet on
MAX_BET = 100      # Maximum bet per line
MIN_BET = 1        # Minimum bet per line

ROWS = 3           # Number of rows in slot machine
COLS = 3           # Number of columns in slot machine

# Number of occurrences for each symbol in the slot machine
symbol_count = {
    "A": 2,   # Symbol A appears 2 times
    "B": 4,   # Symbol B appears 4 times
    "C": 6,   # Symbol C appears 6 times
    "D": 8    # Symbol D appears 8 times
}

# Value (multiplier) of each symbol when forming a winning line
symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


# ---- Helper Functions ----

def check_winnings(columns, lines, bet, values):
    """
    Check if the player has won on any lines.
    - columns: slot machine spin result
    - lines: number of lines the player bet on
    - bet: bet amount per line
    - values: dictionary mapping symbol to payout multiplier
    Returns total winnings and the list of winning lines.
    """
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]  # Take the first symbol of the current line
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:  # If symbols don’t match, break
                break
        else:
            # If loop didn't break, all symbols in this line match
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)  # Store line number (1-based)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    """
    Generate a random spin for the slot machine.
    - rows: number of rows
    - cols: number of columns
    - symbols: dictionary of symbols and their counts
    Returns a 2D list representing the slot machine spin result.
    """
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    current_symbols = all_symbols[:]  # Copy of symbol pool
    for _ in range(cols):
        column = []
        for _ in range(rows):
            value = random.choice(current_symbols)  # Pick random symbol
            current_symbols.remove(value)  # Remove so it isn’t reused immediately
            column.append(value)
        columns.append(column)
    
    return columns


def print_slot_machine(columns):
    """
    Nicely print the slot machine result in row-wise format.
    """
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row])
        print()  # New line after each row


def deposit():
    """
    Ask the player how much money to deposit.
    Ensures input is a valid positive number.
    """
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount


def get_number_of_lines():
    """
    Ask the player how many lines they want to bet on.
    Ensures it’s within the allowed range.
    """
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines


def get_bet():
    """
    Ask the player how much they want to bet per line.
    Ensures it’s within min and max bet range.
    """
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a number.")
    return amount


def spin(balance):
    """
    Perform a slot machine spin:
    - Ask player for number of lines and bet
    - Check if they have enough balance
    - Spin the slot machine and check winnings
    Returns net winnings (winnings - total_bet).
    """
    lines = get_number_of_lines()
    
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"You do not have enough to bet that amount. Your current balance is ${balance}.")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet: ${total_bet}")
    
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    
    winnings, winnings_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print("Winning lines:", *winnings_lines)
    
    return winnings - total_bet


# ---- Main Game Loop ----

def main():
    """
    Main function to run the slot machine game.
    - Ask for deposit
    - Loop until user quits
    - Show balance updates after each spin
    """
    balance = deposit()
    while True:
        print(f"Your current balance is ${balance}")
        answer = input("Press enter to spin (q to quit): ")
        if answer == 'q':
            break
        balance += spin(balance)

    print(f"You left with ${balance}")


# Run the game
main()
