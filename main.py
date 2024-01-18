from tkinter import Tk, ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
import requests
from requests.structures import CaseInsensitiveDict
import freecurrencyapi

url = "https://api.freecurrencyapi.com/v1/currencies"

headers = CaseInsensitiveDict()
headers["apikey"] = "fca_live_HVabMXj6fkPsm7MBBKr0z4nduj6JpKVGf71HdHR6"

try:
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()  # Raise an HTTPError for bad responses
    json_data = resp.json()
except requests.RequestException as e:
    messagebox.showerror("Error", f"Failed to fetch currency data: {e}")
    exit()

try:
    client = freecurrencyapi.Client('fca_live_HVabMXj6fkPsm7MBBKr0z4nduj6JpKVGf71HdHR6')
    api_data = client.latest()
except freecurrencyapi.FreeCurrencyAPIException as e:
    messagebox.showerror("Error", f"Failed to fetch currency exchange rates: {e}")
    exit()

# Functions
def get_value_in_usd(required_currency):
    required_currency = str(required_currency).upper()
    return api_data["data"].get(required_currency, 0)

def get_currency_symbol(required_currency):
    required_currency = str(required_currency).upper()
    return json_data['data'].get(required_currency, {}).get('symbol', 'N/A')

def convert():
    currency_origin = combo1.get()
    currency_origin = get_value_in_usd(currency_origin)
    currency_convert = combo2.get()
    symbol = get_currency_symbol(currency_convert)
    currency_convert = get_value_in_usd(currency_convert)

    if currency_origin == 0 or currency_convert == 0:
        messagebox.showerror("Error", "Invalid currency selection.")
        return

    try:
        amount = float(value.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid number.")
        return

    final_value = (amount / currency_origin) * currency_convert
    final_value = round(final_value, 2)

    result.config(text=f"{symbol} {final_value}")
    print(final_value)

currency = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HRK", 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR']
currency_values = {}

cor0 = '#FFFFFF'  # white
cor1 = '#333333'  # black
cor2 = '#B284BE'  # pink

window = Tk()
window.geometry('300x320')
window.title('Converter')
window.configure(bg=cor0)
window.resizable(height=FALSE, width=FALSE)

# frames
top = Frame(window, width=300, height=60, bg=cor2)
top.grid(row=0, column=0)

main = Frame(window, width=300, height=260, bg=cor0)
main.grid(row=1, column=0)

# top frame
icon = Image.open('images/icon8.png')
icon = icon.resize((40, 40))
icon = ImageTk.PhotoImage(icon)
app_name = Label(top, image=icon, compound=LEFT, text='Currency Converter', height=5, padx=13, pady=30,
                 anchor=CENTER, font=('Arial 16 bold'), bg=cor2, fg=cor0)
app_name.place(x=0, y=0)

# main frame
result = Label(main, text='', width=16, height=2, pady=7, relief='solid', anchor=CENTER,
               font=('Ivy 15 bold'), bg=cor0, fg=cor1)
result.place(x=60, y=10)

from_label = Label(main, text='From', width=8, height=1, pady=0, padx=0, relief='flat', anchor=NW,
                   font=('Ivy 10 bold'), bg=cor0, fg=cor1)
from_label.place(x=48, y=90)
combo1 = ttk.Combobox(main, width=8, justify=CENTER, font=('Ivy 12 bold'))
combo1['values'] = currency
combo1.place(x=50, y=115)

to_label = Label(main, text='To', width=8, height=1, pady=0, padx=0, relief='flat', anchor=NW,
                 font=('Ivy 10 bold'), bg=cor0, fg=cor1)
to_label.place(x=158, y=90)
combo2 = ttk.Combobox(main, width=8, justify=CENTER, font=('Ivy 12 bold'))
combo2['values'] = currency
combo2.place(x=160, y=115)

value = Entry(main, width=22, justify=CENTER, font=('Ivy 12 bold'), relief=SOLID)
value.place(x=50, y=155)
amount = value.get()

button = Button(main, text='Convert', width=19, padx=5, height=1, bg=cor2, fg=cor0,
                font=('Ivy 12 bold'), command=convert)
button.place(x=50, y=210)

window.mainloop()
