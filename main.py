import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox


# функция для калорийности
def get_calories_data_ordered():
    url = 'https://rsport.ria.ru/20220514/kaloriynost-1788483172.html?ysclid=lxt2u1gqcl461725737'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')

        if tables:
            data = []
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['th', 'td'])
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    data.append(row_data)
            return data
        else:
            return 'Таблицы с данными не найдены'
    else:
        return 'Ошибка при отправке запроса на сайт'


# функция для упражнений
def get_exercises_data():
    url = 'https://multiurok.ru/files/kompleks-obshcherazvivaiushchikh-uprazhnenii-v-tab.html?ysclid=lxt3mtfjna754993115'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        exercise_data = []
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                row_data = [cell.get_text(strip=True) for cell in cells]
                exercise_data.append(row_data)
        return exercise_data
    else:
        return 'Ошибка при отправке запроса на сайт'


# функция для советов
def get_health_tips():
    url = 'https://www.fbuz04.ru/index.php/o-centre/press-sluzhba/10-samykh-glavnykh-pravil-zdorovogo-obraza-zhizni?ysclid=lxt6zejyv9918213684'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tips_data = []
        for item in soup.find_all('h2'):
            tips_data.append([item.get_text(strip=True)])
        paragraph_list = soup.find_all('p')
        for paragraph in paragraph_list:
            tips_data.append([paragraph.get_text(strip=True)])
        return tips_data
    else:
        return 'Ошибка при отправке запроса на сайт'


# отображение данных в таблице
def show_data(data, columns):
    data_window = tk.Toplevel(root)
    tree = ttk.Treeview(data_window, columns=columns, show='headings')
    tree.pack(expand=True, fill='both')

    # настройка колонок
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    # добавление данных в таблицу
    for row in data:
        tree.insert('', 'end', values=row)

    # настройка шрифта
    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 12))
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))


# функция для обработки кнопки калорийности
def get_calories_button_click():
    data = get_calories_data_ordered()
    if isinstance(data, list):
        columns = ['Продукт', 'Калории', 'Белки', 'Жиры', 'Углеводы']
        show_data(data, columns)
    else:
        show_data([[data]], ['Ошибка'])


# функция для обработки кнопки упражнений
def get_exercises_button_click():
    data = get_exercises_data()
    if isinstance(data, list):
        columns = ['Упражнение', 'Повторы', 'Подходы']
        show_data(data, columns)
    else:
        show_data([[data]], ['Ошибка'])


# функция для обработки кнопки советов
def get_health_tips_button_click():
    data = get_health_tips()
    if isinstance(data, list):
        columns = ['Советы']
        show_data(data, columns)
    else:
        show_data([[data]], ['Ошибка'])


# функция для входа в систему
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == 'user' and password == 'password':  # здесь можно добавить реальную проверку
        auth_window.destroy()
        main_app()
    else:
        messagebox.showerror('Ошибка', 'Неверный логин или пароль')

# основное окное со всеми кнопками
def main_app():
    global root
    root = tk.Tk()
    root.title("Приложение здорового образа жизни")
    root.geometry("800x600")
    background_image = tk.PhotoImage(file="./myaso-original.png")  # Путь к изображению заднего фона
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # кнопочки
    calories_button = tk.Button(root, text='Получить данные о калорийности продуктов',
                                command=get_calories_button_click, font=('Arial', 14))
    calories_button.pack(pady=10)
    calories_button.config(width=40, height=2, bg='white')

    exercises_button = tk.Button(root, text='Получить данные о физических упражнениях',
                                 command=get_exercises_button_click, font=('Arial', 14))
    exercises_button.pack(pady=10)
    exercises_button.config(width=40, height=2, bg='blue')

    health_tips_button = tk.Button(root, text='Получить советы по здоровому образу жизни',
                                   command=get_health_tips_button_click, font=('Arial', 14))
    health_tips_button.pack(pady=10)
    health_tips_button.config(width=40, height=2, bg='red')

    root.mainloop()


# окно авторизации
auth_window = tk.Tk()
auth_window.title("Авторизация")
auth_window.geometry("400x300")

tk.Label(auth_window, text="Логин", font=('Arial', 14)).pack(pady=10)
username_entry = tk.Entry(auth_window, font=('Arial', 14))
username_entry.pack(pady=10)

tk.Label(auth_window, text="Пароль", font=('Arial', 14)).pack(pady=10)
password_entry = tk.Entry(auth_window, font=('Arial', 14), show='*')
password_entry.pack(pady=10)

login_button = tk.Button(auth_window, text="Войти", command=login, font=('Arial', 14))
login_button.pack(pady=10)
login_button.config(width=20, height=2, bg='green')

auth_window.mainloop()
