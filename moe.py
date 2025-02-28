import tkinter as tk  # Библиотека для создания графического интерфейса
import segno  # Библиотека для генерации QR-кодов
import aspose.barcode.generation as barcode  # Библиотека для генерации штрихкодов
from aspose.pydrawing import Color  # Для работы с цветами
from PIL import Image, ImageTk  # Для работы с изображениями
from os import get_handle_inheritable  # Не используется в коде

def html_to_rgb(html_color):
    #Преобразует HTML-цвет в RGB
    html_color = html_color.lstrip("#")  # Убирает символ '#'
    return tuple(int(html_color[i:i+2], 16) for i in (0, 2, 4))  # Преобразует HEX в RGB

class MyGUI:
    def __init__(self):

        # Функция для открытия второго окна (выбор дизайна)
        def open_second_window(choice):
            self.third_window.withdraw()  # Скрывает третье окно
            self.user_choice = choice  # Сохраняет выбор пользователя (QR-код или штрихкод)
            self.root.withdraw()  # Скрывает главное окно
            self.second_window.deiconify()  # Показывает второе окно
            self.label.config(text=f"Выберите дизайн {choice}а")  # Обновляет текст метки

        # Функция для открытия третьего окна (ввод текста)
        def open_third_window(design):
            self.second_window.withdraw()  # Скрывает второе окно
            self.third_window.deiconify()  # Показывает третье окно
            custom_colour = self.textbox1.get("1.0", tk.END).strip()  # Получает пользовательский цвет

            if design == "your colour" and custom_colour:
                design = custom_colour  # Использует пользовательский цвет

            if design == 'classic':
                design = 'black'  # Классический цвет — чёрный

            self.label1.config(text=f"Модель {self.user_choice}")  # Обновляет текст метки
            self.label2.config(text=f"Цвет {design}")  # Обновляет текст метки

        # Функция для возврата на главное окно
        def open_first_window():
            self.second_window.withdraw()  # Скрывает второе окно
            self.third_window.withdraw()  # Скрывает третье окно
            self.root.deiconify()  # Показывает главное окно

        # Функция для генерации и отображения изображения
        def open_image_window(design):
            self.third_window.withdraw()  # Скрывает третье окно
            user_text = self.textbox.get("1.0", tk.END).strip()  # Получает текст от пользователя

            # Генерация QR-кода
            if self.user_choice == 'QR-код':
                if design == "classic":
                    qr_color = "black"  # Классический цвет — чёрный

                elif design == "your colour":
                    qr_color = self.textbox1.get("1.0", tk.END).strip()  # Пользовательский цвет

                else:
                    qr_color = design

                qrcode = segno.make_qr(user_text)  # Создаёт QR-код
                qrcode.save("basic_qrcode.png", dark=qr_color)  # Сохраняет QR-код в файл
                image_obj = "basic_qrcode.png"  # Путь к изображению

            # Генерация штрихкода
            elif self.user_choice == 'штрихкод':
                if design == "classic":
                    sh_color = "black"  # Классический цвет — чёрный

                elif design == "your colour":
                    sh_color = self.textbox1.get("1.0", tk.END).strip()  # Пользовательский цвет

                else:
                    sh_color = design

                if sh_color.startswith("#"):
                    sh_color_rgb = html_to_rgb(sh_color)
                    sh_color_obj = Color.from_argb(*sh_color_rgb)  # Создаёт объект Color из RGB

                else:
                    sh_color_obj = getattr(Color, sh_color.lower(), Color.black)  # Преобразует цвет в объект Color

                generator = barcode.BarcodeGenerator(barcode.EncodeTypes.CODE39)  # Создаёт генератор штрихкода
                generator.code_text = user_text  # Устанавливает текст для штрихкода
                generator.parameters.resolution = 300  # Устанавливает разрешение
                generator.parameters.barcode.x_dimension.pixels = 4  # Устанавливает размер штрихов
                generator.parameters.barcode.bar_color = sh_color_obj  # Устанавливает цвет штрихов
                generator.save("barcode.png")  # Сохраняет штрихкод в файл
                image_obj = "barcode.png"  # Путь к изображению

            # Загрузка и отображение изображения
            try:
                self.image = Image.open(image_obj)  # Открывает изображение
                self.image = self.image.resize((300, 300))  # Изменяет размер изображения
                self.tk_image = ImageTk.PhotoImage(self.image)  # Преобразует изображение для Tkinter
                self.image_label.config(image=self.tk_image)  # Отображает изображение в Label
                self.image_label.image = self.tk_image  # Сохраняет ссылку на изображение

            except FileNotFoundError:
                self.image_label.config(text="Изображение не найдено!")  # Обработка ошибки

            self.image_window.deiconify()  # Показывает окно с изображением

        # Настройка главного окна
        self.root = tk.Tk()
        self.root.geometry("500x330")
        self.root.title("Generation")
        self.root.configure(bg='pink')

        # Метка для выбора типа кода
        self.label = tk.Label(text="Выберите, что вы хотите создать", font=('Arial', 18))
        self.label.pack(padx=10, pady=20)

        # Фрейм для кнопок выбора
        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=1)

        # Кнопка для выбора QR-кода
        self.btn1 = tk.Button(self.buttonframe, text='QR-код', font=('Arial', 18), height=5, width=10, bg='PaleVioletRed1', command=lambda: open_second_window("QR-код"))
        self.btn1.grid(row=0, column=0, padx=10, pady=20)

        # Кнопка для выбора штрихкода
        self.btn2 = tk.Button(self.buttonframe, text='штрихкод', font=('Arial', 18), height=5, width=10, bg='PaleVioletRed1', command=lambda: open_second_window("штрихкод"))
        self.btn2.grid(row=0, column=1, padx=10, pady=20)

        self.buttonframe.pack()

        # Настройка второго окна (выбор дизайна)
        self.second_window = tk.Toplevel(self.root)
        self.second_window.title("Опции для создания")
        self.second_window.geometry("500x330")
        self.second_window.withdraw()  # Скрывает окно при запуске
        self.second_window.configure(bg='pink')

        # Метка для выбора дизайна
        self.label = tk.Label(self.second_window, text="Выберите дизайн", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)

        # Переменная для хранения выбранного дизайна
        self.option = tk.StringVar(value="None")

        # Радиокнопки для выбора цвета
        self.check1 = tk.Radiobutton(self.second_window, text='classic', variable=self.option, value='classic')
        self.check1.pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        self.check2 = tk.Radiobutton(self.second_window, text='red', variable=self.option, value='red')
        self.check2.pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        self.check3 = tk.Radiobutton(self.second_window, text='blue', variable=self.option, value='blue')
        self.check3.pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        self.check4 = tk.Radiobutton(self.second_window, text='yellow', variable=self.option, value='yellow')
        self.check4.pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        self.check5 = tk.Radiobutton(self.second_window, text='green', variable=self.option, value='green')
        self.check5.pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        self.check6 = tk.Radiobutton(self.second_window, text='your colour', variable=self.option, value='your colour')
        self.check6.pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        # Текстовое поле для ввода пользовательского цвета
        self.textbox1 = tk.Text(self.second_window, height=1)
        self.textbox1.pack(padx=30, pady=0)

        # Кнопка "Назад" для возврата на главное окно
        self.back_button = tk.Button(self.second_window, text="Назад", command=open_first_window)
        self.back_button.pack(side=tk.LEFT, padx=30, pady=10)

        # Кнопка "Далее" для перехода к следующему окну
        self.next_button = tk.Button(self.second_window, text="Далее", command=lambda: open_third_window(self.option.get()))
        self.next_button.pack(side=tk.RIGHT, padx=30, pady=10)

        # Настройка третьего окна (ввод текста)
        self.third_window = tk.Toplevel(self.root)
        self.third_window.title("Почти все!")
        self.third_window.geometry("500x330")
        self.third_window.withdraw()  # Скрывает окно при запуске
        self.third_window.configure(bg='pink')

        # Метка для ввода текста
        self.label0 = tk.Label(self.third_window, text="Введите текст или ссылку для генерации", font=('Arial', 18))
        self.label0.pack(padx=10, pady=10)

        # Текстовое поле для ввода текста
        self.textbox = tk.Text(self.third_window, height=4)
        self.textbox.pack(padx=30, pady=10)

        # Фрейм для кнопок и меток
        self.buttonframe2 = tk.Frame(self.third_window)
        self.buttonframe2.columnconfigure(1, weight=1)
        self.buttonframe2.columnconfigure(2, weight=1)

        # Метка для отображения выбранной модели
        self.label1 = tk.Label(self.buttonframe2, text="", font=('Arial', 18))
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        # Кнопка для изменения модели
        self.button1 = tk.Button(self.buttonframe2, text="Изменить модель", font=('Arial', 14), width=18, bg='PaleVioletRed1', command=open_first_window)
        self.button1.grid(row=0, column=1, padx=10, pady=10)

        # Метка для отображения выбранного цвета
        self.label2 = tk.Label(self.buttonframe2, text="", font=('Arial', 18))
        self.label2.grid(row=1, column=0, padx=10, pady=10)

        # Кнопка для изменения цвета
        self.button2 = tk.Button(self.buttonframe2, text="Изменить цвет", font=('Arial', 14), width=18, bg='PaleVioletRed1', command=lambda: open_second_window(self.user_choice))
        self.button2.grid(row=1, column=1, padx=10, pady=10)

        self.buttonframe2.pack(padx=10, pady=10)

        # Кнопка "Назад" для возврата на второе окно
        self.back_button = tk.Button(self.third_window, text="Назад", command=lambda: open_second_window(self.user_choice))
        self.back_button.pack(side=tk.LEFT, padx=30, pady=10)

        # Кнопка "Завершить" для генерации изображения
        self.next_button = tk.Button(self.third_window, text="Завершить", bg='PaleVioletRed1', command=lambda: open_image_window(self.option.get()))
        self.next_button.pack(side=tk.RIGHT, padx=30, pady=10)

        # Настройка окна для отображения изображения
        self.image_window = tk.Toplevel(self.root)
        self.image_window.title("Готово!")
        self.image_window.geometry("500x330")
        self.image_window.configure(bg='pink')
        self.image_window.withdraw()  # Скрывает окно при запуске

        # Метка для отображения изображения или сообщения об ошибке
        self.image_label = tk.Label(self.image_window, text="", font=('Arial', 18))
        self.image_label.pack(pady=10)

        self.root.mainloop()  # Запуск главного цикла приложения

MyGUI()  