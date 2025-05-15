# Импорт библиотек и настрйока окружения
# Основные библиотеки для работы с GUI
import tkinter as tk  # Основной модуль для создания графического интерфейса
from tkinter import messagebox  # Модуль для отображения всплывающих сообщений

# Библиотеки для генерации QR-кодов
import segno  # Мощный генератор QR-кодов

# Библиотеки для работы с штрихкодами
import aspose.barcode.generation as barcode  # Генератор штрихкодов
from aspose.pydrawing import Color  # Работа с цветами для штрихкодов

# Библиотеки для работы с изображениями
from PIL import Image, ImageTk  # Обработка и отображение изображений

# Дополнительные утилиты
import io  # Работа с потоками ввода-вывода
import win32clipboard  # Доступ к буферу обмена Windows


# Вспомогательные функции

def html_to_rgb(html_color):
    """Конвертирует HTML-цвет (например, '#RRGGBB') в кортеж RGB"""
    html_color = html_color.lstrip("#")
    return tuple(int(html_color[i:i + 2], 16) for i in (0, 2, 4))


# Основной класс приложения

class MyGUI:
    """
    Главный класс приложения, реализующий весь функционал генератора QR-кодов и штрихкодов.
    Содержит методы для создания интерфейса и обработки пользовательских действий.
    """

    def __init__(self):
        """
        Инициализация приложения. Создает все необходимые окна и элементы интерфейса.
        """

        def open_second_window(choice):
            """
            Открывает окно выбора дизайна (цвета) для выбранного типа кода.
            Скрывает другие окна и отображает окно выбора дизайна.
            """
            self.save_window.withdraw()
            self.user_choice = choice  # Сохраняем выбор пользователя (QR-код или штрихкод)
            self.root.withdraw()  # Скрываем главное окно
            self.second_window.deiconify()  # Показываем окно выбора дизайна
            self.label.config(text=f"Выберите дизайн {choice}а")  # Обновляем текст заголовка

        def open_third_window(design):
            """
            Открывает окно для ввода текста/ссылки, который будет закодирован.
            Обрабатывает пользовательский выбор цвета и сохраняет его.
            """
            self.second_window.withdraw()
            self.save_window.withdraw()
            self.third_window.deiconify()

            # Обработка пользовательского цвета
            custom_colour = self.textbox1.get("1.0", tk.END).strip()
            if design == "your colour" and custom_colour:
                design = custom_colour  # Используем пользовательский цвет
            if design == 'classic':
                design = 'black'  # Классический вариант - черный цвет

            # Обновляем информацию о выборе пользователя
            self.label1.config(text=f"Модель {self.user_choice}")
            self.label2.config(text=f"Цвет {design}")
            self.selected_design = design  # Сохраняем выбранный дизайн для дальнейшего использования

        def open_first_window():
            """
            Возврат в главное окно приложения. Скрывает все другие окна.
            """
            self.second_window.withdraw()
            self.third_window.withdraw()
            self.save_window.withdraw()
            self.image_window.withdraw()
            self.root.deiconify()  # Показываем главное окно

        def update_size_options():
            """
            Обновляет доступные варианты размеров в зависимости от выбранного типа кода.
            Удаляет старые радиокнопки и создает новые с актуальными размерами.
            """
            # Удаляем все существующие радиокнопки
            for widget in self.save_window.pack_slaves():
                if isinstance(widget, tk.Radiobutton):
                    widget.destroy()

            # Определяем доступные размеры в зависимости от типа кода
            sizes = []
            if self.user_choice == "QR-код":
                sizes = ["300x300", "400x400", "500x500"]  # Квадратные размеры для QR-кодов
            elif self.user_choice == "штрихкод":
                sizes = ["200x100", "300x150", "400x200"]  # Прямоугольные размеры для штрихкодов

            self.size_option.set("None")  # Сбрасываем текущий выбор размера

            # Создаем новые радиокнопки для каждого размера
            tk.Radiobutton(
                self.save_window,
                text=sizes[0],
                variable=self.size_option,
                value=sizes[0]
            ).pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

            tk.Radiobutton(
                self.save_window,
                text=sizes[1],
                variable=self.size_option,
                value=sizes[1]
            ).pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

            tk.Radiobutton(
                self.save_window,
                text=sizes[2],
                variable=self.size_option,
                value=sizes[2]
            ).pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        def open_size_selection():
            """
            Открывает окно выбора размера генерируемого изображения.
            Обновляет доступные варианты размеров перед показом окна.
            """
            self.third_window.withdraw()
            update_size_options()  # Обновляем варианты размеров
            self.save_window.deiconify()  # Показываем окно выбора размера

        def generate_and_show_image(width, height):
            """
            Генерирует изображение (QR-код или штрихкод) с заданными параметрами
            и отображает его в интерфейсе.
            """
            user_text = self.textbox.get("1.0", tk.END).strip()  # Получаем текст для кодирования
            design = self.selected_design  # Получаем выбранный дизайн

            if self.user_choice == 'QR-код':
                # Обработка цвета для QR-кода
                qr_color = design
                if design == "classic":
                    qr_color = "black"
                elif design == "your colour":
                    qr_color = self.textbox1.get("1.0", tk.END).strip()

                # Генерация QR-кода
                qrcode = segno.make_qr(user_text)
                qrcode.save(
                    "basic_qrcode.png",
                    dark=qr_color,
                    scale=1,
                    border=0,
                    kind='png'
                )

                # Изменение размера и сохранение изображения
                image = Image.open("basic_qrcode.png").resize((width, height))
                image.save("basic_qrcode.png")
                image_obj = "basic_qrcode.png"

            elif self.user_choice == 'штрихкод':
                # Обработка цвета для штрихкода
                sh_color = design
                if design == "classic":
                    sh_color = "black"
                elif design == "your colour":
                    sh_color = self.textbox1.get("1.0", tk.END).strip()

                # Преобразование цвета в формат, понятный библиотеке штрихкодов
                if sh_color.startswith("#"):
                    sh_color_rgb = html_to_rgb(sh_color)
                    sh_color_obj = Color.from_argb(*sh_color_rgb)
                else:
                    sh_color_obj = getattr(Color, sh_color.lower(), Color.black)

                # Генерация штрихкода
                generator = barcode.BarcodeGenerator(barcode.EncodeTypes.CODE39)
                generator.code_text = user_text
                generator.parameters.resolution = 300
                generator.parameters.barcode.x_dimension.pixels = 4
                generator.parameters.barcode.bar_color = sh_color_obj

                generator.save("barcode.png")

                # Изменение размера и сохранение изображения
                image = Image.open("barcode.png").resize((width, height))
                image.save("barcode.png")
                image_obj = "barcode.png"

            try:
                # Отображение сгенерированного изображения в интерфейсе
                self.image = Image.open(image_obj)
                self.tk_image = ImageTk.PhotoImage(self.image)
                self.image_label.config(image=self.tk_image, text="")
                self.image_label.image = self.tk_image
            except FileNotFoundError:
                self.image_label.config(text="Изображение не найдено!")

        def open_image_display():
            """
            Открывает окно с готовым изображением после выбора размера.
            Проверяет, что размер был выбран, и генерирует изображение.
            """
            selected_size = self.size_option.get()
            if not selected_size or selected_size == "None":
                tk.messagebox.showerror("Ошибка", "Пожалуйста, выберите размер перед сохранением.")
                return

            # Получаем ширину и высоту из выбранного размера
            width, height = map(int, selected_size.split("x"))
            generate_and_show_image(width, height)  # Генерируем изображение

            self.save_window.withdraw()
            self.image_window.deiconify()  # Показываем окно с результатом

        # Создание и настройка графического интерфейса

        # Главное окно приложения
        self.root = tk.Tk()
        self.root.geometry("500x330")
        self.root.title("Генерация")
        self.root.configure(bg='pink')  # Устанавливаем розовый фон

        # Заголовок главного окна
        tk.Label(
            self.root,
            text="Выберите, что вы хотите создать",
            font=('Arial', 18)
        ).pack(padx=10, pady=20)

        # Фрейм для кнопок выбора типа кода
        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=1)
        self.buttonframe.pack()

        # Кнопка для выбора генерации QR-кода
        tk.Button(
            self.buttonframe,
            text='QR-код',
            font=('Arial', 18),
            height=5,
            width=10,
            bg='PaleVioletRed1',
            command=lambda: open_second_window("QR-код")
        ).grid(row=0, column=0, padx=10, pady=20)

        # Кнопка для выбора генерации штрихкода
        tk.Button(
            self.buttonframe,
            text='штрихкод',
            font=('Arial', 18),
            height=5,
            width=10,
            bg='PaleVioletRed1',
            command=lambda: open_second_window("штрихкод")
        ).grid(row=0, column=1, padx=10, pady=20)

        # Окно выбора дизайна (цвета)
        self.second_window = tk.Toplevel(self.root)
        self.second_window.title("Опции для создания")
        self.second_window.geometry("500x330")
        self.second_window.withdraw()  # Скрываем окно при запуске
        self.second_window.configure(bg='pink')

        # Заголовок окна выбора дизайна
        self.label = tk.Label(
            self.second_window,
            text="Выберите дизайн",
            font=('Arial', 18)
        )
        self.label.pack(padx=10, pady=10)

        # Переменная для хранения выбранного дизайна
        self.option = tk.StringVar(value="None")

        # Радиокнопки для выбора цвета/дизайна
        tk.Radiobutton(
            self.second_window,
            text='classic',
            variable=self.option,
            value='classic'
        ).pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        tk.Radiobutton(
            self.second_window,
            text='red',
            variable=self.option,
            value='red'
        ).pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        tk.Radiobutton(
            self.second_window,
            text='blue',
            variable=self.option,
            value='blue'
        ).pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        tk.Radiobutton(
            self.second_window,
            text='yellow',
            variable=self.option,
            value='yellow'
        ).pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        tk.Radiobutton(
            self.second_window,
            text='green',
            variable=self.option,
            value='green'
        ).pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        # Опция для ввода пользовательского цвета
        tk.Radiobutton(
            self.second_window,
            text='your colour',
            variable=self.option,
            value='your colour'
        ).pack(side=tk.TOP, anchor=tk.W, padx=30, pady=5)

        # Текстовое поле для ввода пользовательского цвета
        self.textbox1 = tk.Text(
            self.second_window,
            height=1
        )
        self.textbox1.pack(padx=30, pady=0)

        # Кнопки навигации в окне выбора дизайна
        tk.Button(
            self.second_window,
            text="Назад",
            command=open_first_window
        ).pack(side=tk.LEFT, padx=30, pady=10)

        tk.Button(
            self.second_window,
            text="Далее",
            command=lambda: open_third_window(self.option.get())
        ).pack(side=tk.RIGHT, padx=30, pady=10)

        # Окно ввода текста для кодирования
        self.third_window = tk.Toplevel(self.root)
        self.third_window.title("Почти все!")
        self.third_window.geometry("500x330")
        self.third_window.withdraw()
        self.third_window.configure(bg='pink')

        # Заголовок окна ввода текста
        tk.Label(
            self.third_window,
            text="Введите текст или ссылку для генерации",
            font=('Arial', 18)
        ).pack(padx=10, pady=10)

        # Текстовое поле для ввода данных
        self.textbox = tk.Text(self.third_window, height=4)
        self.textbox.pack(padx=30, pady=10)

        # Фрейм для отображения информации и кнопок
        self.buttonframe2 = tk.Frame(self.third_window)
        self.buttonframe2.columnconfigure(1, weight=1)
        self.buttonframe2.columnconfigure(2, weight=1)
        self.buttonframe2.pack(padx=10, pady=10)

        # Метки для отображения выбранных параметров
        self.label1 = tk.Label(self.buttonframe2, text="", font=('Arial', 18))
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        # Кнопка для изменения типа кода
        tk.Button(
            self.buttonframe2,
            text="Изменить модель",
            font=('Arial', 14),
            width=18,
            bg='PaleVioletRed1',
            command=open_first_window
        ).grid(row=0, column=1, padx=10, pady=10)

        self.label2 = tk.Label(self.buttonframe2, text="", font=('Arial', 18))
        self.label2.grid(row=1, column=0, padx=10, pady=10)

        # Кнопка для изменения цвета
        tk.Button(
            self.buttonframe2,
            text="Изменить цвет",
            font=('Arial', 14),
            width=18,
            bg='PaleVioletRed1',
            command=lambda: open_second_window(self.user_choice)
        ).grid(row=1, column=1, padx=10, pady=10)

        # Кнопки навигации в окне ввода текста
        tk.Button(
            self.third_window,
            text="Назад",
            command=lambda: open_second_window(self.user_choice)
        ).pack(side=tk.LEFT, padx=30, pady=10)

        tk.Button(
            self.third_window,
            text="Далее",
            command=open_size_selection
        ).pack(side=tk.RIGHT, padx=30, pady=10)

        # Окно выбора размера изображения
        self.save_window = tk.Toplevel(self.root)
        self.save_window.title("Сохранение")
        self.save_window.geometry("500x330")
        self.save_window.withdraw()
        self.save_window.configure(bg='pink')

        # Переменная для хранения выбранного размера
        self.size_option = tk.StringVar()

        # Заголовок окна выбора размера
        tk.Label(
            self.save_window,
            text="Выберите размер",
            font=("Arial", 18)
        ).pack(padx=10, pady=20)

        # Фрейм для кнопок навигации
        self.button_frame = tk.Frame(self.save_window, bg='pink')
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Кнопки навигации в окне выбора размера
        tk.Button(
            self.button_frame,
            text="Назад",
            command=lambda: open_third_window(self.selected_design)
        ).pack(side=tk.LEFT, padx=30)

        tk.Button(
            self.button_frame,
            text="Завершить",
            bg='PaleVioletRed1',
            command=open_image_display
        ).pack(side=tk.RIGHT, padx=30)

        # Окно отображения готового изображения
        self.image_window = tk.Toplevel(self.root)
        self.image_window.title("Готово!")
        self.image_window.geometry("530x530")
        self.image_window.withdraw()
        self.image_window.configure(bg='pink')

        # Фрейм для кнопок в окне изображения
        self.button_frame_img = tk.Frame(self.image_window, bg='pink')
        self.button_frame_img.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        # Кнопки управления в окне изображения
        tk.Button(
            self.button_frame_img,
            text="Редактировать",
            command=lambda: open_third_window(self.selected_design)
        ).pack(side=tk.LEFT, padx=30)

        tk.Button(
            self.button_frame_img,
            text="Скопировать в буфер обмена",
            bg='PaleVioletRed1',
            command=self.save_image_dialog
        ).pack(side=tk.RIGHT, padx=30)

        # Метка для отображения сгенерированного изображения
        self.image_label = tk.Label(
            self.image_window,
            text="",
            font=('Arial', 18)
        )
        self.image_label.pack(pady=10)

        # Запуск главного цикла приложения
        self.root.mainloop()

    # Методы для работы с буфером обмена

    def copy_image_to_clipboard(self, pil_image):
        """
        Копирует изображение в буфер обмена Windows.

        Args:
            pil_image (PIL.Image): Изображение для копирования
        """
        output = io.BytesIO()
        pil_image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]  # Удаляем заголовок BMP
        output.close()

        # Копирование данных в буфер обмена
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def save_image_dialog(self):
        """
        Обрабатывает запрос на копирование изображения в буфер обмена.
        Показывает сообщения об успехе или ошибке.
        """
        if not hasattr(self, 'image') or self.image is None:
            messagebox.showerror("Ошибка", "Изображение не сгенерировано.")
            return

        try:
            self.copy_image_to_clipboard(self.image)
            messagebox.showinfo("Успех", "Изображение скопировано в буфер обмена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать изображение: {e}")


if __name__ == "__main__":
    MyGUI()