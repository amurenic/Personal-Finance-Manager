def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Пожалуйста, введите корректное число.")

def get_int_input_with_exit(prompt):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'q':
            print("Завершение программы.")
            exit()
        try:
            return int(user_input)
        except ValueError:
            print("Пожалуйста, введите корректное число или 'q' для выхода.")

def get_percentage_input(prompt, remaining_percentage, remaining_balance):
    while True:
        percentage = get_int_input(prompt)
        if percentage > remaining_percentage:
            print(f"Ошибка! Доступно только {remaining_percentage}%.")
        else:
            return percentage

def edit_categories(categories):
    while True:
        print("\nТекущие категории для распределения средств:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        print("\nВы можете:")
        print("1. Добавить новую категорию")
        print("2. Удалить существующую категорию")
        print("3. Продолжить распределение средств")

        choice = input("Выберите действие (1, 2, 3): ")

        if choice == '1':
            new_category = input("Введите название новой категории: ")
            if new_category:
                categories.append(new_category)
                print(f"Категория '{new_category}' добавлена.")
        elif choice == '2':
            try:
                del_index = int(input("Введите номер категории для удаления: ")) - 1
                if 0 <= del_index < len(categories):
                    print(f"Категория '{categories[del_index]}' удалена.")
                    del categories[del_index]
                else:
                    print("Неверный номер категории.")
            except ValueError:
                print("Пожалуйста, введите корректный номер.")
        elif choice == '3':
            break
        else:
            print("Некорректный выбор, попробуйте снова.")

while True:
    print('Планирование бюджета на месяц\n')

    # Запрос зарплаты и доп. дохода
    salary = get_int_input_with_exit('Введите сумму зарплаты: ')
    add_income = get_int_input_with_exit('Введите сумму дополнительного дохода: ')

    # Проезд и дни работы
    dailly_fare = get_int_input_with_exit('Введите сумму ежедневного проезда: ')
    work_days = get_int_input_with_exit('Сколько дней в месяце Вы работаете: ')
    print()

    # Коммунальные платежи
    print('Введите суммы из квитанций для оплаты')
    internet = get_int_input_with_exit('Интернет: ')
    electricity = get_int_input_with_exit('Электроэнергия: ')
    heating = get_int_input_with_exit('Отопление: ')
    public_service = get_int_input_with_exit('Прочие коммунальные услуги: ')
    communal_payments = electricity + heating + public_service + internet

    # Аренда
    rent = get_int_input_with_exit('Введите сумму аренды жилья (если нет - введите 0): ')
    print()

    # Кредиты
    print('Введите сумму каждого платежа по кредитам:')
    print('(платежей нет/ввели все платежи - нажмите 0)')
    total_payment = 0
    count_payment = 0
    while True:
        count_payment += 1
        monthly_credit_payment = get_int_input_with_exit(f'{count_payment}-й платёж: ')
        if monthly_credit_payment == 0:
            break
        total_payment += monthly_credit_payment

    # Домашние животные
    is_pet = get_int_input_with_exit('Сколько у Вас домашних животных? (нет - введите 0): ')

    # Категории для распределения средств
    default_categories = ["Питание", "Бытовая химия и косметика", "Подарки", "Развлечения", "Накопления"]
    if is_pet > 0:
        default_categories.insert(1, "Домашние животные")

    # Пользователь может редактировать категории
    edit_categories(default_categories)

    # Вычисления общ суммы обязательных трат
    monthly_fare = dailly_fare * work_days
    obligatory_payments = monthly_fare + communal_payments + rent + total_payment
    free_balance = salary + add_income - obligatory_payments

    # Запрос распределения процентов
    print('\nВведите проценты для распределения оставшихся средств по следующим категориям. Общая сумма процентов не должна превышать 100%.')
    remaining_percentage = 100
    allocated_amounts = {}

    for category in default_categories:
        remaining_balance = free_balance * remaining_percentage / 100
        prompt_message = f'Какую часть процентов хотите выделить на {category}? (доступно: {remaining_percentage}%, {remaining_balance:.2f} руб.): '
        percentage = get_percentage_input(prompt_message, remaining_percentage, remaining_balance)
        remaining_percentage -= percentage
        allocated_amounts[category] = free_balance * percentage / 100
        if remaining_percentage == 0:
            break

    # Вывод обязательных платежей перед распределением оставшихся средств
    print("\nОбязательные платежи:")
    if dailly_fare > 0:
        print(f'Отложить на проезд: {monthly_fare} руб.')
    print(f'Отложить на коммунальные услуги: {communal_payments} руб.')
    print(f'Отложить на кредиты: {total_payment} руб.')

    # Вывод распределения оставшихся средств
    print("\nРаспределение оставшихся средств:")
    for category, amount in allocated_amounts.items():
        print(f'{category}: {amount:.2f} руб.')

    # Проверка остатков процентов и вывод нераспределённой суммы
    if remaining_percentage > 0:
        leftover_amount = free_balance * remaining_percentage / 100
        print(f"\nОсталось {remaining_percentage}% нераспределённых средств, что составляет {leftover_amount:.2f} руб.")

    # Подсказка для продолжения или завершения программы
    cont = get_int_input("\nПродолжить расчет бюджета на следующий месяц? (1 - да, 0 - нет): ")
    if cont != 1:
        print("Завершение программы.")
        break
