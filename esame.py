class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name
    

    def get_data(self):
        values = []
        #provo ad aprire il file e leggerlo
        try: 
            my_file = open(self.name, 'r')
            lines = my_file.readlines()
            my_file.close()
        except:
            raise ExamException("Errore nella lettura del file")
        
        old_elements = None
        
        #divido le line ad ogni virgola
        for line in lines:
            elements = line.split(',')

            
            try:
                elements[1] = int(elements[1])
            except:
                continue

            if len(elements) <2:
                continue

            if len(elements) > 2:
                elements = elements[:2]

            if elements[1] <= 0:
                continue

            if len(elements[0]) < 7:
                continue

            date = elements[0].split("-")

            if len(date) != 2:
                continue

            if not date[0].isdigit() or not date[1].isdigit():
                continue

            if(int(date[1]) < 1 or int(date[1]) > 12):
                continue

            if old_elements is not None:
                if elements[0] == old_elements[0]:
                    raise ExamException("date duplicate")
                
                old_date = old_elements[0].split("-")

                if old_date[0] == date[0] and old_date[1] > date[1]:
                    raise ExamException("i mesi non sono in ordine")
                
                if old_date[0] > date[0]:
                    raise ExamException("Gli anni non sono in ordine")
                
            old_elements = elements
            
            values.append(['-'.join(date), elements[1]])

        return values


def find_min_max(time_series):

    if not time_series:
        return {}
    
    dictionary = {}
    
    cont = 0
    primo_anno = 0

    # primo_anno = int(time_series[0][0].split('-')[0])
    # ultimo_anno = int(time_series[-1][0].split('-')[0])

    for el in time_series:
        p = el[1]
        el = el[0].split('-')
        el.append(p)

        anno_corr = int(el[0])

        if primo_anno == 0:
            primo_anno = anno_corr
        
        if cont == 0:
            prev_year = anno_corr
            cont += 1
        
        else:
            if prev_year != anno_corr:
                cont +=1
                prev_year = anno_corr
    
    i = 0

    while(i < cont):
        calcio = primo_anno
        
        max = []
        min = []
        max_min = {}

        for elements in time_series:
            p = elements[1]
            elements = elements[0].split('-')
            elements.append(p)

            if primo_anno == int(elements[0]):
                if max == [] and min == []:
                    if max == []:
                        valore_massimo = elements[2]
                        max.append(elements[1])

                    if min == []:
                        val_min = elements[2]
                        min.append(elements[1])

                else:
                    if valore_massimo == elements[2]:
                        max.append(elements[1])

                    if val_min == elements[2]:
                        min.append(elements[1])

                    if valore_massimo < elements[2]:
                        valore_massimo = elements[2]
                        max.clear()
                        max.append(elements[1])

                    if val_min > elements[2]:
                        val_min = elements[2]
                        min.clear()
                        min.append(elements[1])
        
        max_min.update({'max': max, 'min': min})
        
        dictionary.update({str(primo_anno): max_min})
        
        primo_anno = calcio + 1

        i += 1

    return dictionary



# tim_series_file = CSVTimeSeriesFile('shampoo_sales.csv')
# time_series = tim_series_file.get_data()
# print(time_series)

# print(find_min_max(time_series))