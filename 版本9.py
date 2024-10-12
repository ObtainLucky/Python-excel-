import tkinter as tk
import pandas as pd
from tkinter import messagebox, font

class StartPage:
    def __init__(self, master):
        self.master = master
        self.master.title("选择题目类型")
        self.master.geometry("400x200")
        self.custom_font = font.Font(family='黑体', size=20)

        self.label = tk.Label(self.master, text="请选择题目类型", font=self.custom_font)
        self.label.pack(pady=20)

        self.single_button = tk.Button(self.master, text="单选", font=self.custom_font, width=10, height=2, bg='orange', fg='white',
                                        command=lambda: self.start_quiz('单选'))
        self.single_button.pack(pady=20)

        self.multiple_button = tk.Button(self.master, text="多选", font=self.custom_font, width=10, height=2, bg='green', fg='white',
                                        command=lambda: self.start_quiz('多选'))
        self.multiple_button.pack(pady=20)

        self.judge_button = tk.Button(self.master, text="判断", font=self.custom_font, width=10, height=2, bg='blue', fg='white',
                                        command=lambda: self.start_quiz('判断'))
        self.judge_button.pack(pady=20)

    def start_quiz(self, sheet_name):
        self.master.destroy()
        quiz_root = tk.Tk()
        quiz_root.title("大唐杯答题")
        app = QuizApp(quiz_root, f'{sheet_name}.xlsx', sheet_name)
        app.start_timer()
        quiz_root.mainloop()


class QuizApp:
    def __init__(self, master, excel_file, sheet_name):
        self.master = master
        self.df = pd.read_excel(excel_file, sheet_name=sheet_name)
        self.questions = self.df.to_dict(orient='records')
        self.current_question = 0
        
        # 设置字体
        self.custom_font = font.Font(family='黑体', size=16)
        self.button_font = font.Font(family='黑体', size=14)
        
        self.create_widgets()
        self.next_question()
        
    def create_widgets(self):
        self.question_label = tk.Label(self.master, text="", font=self.custom_font)
        self.question_label.pack(pady=20)

        self.option_frame = tk.Frame(self.master)
        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.option_frame, text="", font=self.button_font, width=20, height=2, bg='white', fg='orange',
                               command=lambda i=i: self.check_answer(i))
            button.pack(side=tk.LEFT, padx=10)
            self.option_buttons.append(button)
        self.option_frame.pack(pady=10)

        self.button_frame = tk.Frame(self.master)
        self.previous_button = tk.Button(self.button_frame, text="上一题", font=self.button_font, width=10, height=2, bg='orange', fg='white',
                                       command=self.previous_question, state=tk.DISABLED)
        self.previous_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.button_frame, text="下一题", font=self.button_font, width=10, height=2, bg='red', fg='white',
                                   command=self.next_question)
        self.next_button.pack(side=tk.LEFT, padx=10)

        # 新增显示正确答案的按钮
        self.show_answer_button = tk.Button(self.button_frame, text="显示答案", font=self.button_font, width=10, height=2, bg='yellow', fg='black',
                                         command=self.show_answer, state=tk.DISABLED)
        self.show_answer_button.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.button_frame, text="重新开始", font=self.button_font, width=10, height=2, bg='green', fg='white',
                                       command=self.restart_quiz)
        self.restart_button.pack(side=tk.LEFT, padx=10)
        self.button_frame.pack(pady=20)
        self.time_label = tk.Label(self.master, text="时间： 00:00", font=self.custom_font)
        self.time_label.pack(pady=10)
        
    def start_timer(self):
        self.elapsed_time = 0  # 重置计时器
        self.update_time()  # 立即更新时间显示

    def update_time(self):
        minutes, seconds = divmod(self.elapsed_time, 60)
        time_str = "时间： {:02d}:{:02d}".format(minutes, seconds)
        self.time_label.config(text=time_str)
        self.elapsed_time += 1  # 增加时间
        self.master.after(1000, self.update_time)  #
    def next_question(self):
        if self.current_question < len(self.questions):
            if self.current_question > 0:
                self.previous_button.config(state=tk.NORMAL)
                self.show_answer_button.config(state=tk.NORMAL)  # 使答案按钮可用
            for button in self.option_buttons:
                button.config(bg='white', state=tk.NORMAL)
            self.question_label.config(text=self.questions[self.current_question]['Question'])
            options = self.questions[self.current_question]['Options'].split('\n')
            for i, option in enumerate(options):
                self.option_buttons[i].config(text=option)
            self.current_question += 1
        else:
            messagebox.showinfo("Result", "所有题目已答完！")

    def previous_question(self):
        if self.current_question > 1:
            self.current_question -= 2
            self.next_question()
        if self.current_question == 1:
            self.previous_button.config(state=tk.DISABLED)
        
    def check_answer(self, option):
        for button in self.option_buttons:
            button.config(state=tk.DISABLED)
        if option == self.questions[self.current_question - 1]['Answer']:
            messagebox.showinfo("结果", "正确！")
            self.option_buttons[option].config(bg='green')
            self.master.after(500, self.next_question)
        else:
            messagebox.showerror("结果", "错误！")
            self.option_buttons[option].config(bg='red')
        
    def restart_quiz(self):
        self.current_question = 0
        self.next_question()
        self.previous_button.config(state=tk.DISABLED)
        self.show_answer_button.config(state=tk.DISABLED)  # 重置时，答案按钮也应禁用
        
    # 新增方法，用于显示当前题目的正确答案
    def show_answer(self):
        correct_answer = self.questions[self.current_question - 1]['Correct Answer']
        messagebox.showinfo("正确答案", f"正确答案是：{correct_answer}")
        
# 运行应用
root = tk.Tk()
start_page = StartPage(root)
root.mainloop()
