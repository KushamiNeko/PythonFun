import tkinter as tk

RISK_LIMIT = 5.0
SEPARATOR = "======================="


def main():

    window = tk.Tk()
    window.title("Trading Calculator")
    window.resizable(False, False)
    # window.geometry("300x300")

    # root = tk.Frame(window)
    # root.pack(fill=tk.BOTH, expand=tk.YES)
    # root.grid_columnconfigure(0, weight=1)
    # root.grid_columnconfigure(1, weight=1)

    price = tk.Label(window, text="Price:")
    price.grid(row=0, column=0, sticky=tk.W)

    price_entry = tk.Entry(window, width=20)
    price_entry.grid(row=0, column=1)

    stop = tk.Label(window, text="Stop:")
    stop.grid(row=1, column=0, sticky=tk.W)

    stop_entry = tk.Entry(window, width=20)
    stop_entry.grid(row=1, column=1)

    account = tk.Label(window, text="Account:")
    account.grid(row=2, column=0, sticky=tk.W)

    account_entry = tk.Entry(window, width=20)
    account_entry.grid(row=2, column=1)

    stop_percent_var = tk.StringVar()
    stop_percent = tk.Label(window, textvariable=stop_percent_var)
    stop_percent.grid(row=3, column=0, columnspan=2, sticky=tk.W)

    # stop_percent_var.set("Stop(%):")

    separator = tk.Label(window, text=SEPARATOR)
    separator.grid(row=4, column=0, columnspan=2)

    risk_limit_p = tk.Label(window, text=f"Risk Limit (%): {RISK_LIMIT}")
    risk_limit_p.grid(row=5, column=0, columnspan=2, sticky=tk.W)

    risk_limit_d_var = tk.StringVar()

    risk_limit_d = tk.Label(window, textvariable=risk_limit_d_var)
    risk_limit_d.grid(row=6, column=0, columnspan=2, sticky=tk.W)

    # risk_limit_d_var.set("Total Risk Limit (¥):")

    separator = tk.Label(window, text=SEPARATOR)
    separator.grid(row=7, column=0, columnspan=2)

    trading_size_var = tk.StringVar()
    trading_size = tk.Label(window, textvariable=trading_size_var)
    trading_size.grid(row=8, column=0, columnspan=2, sticky=tk.W)

    # trading_size_var.set("Trading Size (¥): < ")

    trading_unit_var = tk.StringVar()
    trading_unit = tk.Label(window, textvariable=trading_unit_var)
    trading_unit.grid(row=9, column=0, columnspan=2, sticky=tk.W)

    # trading_unit_var.set("Trading Size (株): < ")

    def entry_check(event, label, entry, error_color="red"):
        index = entry.index(tk.INSERT)
        value = entry.get()

        s = value.strip().replace(",", "", -1)

        if s == "":
            label.config(bg=window.cget("background"))
            return None
        else:
            if not s.isdigit():
                label.config(bg=error_color)
                return True
            else:
                label.config(bg=window.cget("background"))

        s = f"{int(s):,}"

        entry.delete(0, tk.END)
        entry.insert(0, s)

        if len(value) < len(s):
            index += 1
        elif len(value) > len(s):
            index -= 1

        entry.icursor(index)

        return False

    def entry_handler(event):
        price_error = entry_check(event, price, price_entry)
        if price_error is None or price_error is True:
            return

        stop_error = entry_check(event, stop, stop_entry)
        if stop_error is None or stop_error is True:
            return

        p = float(price_entry.get().strip().replace(",", "", -1))
        s = float(stop_entry.get().strip().replace(",", "", -1))

        percent = ((s - p) / p) * 100.0
        stop_percent_var.set(f"Stop (%): {percent:,.2f}")

        account_error = entry_check(event, account, account_entry)
        if account_error is None or account_error is True:
            return

        size_p = abs(RISK_LIMIT / percent)

        a = float(account_entry.get().strip().replace(",", "", -1))

        size = min(a * size_p, a)

        unit = size / p

        risk_limit_d_var.set(f"Risk Limit (¥): {a * (RISK_LIMIT / 100.0):,.2f}")

        trading_size_var.set(f"Trading Size (¥): < {size:,.2f}")
        trading_unit_var.set(f"Trading Size (株): < {unit:,.6f}")

    price_entry.bind("<KeyRelease>", lambda event: entry_handler(event))
    stop_entry.bind("<KeyRelease>", lambda event: entry_handler(event))
    account_entry.bind("<KeyRelease>", lambda event: entry_handler(event))

    window.mainloop()


if __name__ == "__main__":
    main()
