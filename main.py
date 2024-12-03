from typing import List


class GradableMixin:
    """
    Base mixin class for any object that can receive grades for courses
    and can be compared based on the average grade.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grades = {}

    def __eq__(self, other):
        return self.average_grade == other.average_grade

    def __ne__(self, other):
        return self.average_grade != other.average_grade

    def __lt__(self, other):
        return self.average_grade < other.average_grade

    def __le__(self, other):
        return self.average_grade <= other.average_grade

    def __gt__(self, other):
        return self.average_grade > other.average_grade

    def __ge__(self, other):
        return self.average_grade >= other.average_grade

    @property
    def average_grade(self) -> float:
        """Calculates average grade among all courses."""
        count, total = 0, 0
        for grades in self.grades.values():
            count += len(grades)
            total += sum(grades)
        return total / count if count > 0 else 0


class Student(GradableMixin):

    def __init__(self, name: str, surname: str, gender: str):
        super().__init__()
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []

    def __str__(self):
        lines = (
            f'Имя: {self.name}',
            f'Фамилия: {self.surname}',
            f'Средняя оценка за домашние задания: {self.average_grade:.1f}',
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}",
            f"Завершенные курсы: {', '.join(self.finished_courses)}"
        )
        return '\n'.join(lines)

    def rate_lecturer(self, lecturer: GradableMixin, course: str, grade: int) -> bool:
        """
        Adds a course grade to a lecturer. Returns True if a grade was
        successfully added, False otherwise.

        A student can give a lecturer a grade only for a finished
        course. Also, the lecturer must be attached to the course, and
        the grade itself must be between 1 and 10.

        """
        if (1 <= grade <= 10 and
                isinstance(lecturer, Lecturer) and
                course in self.finished_courses and
                course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
            return True
        return False


class Mentor:
    """Base class for lecturers and reviewers."""

    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(GradableMixin, Mentor):
    """A mentor that can receive grades from students."""

    def __str__(self):
        lines = (
            f'Имя: {self.name}',
            f'Фамилия: {self.surname}',
            f'Средняя оценка за лекции: {self.average_grade:.1f}',
        )
        return '\n'.join(lines)


class Reviewer(Mentor):
    """A mentor that can give grades to students."""

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def rate_hw(self, student: GradableMixin, course: str, grade: int) -> bool:
        """
        Adds a homework grade to a student. Returns True if a grade was
        successfully added, False otherwise.

        A reviewer can give a student a grade only for a course they
        are attached to. Also, the student must be learning the course,
        and the grade itself must be between 1 and 10.

        """
        if (1 <= grade <= 10 and
                isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
            return True
        return False


def course_average_grade(course: str, people: List[GradableMixin]) -> float:
    """
    Calculates average grade for a course among given people (students
    or lecturers).

    """
    count, total = 0, 0
    for person in people:
        if course in person.grades:
            count += len(person.grades[course])
            total += sum(person.grades[course])
    return total / count if count > 0 else 0


# Fixed testing.
# Create test instances.
student_1 = Student('John', 'Miller', 'male')
student_1.courses_in_progress += ['Python']
student_1.finished_courses += ['PHP', 'TypeScript']
student_2 = Student('Jane', 'Moore', 'female')
student_2.courses_in_progress += ['PHP', 'Python']
student_2.finished_courses += ['TypeScript']
lecturer_1 = Lecturer('James', 'Martin')
lecturer_1.courses_attached += ['Python']
lecturer_2 = Lecturer('Jennifer', 'Martinez')
lecturer_2.courses_attached += ['PHP', 'TypeScript']
reviewer_1 = Reviewer('Joseph', 'Mitchell')
reviewer_1.courses_attached += ['PHP', 'Python']
reviewer_2 = Reviewer('Jessica', 'Morris')
reviewer_2.courses_attached += ['Python', 'TypeScript']
# Test string presentation of newly created instances.
assert str(student_1) == ('Имя: John\n'
                          'Фамилия: Miller\n'
                          'Средняя оценка за домашние задания: 0.0\n'
                          'Курсы в процессе изучения: Python\n'
                          'Завершенные курсы: PHP, TypeScript')
assert str(student_2) == ('Имя: Jane\n'
                          'Фамилия: Moore\n'
                          'Средняя оценка за домашние задания: 0.0\n'
                          'Курсы в процессе изучения: PHP, Python\n'
                          'Завершенные курсы: TypeScript')
assert str(lecturer_1) == ('Имя: James\n'
                           'Фамилия: Martin\n'
                           'Средняя оценка за лекции: 0.0')
assert str(lecturer_2) == ('Имя: Jennifer\n'
                           'Фамилия: Martinez\n'
                           'Средняя оценка за лекции: 0.0')
assert str(reviewer_1) == 'Имя: Joseph\nФамилия: Mitchell'
assert str(reviewer_2) == 'Имя: Jessica\nФамилия: Morris'
# Test conditions that all should result in false assignments.
assert not student_1.rate_lecturer(lecturer_1, 'Python', 10)
assert not student_1.rate_lecturer(lecturer_1, 'PHP', 10)
assert not student_1.rate_lecturer(lecturer_2, 'Python', 10)
assert not student_1.rate_lecturer(lecturer_2, 'TypeScript', 0)
assert not student_1.rate_lecturer(lecturer_2, 'TypeScript', -1)
assert not student_2.rate_lecturer(lecturer_1, 'Python', 5)
assert not student_2.rate_lecturer(lecturer_1, 'TypeScript', 5)
assert not student_2.rate_lecturer(lecturer_2, 'PHP', 5)
assert not student_2.rate_lecturer(lecturer_2, 'TypeScript', 15)
assert not reviewer_1.rate_hw(student_1, 'PHP', 1)
assert not reviewer_1.rate_hw(student_1, 'Python', -1)
assert not reviewer_1.rate_hw(student_1, 'TypeScript', 10)
assert not reviewer_1.rate_hw(student_2, 'TypeScript', 5)
assert not reviewer_1.rate_hw(student_2, 'PHP', 15)
assert not reviewer_2.rate_hw(student_1, 'TypeScript', 10)
assert not reviewer_2.rate_hw(student_1, 'PHP', 10)
assert not reviewer_2.rate_hw(student_2, 'PHP', 10)
assert not reviewer_2.rate_hw(student_2, 'TypeScript', 10)
# No one should have received any grade so far.
assert student_1.grades == {}
assert student_2.grades == {}
assert lecturer_1.grades == {}
assert lecturer_2.grades == {}
assert student_1.average_grade == 0
assert student_2.average_grade == 0
assert lecturer_1.average_grade == 0
assert lecturer_2.average_grade == 0
# Now students and lecturers should get some grades.
assert student_1.rate_lecturer(lecturer_2, 'PHP', 8)
assert student_1.rate_lecturer(lecturer_2, 'TypeScript', 9)
assert student_2.rate_lecturer(lecturer_2, 'TypeScript', 6)
assert reviewer_1.rate_hw(student_1, 'Python', 9)
assert reviewer_1.rate_hw(student_2, 'PHP', 6)
assert reviewer_1.rate_hw(student_2, 'Python', 8)
assert reviewer_2.rate_hw(student_1, 'Python', 10)
assert reviewer_2.rate_hw(student_2, 'Python', 10)
# Test grades structure.
assert student_1.grades == {'Python': [9, 10]}
assert student_2.grades == {'PHP': [6], 'Python': [8, 10]}
assert lecturer_2.grades == {'PHP': [8], 'TypeScript': [9, 6]}
# Test people's average grades.
assert student_1.average_grade == 9.5
assert student_2.average_grade == 8
assert abs(lecturer_2.average_grade - 7.666667) < 1e-5
# Compare student_1 with student_2 and lecturer_1 with lecturer_2.
assert student_1 > student_2
assert student_1 >= student_2
assert student_1 != student_2
assert not (student_1 < student_2)
assert not (student_1 <= student_2)
assert not (student_1 == student_2)
assert lecturer_2 > lecturer_1
assert lecturer_2 >= lecturer_1
assert lecturer_2 != lecturer_1
assert not (lecturer_2 < lecturer_1)
assert not (lecturer_2 <= lecturer_1)
assert not (lecturer_2 == lecturer_1)
# We can even compare students with lectures ¯\_(ツ)_/¯
assert student_1 > student_2 > lecturer_2 > lecturer_1
# Test average grades per course.
assert course_average_grade('Python', [student_1, student_2]) == 9.25
assert course_average_grade('PHP', [student_1, student_2]) == 6
assert course_average_grade('TypeScript', [student_1, student_2]) == 0
assert course_average_grade('Python', [lecturer_1, lecturer_2]) == 0
assert course_average_grade('PHP', [lecturer_1, lecturer_2]) == 8
assert course_average_grade('TypeScript', [lecturer_1, lecturer_2]) == 7.5
# Finally, check if string representation still works well.
assert str(student_1) == ('Имя: John\n'
                          'Фамилия: Miller\n'
                          'Средняя оценка за домашние задания: 9.5\n'
                          'Курсы в процессе изучения: Python\n'
                          'Завершенные курсы: PHP, TypeScript')
assert str(student_2) == ('Имя: Jane\n'
                          'Фамилия: Moore\n'
                          'Средняя оценка за домашние задания: 8.0\n'
                          'Курсы в процессе изучения: PHP, Python\n'
                          'Завершенные курсы: TypeScript')
assert str(lecturer_2) == ('Имя: Jennifer\n'
                           'Фамилия: Martinez\n'
                           'Средняя оценка за лекции: 7.7')
