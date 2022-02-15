def empty_table():
    e = []
    for i in range(0,10):
        p = []
        for d in range(0, 10):
            p.append(0)
        e.append(p)
    return e
            
def load_buildings(buildings):
    t = empty_table()
    for i in buildings:
        coord = i['coordinates']
        t[coord[0]][coord[1]] = i['name']
    return t

def get_building(lists, building):
    for i in lists:
        if i[0] == building:
            return i
    return None

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T', 'q', 'Q', 's', 'S', 'O', 'N', 'D'][magnitude])