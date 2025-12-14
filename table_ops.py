import copy

# Базовые операции
def get_rows_by_number(t, start, stop=None, copy_t=False):
    rows = t.data[start:stop] if stop else [t.data[start]]
    return _copy_or_ref(t, rows, copy_t)

def get_rows_by_index(t, *vals, copy_t=False):
    rows = [r for r in t.data if r and r[0] in vals]
    return _copy_or_ref(t, rows, copy_t)

def _copy_or_ref(t, rows, copy_t):
    if copy_t:
        return Table(data=copy.deepcopy(rows), 
                    headers=copy.deepcopy(t.headers), 
                    types=copy.deepcopy(t.types))
    return Table(data=rows, headers=t.headers, types=t.types)

def get_column_types(t, by_num=True):
    type_map = {datetime:'datetime', bool:'bool', int:'int', float:'float', str:'str'}
    return {(i if by_num else t.headers[i] if i<len(t.headers) else f"col_{i}"): 
            type_map.get(t,'str') for i,t in t.types.items()}

def set_column_types(t, types_dict, by_num=True):
    type_map = {'datetime':datetime, 'bool':bool, 'int':int, 'float':float, 'str':str}
    for k,v in types_dict.items():
        idx = k if by_num else t.headers.index(k)
        t.types[idx] = type_map.get(v,str)
        for r in t.data:
            if idx < len(r):
                r[idx] = t._conv(r[idx], idx)

def get_values(t, col=0):
    idx = col if isinstance(col,int) else t.headers.index(col)
    return [r[idx] if idx<len(r) else None for r in t.data]

def get_value(t, col=0):
    if len(t.data)!=1: raise ValueError("Нужна 1 строка")
    return get_values(t, col)[0]

def set_values(t, vals, col=0):
    idx = col if isinstance(col,int) else t.headers.index(col)
    for i,r in enumerate(t.data):
        if idx<len(r):
            r[idx] = t._conv(vals[i], idx) if i<len(vals) else None
        elif i<len(vals):
            r.append(t._conv(vals[i], idx))

def set_value(t, val, col=0):
    set_values(t, [val], col)

def print_table(t, width=15, ret=False):
    if not t.data and not t.headers: return ""
    all_rows = [t.headers] if t.headers else []
    all_rows.extend(t.data)
    col_w = [min(max(len(str(r[i])) for r in all_rows if i<len(r)), width) 
            for i in range(max(len(r) for r in all_rows) if all_rows else 0)]
    
    lines = []
    if t.headers:
        h = " | ".join(str(h)[:col_w[i]].ljust(col_w[i]) for i,h in enumerate(t.headers) if i<len(col_w))
        lines.append(h); lines.append("-"*len(h))
    
    for r in t.data:
        line = " | ".join(str(r[i])[:col_w[i]].ljust(col_w[i]) if i<len(r) else "".ljust(col_w[i]) 
                         for i in range(len(col_w)))
        lines.append(line)
    
    result = "\n".join(lines) + "\n"
    return result if ret else print(result)

# Арифметические операции
def _arith_op(t, col1, col2, op):
    idx1 = col1 if isinstance(col1,int) else t.headers.index(col1)
    idx2 = col2 if isinstance(col2,int) else t.headers.index(col2)
    
    if t.types.get(idx1, str) not in (int, float, bool) or t.types.get(idx2, str) not in (int, float, bool):
        raise ValueError("Типы должны быть int, float или bool")
    
    result = []
    for r in t.data:
        v1 = r[idx1] if idx1<len(r) else None
        v2 = r[idx2] if idx2<len(r) else None
        if v1 is None or v2 is None:
            result.append(None)
        else:
            try:
                if op == '+': result.append(v1 + v2)
                elif op == '-': result.append(v1 - v2)
                elif op == '*': result.append(v1 * v2)
                elif op == '/': result.append(v1 / v2 if v2 != 0 else None)
            except: result.append(None)
    return result

add = lambda t,c1,c2: _arith_op(t,c1,c2,'+')
sub = lambda t,c1,c2: _arith_op(t,c1,c2,'-')
mul = lambda t,c1,c2: _arith_op(t,c1,c2,'*')
div = lambda t,c1,c2: _arith_op(t,c1,c2,'/')

# Операции сравнения
def _cmp(t, col1, col2, op):
    vals1 = get_values(t, col1)
    if isinstance(col2, (int, str)):
        vals2 = get_values(t, col2)
    else:
        vals2 = [col2] * len(t.data)
    
    ops = {'==': lambda a,b: a==b, '!=': lambda a,b: a!=b,
           '>': lambda a,b: a>b, '<': lambda a,b: a<b,
           '>=': lambda a,b: a>=b, '<=': lambda a,b: a<=b}
    
    return [ops[op](v1, v2) if v1 is not None and v2 is not None else False 
            for v1, v2 in zip(vals1, vals2)]

eq = lambda t,c1,c2: _cmp(t,c1,c2,'==')
ne = lambda t,c1,c2: _cmp(t,c1,c2,'!=')
gr = lambda t,c1,c2: _cmp(t,c1,c2,'>')
ls = lambda t,c1,c2: _cmp(t,c1,c2,'<')
ge = lambda t,c1,c2: _cmp(t,c1,c2,'>=')
le = lambda t,c1,c2: _cmp(t,c1,c2,'<=')

# Фильтрация
def filter_rows(t, bools, copy_t=False):
    rows = [r for r, b in zip(t.data, bools) if b]
    return _copy_or_ref(t, rows, copy_t)
