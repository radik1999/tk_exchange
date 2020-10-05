from tkinter import *
import ccy
from tools import *
from exchange import Exchange

root = root_in_center(450, 350)
exchange = Exchange()


search_string = [f'{country}({country_code}): {ccy.countryccy(country_code)}'  # список країн, кодів країн,
                 for country_code, country in ccy.countries().items()          # та їхніх кодів валют
                 if ccy.countryccy(country_code)]                              # по яким буде здійснюватись
                                                                               # пошук


se = SearchEntry(root, search_string, width=30, font=('Times', 14, 'normal'))
se.focus_set()

rate_board = Frame(root)

scroll_bar = Scrollbar(rate_board)

currency_lst = Listbox(rate_board, width=30, height=14, yscrollcommand=scroll_bar.set)

scroll_bar.configure(command=currency_lst.yview)

currency_lst.insert(END, 'Currency' + ' '*33 + 'Cost')
currency_lst.insert(END, '-'*50)

confirm = Button(root, text='Find', width=10)


def get_currency(event=None):
    currency_lst.delete(2, END)  # clear rate board
    country_code = se.get()[-3:]  # getting country code, 3 last symbols of entry
    prior_rates = {'USD': None, 'EUR': None, 'RUB': None, 'UAH': None}
    try:
        rates = exchange.get_all_rate_by_country_code(country_code)
    except TypeError:
        currency_lst.insert(2, 'There isn\'t such currency')
    else:
        for code in prior_rates:
            prior_rates[code] = rates.pop(code)
        sorted_rates = list(rates)
        sorted_rates.sort()
        sorted_rates.reverse()
        for code in sorted_rates:
            output = f'{code}{rates[code]:^80}'
            currency_lst.insert(2, output)
            currency_lst.insert(3, '-'*50)
        for code in prior_rates:
            output = f'{code}{prior_rates[code]:^80}'
            currency_lst.insert(2, output)
            currency_lst.insert(3, '-'*50)


se.bind('<Return>', get_currency)
confirm.configure(command=get_currency)

confirm.grid(row=0, column=1, sticky=W)

currency_lst.pack(side=LEFT)
scroll_bar.pack(side=RIGHT, fill=Y)
rate_board.grid(row=1, column=0, columnspan=2)

se.grid(row=0, column=0, sticky=E, padx=30, pady=20)

root.mainloop()
