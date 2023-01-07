class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lect(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and course in
                lecturer.courses_attached and course in
                self.courses_in_progress or course in self.finished_courses):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        all_grades = []

        for course in self.grades:
            all_grades.extend(self.grades[course])

        if len(all_grades) > 0:
            avg_grade = round(sum(all_grades) / len(all_grades), 1)
        else:
            avg_grade = 0

        courses_in_progress_str = ", ".join(self.courses_in_progress)
        finished_courses_str = ", ".join(self.finished_courses)

        preview = f"Имя: {self.name}\nФамилия: {self.surname}\n"
        preview += f"Средняя оценка за домашние задания: {avg_grade}\n"
        preview += f"Курсы в процессе изучения: {courses_in_progress_str}\n"
        preview += f"Завершенные курсы: {finished_courses_str}"
        return preview

    def __eq__(self, other):
        if isinstance(other, Student):
            self_grades = []
            other_grades = []

            for course in self.grades:
                self_grades.extend(self.grades[course])

            for course in other.grades:
                other_grades.extend(other.grades[course])

            if len(self_grades) > 0:
                self_avg_grade = sum(self_grades) / len(self_grades)
            else:
                self_avg_grade = 0

            if len(other_grades) > 0:
                other_avg_grade = sum(other_grades) / len(other_grades)
            else:
                other_avg_grade = 0

            return self_avg_grade == other_avg_grade

    def __lt__(self, other):
        if isinstance(other, Student):
            self_grades = []
            other_grades = []

            for course in self.grades:
                self_grades.extend(self.grades[course])

            for course in other.grades:
                other_grades.extend(other.grades[course])

            if len(self_grades) > 0:
                self_avg_grade = sum(self_grades) / len(self_grades)
            else:
                self_avg_grade = 0

            if len(other_grades) > 0:
                other_avg_grade = sum(other_grades) / len(other_grades)
            else:
                other_avg_grade = 0

            return self_avg_grade < other_avg_grade

    def __le__(self, other):
        if isinstance(other, Student):
            self_grades = []
            other_grades = []

            for course in self.grades:
                self_grades.extend(self.grades[course])

            for course in other.grades:
                other_grades.extend(other.grades[course])

            if len(self_grades) > 0:
                self_avg_grade = sum(self_grades) / len(self_grades)
            else:
                self_avg_grade = 0

            if len(other_grades) > 0:
                other_avg_grade = sum(other_grades) / len(other_grades)
            else:
                other_avg_grade = 0

            return self_avg_grade <= other_avg_grade


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and isinstance(self, Reviewer) and
                course in self.courses_attached and course in
                student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        all_grades = []

        for course in self.grades:
            all_grades.extend(self.grades[course])

        if len(all_grades) > 0:
            avg_grade = round(sum(all_grades) / len(all_grades), 1)
        else:
            avg_grade = 0
        preview = f"Имя: {self.name}\nФамилия: {self.surname}\n"
        preview += f"Средняя оценка за лекции: {avg_grade}"

        return preview

    def __eq__(self, other):
        if isinstance(other, Lecturer):
            self_grades = []
            other_grades = []

            for course in self.grades:
                self_grades.extend(self.grades[course])

            for course in other.grades:
                other_grades.extend(other.grades[course])

            if len(self_grades) > 0:
                self_avg_grade = sum(self_grades) / len(self_grades)
            else:
                self_avg_grade = 0

            if len(other_grades) > 0:
                other_avg_grade = sum(other_grades) / len(other_grades)
            else:
                other_avg_grade = 0

            return self_avg_grade == other_avg_grade

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            self_grades = []
            other_grades = []

            for course in self.grades:
                self_grades.extend(self.grades[course])

            for course in other.grades:
                other_grades.extend(other.grades[course])

            if len(self_grades) > 0:
                self_avg_grade = sum(self_grades) / len(self_grades)
            else:
                self_avg_grade = 0

            if len(other_grades) > 0:
                other_avg_grade = sum(other_grades) / len(other_grades)
            else:
                other_avg_grade = 0

            return self_avg_grade < other_avg_grade

    def __le__(self, other):
        if isinstance(other, Lecturer):
            self_grades = []
            other_grades = []

            for course in self.grades:
                self_grades.extend(self.grades[course])

            for course in other.grades:
                other_grades.extend(other.grades[course])

            if len(self_grades) > 0:
                self_avg_grade = sum(self_grades) / len(self_grades)
            else:
                self_avg_grade = 0

            if len(other_grades) > 0:
                other_avg_grade = sum(other_grades) / len(other_grades)
            else:
                other_avg_grade = 0

            return self_avg_grade <= other_avg_grade


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        preview = f"Имя: {self.name}\nФамилия: {self.surname}"
        return preview


def student_avg_course_grade(students, course):
    all_grades = []

    for student in students:
        if course in student.grades:
            all_grades.extend(student.grades[course])

    if len(all_grades) > 0:
        avg_grade = round(sum(all_grades) / len(all_grades), 1)
    else:
        return f"За курс {course} студенты ещё не получали оценок."

    return f"Средняя оценка студентов за курс {course}: {avg_grade}"


def lecturer_avg_course_grade(lecturers, course):
    all_grades = []

    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])

    if len(all_grades) > 0:
        avg_grade = round(sum(all_grades) / len(all_grades), 1)
    else:
        return f"За курс {course} лекторы ещё не получали оценок."

    return f"Средняя оценка лекторов за курс {course}: {avg_grade}"


def main():
    student1 = Student("Patrick", "Mahomes", "man")
    student2 = Student("Justin", "Fields", "dog")
    reviewer1 = Reviewer("Tom", "Brady")
    reviewer2 = Reviewer("Aaron", "Rogers")
    lecturer1 = Lecturer("William", "Belichik")
    lecturer2 = Lecturer("Urban", "Meyer")

    student1.finished_courses += ["C++"]
    student1.courses_in_progress += ["Python", "SQL", "R"]

    student2.finished_courses += ["C++"]
    student2.courses_in_progress += ["Python", "R"]

    lecturer1.courses_attached += ["C++", "Python", "R", "SQL"]
    lecturer2.courses_attached += ["SQL", "R"]

    reviewer1.courses_attached += ["C++", "Python", "R", "SQL"]
    reviewer2.courses_attached += ["C++", "Python", "SQL", "R"]

    student1.rate_lect(lecturer1, "C++", 10)
    student1.rate_lect(lecturer1, "Python", 8)
    student1.rate_lect(lecturer1, "R", 10)
    student1.rate_lect(lecturer1, "SQL", 9)
    student1.rate_lect(lecturer2, "R", 2)
    student1.rate_lect(lecturer2, "SQL", 4)

    student2.rate_lect(lecturer1, "C++", 10)
    student2.rate_lect(lecturer1, "Python", 10)
    student2.rate_lect(lecturer1, "R", 10)
    student2.rate_lect(lecturer2, "R", 5)

    reviewer1.rate_hw(student1, "Python", 10)
    reviewer1.rate_hw(student1, "R", 10)
    reviewer1.rate_hw(student1, "SQL", 9)
    reviewer1.rate_hw(student2, "Python", 6)
    reviewer1.rate_hw(student2, "R", 4)

    reviewer2.rate_hw(student1, "Python", 10)
    reviewer2.rate_hw(student1, "R", 10)
    reviewer2.rate_hw(student1, "SQL", 10)

    reviewer2.rate_hw(student2, "Python", 5)
    reviewer2.rate_hw(student2, "R", 5)

    print("Студенты:\n")
    print(student1, '\n')
    print(student2, '\n')
    print("Лекторы:\n")
    print(lecturer1, '\n')
    print(lecturer2, '\n')
    print("Проверяющие:\n")
    print(reviewer1, '\n')
    print(reviewer2, '\n')

    if lecturer1 > lecturer2:
        print(f"Средняя оценка у {lecturer1.name} {lecturer1.surname} выше.")
    elif lecturer1 == lecturer2:
        prompt = f"Средняя оценка у лекторов {lecturer1.surname} и "
        prompt += f"{lecturer2.surname} равна."
        print(prompt)
    else:
        print(f"Средняя оценка у {lecturer2.name} {lecturer2.surname} выше.")

    if student1 > student2:
        print(f"Средняя оценка у {student1.name} {student1.surname} выше.")
    elif student1 == student2:
        prompt = f"Средняя оценка у студнтов {student1.surname} и "
        prompt += f"{student2.surname} равна."
        print(prompt)
    else:
        print(f"Средняя оценка у {student2.name} {student2.surname} выше.")

    print()

    students = [student1, student2]
    lecturers = [lecturer1, lecturer2]
    courses = ["Python", "C++", "R", "SQL"]

    for course in courses:
        print(lecturer_avg_course_grade(lecturers, course))
        print(student_avg_course_grade(students, course), "\n")


if __name__ == '__main__':
    main()