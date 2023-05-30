# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:36:24 2023

@author: yy
"""


from scipy.optimize import minimize
import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculations")
        self.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        self.temperature_label = ttk.Label(self, text="当前室温（摄氏度）:")
        self.temperature_entry = ttk.Entry(self)

        self.frequency_label = ttk.Label(self, text="想要发射混合的频率（Hz）:")
        self.frequency_entry = ttk.Entry(self)

        self.distance_label = ttk.Label(self, text="预设的l距离单位（m）:")
        self.distance_entry = ttk.Entry(self)

        self.angle_label = ttk.Label(self, text="希望寻找的角度单位（度）:")
        self.angle_entry = ttk.Entry(self)

        self.calculate_button = ttk.Button(self, text="Calculate", command=self.calculate)

        self.result_label = ttk.Label(self, text="Result:")
        self.result_text = tk.Text(self, height=5, width=25)
        
        # Grid layout
        self.temperature_label.grid(row=0, column=0, sticky="w")
        self.temperature_entry.grid(row=0, column=1)

        self.frequency_label.grid(row=1, column=0, sticky="w")
        self.frequency_entry.grid(row=1, column=1)

        self.distance_label.grid(row=2, column=0, sticky="w")
        self.distance_entry.grid(row=2, column=1)

        self.angle_label.grid(row=3, column=0, sticky="w")
        self.angle_entry.grid(row=3, column=1)

        self.calculate_button.grid(row=4, column=0, columnspan=2)

        self.result_label.grid(row=5, column=0, sticky="w")
        self.result_text.grid(row=6, column=0, columnspan=2)

    def calculate(self):
        try:
            T = float(self.temperature_entry.get())
            v = float(self.frequency_entry.get())
            l_guess = float(self.distance_entry.get())
            theta_guess = float(self.angle_entry.get())

            V=331.6+T*0.6

            def equations(vars):
                l, theta = vars
                m1 = 1
                m2 = 3
                eq1 = l*np.sin(theta/180*np.pi) - m1*V/2000/2
                eq2 = l*np.sin((60-theta)/180*np.pi) - m2*V/v/2
                return np.sqrt(eq1**2 + eq2**2)

            result = minimize(equations, (l_guess, theta_guess), bounds=((0, None), (0, 60)))
            l, theta = result.x

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"l: {l}\ntheta: {theta}")

        except ValueError:
            messagebox.showerror("Error", "请在所有字段中输入数字。")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()