## Основная функция, которая считает совместное пребывание на уроке
def appearance(intervals):

    # Для оптимизации убираем необходимость сверять интервалы учителя и ученика с интервалом урока 
    # путем сужения границ интервала до границ урока
    intervals['pupil'] = make_in_shape(intervals['pupil'], intervals['lesson'])
    intervals['tutor'] = make_in_shape(intervals['tutor'], intervals['lesson'])

    # Внутри каждого списков учителя и ученика структурируем интервалы в подсписки, а затем 
    # преобразуем пересекающиеся диапазоны внутри одного списка
    pupil = get_intervals(intervals['pupil'])
    pupil = make_intersection_intervals(pupil)

    tutor = get_intervals(intervals['tutor'])
    tutor = make_intersection_intervals(tutor)
    

    joint_intervals = 0
    for interval_p in pupil:
        for interval_t in tutor:
            # Вычисляем диапазоны совпадения интервалов и считаем их длину
            # (секунды)
            joint_intervals += len(range(max(interval_p[0], interval_t[0]), 
                                            min(interval_p[-1], interval_t[-1])))

    return joint_intervals
    
## Функция сдвигает границы набора интервалов до границ урока          
def make_in_shape(interval, shape_interval):
    interval[0] = max(interval[0], shape_interval[0])
    interval[-1] = min(interval[-1], shape_interval[-1])
    return interval

## Функция структурирует интервалы на подсписки
def get_intervals(intervals):
    buf = []
    for i in range(0, len(intervals)):
        if not i % 2:
            subbuf = []
            subbuf.append(intervals[i])
            subbuf.append(intervals[i + 1])
            buf.append(subbuf)
    return buf

## Функция ищет внутри одного списка пересечения и соединяет в один подинтервал
def make_intersection_intervals(interval):
    i = 0
    while i < len(interval)-1:
        if len(interval) > 1:
            if interval[i][0] < interval[i + 1][0] and interval[i][-1] > interval[i + 1][0]:
                if interval[i+1][-1] < interval[i][-1]:
                    interval[i] = [interval[i][0], interval[i][-1]]    
                elif interval[i+1][-1] > interval[i][-1]:
                    interval[i] = [interval[i][0], interval[i+1][-1]]
                interval.pop(i+1)
            else:
                i+=1
    return interval

        
tests = [
    {'data': {'lesson': [1594663200, 1594666800],
    
             'pupil': [1594663340, 1594663389, 
                        1594663390, 1594663395, 
                        1594663396, 1594666472],

             'tutor': [1594663290, 1594663430, 
                        1594663443, 1594666473]},
     'answer': 3117
    },
    {'data': {'lesson': [1594702800, 1594706400],
    
             'pupil': [1594702789, 1594704500, 
                        1594702807, 1594704542, 
                        1594704512, 1594704513, 
                        1594704564, 1594705150, 
                        1594704581, 1594704582, 
                        1594704734, 1594705009, 
                        1594705095, 1594705096, 
                        1594705106, 1594706480, 
                        1594705158, 1594705773, 
                        1594705849, 1594706480, 
                        1594706500, 1594706875, 
                        1594706502, 1594706503, 
                        1594706524, 1594706524, 
                        1594706579, 1594706641],

             'tutor': [1594700035, 1594700364, 
                        1594702749, 1594705148, 
                        1594705149, 1594706463]},
    'answer': 3577
    },
    {'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 
                        1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['data'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
