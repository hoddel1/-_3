import pickle

def load_table(file, auto=False):
    with open(file, 'rb') as f:
        d = pickle.load(f)
    return Table(data=d.get('data'), headers=d.get('headers'), types=d.get('types'), auto=auto)

def save_table(table, file):
    with open(file, 'wb') as f:
        pickle.dump({'data': table.data, 'headers': table.headers, 'types': table.types}, f)
