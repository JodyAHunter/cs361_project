import requests

# https://app.exchangerate-api.com/ API used to request currency conversion rates and symbols

latest_update = "New feature: You can now enter 'help' to see all of the currency symbols available in this\n" \
                "program. If you use this feature when prompted for a currency symbol,\n" \
                "then you will have to start over at the beginning.\n"

codes_url = f"https://v6.exchangerate-api.com/v6/d6ad9855ac095fdd8f431e69/codes"
codes_response = requests.get(codes_url)
codes_data = codes_response.json()
symbols = codes_data['supported_codes']


def convert_currency(converted_from, converted_to, amount):
    converted_to_currency = None
    converted_from_currency = None

    for symbol in symbols:
        if symbol[0] == converted_from:
            converted_from_currency = symbol[1]
        elif symbol[0] == converted_to:
            converted_to_currency = symbol[1]
        if converted_to_currency is not None and converted_from_currency is not None:
            break

    if converted_from_currency is None or converted_to_currency is None:
        print("Two valid currency symbols were not received. Please try again.\n"
              "You may also enter 'help' to see the available currency symbols\n")
        return

    rates_url = f"https://v6.exchangerate-api.com/v6/d6ad9855ac095fdd8f431e69/latest/{converted_from}"
    rates_response = requests.get(rates_url)
    rates_data = rates_response.json()
    rates = rates_data["conversion_rates"]

    print(f"\nConverting {amount} in {converted_from_currency} to {converted_to_currency}...")
    converted_currency = float(amount) * rates[converted_to]
    print(f"You have {converted_currency:0,.2f} in {converted_to_currency}!\n")


def exit_program():
    print("---------------------------------------\n"
          "Thank you for using my conversion tool!\n"
          "---------------------------------------\n")
    exit(0)


def display_currencies():
    print("You can find all of the available currencies and their symbols below!\n\n"
          "SYMBOL, CURRENCY\n"
          "-----------------")

    for symbol in symbols:
        print(f"{symbol[0]}, {symbol[1]}")
    print("\n")


def check_input(user_response):
    if user_response == 'quit':
        exit_program()
    elif user_response == 'help':
        display_currencies()
    elif user_response == '1' or user_response == 'currency':
        from_input = input("Please enter the symbol for the currency you want to convert from (eg. 'USD'): ")
        check_input(from_input)
        to_input = input("Please enter the symbol for the currency you want to convert to (eg. 'EUR'): ")
        check_input(to_input)
        amount_input = input("Please enter the amount of currency you want to convert from (eg. '100.00'): ")
        check_input(amount_input)
        convert_currency(from_input, to_input, amount_input)


if __name__ == "__main__":

    print("-----------------------------------------\n"
          "WELCOME TO MY CURRENCY CONVERSION PROJECT\n"
          "-----------------------------------------")

    print("********************************************************************************************\n"
          f"{latest_update}"
          "********************************************************************************************\n")

    while True:
        user_input = input("Please enter '1' or 'currency' to convert one form of currency to another.\n"
                           "If you would like to exit the program at any time, please enter 'quit': ")

        check_input(user_input)
