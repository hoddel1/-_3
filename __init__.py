from datetime import datetime

class Table:
    def __init__(self, data=None, headers=None, types=None, auto=False):
        self.data = data or []
        self.headers = headers or []
        self.types = types or {}
        
        if auto and self.data:
            self.types = self._detect()
            self._convert_all()
    
    def _detect(self):
        if not self.data: return {}
        cols = max(len(r) for r in self.data)
        types = {}
        
        for i in range(cols):
            vals = [str(r[i]).strip() for r in self.data if i<len(r) and r[i] not in (None, '')]
            if not vals: types[i] = str; continue
            
            # Проверка типов
            dt_ok = all(_try_dt(v) for v in vals)
            bool_ok = all(v.lower() in ('true','false','1','0','yes','no','y','n','t','f') for v in vals)
            int_ok = all(v.replace('-','',1).isdigit() and '.' not in v for v in vals)
            float_ok = all(_try_float(v) for v in vals)
            
            if dt_ok: types[i] = datetime
            elif bool_ok: types[i] = bool
            elif int_ok: types[i] = int
            elif float_ok: types[i] = float
            else: types[i] = str
        
        return types
    
    def _convert_all(self):
        for r in self.data:
            for i, t in self.types.items():
                if i < len(r):
                    r[i] = self._conv(r[i], i)
    
    def _conv(self, v, i):
        if v is None: return None
        if i not in self.types: return v
        t = self.types[i]
        try:
            if t == datetime: return _to_dt(v)
            if t == bool: return str(v).lower() in ('true','1','yes','y','t')
            if t == int: return int(float(v)) if isinstance(v,str) else int(v)
            if t == float: return float(v)
            return str(v)
        except:
            return v

def _try_dt(v):
    for f in ['%Y-%m-%d', '%d.%m.%Y', '%Y/%m/%d', '%Y-%m-%d %H:%M:%S']:
        try: datetime.strptime(str(v), f); return True
        except: pass
    return False

def _to_dt(v):
    if isinstance(v, datetime): return v
    for f in ['%Y-%m-%d', '%d.%m.%Y', '%Y/%m/%d', '%Y-%m-%d %H:%M:%S']:
        try: return datetime.strptime(str(v), f)
        except: pass
    return str(v)

def _try_float(v):
    try: float(v); return True
    except: return False

detect_types = lambda d: Table._detect(d)
