def calcAverageGrades(grades):
    if not grades:
        return 0
    result = 0
    sum_lp = 0
    for grade in grades:
        if grade.weighted:
            sum_lp += grade.creditpoints
            result += grade.value * grade.creditpoints
    if sum_lp == 0:
        return 0
    return result/sum_lp
