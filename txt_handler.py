def save_table(table, file):
    from .table_ops import print_table
    with open(file, 'w', encoding='utf-8') as f:
        f.write(print_table(table, ret=True))
