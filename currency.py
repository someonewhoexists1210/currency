import requests, os
from dotenv import load_dotenv
from rich.console import Console

console = Console()

load_dotenv()
API_KEY = os.getenv('API_KEY')

def make_request(url):
    response = requests.get(url)
    return response.json()

def get_currency(curr):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{curr}'
    data = make_request(url)

    return data['conversion_rates']

def convert_currency(amount, from_currency, to_currency):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}'
    data = make_request(url)

    return data['conversion_result']

def main():
    base = input('Enter the base currency: ').upper()
    conversion = input('Select an option: \n1. Get conversion rate\n2. Convert amouht\n')
    if conversion == '1':
        rates = get_currency(base)
        count = 0
        for rate in rates:
            if count % 5 == 0:
                print()
            console.print(f'{rate}: {rates[rate]}', end='\t', style='bold blue')
            count += 1
    elif conversion == '2':
        amount = input('Enter the amount: ')
        to_currency = input('Enter the currency to convert to: ').upper()
        result = convert_currency(amount, base, to_currency)
        console.print(f'{amount} {base} is equal to {result} {to_currency}', style='bold green')
    else:
        console.print('Invalid option', style='bold red')

main()