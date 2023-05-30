import sys
from scipy.optimize import minimize
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox

class InputDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="当前室温（摄氏度）:").grid(row=0)
        tk.Label(master, text="想要发射混合的频率（Hz）:").grid(row=1)
        tk.Label(master, text="预设的l距离（单位（m））:").grid(row=2)
        tk.Label(master, text="希望寻找的角度（单位（度））:").grid(row=3)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)
        self.e4 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)

        return self.e1  # initial focus

    def apply(self):
        try:
            self.result = (float(self.e1.get()), float(self.e2.get()), float(self.e3.get()), float(self.e4.get()))
        except ValueError:
            messagebox.showerror("Error", "请在所有字段中输入数字。")
            self.result = None

    def cancel(self, event=None):
        # 重写这个方法以处理窗口的关闭事件
        self.master.destroy()
        sys.exit()  # 结束Python进程


def calculate():
    try:
        d = InputDialog(root)
    except SystemExit:  # 捕获系统退出事件
        return

    if d.result is not None:
        T, v, l_guess, theta_guess = d.result
        V=331.6+T*0.6

        def equations(vars):
            l, theta = vars
            m1 = 1
            m2 = 3
            eq1 = l*np.sin(np.radians(theta)) - m1*V/2000/2
            eq2 = l*np.sin(np.radians(60)-theta) - m2*V/v/2
            return np.sqrt(eq1**2 + eq2**2)

        result = minimize(equations, (l_guess, theta_guess), bounds=((0, None), (10, 50)))
        l, theta = result.x

        messagebox.showinfo("Result", f"l: {l}\ntheta: {theta}")


root = tk.Tk()
root.withdraw()  # 隐藏主窗口

calculate()

root.mainloop()
