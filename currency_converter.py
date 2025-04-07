import requests # type: ignore
from PIL import Image, ImageTk # type: ignore
from tkinter import *
from tkinter import ttk
import re

def real_time_currency_converter(url):
    data = requests.get(url).json()
    currencies = data['rates']

    def convert(from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / currencies[from_currency]
        amount = round(amount * currencies[to_currency], 4)
        return amount

    return convert, currencies, data

def perform_conversion():
    try:
        amount = float(amount_field.get())
        from_curr = from_currency_variable.get()
        to_curr = to_currency_variable.get()
        converted_amount = convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 3)
        converted_amount_field_label.config(text=str(converted_amount))
    except Exception as e:
        converted_amount_field_label.config(text="Error")

def restrict_number_only(P):
    regex = re.compile(r"^\d*\.?\d*$")
    return regex.match(P) is not None

url = 'https://api.exchangerate-api.com/v4/latest/USD'
convert, currencies, data = real_time_currency_converter(url)

root = Tk()
root.title('Currency Converter')
root.geometry('1366x768')
root.config(background='skyblue')

intro_label = Label(root, text='Welcome to Real Time Currency Converter', bg='white', fg='red', relief=RAISED, borderwidth=3)
intro_label.config(font=('Arial', 25, 'bold'))
intro_label.place(x=350, y=100)

from_currency_variable = StringVar(root)
to_currency_variable = StringVar(root)
font = ('Courier', 12, 'bold')
ttk.Style().configure('TCombobox', padding=6)

from_currency_dropdown = ttk.Combobox(root, textvariable=from_currency_variable, values=list(currencies.keys()),
                                      font='Ivy 10 bold', state='readonly', width=17, justify=CENTER)
from_currency_dropdown.place(x=350, y=250)
from_currency_dropdown.set("USD")

to_currency_dropdown = ttk.Combobox(root, textvariable=to_currency_variable, values=list(currencies.keys()),
                                    font='Ivy 10 bold', state='readonly', width=17, justify=CENTER)
to_currency_dropdown.place(x=870, y=250)
to_currency_dropdown.set("INR")

vcmd = (root.register(restrict_number_only), '%P')
amount_field = Entry(root, bd=3, relief=SOLID, font='Ivy 20 bold', justify=CENTER, width=12, validate='key', validatecommand=vcmd)
amount_field.place(x=350, y=350)

converted_amount_field_label = Label(root, text='', fg='black', bg='white', relief=SOLID, font='Ivy 20 bold', justify=CENTER, width=11,
                                     borderwidth=3)
converted_amount_field_label.place(x=835, y=350)

convert_button = Button(root, text='Convert', bg='white', fg='blue', command=perform_conversion)
convert_button.config(font=('Ivy', 20, 'bold'))
convert_button.place(x=635, y=500)

root.mainloop()
