
def reverse_numbers(grades):
    new_grades = []
    for i in grades:
        a = int(i / 10)
        b = int(i % 10)
        new_number = b*10 + a
        new_grades.append(new_number)
    return new_grades

old_grades = [35, 46, 57, 91, 29]
new_grades = reverse_numbers(old_grades)
print(f"輸入:{old_grades}")
print(f"輸出:{new_grades}")