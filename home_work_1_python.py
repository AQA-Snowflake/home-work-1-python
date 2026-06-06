# Определяем класс Student, представляющий студента
class Student:
    """
    Класс, представляющий студента.
    Атрибуты:
        name (str): Имя.
        surname (str): Фамилия.
        gender (str): Пол.
        finished_courses (list): Список завершённых курсов.
        courses_in_progress (list): Список курсов, которые сейчас изучаются.
        grades (dict): Словарь с оценками за домашние задания.
            Ключ – название курса, значение – список оценок.
    """

    # Конструктор класса Student
    def __init__(self, name, surname, gender):
        # Сохраняем имя студента
        self.name = name
        # Сохраняем фамилию студента
        self.surname = surname
        # Сохраняем пол студента
        self.gender = gender
        # Инициализируем пустой список завершённых курсов
        self.finished_courses = []
        # Инициализируем пустой список курсов в процессе изучения
        self.courses_in_progress = []
        # Инициализируем пустой словарь для оценок
        self.grades = {}

    # Метод для выставления оценки лектору
    def rate_lecture(self, lecturer, course, grade):
        """
        Выставить оценку лектору за лекцию.
        Проверяет, что lecturer является экземпляром Lecturer,
        студент записан на курс, а лектор прикреплён к этому курсу.
        """
        # Проверяем, является ли lecturer лектором, что студент изучает курс и лектор прикреплён к этому курсу
        if (isinstance(lecturer, Lecturer)
                and course in self.courses_in_progress
                and course in lecturer.courses_attached):
            # Добавляем оценку в словарь лектора, используя setdefault для создания списка при первом обращении
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            # Если хотя бы одно условие не выполнено – возвращаем строку 'Ошибка'
            return 'Ошибка'

    # Приватный метод для вычисления средней оценки студента за домашние задания
    def _average_grade(self):
        """Возвращает среднюю оценку за домашние задания по всем курсам."""
        # Собираем все оценки студента в один плоский список
        all_grades = [g for grades in self.grades.values() for g in grades]
        # Если нет ни одной оценки – возвращаем 0
        if not all_grades:
            return 0
        # Вычисляем среднее арифметическое всех оценок
        return sum(all_grades) / len(all_grades)

    # Переопределение магического метода __str__ для строкового представления студента
    def __str__(self):
        # Получаем среднюю оценку
        avg = self._average_grade()
        # Формируем строку с курсами в процессе, разделёнными запятой (если есть)
        courses_in_progress = ', '.join(self.courses_in_progress) if self.courses_in_progress else ''
        # Формируем строку с завершёнными курсами, разделёнными запятой (если есть)
        finished_courses = ', '.join(self.finished_courses) if self.finished_courses else ''
        # Возвращаем многострочную строку с информацией о студенте
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg:.1f}\n'
                f'Курсы в процессе изучения: {courses_in_progress}\n'
                f'Завершенные курсы: {finished_courses}')

    # Реализация оператора равенства для студентов (по средней оценке)
    def __eq__(self, other):
        # Проверяем, является ли другой объект студентом
        if not isinstance(other, Student):
            return NotImplemented
        # Сравниваем средние оценки
        return self._average_grade() == other._average_grade()

    # Реализация оператора меньше для студентов
    def __lt__(self, other):
        # Проверяем, является ли другой объект студентом
        if not isinstance(other, Student):
            return NotImplemented
        # Сравниваем средние оценки
        return self._average_grade() < other._average_grade()

    # Оператор <= реализуем через < и ==
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    # Оператор > как отрицание <=
    def __gt__(self, other):
        return not self.__le__(other)

    # Оператор >= как отрицание <
    def __ge__(self, other):
        return not self.__lt__(other)


# Определяем базовый класс Mentor (родитель для Lecturer и Reviewer)
class Mentor:
    """
    Родительский класс для преподавателей.
    Атрибуты:
        name (str): Имя.
        surname (str): Фамилия.
        courses_attached (list): Список закреплённых курсов.
    """

    # Конструктор класса Mentor
    def __init__(self, name, surname):
        # Сохраняем имя преподавателя
        self.name = name
        # Сохраняем фамилию преподавателя
        self.surname = surname
        # Инициализируем пустой список закреплённых курсов
        self.courses_attached = []


# Класс Lecturer, наследующий от Mentor
class Lecturer(Mentor):
    """
    Класс, представляющий лектора.
    Дополнительно хранит оценки за лекции.
    """

    # Конструктор лектора
    def __init__(self, name, surname):
        # Вызываем конструктор родительского класса для инициализации имени, фамилии и списка курсов
        super().__init__(name, surname)
        # Инициализируем словарь для хранения оценок за лекции (ключ – курс, значение – список оценок)
        self.grades = {}

    # Приватный метод для вычисления средней оценки лектора
    def _average_grade(self):
        """Средняя оценка за лекции по всем курсам."""
        # Собираем все оценки лектора в один список
        all_grades = [g for grades in self.grades.values() for g in grades]
        # Если оценок нет – возвращаем 0
        if not all_grades:
            return 0
        # Вычисляем среднее арифметическое
        return sum(all_grades) / len(all_grades)

    # Переопределение __str__ для вывода информации о лекторе
    def __str__(self):
        # Получаем среднюю оценку
        avg = self._average_grade()
        # Возвращаем отформатированную строку
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {avg:.1f}')

    # Оператор равенства для сравнения лекторов по средней оценке
    def __eq__(self, other):
        # Проверяем, является ли other лектором
        if not isinstance(other, Lecturer):
            return NotImplemented
        # Сравниваем средние оценки
        return self._average_grade() == other._average_grade()

    # Оператор < для лекторов
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    # Оператор <=
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    # Оператор >
    def __gt__(self, other):
        return not self.__le__(other)

    # Оператор >=
    def __ge__(self, other):
        return not self.__lt__(other)


# Класс Reviewer (проверяющий), наследующий от Mentor
class Reviewer(Mentor):
    """
    Класс, представляющий эксперта, проверяющего домашние задания.
    """

    # Метод для выставления оценки студенту за домашнее задание
    def rate_hw(self, student, course, grade):
        """
        Выставить оценку студенту за домашнее задание.
        Проверяет, что student – экземпляр Student,
        курс закреплён за проверяющим и студент его изучает.
        """
        # Проверяем, что student – студент, курс есть в списке проверяющего и студент его проходит
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress):
            # Добавляем оценку в словарь студента
            student.grades.setdefault(course, []).append(grade)
        else:
            # Иначе возвращаем ошибку
            return 'Ошибка'

    # Переопределение __str__ для проверяющего (без средних оценок)
    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


# Функция для вычисления средней оценки за домашние задания у группы студентов по конкретному курсу
def average_student_grade_for_course(students, course):
    """
    Вычисляет среднюю оценку за домашние задания у списка студентов по указанному курсу.
    """
    # Список для сбора всех оценок по курсу
    grades = []
    # Проходим по каждому студенту из переданного списка
    for s in students:
        # Если объект является студентом и у него есть оценки по нужному курсу
        if isinstance(s, Student) and course in s.grades:
            # Добавляем все оценки этого студента по данному курсу
            grades.extend(s.grades[course])
    # Если нет ни одной оценки – возвращаем 0
    if not grades:
        return 0
    # Возвращаем среднее арифметическое
    return sum(grades) / len(grades)


# Функция для вычисления средней оценки за лекции у группы лекторов по конкретному курсу
def average_lecturer_grade_for_course(lecturers, course):
    """
    Вычисляет среднюю оценку за лекции у списка лекторов по указанному курсу.
    """
    # Список для сбора оценок лекторов
    grades = []
    # Проходим по каждому лектору
    for l in lecturers:
        # Если объект – лектор и у него есть оценки по курсу
        if isinstance(l, Lecturer) and course in l.grades:
            # Добавляем оценки
            grades.extend(l.grades[course])
    # Если оценок нет – 0
    if not grades:
        return 0
    # Среднее арифметическое
    return sum(grades) / len(grades)


# Блок демонстрации работы (выполняется только при запуске этого файла, а не при импорте)
if __name__ == '__main__':
    # Создаём экземпляр лектора Иванова
    lecturer1 = Lecturer('Иван', 'Иванов')
    # Создаём второго лектора Петрову
    lecturer2 = Lecturer('Мария', 'Петрова')
    # Создаём проверяющего Петрова
    reviewer1 = Reviewer('Пётр', 'Петров')
    # Создаём второго проверяющего Сидорову
    reviewer2 = Reviewer('Анна', 'Сидорова')
    # Создаём студентку Алёхину
    student1 = Student('Ольга', 'Алёхина', 'Ж')
    # Создаём студента Смирнова
    student2 = Student('Игорь', 'Смирнов', 'М')

    # Закрепляем за лектором Ивановым курсы Python и C++
    lecturer1.courses_attached += ['Python', 'C++']
    # Лектор Петрова закреплена за Python и Java
    lecturer2.courses_attached += ['Python', 'Java']
    # Проверяющий Петров закреплён за Python и C++
    reviewer1.courses_attached += ['Python', 'C++']
    # Проверяющая Сидорова закреплена за Python и Java
    reviewer2.courses_attached += ['Python', 'Java']

    # Студентка Алёхина изучает Python и Java
    student1.courses_in_progress += ['Python', 'Java']
    # Студент Смирнов изучает Python и C++
    student2.courses_in_progress += ['Python', 'C++']
    # Задаём список завершённых курсов для Алёхиной
    student1.finished_courses = ['Введение в программирование']
    # Задаём завершённые курсы для Смирнова
    student2.finished_courses = ['Основы Git']

    # Проверяющий Петров выставляет оценки студентке Алёхиной по Python
    reviewer1.rate_hw(student1, 'Python', 10)
    # Ещё одну оценку по Python
    reviewer1.rate_hw(student1, 'Python', 8)
    # Проверяющая Сидорова выставляет оценку по Java
    reviewer2.rate_hw(student1, 'Java', 9)
    # Петров оценивает Смирнова по Python
    reviewer1.rate_hw(student2, 'Python', 7)
    # Петров оценивает Смирнова по C++
    reviewer1.rate_hw(student2, 'C++', 6)

    # Алёхина оценивает лекцию Иванова по Python
    student1.rate_lecture(lecturer1, 'Python', 10)
    # Алёхина оценивает лекцию Петровой по Java
    student1.rate_lecture(lecturer2, 'Java', 8)
    # Смирнов оценивает лекцию Иванова по C++
    student2.rate_lecture(lecturer1, 'C++', 9)
    # Смирнов оценивает лекцию Петровой по Python
    student2.rate_lecture(lecturer2, 'Python', 7)

    # Вывод информации о проверяющих
    print('=== Проверяющие ===')
    print(reviewer1)  # вызов __str__ для Петрова
    print()
    print(reviewer2)  # вызов __str__ для Сидоровой
    print()

    # Вывод информации о лекторах
    print('=== Лекторы ===')
    print(lecturer1)  # вызов __str__ для Иванова
    print()
    print(lecturer2)  # вызов __str__ для Петровой
    print()

    # Вывод информации о студентах
    print('=== Студенты ===')
    print(student1)   # вызов __str__ для Алёхиной
    print()
    print(student2)   # вызов __str__ для Смирнова
    print()

    # Демонстрация сравнения лекторов
    print('Сравнение лекторов по средней оценке:')
    print(f'{lecturer1.name} > {lecturer2.name}: {lecturer1 > lecturer2}')  # сравнение через __gt__
    print(f'{lecturer1.name} == {lecturer2.name}: {lecturer1 == lecturer2}')  # сравнение через __eq__

    # Демонстрация сравнения студентов
    print('\nСравнение студентов по средней оценке:')
    print(f'{student1.name} > {student2.name}: {student1 > student2}')  # __gt__
    print(f'{student1.name} < {student2.name}: {student1 < student2}')  # __lt__

    # Вызов функций для подсчёта средних оценок по курсу
    print('\nСредняя оценка студентов по курсу Python:',
          average_student_grade_for_course([student1, student2], 'Python'))
    print('Средняя оценка лекторов по курсу Python:',
          average_lecturer_grade_for_course([lecturer1, lecturer2], 'Python'))