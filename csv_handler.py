import csv

def load_table(file, delim=',', headers=True, auto=False):
    with open(file, 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f, delimiter=delim))
    
    h = rows[0] if headers and rows else [f"col_{i}" for i in range(len(rows[0]))] if rows else []
    d = rows[1:] if headers and rows else rows
    
    return Table(data=d, headers=h, auto=auto)

def save_table(table, file, delim=',', headers=True):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=delim)
        if headers and table.headers: w.writerow(table.headers)
        w.writerows([[v if v is not None else '' for v in r] for r in table.data])
