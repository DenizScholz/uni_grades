def calcAverageGrades(grades):
    if not grades:
        return 0
    result = 0
    sum_lp = 0
    for grade in grades:
        sum_lp += grade.creditpoints
        result += grade.value * grade.creditpoints
    return result/sum_lp
