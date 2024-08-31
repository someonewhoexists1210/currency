import time
import os
import json
import requests
from dotenv import load_dotenv
from rich.console import Console

console = Console()

load_dotenv()
API_KEY = os.getenv('API_KEY')
CACHE_FILE = 'currency_cache.json'
CACHE_EXPIRATION = 3600 * 24

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file)

cache = load_cache()

def make_request(url):
    response = requests.get(url)
    return response.json()

def get_currency(curr):
    current_time = time.time()
    
    if curr in cache and (current_time - cache[curr]['timestamp']) < CACHE_EXPIRATION:
        console.print(f"Using cached rates for {curr}", style="bold yellow")
        return cache[curr]['rates']
    
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{curr}'
    data = make_request(url)
    
    cache[curr] = {
        'rates': data['conversion_rates'],
        'timestamp': current_time
    }
    
    save_cache(cache)
    
    return data['conversion_rates']

def convert_currency(amount, from_currency, to_currency):
    rates = get_currency(from_currency)
    return round(float(amount) * rates[to_currency], 2)

def main():
    base = input('Enter the base currency: ').upper()
    conversion = input('Select an option: \n1. Get conversion rate\n2. Convert amount\n')
    
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