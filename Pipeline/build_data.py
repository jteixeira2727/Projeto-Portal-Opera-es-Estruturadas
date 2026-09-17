import openpyxl, json, re, unicodedata, os
import urllib.parse
from datetime import datetime, date
from openpyxl.utils import column_index_from_string

SRC = '/tmp/ativos.xlsx'
wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
sheetnames = wb.sheetnames

def norm(s):
    if s is None: return ''
    s = str(s)
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode('ascii')
    return re.sub(r'\s+',' ', s).strip().lower()

def to_jsonable(v):
    if isinstance(v, (datetime, date)):
        return v.isoformat()[:10]
    if isinstance(v, float):
        if v != v:  # NaN
            return None
        return round(v, 6)
    if isinstance(v, str):
        return v.strip()
    return v

# ---------- Posições por fundo (transcrito de "Portfólio Atual" no PPT, ref. 07/2026) ----------
# Cada operação do Excel pode estar presente em mais de um dos 7 fundos Mauá Capital.
# Tupla: (fundo, nome no PPT, saldo_curva_mm, saldo_mtm_mm, %ativos_do_fundo, ltv, duration_anos,
#         %_do_cri_detido, tranche, %_subordinacao, taxa, emissor/securitizadora, vencimento, chave_operacao_excel)
# chave_operacao_excel = None quando o ativo do PPT não tem aba correspondente na planilha (gap conhecido).
FUND_POSITION_ROWS = [
    ('MCRED','MSB Edson',61.4,61.4,0.644,0.55,None,1.00,'Única',None,'IPCA + 12,00%','Habitasec','Mai/26','MSB Edson'),
    ('MCRED','Vitacon - Mezanino',33.9,33.9,0.356,0.34,1.3,1.00,'Subordinada',0.35,'CDI + 8,15%','Opea','Dez/29','Vitacon'),

    ('MCRE','LA Shopping',143.4,137.5,0.121,0.38,5.0,1.00,'Única',None,'IPCA + 11,25%','Opea','Jan/39','LA'),
    ('MCRE','Vitacon - Sênior',61.8,61.8,0.054,0.21,1.3,1.00,'Sênior',0.35,'CDI + 4,07%','Opea','Dez/29','Vitacon'),
    ('MCRE','IBL',54.9,53.7,0.047,0.59,5.0,1.00,'Sênior',0.37,'IPCA + 9,70%','Opea','Out/38','IBL'),
    ('MCRE','Business Park',33.8,31.9,0.028,0.36,2.5,1.00,'Única',None,'IPCA + 10,98%','Opea','Nov/31','MZO'),
    ('MCRE','MSB Axis',30.1,30.0,0.026,0.75,2.4,1.00,'Única',None,'IPCA + 11,00%','Habitasec','Abr/29','MSB Axis'),
    ('MCRE','Renda Residencial',5.5,5.0,0.004,0.37,2.6,1.00,'Subordinada',0.20,'IPCA + 15,00%','Habitasec','Ago/32','Renda Residencial'),

    ('MCCE','FII inVista',236.9,236.9,0.154,0.32,5.6,0.934,'Sênior',0.29,'IPCA + 10,44%','N/A','Mai/44','inVista'),
    ('MCCE','Vista Faria Lima',96.5,93.0,0.060,0.64,5.0,0.292,'Única',None,'IPCA + 8,57%','Opea','Nov/32','Vista Faria Lima'),
    ('MCCE','Mega Moda',73.5,71.6,0.047,0.48,3.8,0.385,'Sênior',0.17,'IPCA + 10,20%','Opea','Dez/34','MegaModa'),
    ('MCCE','FII Grand Mercure',71.6,71.6,0.047,0.51,3.5,1.00,'Sênior',0.52,'IPCA + 10,00%','N/A','Set/30', None),
    ('MCCE','MSB Axis',57.0,56.6,0.037,0.75,2.4,1.00,'Única',None,'IPCA + 11,00%','Habitasec','Abr/29','MSB Axis'),
    ('MCCE','FII Planta - Mezanino',56.0,56.0,0.036,None,3.0,1.00,'Mezanino',0.42,'IPCA + 12,00%','N/A','Nov/28','Planta - Ed. Lara'),
    ('MCCE','PKK – IPCA',43.6,40.1,0.026,0.63,3.8,1.00,'Única',None,'IPCA + 10,06%','Opea','Abr/35','PKK'),
    ('MCCE','Ilog - Tamboré',40.1,39.3,0.026,None,3.8,1.00,'Única',None,'IPCA + 9,50%','Leverage','Abr/31','Ilog'),
    ('MCCE','Moby',40.9,38.0,0.025,0.24,3.5,1.00,'Única',None,'IPCA + 10,55%','Opea','Mai/34','Moby'),
    ('MCCE',"Habib's - Sr",36.7,34.2,0.022,0.41,5.1,1.00,'Sênior',0.33,'IPCA + 8,50%','Canal','Jun/38','Habibs'),
    ('MCCE','Apil – CDI',31.8,31.8,0.021,0.27,3.4,1.00,'Única',None,'CDI + 4,50%','Opea','Jul/35','Apil'),
    ('MCCE','MSB Triu',33.4,31.5,0.020,0.47,2.0,1.00,'Única',None,'IPCA + 10,50%','Habitasec','Set/28','MSB Triu'),
    ('MCCE','Apil – IPCA',33.8,29.9,0.019,0.27,4.0,1.00,'Única',None,'IPCA + 9,06%','Opea','Jul/35','Apil'),
    ('MCCE','Pirelli',31.3,29.8,0.019,0.99,5.5,0.857,'Única',None,'IPCA + 8,00%','Canal','Set/39','Pirelli'),
    ('MCCE','PKK – CDI 2',29.2,29.2,0.019,0.63,3.3,1.00,'Única',None,'CDI + 5,00%','Opea','Abr/35','PKK'),
    ('MCCE','OAD',22.7,22.7,0.015,0.65,0.4,0.817,'Única',None,'CDI + 6,00%','Opea','Dez/26','OAD'),
    ('MCCE','Hines',19.4,18.8,0.012,1.00,0.7,1.00,'Única',None,'IPCA + 9,70%','Opea','Dez/27','Hines'),
    ('MCCE',"Habib's – Sub",17.8,16.7,0.011,0.61,4.7,1.00,'Subordinada',0.33,'IPCA + 11,35%','Canal','Jun/38','Habibs'),
    ('MCCE','PKK – CDI',11.7,11.7,0.008,0.63,0.9,1.00,'Única',None,'CDI + 4,78%','Opea','Abr/28','PKK'),
    ('MCCE','LBV',10.7,10.7,0.007,0.29,2.8,1.00,'Sênior',0.38,'CDI + 5,00%','Canal','Jun/33','LBV'),

    ('MCCI','Pirelli',155.1,153.5,0.096,0.99,5.5,0.857,'Única',None,'IPCA + 8,00%','Canal','Set/39','Pirelli'),
    ('MCCI','Newport',159.1,144.6,0.091,0.57,3.2,0.941,'Única',None,'IPCA + 6,72%','Opea','Mai/31','NewPort'),
    ('MCCI','Dutra Log',114.0,112.7,0.071,0.67,3.5,1.00,'Única',None,'IPCA + 8,00%','Opea','Fev/34','Dutra'),
    ('MCCI','Emergent Cold',112.3,106.7,0.067,0.42,5.6,1.00,'Única',None,'IPCA + 10,22%','Vert','Jan/41','ECLA'),
    ('MCCI','Tellus River South',89.2,88.7,0.056,0.35,2.2,0.970,'Única',None,'IPCA + 9,00%','Riza Sec','Fev/29','Tellus River South'),
    ('MCCI','FII York',81.1,74.4,0.047,0.60,3.7,1.00,'Única',None,'IPCA + 7,04%','Riza Sec','Ago/34','FII York'),
    ('MCCI','Superfrio',73.1,71.5,0.045,0.56,2.3,1.00,'Única',None,'IPCA + 9,60%','Opea','Out/31','Superfrio'),
    ('MCCI','Telmec',56.7,52.6,0.033,0.59,5.2,1.00,'Única',None,'IPCA + 8,30%','Opea','Dez/38','Telmec'),
    ('MCCI','Residencial Jardins',57.5,52.3,0.033,0.53,2.4,1.00,'Única',None,'IPCA + 9,25%','Habitasec','Set/32','Residencial Jardins'),
    ('MCCI','Alianza Mauá',53.2,49.1,0.031,0.53,4.1,1.00,'Única',None,'IPCA + 7,20%','Riza Sec','Fev/32','Alianza Mauá'),
    ('MCCI','BRF',49.5,47.6,0.030,0.62,5.4,0.290,'Única',None,'IPCA + 7,50%','Bari Sec','Jan/39','BRF '),
    ('MCCI','Residencial Itaim',39.7,39.2,0.025,0.49,0.5,1.00,'Única',None,'IPCA + 7,85%','Habitasec','Dez/26','Residencial Itaim'),
    ('MCCI','Green Towers',38.7,37.8,0.024,0.78,3.6,0.250,'Única',None,'IPCA + 8,66%','Opea','Dez/34','GT'),
    ('MCCI','JALGP',37.7,36.3,0.023,None,2.2,1.00,'Sênior',0.39,'IPCA + 10,90%','Opea','Dez/30','JALGP'),
    ('MCCI','Evolution',36.7,35.9,0.022,0.43,3.9,0.635,'Única',None,'IPCA + 6,25%','Habitasec','Dez/34','Evolution'),
    ('MCCI','Lux',34.0,33.9,0.021,None,2.9,1.00,'Sênior',0.27,'CDI + 3,00%','Leverage','Fev/31','Lux'),
    ('MCCI','SKR',34.2,32.4,0.020,None,2.7,1.00,'Sênior',0.30,'IPCA + 10,90%','Opea','Dez/32','SKR'),
    ('MCCI','Alianza GRU',31.3,28.1,0.018,0.53,4.1,1.00,'Única',None,'IPCA + 7,20%','Riza Sec','Jan/32','Alianza GRU'),
    ('MCCI','BR Properties',27.0,27.6,0.017,0.36,2.9,0.333,'Única',None,'CDI + 2,00%','Opea','Ago/31','BR Prop'),
    ('MCCI','WT Log',28.1,26.2,0.016,0.26,3.8,1.00,'Única',None,'IPCA + 8,14%','Canal','Dez/35','WT Log'),
    ('MCCI','Villa XP',27.0,21.4,0.013,1.12,7.8,0.040,'Única',None,'IPCA + 5,00%','Riza Sec','Abr/36','Villa XP'),
    ('MCCI','Renda Residencial',15.2,14.2,0.009,0.30,2.9,1.00,'Sênior',0.20,'IPCA + 8,12%','Habitasec','Ago/32','Renda Residencial'),
    ('MCCI','Vogue Square',11.7,13.2,0.008,0.34,2.1,0.857,'Única',None,'IPCA + 12,00%','Habitasec','Dez/29', 'Calçada'),
    ('MCCI','Localfrio',9.5,8.8,0.006,0.49,2.6,0.162,'Sênior',0.20,'IPCA + 6,00%','Riza Sec','Dez/31','Localfrio'),

    ('MCFA','FII York',4.5,4.3,0.095,0.60,3.7,1.00,'Única',None,'IPCA + 7,04%','Riza Sec','Ago/34','FII York'),
    ('MCFA','Newport',4.8,4.2,0.094,0.57,3.2,0.941,'Única',None,'IPCA + 6,72%','Opea','Mai/31','NewPort'),
    ('MCFA','Residencial Jardins',3.9,3.7,0.083,0.53,2.4,1.00,'Única',None,'IPCA + 9,25%','Habitasec','Set/32','Residencial Jardins'),
    ('MCFA','Alianza Mauá',3.6,3.4,0.076,0.53,4.1,1.00,'Única',None,'IPCA + 7,20%','Riza Sec','Fev/32','Alianza Mauá'),
    ('MCFA','Superfrio',3.4,3.3,0.074,0.56,2.3,1.00,'Única',None,'IPCA + 9,60%','Opea','Out/31','Superfrio'),
    ('MCFA','Residencial Itaim',2.7,2.7,0.060,0.49,0.5,1.00,'Única',None,'IPCA + 7,85%','Habitasec','Dez/26','Residencial Itaim'),
    ('MCFA','Green Towers',2.6,2.6,0.058,0.78,3.6,0.250,'Única',None,'IPCA + 8,66%','Opea','Dez/34','GT'),
    ('MCFA','Evolution',2.5,2.3,0.052,0.43,3.9,0.635,'Única',None,'IPCA + 6,25%','Habitasec','Dez/34','Evolution'),
    ('MCFA','Alianza GRU',2.1,2.2,0.048,0.53,4.1,1.00,'Única',None,'IPCA + 7,20%','Riza Sec','Jan/32','Alianza GRU'),
    ('MCFA','Renda Residencial',1.4,1.4,0.030,0.30,2.9,1.00,'Sênior',0.20,'IPCA + 8,12%','Habitasec','Ago/32','Renda Residencial'),
    ('MCFA','Vogue Square',1.2,1.3,0.030,0.34,2.1,0.857,'Única',None,'IPCA + 12,00%','Habitasec','Dez/29', 'Calçada'),
    ('MCFA','Localfrio',0.6,0.6,0.014,0.49,2.6,0.162,'Sênior',0.20,'IPCA + 6,00%','Riza Sec','Dez/31','Localfrio'),

    ('MCEQ','IBL',11.2,10.9,0.090,0.59,5.0,1.00,'Sênior',0.37,'IPCA + 9,70%','Opea','Out/38','IBL'),
    ('MCEQ','Tellus River South',10.4,10.3,0.085,0.35,2.2,0.970,'Única',None,'IPCA + 9,00%','Riza Sec','Fev/29','Tellus River South'),
    ('MCEQ',"Habib's – Sr",10.3,9.6,0.079,0.41,5.1,1.00,'Sênior',0.33,'IPCA + 8,50%','Canal','Jun/38','Habibs'),
    ('MCEQ','FII York',10.1,9.3,0.076,0.60,3.7,1.00,'Única',None,'IPCA + 7,04%','Riza Sec','Ago/34','FII York'),
    ('MCEQ','LBV',9.2,9.2,0.076,0.29,2.8,1.00,'Sênior',0.38,'CDI + 5,00%','Canal','Jun/33','LBV'),
    ('MCEQ','OAD',6.4,6.4,0.052,0.65,0.4,0.817,'Única',None,'CDI + 6,00%','Opea','Dez/26','OAD'),
    ('MCEQ','Vogue Square',6.0,6.7,0.055,0.34,2.1,0.857,'Única',None,'IPCA + 12,00%','Habitasec','Dez/29', 'Calçada'),
    ('MCEQ','Renda Residencial',5.4,5.1,0.042,0.30,2.9,1.00,'Sênior',0.20,'IPCA + 8,12%','Habitasec','Ago/32','Renda Residencial'),
    ('MCEQ',"Habib's – Sub",5.7,5.3,0.044,0.61,4.7,1.00,'Subordinada',0.33,'IPCA + 11,35%','Canal','Jun/38','Habibs'),
    ('MCEQ','BR Properties',1.0,1.1,0.009,0.36,2.9,0.333,'Única',None,'CDI + 2,00%','Opea','Ago/31','BR Prop'),

    ('MCCL','Planta – Ed. Lara',32.1,31.6,0.279,None,1.6,1.00,'Única',None,'IPCA + 16,00%','Leverage','Abr/29','Planta - Ed. Lara'),
    ('MCCL','FII inVista',18.1,18.1,0.160,0.32,5.6,0.934,'Sênior',0.29,'IPCA + 10,44%','N/A','Mai/44','inVista'),
]

FUND_POSITIONS_BY_OP = {}
for (fund, ativo, sc, smtm, pct_ativos, ltv, dur, pct_cri, tranche, pct_sub, taxa, emissor, venc, key) in FUND_POSITION_ROWS:
    if key is None:
        continue
    FUND_POSITIONS_BY_OP.setdefault(key, []).append({
        'fundo': fund,
        'ativo_ppt': ativo,
        'saldo_curva_mm': sc,
        'saldo_mtm_mm': smtm,
        'pct_ativos_fundo': pct_ativos,
        'ltv': ltv,
        'duration': dur,
        'pct_do_cri': pct_cri,
        'tranche': tranche,
        'pct_sub': pct_sub,
        'taxa': taxa,
        'emissor': emissor,
        'vencimento': venc,
    })
# ordena por saldo curva desc dentro de cada operação (maior fundo primeiro)
for key in FUND_POSITIONS_BY_OP:
    FUND_POSITIONS_BY_OP[key].sort(key=lambda r: -(r['saldo_curva_mm'] or 0))

DIVIDERS = {'MCCI','MCCE','MCRE','MCRED','MCCL'}

# ---------- Grouping ----------
groups = []
cur_group = None
for name in sheetnames:
    if name in DIVIDERS:
        cur_group = {'code': name, 'sheets': []}
        groups.append(cur_group)
        continue
    if name in ('Resumo','Portfolio Atual -->','Feriados'):
        continue
    if cur_group is not None:
        cur_group['sheets'].append(name)

def classify(name):
    n = norm(name)
    if 'indicador' in n: return 'indicadores'
    if 'fluxo' in n: return 'fluxo'
    if 'suporte' in n: return 'suporte'
    if 'old' in n: return 'old'
    return 'base'

# Operações que saíram do portfólio (pedido do usuário) e não devem aparecer no portal,
# mesmo que a aba ainda exista na planilha. Não é possível usar "aba oculta" como regra
# automática pra isso: das 5, WT Morumbi/UMC/Lotus/Tarjab têm a aba oculta na planilha,
# mas Windsor está com a aba visível — "oculta" não é sinônimo de "fora do portfólio".
# Alianza Mauá / Alianza GRU (44ª rodada): pedido do usuário pra CONSOLIDAR as 2 séries numa
# única aba "Alianza GRU e Mauá" (compartilham garantias/cascata/Fundo de Reserva -- ver
# sobre_operacao) -- diferente das demais EXCLUDED_OPERATIONS acima (que saíram do portfólio
# de verdade), essas 2 continuam nele, só que fora do loop genérico de 1 aba = 1 operação (ver
# bloco especial no loop principal, mais abaixo, que monta a operação consolidada a partir das
# 2 abas na MESMA posição em que 'Alianza Mauá' apareceria).
EXCLUDED_OPERATIONS = {'WT Morumbi', 'UMC', 'Lotus', 'Windsor', 'Tarjab', 'Alianza Mauá', 'Alianza GRU'}

base_ops_by_group = []
fluxo_sheets = []
indicadores_sheets = []
for g in groups:
    ops = []
    for name in g['sheets']:
        c = classify(name)
        if c == 'base':
            if name in EXCLUDED_OPERATIONS:
                # 'Alianza Mauá'/'Alianza GRU' (ver comentário em EXCLUDED_OPERATIONS acima):
                # no lugar exato onde 'Alianza Mauá' apareceria (a 1ª das 2 abas na ordem da
                # planilha), insere um marcador de operação CONSOLIDADA -- o loop principal
                # reconhece esse nome e monta o conteúdo via build_alianza_consolidado() em vez
                # do parsing genérico de 1 aba. Preserva a posição/ordem original na sidebar
                # (entre 'NewPort' e 'GT'), sem precisar reordenar nada.
                if name == 'Alianza Mauá':
                    ops.append('Alianza GRU e Mauá')
                continue
            ops.append(name)
        elif c == 'fluxo':
            fluxo_sheets.append(name)
        elif c == 'indicadores':
            indicadores_sheets.append(name)
    base_ops_by_group.append((g['code'], ops))

SPECIAL_FLUXO = {
  'Alianza Mauá': ['Alianza - Fluxo'],
  'Tarjab': ['Tarjab Fluxo'],
  'Tellus River South': ['Tellus -  Fluxo'],
  'JALGP': ['JALGP I - Fluxo','JALGP II - Fluxo'],
}

def find_fluxo(base):
    if base in SPECIAL_FLUXO:
        return SPECIAL_FLUXO[base]
    nb = norm(base)
    return [s for s in fluxo_sheets if norm(s).startswith(nb) and 'old' not in norm(s)]

def find_indicadores(base):
    nb = norm(base)
    return [s for s in indicadores_sheets if norm(s).startswith(nb) and 'old' not in norm(s)]

# ---------- Base sheet (papel / garantias / covenants) parser ----------
HEADER_SYNONYMS = {
    'exigido':'exigido','check':'check','obs':'obs','documento':'documento',
    'status':'status','ultima atualizacao':'ultima_atualizacao',
    'proxima atualizacao':'proxima_atualizacao','atual':'atual',
}

def parse_base_sheet(name):
    ws = wb[name]
    rows = list(ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True))

    def cell(r, c):
        if r-1 >= len(rows): return None
        row = rows[r-1]
        if c-1 >= len(row): return None
        return row[c-1]

    papel_header_row = None
    for r in range(1, min(12, ws.max_row)+1):
        v = cell(r,1)
        if v and 'informa' in norm(v) and ('papel' in norm(v) or 'operacao' in norm(v) or 'cri' in norm(v) or 'ativo' in norm(v) or 'fundo' in norm(v)):
            papel_header_row = r
            break
    if papel_header_row is None:
        papel_header_row = 5

    cov_header_row = None
    item_col = None
    for r in range(max(1,papel_header_row-2), min(papel_header_row+3, ws.max_row)+1):
        row = rows[r-1] if r-1 < len(rows) else []
        for c_idx, v in enumerate(row, start=1):
            if v and 'itens de acompanha' in norm(v):
                cov_header_row = r; item_col = c_idx
                break
        if cov_header_row: break

    cov_cols = {}
    if cov_header_row:
        row = rows[cov_header_row-1]
        # Pára no 1º par de colunas em branco seguidas depois do item_col -- todas as abas
        # conferidas têm exatamente esse padrão (2 colunas vazias entre "Status" e a próxima
        # tabela não relacionada, ex.: "Locatário"/"Tabela de Unidades"/"Data Início"). Sem
        # esse corte, uma tabela vizinha que por coincidência reusa um header igual (achado
        # na MSB Axis, 37ª rodada: a "Tabela de Unidades" tem sua PRÓPRIA coluna "Status" —
        # com valores "Estoque"/"Vendido" — que sobrescrevia o "Status" de verdade do
        # covenant, ex. "Enquadrado"/"Verificar", porque o loop simplesmente sobrescrevia
        # cov_cols['status'] pra qualquer coluna com esse nome à direita, sem limite).
        blank_run = 0
        for c_idx, v in enumerate(row, start=1):
            if c_idx <= item_col: continue
            if v is None or (isinstance(v, str) and not v.strip()):
                blank_run += 1
                if blank_run >= 2:
                    break
                continue
            blank_run = 0
            key = norm(v)
            if key in HEADER_SYNONYMS:
                cov_cols[HEADER_SYNONYMS[key]] = c_idx

    covenants = []
    andamento_notes = []
    if cov_header_row:
        blank_streak = 0
        r = cov_header_row + 1
        in_andamento = False
        while r <= ws.max_row:
            row = rows[r-1] if r-1 < len(rows) else []
            def g(c):
                return row[c-1] if c and c-1 < len(row) else None
            item_val = g(item_col)
            if item_val and 'acompanhamentos em andamento' in norm(item_val):
                in_andamento = True; r += 1; continue
            if in_andamento:
                if item_val:
                    andamento_notes.append(str(item_val)); blank_streak = 0
                else:
                    blank_streak += 1
                    if blank_streak > 3: break
                r += 1; continue
            check_vals = [g(cov_cols.get(k)) for k in ('exigido','atual','status')]
            if not item_val and all(v in (None,'') for v in check_vals):
                blank_streak += 1
                if blank_streak > 2: break
                r += 1; continue
            blank_streak = 0
            if item_val:
                entry = {'item': str(item_val)}
                for k, c in cov_cols.items():
                    v = g(c)
                    if v not in (None,''):
                        entry[k] = to_jsonable(v)
                covenants.append(entry)
            r += 1

    kv = []
    r = papel_header_row + 1
    blank_streak = 0
    bullet_buffer = []  # blank-col-A rows whose col B starts with '-' (bullet continuation lines)
    while r <= ws.max_row:
        row = rows[r-1] if r-1 < len(rows) else []
        a = row[0] if len(row)>0 else None
        b = row[1] if len(row)>1 else None
        if a in (None,''):
            if isinstance(b, str) and b.strip().startswith('-'):
                bullet_buffer.append(b.strip())
                blank_streak = 0
                r += 1
                continue
            blank_streak += 1
            if blank_streak > 3: break
        else:
            blank_streak = 0
            label = str(a).strip()
            if norm(label).startswith('descricao'):
                # merge any buffered bullet lines (before this row) + this row's value +
                # any bullet lines that continue immediately after it, into one list
                bullets = list(bullet_buffer)
                bullet_buffer = []
                if b not in (None,''):
                    bullets.append(str(b).strip())
                r2 = r + 1
                while r2 <= ws.max_row:
                    row2 = rows[r2-1] if r2-1 < len(rows) else []
                    a2 = row2[0] if len(row2)>0 else None
                    b2 = row2[1] if len(row2)>1 else None
                    if a2 in (None,'') and isinstance(b2, str) and b2.strip().startswith('-'):
                        bullets.append(b2.strip())
                        r2 += 1
                    else:
                        break
                kv.append((label, bullets))
                r = r2
                continue
            else:
                bullet_buffer = []  # discard: buffered bullets didn't belong to a Descrição field
                kv.append((label, to_jsonable(b) if b not in (None,'') else None))
                # Taxa de Juros (aquisição) -- pedido do usuário: "No quadrante da
                # remuneração, vamos colocar para casos que compramos fora da curva... trazer
                # a informação IPCA + 7,20% (emissão) e IPCA + X% (aquisição)". Verificado
                # célula a célula nas 43 abas ("Taxa de Juros" + colunas vizinhas): SÓ a Vista
                # Faria Lima tem um número puro na 3ª coluna (linha 22: ['Taxa de Juros',
                # 0.085671, 9.44, None, None]) -- todas as outras têm None, texto (ex.: NewPort
                # "> 3 meses de carência") ou nem têm 3ª coluna. Confirmado também pela
                # apresentação consolidada (PDF): "Papel emitido a IPCA + 8,57%, adquirido no
                # secundário a IPCA + 9,44%". Por isso, checagem genérica (não hardcoded pro
                # nome da aba) -- funciona hoje só pra Vista Faria Lima mas se aplica
                # automaticamente a qualquer outra operação que um dia tenha esse mesmo padrão
                # bruto na planilha. A 3ª coluna vem em escala 0-100 (9.44 = 9,44%), diferente
                # da 2ª coluna que já vem em fração (0.085671 = 8,5671%) -- por isso /100.
                if norm(label).startswith('taxa de juros'):
                    c_val = row[2] if len(row) > 2 else None
                    if isinstance(c_val, (int, float)) and not isinstance(c_val, bool):
                        kv.append((label + ' (Aquisição)', c_val / 100))
        r += 1

    first_asset_idx = None
    for i,(a,b) in enumerate(kv):
        na = norm(a)
        if na.startswith('tipo de ativo') or na.startswith('tipos de ativo'):
            first_asset_idx = i; break

    if first_asset_idx is None:
        papel_kv = kv; assets = []
    else:
        papel_kv = kv[:first_asset_idx]
        asset_kv = kv[first_asset_idx:]
        assets = []; cur = None
        for a,b in asset_kv:
            if b is None and 'informa' in norm(a) and 'garantia' in norm(a):
                continue
            na = norm(a)
            if na.startswith('tipo de ativo') or na.startswith('tipos de ativo'):
                if cur is not None: assets.append(cur)
                cur = {}
            if cur is None: cur = {}
            if a in cur:
                cur[a] = (str(cur[a]) + ' ' + str(b)) if b else cur[a]
            else:
                cur[a] = b
        if cur: assets.append(cur)

    # papel_kv (correção -- pedido do usuário: "checar os saldos devedores... vamos mapear
    # essas diferenças e ajustar aonde tiver que ajustar"): em pelo menos 12 abas (Apil, ECLA,
    # Habibs, IBL, JALGP, LBV, Lux, MegaModa, PKK, Pirelli, SKR + outras a confirmar), a seção
    # "Informações do Papel" no topo da aba (bloco CONSOLIDADO/total da operação) é seguida,
    # mais abaixo na MESMA aba, por um bloco de abertura POR SÉRIE ("1ª Série - Sênior", "2ª
    # Série - Subordinada" etc.) que repete os MESMOS rótulos (Volume Emissão, Montante Atual
    # CRI, % do CRI...) com o valor de CADA série isoladamente. Conferido linha a linha contra
    # a planilha (IBL: bloco topo tem Volume Emissão=97.000.000/Montante Atual CRI=100.332.218,
    # que bate exatamente com a soma das 3 séries abertas mais abaixo -- 65M+22M+10M=97M e
    # 63,42M+22,26M+14,65M=100,33M) -- confirma que o bloco do TOPO já É o total consolidado
    # correto, sem precisar somar nada.
    # O loop de leitura de kv (acima) não tem como saber onde o bloco "Informações do Papel"
    # termina (só para depois de >3 linhas em branco seguidas na coluna A, o que raramente
    # acontece entre um bloco e o próximo) -- por isso ele segue lendo direto pros blocos de
    # série, e o dict abaixo, ao ver o MESMO rótulo de novo, CONCATENAVA os 2 valores com espaço
    # (ex.: "100332218.90055 63418344.81255 22264165.198 14649708.89") -- um número limpo e
    # correto virando um texto ilegível, que quebra qualquer formatação numérica (fmtSaldoMM/
    # fmtBRLCompact) tanto no quickstat "Saldo Devedor" quanto na tabela de Operações. Fix:
    # ignora ocorrências repetidas do mesmo rótulo (mantém só a 1ª, que é sempre a do bloco
    # consolidado do topo) em vez de concatenar. Não mexe no parsing por série em si (usado
    # em outro lugar, se algum dia precisar do detalhe por série) -- só evita que esse detalhe
    # vaze pra dentro do valor "resumo" da operação.
    papel = {}
    for a,b in papel_kv:
        if b is None and 'informa' in norm(a) and ('garantia' in norm(a) or 'papel' in norm(a)):
            continue
        if a not in papel:
            papel[a] = b

    # inVista -- Volume de Emissão correto (pedido do usuário, que apontou a célula direto:
    # "está na nossa planilha em excel, coluna F linha 51"): não está na tabela "Informações
    # do Papel" no topo da aba (que só tem CONTAGEM de cotas -- "Volume Emissão - Total
    # (Cotas)" 102.092.483, um número de cotas, não R$ -- ver PAPEL_VALUE_OVERRIDE/find_papel_
    # value). O valor certo em R$ está numa mini-tabela mais abaixo, própria dessa aba (linhas
    # 42-51: colunas Fundo | Data | Quantidade de cotas | Valor nominal + Custos | Valor
    # nominal | Volume), na linha "Total Cota Sr" (a soma em R$ das 4 ofertas da cota Sênior,
    # a que a Mauá detém), coluna "Volume" -- R$ 271.997.520,12. Estrutura de sub-tabela não
    # vista em nenhuma outra aba, por isso extração pontual (não um sinônimo genérico) --
    # injeta como chave sintética em `papel`, consumida via PAPEL_VALUE_OVERRIDE['inVista'].
    if name == 'inVista':
        for r in range(1, ws.max_row+1):
            a_cell = cell(r, 1)
            if a_cell and norm(str(a_cell)) == 'total cota sr':
                v = cell(r, 6)  # coluna F = 'Volume'
                if isinstance(v, (int, float)):
                    papel['Volume Emissão (Total Cota Sr)'] = v
                break

    # Ilog -- Volume Integralizado correto (pedido do usuário: "o volume de emissão é de
    # 100mm, mas só foi integralizado [uma fração]... faz mais sentido usar o integralizado,
    # dado que o total ainda não virou dinheiro"): a aba não tem uma célula única com esse
    # total em R$ -- só uma mini-tabela própria ("Integralizações 1ª Série (Tamboré)", coluna
    # E a partir da linha do título, sub-cabeçalho Data|Quantidade|PU|Financeiro), 1 linha por
    # aporte/integralização (a 1ª em 29/04/26 por R$33.691.000, PU=1000; uma 2ª em 27/08/26 por
    # R$38.631.365,92, PU já corrigido a R$1.188,66). A 2ª Série (Guarulhos) tem sua própria
    # mini-tabela equivalente mas sem nenhum aporte ainda (Quantidade Integralizada=0).
    # Correção (pedido do usuário, direto): "esse [aporte de agosto] entraria apenas na
    # atualização de agosto, nessa atualização de julho fica só os 33mm mesmo" -- o portal
    # está no snapshot de Julho/2026 (ver AS_OF_OVERRIDE mais abaixo), então só conta aportes
    # com Data <= esse corte; sem esse filtro, a soma incluía o aporte de agosto, que ainda
    # não tinha acontecido na data de referência deste snapshot.
    if name == 'Ilog':
        for r in range(1, ws.max_row+1):
            header_v = cell(r, 5)
            if header_v and 'integralizacoes' in norm(str(header_v)) and 'tambore' in norm(str(header_v)):
                total = 0.0
                found_any = False
                rr = r + 2  # pula a linha do título e a linha de sub-cabeçalho (Data|Quantidade|PU|Financeiro)
                while rr <= ws.max_row:
                    data_v = cell(rr, 5)
                    if not isinstance(data_v, (datetime, date)):
                        break
                    data_only = data_v.date() if isinstance(data_v, datetime) else data_v
                    fin_v = cell(rr, 8)
                    if isinstance(fin_v, (int, float)) and data_only <= AS_OF_OVERRIDE:
                        total += fin_v
                        found_any = True
                    rr += 1
                if found_any:
                    papel['Aportes Acumulados 1ª Série (Tamboré)'] = total
                break

    return {'papel': papel, 'garantias': assets, 'covenants': covenants, 'andamento': andamento_notes}

# ---------- Fluxo parser (curated) ----------
CURATED_PATTERNS = [
    ('saldo_devedor', lambda k: k=='saldo devedor'),
    ('saldo_devedor', lambda k: 'saldo devedor' in k and 'maximo' not in k),
    ('juros', lambda k: k=='juros'),
    ('amortizacao', lambda k: k.startswith('amortizacao') and 'minima' not in k),
    ('pmt', lambda k: k=='pmt financeira'),
    ('pmt', lambda k: k=='pmt'),
    ('ic', lambda k: 'ic' in k and 'medi' in k and 'minimo' not in k),
    ('ic', lambda k: k=='ic'),
    ('ic', lambda k: 'indice de cobertura' in k or 'ic gerencial' in k or 'ic total' in k or k.startswith('ic ')),
    ('ic_spot', lambda k: k=='ic'),
    ('ic_minimo', lambda k: 'ic minimo' in k or 'ic - minimo' in k or 'ic min' in k),
    ('ltv', lambda k: k=='ltv'),
    ('ltv', lambda k: k.startswith('ltv')),
    ('valor_garantia', lambda k: 'valor do imovel' in k or 'valor garantia' in k or 'valor de avaliacao' in k or k.startswith('valuation')),
    ('arrecadacao', lambda k: 'arrecadacao' in k or 'aluguel recebido' in k or 'valor bruto' in k or 'recebiveis' in k or 'recebimento aluguel' in k),
    ('quantidade', lambda k: k=='quantidade'),
    ('pu', lambda k: k=='pu'),
    ('tai', lambda k: k=='tai'),
    # Amex/amortização extraordinária (46ª rodada, pedido explícito do usuário: "tem
    # operações que tem amex sim, então devemos considerar"). Mesmo padrão de prioridade já
    # usado pra PMT (variante "Financeira/Financeiro" primeiro, só then a bare genérica) --
    # em várias abas a coluna "Amex" pura é uma taxa/proporção pequena (ex.: 0,74) e o valor
    # em R$ de fato mora numa coluna "Amex Financeiro(a)" separada (ver override pontual pra
    # MSB Triu, onde o nome dessa 2ª coluna nem repete "Amex", só "Financeiro").
    ('amex', lambda k: k in ('amex financeiro', 'amex financeira')),
    ('amex', lambda k: k.rstrip('.').strip() == 'amex'),
]

# Amex (46ª rodada): operações onde a coluna "Amex" bare do match genérico NÃO é confiável
# como valor em R$ e não há uma variante "Financeiro(a)" alternativa segura pra usar via
# override -- por isso ficam de fora da tabela em vez de arriscar mostrar um número errado:
#   - IBL: operação em 2 tranches (Série 1 Sr / Série 2 Mez), cada uma com seu próprio
#     "Amex Sr"/"Amex Mez" (R$) e mais 2 colunas "Amex" derivadas (proporções pequenas, ex.
#     0,74 e 0,0007) -- não existe uma coluna "Amex" consolidada Sr+Mez na aba, então
#     qualquer campo único aqui ficaria incompleto (só uma tranche) ou errado (pegando a
#     proporção em vez do valor).
#   - Residencial Jardins FL2: aba tem 2 colunas "Amex" duplicadas (sem nome que distinga
#     qual é a "boa"), ambas com valores residuais muito pequenos (ex. 3,16 e 0,004) que não
#     batem com a escala de um valor em R$ de amortização extraordinária dessa operação.
AMEX_UNRELIABLE_SHEETS = {'IBL - Fluxo', 'Residencial Jardins - Fluxo'}

# PAPEL_VALUE_OVERRIDE (pedido do usuário: "vamos ajustar a questão dos Volume de Emissão e
# Saldo Devedor das operações... tem varios errados. como o exemplo de invista"): mapeia, por
# operação, o rótulo EXATO (chave literal do dict `papel`, já lido por parse_base_sheet) que
# deve ser usado pra um campo -- usado quando find_papel_value() por sinônimo genérico acerta
# o rótulo ERRADO porque a aba tem mais de um valor "parecido" (ex.: o valor de uma série
# específica que COINCIDENTEMENTE bate com o sinônimo genérico antes do rótulo certo -- o
# total, ou a fatia que a Mauá realmente detém). Achado auditando as 43 operações em busca de
# abas com mais de um candidato distinto pros sinônimos de Volume Emissão/Saldo Devedor (nem
# toda ambiguidade é bug -- SKR, JALGP [Volume Emissão], Vitacon e Lotus já tinham o rótulo
# "Total" certo sendo escolhido, confirmado por soma das partes; só os casos abaixo estavam
# errados). Cada caso foi verificado 2x: (1) identidade aritmética entre as partes e o total
# na própria aba bruta, (2) cruzado contra a apresentação consolidada em PDF
# (Operações_Estruturadas_07.2026_v7) quando a operação tem slide própria.
PAPEL_VALUE_OVERRIDE = {
    # MegaModa: 'Valor de Emissão' (linha da 2ª Série, R$30MM) batia ANTES de 'Volume Emissão'
    # (linha do topo, consolidado das 2 séries, R$200MM) por causa da ordem de prioridade dos
    # sinônimos genéricos ('valor de emissao' vem antes de 'volume emissao' na lista, sem
    # saber que aqui os 2 termos NÃO são sinônimos nessa aba -- 'Volume' é o total, 'Valor' é
    # só a 2ª série). Confirmado: Montante Atual CRI (R$189,5 MM) é mais coerente com um total
    # de R$200MM (leve amortização ao longo do tempo) do que com R$30MM.
    'MegaModa': {'valor_emissao': 'Volume Emissão'},
    # MSB Edson: 2 séries (220 e 333), cada uma com sua própria linha de "Valor de Emissão"/
    # "Saldo Devedor Atualizado" -- a aba já tem um rótulo "Total" explícito pra cada campo,
    # mas a busca genérica batia na 1ª série (220) por ordem de leitura, nunca chegando no
    # rótulo "Total". Confirmado: 20.000.000 + 48.652.000 = 68.652.000 (Volume Emissão) e
    # 11.734.400,42 + 50.300.592,05 = 62.034.992,47 (Saldo Devedor) batem exatamente com os
    # rótulos "Total" da própria aba.
    'MSB Edson': {'valor_emissao': 'Valor de Emissão Total', 'saldo_devedor': 'Saldo Devedor Atualizado - Total'},
    # JALGP: a Mauá detém 100% da série SÊNIOR e 0% da Subordinada ('% CRI Sêniores - Mauá'=1,
    # '% CRI Sub. - Mauá'=0, ambos na própria aba) -- por isso o Saldo Devedor que representa
    # a exposição real da Mauá é o total SÊNIOR consolidado ('Saldo Devedor Atual - Sênior',
    # R$38,0 MM = soma das 2 sub-séries sêniores, 1ª+3ª), não o valor bruto que a busca
    # genérica pegava (Montante Atual CRI da 1ª Série isolada, R$19,6 MM -- só METADE do
    # sênior). Confirmado também no PDF consolidado ("Saldo Devedor Atualizado - Sênior
    # R$ 37.658.386", mesma ordem de grandeza, mês de referência diferente do da planilha).
    'JALGP': {'saldo_devedor': 'Saldo Devedor Atual - Sênior'},
    # Renda Residencial: ao contrário da JALGP, aqui a Mauá detém AMBAS as séries (Sênior via
    # fundos MCCI/MCEQ/MCFA E Subordinada via MCRE -- confirmado em fund_positions, campo
    # 'pct_do_cri':1.0 nas 2 tranches) -- por isso o Saldo Devedor correto é o TOTAL da
    # operação (Sr+Sub, rótulo "Montante Atual - Operação", R$26,05 MM), não só a fatia
    # Sênior que a busca genérica pegava (R$20,84 MM, faltando a Subordinada de R$5,21 MM que
    # também é da Mauá).
    # Renda Residencial: mesma lógica acima, mas pro Volume Emissão (pedido do usuário, que
    # apontou o valor certo direto: "Volume Emissão – Total R$52.355.000") -- a aba não tem
    # uma linha "Total" pronta pra esse campo (diferente do Saldo Devedor), só 'Valor Emissão
    # (Sr)' (R$41.884.000) e 'Valor de Emissão (Sub)' (R$10.471.000) separadas, com rótulos
    # inconsistentes entre si (Sr sem "de", Sub com "de") -- a busca genérica só reconhecia o
    # padrão 'valor DE emissao' e por isso batia só na Sub, nunca somando as 2. Confirmado:
    # 41.884.000 + 10.471.000 = 52.355.000, exatamente o valor apontado pelo usuário.
    'Renda Residencial': {'saldo_devedor': 'Montante Atual - Operação', 'valor_emissao': ['Valor Emissão (Sr)', 'Valor de Emissão (Sub)']},
    # inVista: ver extração/comentário em parse_base_sheet (bloco "if name == 'inVista'") --
    # o usuário apontou a célula certa direto na planilha (coluna F, linha 51, "Total Cota
    # Sr"). Substitui o valor que a busca genérica pegava ("Volume Emissão - Total (Cotas)",
    # 102.092.483 -- uma CONTAGEM de cotas, não R$).
    'inVista': {'valor_emissao': 'Volume Emissão (Total Cota Sr)'},
    # Ilog: pedido do usuário ("o volume de emissão é de 100 mm, mas só foi integralizado...
    # aqui acho que faz mais sentido usar o integralizado, dado que o total ainda não virou
    # dinheiro") -- ver extração/comentário em parse_base_sheet (bloco "if name == 'Ilog'").
    # Usa o Volume INTEGRALIZADO (dinheiro que já entrou de verdade), não o Volume Emissão
    # (teto autorizado da 1ª+2ª série, R$275MM) -- a 2ª série (Guarulhos) ainda não
    # integralizou nada.
    'Ilog': {'valor_emissao': 'Aportes Acumulados 1ª Série (Tamboré)'},
}

# Override pontual por aba de fluxo: o matching genérico por sinônimo pega a PRIMEIRA
# coluna (da esquerda) que bate no padrão -- na Calçada isso escolhe "Valuation Bolsa RJ"/
# "LTV - Bolsa RJ" pra valor_garantia/ltv, mas a garantia vigente hoje é o Estoque (a
# operação migrou de renda de hotel pra estoque de unidades, ver regra geral #15/#16/#18
# do checklist), então forçamos as colunas "Valor do Estoque"/"LTV - Estoque". Também
# adiciona um campo novo (`noi_calcada`, sem padrão genérico -- só usado quando uma aba
# está listada aqui) puxando a coluna "Valores Recebidos" (o caixa efetivamente recebido
# do hotel/repassado à Calçada no mês, exibido como "NOI Hotel % Calçada").
FLUXO_FIELD_OVERRIDE = {
    'Calçada - Fluxo': {
        'valor_garantia': 'Valor do Estoque',
        'ltv': 'LTV - Estoque',
        'noi_calcada': 'Valores Recebidos',
        # TAI (46ª rodada, usuário reportou "faltou tbm a coluna de TAI"): a aba da Calçada
        # não tem uma coluna "TAI" pura -- tem "Tai Acumulada" (col12, série monotônica
        # subindo até 1,0 -- é um cronograma acumulado, não a taxa periódica) e "TAi
        # Ajustada" (col13, oscila entre ~3% e ~12%, período a período). "TAi Ajustada" é a
        # que corresponde ao mesmo conceito de taxa periódica que "TAI" representa nas
        # demais operações (ver Evolution, escala ~0,3%-0,4% a.m.) -- por isso escolhida
        # aqui, mas fica marcado pro usuário confirmar já que a escala difere bastante entre
        # operações (natural, cada CRI tem seu próprio índice/spread).
        'tai': 'TAi Ajustada',
    },
    # WT Log chama a coluna de arrecadação de locação só de "Aluguel" (sem a palavra
    # "Arrecadação"/"recebido"/etc que o padrão genérico procura), então a coluna ficava
    # de fora da tabela de amortização mensal (32ª/33ª rodada, pedido do usuário).
    'WT Log - Fluxo': {
        'arrecadacao': 'Aluguel',
    },
    # Amex (46ª rodada): nessas 2 abas a coluna "Amex" bare (que o padrão genérico pegaria)
    # é uma taxa pequena (não R$) e a versão em R$ mora numa coluna vizinha SEM "Amex" no
    # nome -- só "Financeiro" mesmo, sem repetir a palavra (por isso não dá pra cobrir isso
    # com o padrão genérico "amex financeiro/financeira" do CURATED_PATTERNS).
    'MSB Triu - Fluxo': {
        'amex': 'Financeiro',
    },
    # CVPAR (46ª rodada, achado ao auditar "ajustar todas as tabelas de amortização"): aba não
    # tem coluna "Saldo Devedor" -- é uma estrutura de cota única (Cota Sênior), com "PL"
    # (Patrimônio Líquido da cota) no lugar. Confirmado: PL do 1º registro (68.000.000) bate
    # exatamente com Quantidade×PU (680.000×100) -- é o mesmo conceito de saldo devedor,
    # só com outro nome.
    'CVPAR - Fluxo': {
        'saldo_devedor': 'PL',
    },
    # inVista (46ª rodada): estrutura de fundo (cotas), não CRI -- "PL Sênior" no lugar de
    # "Saldo Devedor" e "PMT Total" no lugar de "PMT" (ver também FLUXO_DATA_LABEL_OVERRIDE
    # acima pro bug de detecção do cabeçalho "Data Competência"). Sem coluna "Amortização"
    # própria nessa aba -- estrutura é Juros + Amex (extraordinária) só, sem amortização
    # ordinária programada (confirmado: Juros + Amex = PMT Total em todas as linhas testadas).
    'inVista - Fluxo': {
        'saldo_devedor': 'PL Sênior',
        'pmt': 'PMT Total',
    },
}

# inVista (46ª rodada, achado ao investigar o pedido do usuário "ajustar todas as tabelas de
# amortização"): a aba 'inVista - Fluxo' não tem uma célula "Data" pura na linha de cabeçalho
# real (usa "Data Competência") -- o header-detection genérico (procura só por norm(v)=='data'
# exato) pulava direto pra um bloco AUXILIAR de cálculo bem mais à direita na mesma aba (que
# por coincidência tem uma célula "Data" solta lá dentro, parte de um breakdown de dias úteis/
# IPCA sem relação com a tabela real), fazendo a tabela de amortização mostrar só 1 coluna com
# dado ("Amortização", também por coincidência de nome dentro desse bloco auxiliar). Em vez de
# mudar o critério genérico (risco de pegar a coluna errada em alguma outra aba que também
# tenha várias ocorrências soltas da palavra "data"), esse dict deixa explícito, aba por aba,
# qual rótulo literal marca a linha/coluna de Data de verdade quando não é a palavra "Data" pura.
FLUXO_DATA_LABEL_OVERRIDE = {
    'inVista - Fluxo': 'data competencia',
}

def parse_fluxo_sheet(name, max_scan_rows=6, safety_cap=1500, blank_break=15):
    ws = wb[name]
    max_r = min(ws.max_row, max_scan_rows + safety_cap + 5)
    all_rows = list(ws.iter_rows(min_row=1, max_row=max_r, values_only=True))
    data_label = FLUXO_DATA_LABEL_OVERRIDE.get(name, 'data')

    header_row = None; header_vals = None
    for r in range(1, min(max_scan_rows, len(all_rows))+1):
        row = all_rows[r-1]
        for v in row:
            if norm(v) == data_label:
                header_row = r; header_vals = row; break
        if header_row: break
    if header_row is None:
        return None

    data_cols = [i for i,v in enumerate(header_vals) if norm(v)==data_label]
    start_col = data_cols[0]
    end_col = data_cols[1] if len(data_cols) > 1 else len(header_vals)

    raw_colmap = {}
    seen = {}
    for c in range(start_col, end_col):
        v = header_vals[c] if c < len(header_vals) else None
        if v in (None,''): continue
        key = str(v).strip()
        if key in seen:
            seen[key]+=1; key = f"{key}_{seen[key]}"
        else:
            seen[key]=0
        raw_colmap[key] = c

    # map curated fields to actual column index (first match wins per field)
    curated_cols = {}
    normkeys = {k: norm(k) for k in raw_colmap}
    for field, pred in CURATED_PATTERNS:
        if field in curated_cols: continue
        for k, nk in normkeys.items():
            if pred(nk):
                curated_cols[field] = raw_colmap[k]
                break

    # override pontual por aba (ver FLUXO_FIELD_OVERRIDE) -- roda DEPOIS do matching
    # genérico de propósito, pra poder substituir um campo já preenchido (valor_garantia/
    # ltv) e também adicionar campos novos sem padrão genérico (noi_calcada)
    override = FLUXO_FIELD_OVERRIDE.get(name)
    if override:
        for field, literal_header in override.items():
            for k in raw_colmap:
                if norm(k) == norm(literal_header):
                    curated_cols[field] = raw_colmap[k]
                    break

    # ver nota em AMEX_UNRELIABLE_SHEETS (acima) -- remove o match genérico de 'amex' nessas
    # abas em vez de arriscar mostrar um número que não é o valor em R$ de fato.
    if name in AMEX_UNRELIABLE_SHEETS:
        curated_cols.pop('amex', None)

    data_col_idx = None
    for k in raw_colmap:
        if norm(k) == data_label:
            data_col_idx = raw_colmap[k]
            break
    records = []
    blanks = 0
    for r in range(header_row+1, len(all_rows)+1):
        row = all_rows[r-1]
        data_val = row[data_col_idx] if (data_col_idx is not None and data_col_idx < len(row)) else None
        if data_val in (None,''):
            blanks += 1
            if blanks >= blank_break and records: break
        else:
            blanks = 0
            rec = {'data': to_jsonable(data_val)}
            for field, c in curated_cols.items():
                if c < len(row) and row[c] not in (None,''):
                    v = to_jsonable(row[c])
                    if isinstance(v,(int,float)):
                        rec[field] = v
            records.append(rec)
    return records

# ---------- Locatários / rent-roll parser (genérico: só roda se a aba tiver a estrutura) ----------
def parse_rentroll_sheet(name, max_scan_rows=10, safety_cap=300, blank_break=6, max_col=60):
    ws = wb[name]
    max_r = min(ws.max_row, max_scan_rows + safety_cap + 5)
    max_c = min(ws.max_column, max_col)
    all_rows = list(ws.iter_rows(min_row=1, max_row=max_r, max_col=max_c, values_only=True))

    header_row = None; header_vals = None
    for r in range(1, min(max_scan_rows, len(all_rows))+1):
        row = all_rows[r-1]
        keys = {norm(v) for v in row if v}
        if 'locatario' in keys and 'grupo' in keys:
            header_row = r; header_vals = row; break
    if header_row is None:
        return None

    colmap = {}
    for c, v in enumerate(header_vals):
        if v in (None,''): continue
        colmap.setdefault(norm(v), c)

    def col(*names):
        for n in names:
            if n in colmap: return colmap[n]
        return None

    c_locatario = col('locatario')
    c_grupo = col('grupo')
    c_area = col('area locavel m2','area locavel','area m2','area')
    c_aluguel = col('aluguel mensal')
    c_devido = col('aluguel devido')
    c_reajuste = col('indice reajuste')

    records = []
    blanks = 0
    for r in range(header_row+1, len(all_rows)+1):
        row = all_rows[r-1] if r-1 < len(all_rows) else []
        def g(c):
            return row[c] if (c is not None and c < len(row)) else None
        locatario = g(c_locatario)
        if locatario in (None,''):
            blanks += 1
            if blanks >= blank_break and records: break
            continue
        if norm(locatario).startswith('total'):
            break  # início do bloco de subtotais/resumo da própria planilha: fim da lista de locatários
        blanks = 0
        grupo_val = g(c_grupo)
        area_val = g(c_area)
        aluguel_val = g(c_aluguel)
        devido_val = g(c_devido)
        records.append({
            'locatario': str(locatario).strip(),
            'grupo': str(grupo_val).strip() if grupo_val not in (None,'') else str(locatario).strip(),
            'area': area_val if isinstance(area_val,(int,float)) else None,
            'aluguel_mensal': aluguel_val if isinstance(aluguel_val,(int,float)) else None,
            'aluguel_devido': devido_val if isinstance(devido_val,(int,float)) else None,
            'reajuste_raw': str(g(c_reajuste)).strip() if isinstance(g(c_reajuste), str) else None,
        })
    return records if records else None

def aggregate_locatarios(records):
    """Agrega por 'Grupo', com merge de sub-locatárias tipo 'X (sublocatária Y)' -> Y."""
    if not records: return []
    groups = {}
    order = []
    for rec in records:
        grupo = rec['grupo']
        m = re.search(r'\(sublocat[aá]ria\s+(.+?)\)', grupo, re.IGNORECASE)
        if m:
            grupo = m.group(1).strip()
        key = norm(grupo)
        if key not in groups:
            groups[key] = {'nome': grupo, 'locatario_orig': rec['locatario'], 'area': 0.0,
                           'valor_contratado': 0.0, 'valor_pago': 0.0, 'is_cf': False}
            order.append(key)
        g = groups[key]
        if rec['area']:
            g['area'] += rec['area']
        else:
            g['is_cf'] = True
        if rec['aluguel_mensal']:
            g['valor_contratado'] += rec['aluguel_mensal']
        val_pago = rec['aluguel_devido'] if rec['aluguel_devido'] is not None else rec['aluguel_mensal']
        if val_pago:
            g['valor_pago'] += val_pago
    out = []
    for k in order:
        g = groups[k]
        out.append({
            'locatario': g['nome'] if not g['is_cf'] else f"CF - {g['locatario_orig']}",
            'area': round(g['area'],2) if g['area'] else None,
            'valor_contratado': round(g['valor_contratado'],2) if g['valor_contratado'] else None,
            'valor_pago': round(g['valor_pago'],2) if g['valor_pago'] else None,
            'is_cf': g['is_cf'],
        })
    return out

# Curadoria manual por operação: ordem de exibição dos locatários e/ou nome de exibição,
# só usada quando o exemplo de referência do usuário difere da ordem/rótulo natural da planilha.
LOCATARIOS_CURATION = {
    'Evolution': {
        'order': ['elo servicos', 'elo participacoes', 'banco digio s.a'],
        'display_names': {
            'elo servicos': 'Elo Serviços',
            'banco digio s.a': 'Banco Digio',
        },
    },
}

# Link do Google Maps pro endereço de "Informações do Ativo". Quando o usuário manda um
# link específico (ele já sabe a localização exata do imóvel), usa esse link curado; senão,
# cai no fallback de gerar uma busca do Maps a partir do próprio texto do endereço da planilha
# (funciona sem API key, mas pode ser menos preciso se o endereço estiver incompleto).
MAPS_LINKS = {
    'Evolution': 'https://www.google.com/maps/place/Alameda+Xingu,+512+-+Alphaville,+Barueri+-+SP,+06455-030/@-23.5050862,-46.8512499,15.09z/data=!4m6!3m5!1s0x94cf0226c2709065:0x7b8aa0e19a78d6bc!8m2!3d-23.5049751!4d-46.8506924!16s%2Fg%2F11svpm9d28',
    'Calçada': 'https://www.google.com/maps/place/Vogue+Square/@-23.0010839,-43.3964964,309m/data=!3m1!1e3!4m6!3m5!1s0x9bdb9c8ccf6ae3:0x1cbc132a4be5de15!8m2!3d-23.000748!4d-43.396071!16s%2Fg%2F11c5_b845k?entry=ttu&g_ep=EgoyMDI2MDkwMS4wIKXMDSoASAFQAw%3D%3D',
    'BR Prop': 'https://www.google.com/maps/place/BRPR+LOGISTIC+CENTER+-+CAJAMAR+I/data=!4m2!3m1!1s0x0:0x74b12622ffa92410?sa=X&ved=1t:2428&ictx=111',
}

def endereco_maps_link(op_name, endereco_text):
    if op_name in MAPS_LINKS:
        return MAPS_LINKS[op_name]
    if endereco_text:
        return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(str(endereco_text))
    return None

def build_locatarios_table(name):
    raw = parse_rentroll_sheet(name)
    if not raw: return None
    aggr = aggregate_locatarios(raw)
    if not aggr: return None
    tenants = [dict(a) for a in aggr if not a['is_cf']]
    cf_rows = [dict(a) for a in aggr if a['is_cf']]

    curation = LOCATARIOS_CURATION.get(name)
    if curation:
        order = curation.get('order')
        display_names = curation.get('display_names') or {}
        if order:
            order_idx = {k: i for i, k in enumerate(order)}
            tenants.sort(key=lambda t: order_idx.get(norm(t['locatario']), 999))
        for t in tenants:
            k = norm(t['locatario'])
            if k in display_names:
                t['locatario'] = display_names[k]
        for c in cf_rows:
            k = norm(c['locatario'])
            if k in display_names:
                c['locatario'] = display_names[k]

    total_area = sum(t['area'] or 0 for t in tenants)
    total_contratado = sum(t['valor_contratado'] or 0 for t in tenants)
    total_pago_locacoes = sum(t['valor_pago'] or 0 for t in tenants)
    total_pago_cf = sum(c['valor_pago'] or 0 for c in cf_rows)
    total_pago_geral = total_pago_locacoes + total_pago_cf
    # "Valor Contratado" das linhas extras (CF etc.) não existe na planilha — espelha o Valor Pago,
    # igual ao exemplo de referência do usuário.
    total_contratado_geral = total_contratado + total_pago_cf
    valor_m2_locacoes = (total_pago_locacoes/total_area) if total_area else None
    valor_m2_geral = (total_pago_geral/total_area) if total_area else None

    rows = []
    for t in tenants:
        pct = (t['area']/total_area) if (t['area'] and total_area) else None
        rows.append({
            'locatario': t['locatario'], 'area': t['area'], 'pct_ocupacao': pct,
            'valor_contratado': t['valor_contratado'], 'valor_pago': t['valor_pago'],
            'valor_m2': (t['valor_pago']/t['area']) if (t['valor_pago'] and t['area']) else None,
            'reajuste': None,
        })

    extra_rows = []
    for c in cf_rows:
        extra_rows.append({
            'locatario': c['locatario'], 'area': None, 'pct_ocupacao': None,
            'valor_contratado': c['valor_pago'], 'valor_pago': c['valor_pago'],
            'valor_m2': None, 'reajuste': None,
        })

    return {
        'rows': rows,
        'extra_rows': extra_rows,
        # "Total Locações" soma só os locatários (área ocupada = 100% da área locável dos locatários).
        'total_locacoes': {
            'area': round(total_area,2) or None,
            'pct_ocupacao': 1.0 if total_area else None,
            'valor_contratado': round(total_contratado,2) or None,
            'valor_pago': round(total_pago_locacoes,2) or None,
            'valor_m2': valor_m2_locacoes,
        },
        # "Total Pago" soma locatários + linhas extras (CF etc.).
        'total_pago_row': {
            'area': round(total_area,2) or None,
            'pct_ocupacao': 1.0 if total_area else None,
            'valor_contratado': round(total_contratado_geral,2) or None,
            'valor_pago': round(total_pago_geral,2) or None,
            'valor_m2': valor_m2_geral,
        },
    }

# ---------- Informações do Ativo (a partir do bloco de garantia já parseado) ----------
def parse_br_number(s):
    if s is None: return None
    if isinstance(s,(int,float)): return float(s)
    s = str(s)
    m = re.search(r'([\d\.,]+)', s)
    if not m: return None
    num = m.group(1)
    if ',' in num and '.' in num:
        num = num.replace('.', '').replace(',', '.')
    elif ',' in num:
        num = num.replace(',', '.')
    try:
        return float(num)
    except ValueError:
        return None

TICKER_RE = re.compile(r'\b([A-Z]{4}\d{1,2})\b')

def derive_laudo_cadence(dt_last, dt_next):
    if not dt_last or not dt_next: return None
    try:
        d1 = datetime.fromisoformat(str(dt_last)[:10])
        d2 = datetime.fromisoformat(str(dt_next)[:10])
    except ValueError:
        return None
    months = (d2.year-d1.year)*12 + (d2.month-d1.month)
    if 11 <= months <= 13:
        meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
        return f"Anual – todo mês de {meses[d2.month-1]}"
    return None

def format_area_m2(val):
    """Formata área (ABL) de forma consistente pra qualquer operação: sem casas decimais (pedido
    do usuário, feito originalmente na Evolution — "consegue tirar essas duas casas decimais?"),
    com separador de milhar BR e sufixo "m²". A planilha guarda esse dado de 2 formas diferentes
    dependendo da operação — cobre as duas:
    (1) número puro (int/float, ou string só com dígitos/ponto, ex.: 12868.72, '43376', '11332.05')
        — comum quando a célula não tem formatação de texto aplicada;
    (2) texto já formatado em BR com unidade (ex.: '14.929,14 m²', '9.832,00 m²', '52.043 m²')
        — comum quando alguém digitou o valor já com máscara.
    Ambos viram o mesmo formato final (ex.: "14.929 m²"). Não mexe em strings fora desses 2
    padrões (datas, listas de vários números separados por espaço etc.) — apurado achado num
    valor esquisito da Vista Faria Lima ('1931-10-25'), deixado como está até investigar a causa."""
    def fmt(n):
        return format(int(round(n)), ',').replace(',', '.') + ' m²'
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return fmt(val)
    if isinstance(val, str):
        s = val.strip()
        if re.fullmatch(r'-?\d+(?:\.\d+)?', s):
            return fmt(float(s))
        m = re.fullmatch(r'(-?\d{1,3}(?:\.\d{3})*)(?:,\d+)?\s*m²?', s)
        if m:
            return fmt(float(m.group(1).replace('.', '')))
    return val

def build_ativo_info(asset):
    """Curadoria da 'Informações do Ativo' a partir do dict bruto de uma garantia (asset).
    Mapeamento por sinônimo, adaptando ao que a aba realmente tem (sem forçar '—')."""
    if not asset: return None
    nk = {norm(k): k for k in asset.keys()}
    def find(*substrs, exclude=()):
        for nkey, orig in nk.items():
            if any(s in nkey for s in substrs) and not any(e in nkey for e in exclude):
                v = asset[orig]
                if v not in (None,'','#REF!'):
                    return orig, v
        return None, None

    out = {}
    _, tipo_ativo = find('tipo de ativo','tipos de ativo')
    if tipo_ativo: out['tipo_ativo'] = tipo_ativo
    _, ativo_val = find('ativo', exclude=('tipo de ativo','abl','ocupacao','aluguel','locatario'))
    if ativo_val: out['ativo'] = ativo_val

    prop_key, prop_val = find('propriet')
    ticker = None
    for k in asset.keys():
        m = TICKER_RE.search(k)
        if m: ticker = m.group(1); break
    if prop_val:
        out['proprietaria'] = f"{prop_val} ({ticker})" if ticker else prop_val

    _, endereco = find('endereco')
    if endereco: out['endereco'] = endereco

    abl_total_key, abl_total = find('abl total')
    if abl_total: out['abl_total'] = format_area_m2(abl_total)

    abl_adq_val = None
    for k, v in asset.items():
        if k == abl_total_key: continue
        if norm(k).startswith('abl') and v not in (None,''):
            abl_adq_val = str(v)
            abl_adq_val = re.sub(r'\s*\([^)]*\)\s*$', '', abl_adq_val).strip()
            break
    if abl_adq_val: out['abl_adquirido'] = format_area_m2(abl_adq_val)

    _, descricao = find('descri')
    if descricao: out['descricao'] = descricao if isinstance(descricao, list) else [str(descricao)]

    laudo_key, laudo_val = find('valor do ativo','valor de avaliacao','valor do imovel')
    if laudo_val:
        area_num = parse_br_number(abl_adq_val) if abl_adq_val else None
        valor_m2 = (laudo_val/area_num) if (area_num and isinstance(laudo_val,(int,float))) else None
        out['valor_avaliacao'] = {'valor': laudo_val, 'valor_m2': valor_m2}

    _, avaliador = find('laudo de avaliacao','empresa avaliadora','avaliador')
    if avaliador: out['laudo_empresa'] = avaliador

    _, laudo_atual = find('laudo atualizado')
    _, laudo_prox = find('proxima atualizacao')
    cadence = derive_laudo_cadence(laudo_atual, laudo_prox)
    if cadence: out['atualizacao_laudo'] = cadence
    elif laudo_atual: out['atualizacao_laudo'] = f"Última atualização: {fmt_date_br(laudo_atual)}"

    return out if out else None

def fmt_date_br(iso):
    try:
        d = datetime.fromisoformat(str(iso)[:10])
        return d.strftime('%d/%m/%Y')
    except Exception:
        return str(iso)

# fmt_date_mesano (correção pós-publicação -- "essas datas, vamos padronizar... nessa
# formatação: Ago/31"): Data de Emissão/Vencimento no card de "Características da Operação"
# mostravam data cheia (dd/mm/aaaa), pedido do usuário pra padronizar no mesmo formato
# abreviado "Mês/AA" já usado pro Vencimento da tabela de operações (fmtVencAbbr no
# template) e já usado nos valores reais hardcoded de ALIANZA_CARACTERISTICAS_COMPARE
# (ex. 'Jan/22 | Jan/32'). Usa MESES_ABREV_PT/fmt_mes_ano_abrev, definidos mais abaixo no
# arquivo -- ok em Python, resolução de nome global acontece na hora da chamada, não da
# definição.
def fmt_date_mesano(iso):
    try:
        d = datetime.fromisoformat(str(iso)[:10])
        return fmt_mes_ano_abrev(d)
    except Exception:
        return str(iso)

# ---------- Curadoria dos Itens de Acompanhamento (covenants) em 5 categorias canônicas ----------
COVENANT_CATEGORY_ORDER = ['ic','ltv','reserva','garantia','seguro']
COVENANT_CATEGORY_TITLES = {
    'ic': 'Verificação do IC', 'ltv': 'Verificação do LTV', 'reserva': 'Fundo de Reserva',
    'garantia': 'Registro de Garantias', 'seguro': 'Seguro Patrimonial',
}

# Validação calculada (Exigido vs. Atual) do status de covenant, além do que já vem
# pronto da planilha. Só habilitada pra "IC" e "Fundo de Reserva" (únicas categorias
# com valor numérico confiável nas duas pontas na maioria das operações — LTV/Garantias/
# Seguro não têm exigido numérico ou são categóricos, ver roadmap_futuro.md #5) e só
# operação por operação, conforme revisadas (pedido do usuário: "vamos fazendo operação
# por operação porque cada uma tem uma especificidade"). Adicionar aqui só depois de
# conferir os dados daquela operação.
COVENANT_VALIDATION_OPS = {'Evolution'}

# Sincroniza o "Atual" do covenant de LTV curado com o mesmo LTV já usado no quickstat
# "LTV Atual" (derive_ltv_atual, calculado a partir do último registro realizado do
# fluxo). Necessário quando o campo "Atual" estático da tabela de Itens de Acompanhamento
# na aba ficou desatualizado em relação ao fluxo (ex.: BR Prop -- após a substituição de
# garantia de 2025/2026, o "Atual" bruto do LTV usa "Montante Atual CRI" e dá 36,02%,
# enquanto o LTV do fluxo (mesma fonte do "LTV Atual" mostrado alhures no portal) dá
# 36,17% (~36,2%) -- pedido do usuário pra bater com "as outras demonstrações", 34ª
# rodada). Só ativado operação por operação, mesmo padrão do COVENANT_VALIDATION_OPS.
LTV_ATUAL_SYNC_OPS = {'BR Prop'}

# Mesmo racional do LTV_ATUAL_SYNC_OPS acima, mas pro cutoff_date de derive_ltv_atual (42ª
# rodada, achado na MSB Triu -- ver nota na própria função): só ativado operação por operação,
# pra não mudar o "LTV Atual" de operações onde a linha "mais recente com ic+ltv" já é
# confiável mesmo sem cutoff (testado: aplicar o cutoff em todo o portfólio muda o LTV Atual
# de mais 7 operações, cada uma por um motivo possivelmente diferente e não revisado ainda).
LTV_ATUAL_CUTOFF_OPS = {'MSB Triu'}

# Mesma ideia do LTV_ATUAL_SYNC_OPS acima, só que pro "Atual" do covenant de IC/ICSD (36ª
# rodada, Residencial Itaim, ponto 7 -- achado incidentalmente ao investigar o gráfico de
# Índice de Cobertura "errado"). O campo estático "ICSD"/"Atual" do papel (planilha) fica
# uma linha de fluxo "atrasado" em relação ao mês mais recente já apurado -- ex.: papel
# mostra 2,0349x, mas o mês de referência mais atual (Jul/26, conforme a própria mensagem
# do usuário e o gráfico de IC) é 2,3445x (≈"2,34x"). Sem esse sync, a mesma tela mostraria
# 2 valores de "IC atual" diferentes (highlight vs. card de covenant) -- confuso e
# inconsistente. Usa a MESMA linha ("último registro com ic+ltv apurados") já usada por
# derive_ltv_atual(), só que lendo o campo 'ic' em vez de 'ltv'. Só ativado operação por
# operação, mesmo padrão do LTV_ATUAL_SYNC_OPS/COVENANT_VALIDATION_OPS.
IC_ATUAL_SYNC_OPS = {'Residencial Itaim'}

# Ajustes manuais por operação nos Itens de Acompanhamento curados (título/obs de uma
# categoria já existente, ou item extra fora das 5 categorias canônicas, puxado do
# item bruto da planilha por nome). Mesmo padrão do MANUAL_CONTENT/ATIVO_INFO_MANUAL:
# usado quando o usuário pede um ajuste pontual e explícito naquela operação.
COVENANTS_MANUAL = {
    'Calçada': {
        # "Verificação do IC" -> renomear pra "Verificação do IC Gerencial" e tirar o texto (obs)
        #
        # Teste piloto (38ª rodada): usuário pediu pra trazer, só nesta operação, 2 tópicos que
        # não existiam no portal -- Obrigações Pecuniárias (prazos de reporte da CCB) e Quórum de
        # Assembleias (regras de convocação/instalação/deliberação do TS) -- reaproveitando os 2
        # slots das categorias canônicas "garantia" (Registro de Garantias) e "seguro" (Seguro
        # Patrimonial), que na Calçada viravam só "OK"/"Enquadrado" sem muito detalhe. Pedido
        # explícito do usuário: "pode tirar a informação de enquadrado, deixar pra fazer dentro
        # dos itens de cada um" -- ou seja, os 2 cards no nível principal viram só um teaser (obs
        # curto + link), sem chip de status/exigido/atual (que não fazem sentido pra esse tipo de
        # conteúdo -- não é um covenant de enquadramento, é uma lista de obrigações de reporte e
        # regras de quórum). "_clear" é um mecanismo novo em apply_covenants_manual (ver abaixo):
        # remove esses campos do entry depois do 'retitle' de cada categoria, em vez de só
        # sobrescrever. O detalhamento completo (13 itens de Obrigações + 4 seções de Quórum,
        # cada um com a cláusula do CCB/TS de origem) mora em OBRIGACOES_PECUNIARIAS_BY_OP /
        # QUORUM_ASSEMBLEIA_BY_OP, abertos numa sub-página própria (mesmo padrão visual do "Ver
        # quebra do cálculo"/"Ver tabela de integralizações" já usado noutras operações) --
        # conteúdo colado pelo usuário a partir da CCB e do Termo de Securitização, não vem da
        # planilha.
        'retitle': {
            'ic': {'item': 'Verificação do IC Gerencial', 'obs': ''},
            'garantia': {
                'item': 'Obrigações',
                'obs': 'Relatórios periódicos e prazos de reporte previstos na CCB — ver detalhamento completo.',
                '_has_obrigacoes_subpage': True,
                '_clear': ['exigido', 'atual', 'status', 'documento', 'ultima_atualizacao', 'proxima_atualizacao'],
            },
            'seguro': {
                'item': 'Quórum de Assembleias',
                'obs': 'Regras de convocação, instalação e deliberação da Assembleia Geral de Titulares de CRI — ver detalhamento completo.',
                '_has_quorum_subpage': True,
                '_clear': ['exigido', 'atual', 'status', 'documento', 'ultima_atualizacao', 'proxima_atualizacao'],
            },
        },
        # item extra, fora das 5 categorias canônicas, puxado do item bruto "Cessão Conta
        # Vinculada" da planilha, inserido logo após o card de IC
        'extra_items': [
            {'raw_item': 'Cessão Conta Vinculada', 'item': 'Verificação Cessão Conta Vinculada',
             'insert_after': 'ic', '_is_pct': True},
        ],
    },
    'Localfrio': {
        # "Verificação do IC" -> "Verificação do IC Gerencial" (mesmo padrão da Calçada); aqui
        # o obs original ("Acompanhar se... Não tem mínimo para essa operação.") continua válido,
        # então só o título muda (obs não é sobrescrito).
        'retitle': {'ic': {'item': 'Verificação do IC Gerencial'}},
        # item extra "Convenants" (bruto) = covenant financeiro Dívida Líquida/EBITDA (AGT
        # 29/08/2022), fora das 5 categorias canônicas. Ganha link pra sub-página com a tabela de
        # quebra do cálculo do EBITDA/Índice de Cobertura de Serviço da Dívida (ver
        # COVENANT_CALC_BY_OP / parse_covenant_calc_localfrio, fonte: bloco "Movecta" na aba
        # 'Localfrio' colunas L:R linhas 33-52).
        'extra_items': [
            {'raw_item': 'Convenants', 'item': 'Covenant Financeiro (Dívida Líquida/EBITDA)',
             'insert_after': 'ic', '_has_calc_subpage': True},
        ],
    },
    'WT Log': {
        # Os obs brutos da aba são parágrafos jurídicos enormes (definição completa de
        # "Recebíveis", processo de reforço de garantias, lista de seguradoras aceitas
        # etc.) -- pedido do usuário pra encurtar e ficar no mesmo padrão conciso das
        # outras operações (ver ex.: Evolution/CVPAR, obs de 1-2 linhas).
        'retitle': {
            'ic': {'obs': 'Recebíveis de locação da fração ideal (25%) da Devedora nos imóveis frente ao PMT (Amortização + Juros) das Notas Comerciais.'},
            'ltv': {'obs': 'Se ultrapassado, Devedora tem 15 du para propor reforço de garantias; recomposição em até 5 du após aprovação em Assembleia de Titulares.'},
            'reserva': {'obs': 'Valor mínimo = soma das 3 próximas parcelas de Remuneração e Amortização das Notas Comerciais.'},
            'seguro': {'obs': 'Seguro patrimonial com seguradora de primeira linha (rating ≥ AA), vigência mínima de 12 meses, no valor de reconstrução dos imóveis.'},
        },
    },
    'BR Prop': {
        # Item extra "Dívida Financeira Líquida/Propriedades para investimento" (raw item
        # da aba), fora das 5 categorias canônicas -- pedido do usuário (34ª rodada) pra
        # trazer esse covenant pro card (hoje -33%, exigido <50%, enquadrado). Inserido
        # logo após o LTV (ambos são métricas de alavancagem sobre o valor da garantia).
        'extra_items': [
            {'raw_item': 'Dívida Financeira Líquida/Propriedades para investimento',
             'item': 'Dívida Líquida/Propriedades para Investimento',
             'insert_after': 'ltv', '_is_pct': True},
        ],
    },
    'Residencial Jardins': {
        # Ponto 8 (35ª rodada): obs originais são parágrafos jurídicos longos -- encurtados
        # pro mesmo padrão conciso de 1-2 linhas usado nas outras operações (ver WT Log acima).
        'retitle': {
            'ic': {'obs': 'ICSD Médio apurado mensalmente a partir do 15º mês da emissão; abaixo de 1,25x incide prêmio sobre o saldo das Debêntures.'},
            'ltv': {'obs': 'Apuração anual a partir do 12º mês da 1ª Data de Integralização.'},
            'reserva': {'obs': 'Mínimo de 1x a Remuneração até o 12º mês e 3x a partir do 13º mês, com recomposição obrigatória em caso de uso.'},
        },
        # itens extras pedidos pelo usuário ("um tópico do seguro e registro garantias"),
        # hoje fora das 5 categorias canônicas: "Seguros dos Imóveis" puxado por nome (raw_item,
        # mesmo padrão de sempre) e "Registro de Garantias" como item sintético (não existe uma
        # única linha bruta -- consolida as 5 AF de Imóvel + AF de Ações + Cessão Fiduciária dos
        # Recebíveis, todas "OK"/"Enquadrado" na aba, ver 'literal' em apply_covenants_manual).
        # Ordem de insert_after (ambos após "reserva") faz Registro entrar antes de Seguro,
        # batendo com a ordem canônica ic/ltv/reserva/garantia/seguro.
        'extra_items': [
            {'raw_item': 'Seguros dos Imóveis', 'item': 'Seguro Patrimonial',
             'obs': 'Seguro dos imóveis renovado com 15 dias de antecedência do vencimento da apólice.',
             'insert_after': 'reserva'},
            {'literal': {
                'item': 'Registro de Garantias', 'exigido': 'OK', 'atual': 'OK', 'status': 'Enquadrado',
                'obs': 'Alienação Fiduciária dos 5 imóveis e das ações da Promontoria Imóveis 5, e Cessão Fiduciária dos Recebíveis, devidamente registradas.',
                'documento': 'Contratos de Alienação Fiduciária de Imóveis / de Ações / Cessão Fiduciária de Recebíveis',
             }, 'insert_after': 'reserva'},
        ],
    },
    'MSB Axis': {
        # 37ª rodada, ponto 5: obs curtos, mesmo padrão das últimas operações.
        'retitle': {
            'ic': {'obs': 'Razão entre o VPL do Fluxo de Caixa (receita de carteira + estoque projetada) e o Saldo Devedor dos CRI, mantida em patamar igual ou superior a 1,30x.'},
            'garantia': {'obs': 'Registro da Alienação Fiduciária de Imóveis em até 30 dias contados da prenotação.'},
        },
        # Ponto 4: item bruto "Acompanhamento Estrutura de Capital" já existe na planilha
        # (exigido >=20%, atual ~37%) mas ficava fora das 5 categorias canônicas -- trazido
        # como item extra, mesmo mecanismo de sempre (raw_item por nome), logo após o IC.
        'extra_items': [
            {'raw_item': 'Acompanhamento Estrutura de Capital', 'item': 'Estrutura de Capital',
             'obs': 'Razão entre (i) o montante aportado na Emitente pelos sócios/investidores e (ii) a exposição de caixa estimada do empreendimento, mantida igual ou superior a 20%.',
             'insert_after': 'ic', '_is_pct': True},
            # Ajuste pós-publicação, ponto 1: card "Integralizações" com link pra sub-página
            # (mesmo padrão visual do "Ver quebra do cálculo" da Localfrio) -- item sintético,
            # sem exigido/atual/status (não é um covenant de enquadramento, só um resumo com
            # link pra tabela de abertura). Fonte: parse_integralizacoes_axis().
            {'literal': {
                'item': 'Integralizações',
                'obs': 'Integralizações realizadas conforme liberações dos CRI e evolução da obra, pari passu com os aportes de equity.',
            }, 'insert_after': 'garantia', '_has_integralizacoes_subpage': True},
        ],
    },
    'MSB Triu': {
        # 43ª rodada, ponto 8 -- mesmo card "Integralizações" com sub-página da MSB Axis (ver
        # parse_integralizacoes_triu). 'garantia' não existe mais nas categorias canônicas da
        # Triu (os 2 itens "Registro de Garantias"/"Seguro Patrimonial" saíram na 42ª rodada,
        # ajuste pós-publicação -- ver install_obrigacoes_quorum_placeholders), então insere
        # depois de 'reserva' (Fundo de Reserva), que é a última categoria canônica de fato
        # presente antes dos placeholders Obrigações/Quórum.
        'extra_items': [
            {'literal': {
                'item': 'Integralizações',
                'obs': 'Integralizações realizadas conforme liberações dos CRI e evolução da obra, pari passu com os aportes de equity.',
            }, 'insert_after': 'reserva', '_has_integralizacoes_subpage': True},
        ],
    },
    'MSB Edson': {
        # 43ª rodada, ponto 8 -- idem, inserido depois de 'ic' (única categoria canônica
        # presente na Edson).
        'extra_items': [
            {'literal': {
                'item': 'Integralizações',
                'obs': 'Integralizações realizadas conforme liberações dos CRI e evolução da obra.',
            }, 'insert_after': 'ic', '_has_integralizacoes_subpage': True},
        ],
    },
}

def apply_covenants_manual(op_name, result, raw_covenants):
    manual = COVENANTS_MANUAL.get(op_name)
    if not manual:
        return result
    for entry in result:
        override = manual.get('retitle', {}).get(entry.get('_categoria'))
        if override:
            # "_clear" (38ª rodada, Calçada): lista de campos pra REMOVER do entry depois do
            # update abaixo, em vez de só sobrescrever -- usado quando uma categoria canônica
            # (que normalmente tem exigido/atual/status de covenant) vira um item puramente
            # informativo com sub-página própria (ver COVENANTS_MANUAL['Calçada'] acima). A
            # própria chave "_clear" nunca vai parar no entry (é retirada do override antes do
            # update, senão sobraria um campo "_clear" bruto no JSON final).
            override = dict(override)
            clear_fields = override.pop('_clear', None)
            entry.update(override)
            if clear_fields:
                for f in clear_fields:
                    entry.pop(f, None)
    for extra in manual.get('extra_items', []):
        if 'literal' in extra:
            # item sintético (não vem de uma única linha bruta da planilha) -- usado
            # quando o card precisa consolidar várias linhas brutas (ex.: Registro de
            # Garantias da Residencial Jardins, que junta 5 AF de Imóvel + AF de Ações +
            # Cessão Fiduciária, todas "OK", num único item resumido).
            entry = dict(extra['literal'])
            entry.setdefault('item', extra.get('item', 'Item'))
        else:
            raw = next((c for c in raw_covenants if norm(c.get('item','')) == norm(extra['raw_item'])), None)
            if raw is None:
                continue
            entry = dict(raw)
            entry['item'] = extra['item']
            if extra.get('obs'):
                entry['obs'] = extra['obs']
        entry['_categoria'] = 'manual'
        if extra.get('_is_ratio'):
            entry['_is_ratio'] = True
        if extra.get('_is_pct'):
            entry['_is_pct'] = True
        if extra.get('_has_calc_subpage'):
            entry['_has_calc_subpage'] = True
        # Ajuste pós-publicação (37ª rodada, MSB Axis, ponto 1): mesmo padrão visual do link
        # "_has_calc_subpage" (Localfrio), mas pra uma sub-página com formato de tabela
        # diferente (abertura de integralizações por data, não uma tabela de períodos como
        # colunas) -- flag própria pra não forçar o formato do covenant_calc.
        if extra.get('_has_integralizacoes_subpage'):
            entry['_has_integralizacoes_subpage'] = True
        insert_idx = len(result)
        after_cat = extra.get('insert_after')
        if after_cat:
            for i, e in enumerate(result):
                if e.get('_categoria') == after_cat:
                    insert_idx = i + 1
                    break
        result.insert(insert_idx, entry)
    return result

def parse_covenant_number(val):
    """Extrai um número comparável de um valor de covenant (exigido ou atual), que na
    planilha pode vir como número pronto ou como texto em formatos variados
    (">1,20", ">=1,4X", "1,20x", "-", "OK"). Retorna (operador, número) ou None quando
    não dá pra extrair um número de verdade (texto livre, "-", "OK")."""
    if isinstance(val, (int, float)):
        return ('>=', float(val))
    if val is None:
        return None
    s = str(val).strip()
    if not s or s in ('-', '—', 'N/A', 'NA'):
        return None
    m = re.match(r'^(>=|<=|>|<)?\s*([0-9]+(?:[.,][0-9]+)?)\s*[xX]?$', s)
    if not m:
        return None
    op = m.group(1) or '>='
    try:
        num = float(m.group(2).replace(',', '.'))
    except ValueError:
        return None
    return (op, num)

def compute_covenant_check(exigido_raw, atual_raw):
    """Compara Exigido x Atual e retorna se bate (ok=True) segundo o operador do
    Exigido (>=, >, <=, <; default >= quando o valor vem puro sem operador). None
    quando algum dos dois lados não é um número extraível (ver parse_covenant_number)."""
    ex = parse_covenant_number(exigido_raw)
    at = parse_covenant_number(atual_raw)
    if ex is None or at is None:
        return None
    op, ex_val = ex
    _, at_val = at
    if op == '>=': ok = at_val >= ex_val
    elif op == '>': ok = at_val > ex_val
    elif op == '<=': ok = at_val <= ex_val
    elif op == '<': ok = at_val < ex_val
    else: ok = at_val >= ex_val
    return {'ok': ok, 'exigido_val': round(ex_val, 6), 'atual_val': round(at_val, 6), 'op': op}

def attach_covenant_calc(entry):
    """Anexa entry['_calc'] com o resultado do cálculo e se diverge do status que veio
    pronto da planilha (só quando o status é claramente 'enquadrado' ou 'desenquadrado'
    — 'verificar'/vazio não têm um lado claro pra comparar, aí só mostra o cálculo)."""
    calc = compute_covenant_check(entry.get('exigido'), entry.get('atual'))
    if calc is None:
        return
    status_norm = norm(entry.get('status',''))
    diverge = None
    if 'desenquadr' in status_norm:
        diverge = calc['ok'] is True
    elif 'enquadr' in status_norm:
        diverge = calc['ok'] is False
    calc['diverge'] = diverge
    entry['_calc'] = calc

def covenant_tok(s):
    return re.sub(r'[^a-z0-9]+', ' ', norm(s)).strip()

def covenant_has_word(t, w):
    return w in t.split()

def covenant_bucket_of(item_text):
    """Extraída de curate_covenants() pra poder ser reaproveitada fora dali (ver
    find_covenant_ultima_atualizacao, usada pelo corte do IC_ATUAL_SYNC_OPS) -- mesma regra
    de categorização, uma única fonte de verdade."""
    t = covenant_tok(item_text)
    if covenant_has_word(t, 'ltv'):
        return 'ltv'
    if covenant_has_word(t, 'ic') or covenant_has_word(t, 'icsd') or ('indice' in t and 'cobertura' in t):
        return 'ic'
    if 'fundo' in t and 'reserva' in t:
        return 'reserva'
    if ('alienacao' in t and 'fiduciaria' in t) or ('registro' in t and 'garantia' in t):
        return 'garantia'
    if 'seguro' in t and 'patrimonial' in t:
        return 'seguro'
    return None

# obligation_bucket_of / mine_obligation_items (48ª rodada): correção sobre a 46ª/47ª -- o
# usuário apontou que o bloco "Obrigações" da aba de Acompanhamento estava errado: só tinha os
# cards sintéticos "Obrigações"/"Quórum de Assembleias" (instalados por
# install_obrigacoes_quorum_placeholders, quase sempre "conteúdo ainda não cadastrado"), e
# Quórum de Assembleias nem devia estar ali ("você trouxe informações de quorum de
# assembleias.. não faz sentido"). Pedido explícito: "aqui eu te falei em obrigações vamos
# trazer seguro, laudo, dfs e etc... tudo que é obrigações que tem a necessidade de entrega".
# Essa é exatamente a massa de itens brutos identificada na investigação da 46ª rodada como
# "hoje 100% oculta" (DF Anual/Trimestral, Laudo de Avaliação, Seguro/apólices, Cessão
# Fiduciária) -- covenant_bucket_of() não cobre nenhum desses (só sabe 'seguro'+'patrimonial'
# juntos, nada de laudo/DF/cessão). obligation_bucket_of() é um classificador PARALELO, mais
# amplo, só pra esses 4 tipos de obrigação de entrega/renovação -- roda direto sobre a lista de
# covenants BRUTA (independente do que curate_covenants() já escolheu pelos 5 buckets
# canônicos): não há sobreposição real (nenhum item de ic/ltv/reserva bate aqui, conferido
# item a item nas 43 operações) e o pick canônico de 'seguro'/'garantia' de qualquer forma
# nunca sobrevive em result (sempre removido por install_obrigacoes_quorum_placeholders via
# LEGACY_TITLES) -- então reaproveitar o texto bruto original aqui é estritamente uma
# melhoria, nunca uma duplicata.
def obligation_bucket_of(item_text):
    t = covenant_tok(item_text)
    if 'seguro' in t or 'apolice' in t:
        return 'seguro'
    if 'laudo' in t:
        return 'laudo'
    if 'cessao' in t:
        return 'cessao'
    if ('demonstra' in t and 'financeir' in t) or re.search(r'\b(df|dfs)\b', t) or 'balanc' in t or 'declaracao' in t:
        return 'df'
    return None

def _sane_iso_date(v):
    """Descarta datas-lixo tipo '1900-02-28' (bug clássico do sistema de datas do Excel: uma
    célula formatada como data mas vazia/com valor não-data vira um serial baixo, que o
    openpyxl lê como uma data real pertinho do epoch de 1900 -- achado ao minerar
    'Renovação Apólices e Endossos' da MegaModa, ver mine_obligation_items). Qualquer ano
    < 2000 aqui é sinal do mesmo bug, não uma data de acompanhamento real -- trata como
    ausente em vez de deixar a linha aparecer como "Vencido" por um artefato de parsing."""
    if isinstance(v, str) and re.match(r'^\d{4}-\d{2}-\d{2}$', v) and v < '2000-01-01':
        return None
    return v

def mine_obligation_items(covenants):
    """Ao contrário de curate_covenants() (que escolhe 1 candidato por categoria via pick()),
    aqui TODOS os itens que baterem entram como linhas distintas -- uma operação pode ter DF
    Anual E DF Trimestral, que são 2 obrigações diferentes, não uma escolha entre as duas.
    Mantém o texto/dados originais da planilha (item, exigido, atual, status, datas, obs) --
    só adiciona _categoria pra classificar em Obrigações.

    _acomp_only=True (49ª rodada, correção sobre a 48ª): esses itens são pra alimentar SÓ a
    sub-aba Obrigações da aba de Acompanhamento (visão cross-portfolio) -- NÃO o painel "Itens
    de Acompanhamento" da página de detalhe de cada operação. O usuário já tinha pedido, rodadas
    atrás, pra consolidar esse tipo de detalhe (DFs, laudo, seguro, cessão...) dentro de UM card
    "Obrigações" só naquele painel (em vez de 1 card por item) -- "já tínhamos ajustado esse
    ponto para deixar tudo dentro de Obrigações [...] por favor ajustar para o jeito que estava
    antes". A 48ª rodada, ao colocar esses itens direto em `result` (op.covenants), quebrou
    esse acordo sem querer: como op.covenants alimenta os 2 lugares (painel de detalhe E aba de
    Acompanhamento), os itens minerados passaram a aparecer como cards extras também no painel
    de detalhe. O frontend (showDetail) agora filtra por esse flag antes de montar o painel de
    detalhe -- allCovenantRows() (Acompanhamento) continua incluindo tudo, sem filtro."""
    out = []
    for c in covenants or []:
        bucket = obligation_bucket_of(c.get('item', ''))
        if not bucket:
            continue
        entry = dict(c)
        entry['_categoria'] = bucket
        entry['_acomp_only'] = True
        if 'proxima_atualizacao' in entry:
            entry['proxima_atualizacao'] = _sane_iso_date(entry['proxima_atualizacao'])
            if entry['proxima_atualizacao'] is None:
                del entry['proxima_atualizacao']
        if 'ultima_atualizacao' in entry:
            entry['ultima_atualizacao'] = _sane_iso_date(entry['ultima_atualizacao'])
            if entry['ultima_atualizacao'] is None:
                del entry['ultima_atualizacao']
        out.append(entry)
    return out

def find_covenant_ultima_atualizacao(covenants, categoria):
    """Devolve a 'Última Atualização' (string ISO) do primeiro covenant bruto que cair na
    categoria dada (ver covenant_bucket_of) -- usado como corte de data pro
    derive_ic_atual() do IC_ATUAL_SYNC_OPS (ver nota lá)."""
    for c in covenants or []:
        if covenant_bucket_of(c.get('item','')) == categoria:
            ua = c.get('ultima_atualizacao')
            if isinstance(ua, str):
                return ua
    return None

def curate_covenants(covenants, ic_minimo_fallback=None, op_name=None, ltv_atual_sync=None, ic_atual_sync=None):
    buckets = {k: [] for k in COVENANT_CATEGORY_ORDER}
    for c in covenants:
        cat = covenant_bucket_of(c.get('item',''))
        if cat == 'ltv':
            buckets['ltv'].append(c)
        elif cat == 'ic':
            # cobre abas que abreviam o item como "IC", como "ICSD" (Índice de Cobertura do
            # Serviço da Dívida -- ex.: Residencial Itaim, 36ª rodada) e as que escrevem por
            # extenso "Índice de Cobertura" (ex.: WT Log, CVPAR, Alianza Mauá, MZO,
            # Residencial Jardins) -- antes só "IC" batia, e o item ficava de fora das 5
            # categorias canônicas (oculto por padrão), fazendo a "Verificação do IC" nem
            # aparecer nesses casos. Correção geral de parsing, não específica de operação.
            buckets['ic'].append(c)
        elif cat == 'reserva':
            buckets['reserva'].append(c)
        elif cat == 'garantia':
            buckets['garantia'].append(c)
        elif cat == 'seguro':
            buckets['seguro'].append(c)
        # itens que não batem em nenhuma categoria ficam ocultos por padrão

    def pick(cands, key):
        if not cands: return None
        if len(cands) == 1: return cands[0]
        if key == 'ic':
            # prefere o item com lógica de média móvel (evita pegar o "IC spot" quando há duplicata)
            for c in cands:
                ob = norm(c.get('obs',''))
                if 'media' in ob or 'movel' in ob or '3 meses' in ob or '3 ultimas' in ob or '3 ultimos' in ob:
                    return c
            # Ajuste pós-publicação (42ª rodada, MSB Triu): quando há 2 linhas brutas batendo
            # em "ic" (ex.: "IC - Cash Out", uma condição de gatilho binária pra liberação de
            # recursos, com "Atual" textual "SIM"/"OK" -- não é o índice de cobertura de
            # verdade) e "IC" (a razão VPL/saldo devedor, com "Atual" numérico), o fallback
            # abaixo (só olha se 'exigido' é numérico) pegava a 1ª linha da planilha às cegas
            # -- nesse caso "IC - Cash Out", produzindo um card sem sentido ("Atual: SIM").
            # Prefere aqui, antes do fallback genérico, o candidato cujo 'atual' também é
            # numérico (um índice de cobertura de verdade sempre reporta um valor apurado, não
            # um "SIM"/"OK" categórico de gatilho) -- regra geral, não específica da Triu.
            numeric_atual = [c for c in cands if isinstance(c.get('atual'), (int,float))]
            if len(numeric_atual) == 1:
                return numeric_atual[0]
        # fallback: prefere o que tem 'exigido' numérico populado, senão o primeiro
        for c in cands:
            if isinstance(c.get('exigido'), (int,float)):
                return c
        return cands[0]

    # used_raw_items (correção pós-publicação, 49ª rodada): texto bruto (normalizado) de cada
    # linha da planilha já consumida por um pick canônico IC/LTV/reserva (essas 3 categorias
    # SEMPRE aparecem tal qual -- "Verificação do IC"/"Verificação do LTV"/"Fundo de Reserva")
    # ou por um 'extra_item' de COVENANTS_MANUAL (também sempre mostrado) -- usado mais abaixo
    # pra EXCLUIR essas mesmas linhas de mine_obligation_items() e evitar duplicata. Bug real
    # achado na Calçada: a linha bruta "Cessão Conta Vinculada" já vira o item extra "Verificação
    # Cessão Conta Vinculada" (Ordinário, _is_pct, ver COVENANTS_MANUAL['Calçada']['extra_items'])
    # -- mas como o TEXTO bruto também contém "cessao", obligation_bucket_of() batia nela de novo
    # e mine_obligation_items() criava uma 2ª cópia solta (sem o retitle/_is_pct do extra_item,
    # então Exigido/Atual apareciam com a formatação bruta em vez de %) marcada _categoria=
    # 'cessao' -> _tipo='obrigacao', indo parar errado na sub-aba Obrigações (usuário: "eu tinha
    # te falado que era um acompanhamento ordinário [...] essa informação deve ser passada igual
    # está na página dela em %").
    # IMPORTANTE: 'garantia'/'seguro' (as outras 2 categorias canônicas) ficam DE FORA dessa
    # exclusão de propósito -- install_obrigacoes_quorum_placeholders() (ver abaixo) sempre
    # STRIPA esses 2 picks (título vira exatamente "Registro de Garantias"/"Seguro Patrimonial",
    # removido via LEGACY_TITLES) e os substitui pelos 2 cards-placeholder sintéticos; ou seja,
    # o pick canônico NUNCA é realmente mostrado como dado de seguro/garantia -- é a mineração
    # abaixo que recupera essas mesmas linhas brutas como itens de Obrigações de verdade (ex.:
    # "Seguro Patrimonial"/"Seguro do Ativo" da Calçada). Excluir esse texto aqui apagaria a
    # ÚNICA fonte de dado real de seguro/garantia pra Obrigações, em qualquer operação.
    used_raw_items = set()
    result = []
    for key in COVENANT_CATEGORY_ORDER:
        chosen = pick(buckets[key], key)
        if not chosen: continue
        if key in ('ic', 'ltv', 'reserva'):
            used_raw_items.add(norm(chosen.get('item','')))
        entry = dict(chosen)
        entry['item'] = COVENANT_CATEGORY_TITLES[key]
        entry['_categoria'] = key
        if key == 'ic':
            entry['_is_ratio'] = True
            if entry.get('exigido') in (None,'','-') and ic_minimo_fallback is not None:
                entry['exigido'] = round(ic_minimo_fallback, 6)
            if ic_atual_sync is not None and op_name in IC_ATUAL_SYNC_OPS:
                # ver nota em IC_ATUAL_SYNC_OPS -- "Atual" estático do papel fica 1 mês
                # atrasado em relação ao IC realmente mais recente (mesma linha usada pelo
                # gráfico de Índice de Cobertura).
                entry['atual'] = round(ic_atual_sync, 6)
        if key == 'ltv' and ltv_atual_sync is not None and op_name in LTV_ATUAL_SYNC_OPS:
            entry['atual'] = round(ltv_atual_sync, 6)
            # exibido com 1 casa decimal (36,2%), igual ao quickstat "LTV Atual" (que já
            # usa 1 casa) -- sem _is_pct o valor cai no fmtGeneric (2 casas fixas, "36,17%"),
            # divergente da própria demonstração "LTV Atual" da mesma tela.
            entry['_is_pct'] = True
            entry['_pct_decimals'] = 1
        if key in ('ic', 'reserva') and op_name in COVENANT_VALIDATION_OPS:
            attach_covenant_calc(entry)
        result.append(entry)
    result = apply_covenants_manual(op_name, result, covenants)
    result = install_obrigacoes_quorum_placeholders(result)
    manual = COVENANTS_MANUAL.get(op_name, {})
    for extra in manual.get('extra_items', []):
        if 'raw_item' in extra:
            used_raw_items.add(norm(extra['raw_item']))
    mining_source = [c for c in covenants if norm(c.get('item','')) not in used_raw_items]
    result.extend(mine_obligation_items(mining_source))
    for entry in result:
        entry['_tipo'] = covenant_tipo(entry, op_name)
    return result

# OBRIGACOES_REVISADAS_OPS (49ª rodada): o usuário está revisando a categorização de Obrigações
# operação por operação (começou por Calçada, depois Alianza GRU e Mauá) e pediu, nesse meio
# tempo, pra sub-aba Obrigações da aba de Acompanhamento mostrar SÓ as operações já revisadas --
# "por enquanto na aba de acompanhamento obrigações, deixar só as operações que estamos
# ajustando" -- em vez das 31 operações com dado minerado automaticamente (que ainda não
# passaram pela curadoria manual dele, incluindo o bug de data já achado na MegaModa). O
# Ordinário fica como está, sem filtro ("na parte de ordinário pode deixar do jeito que está
# mesmo") -- só os 5 buckets canônicos de sempre, não passaram por mineração nova. Adicionar o
# nome da operação aqui assim que ela for revisada; nenhum outro lugar do portal (painel de
# detalhe, sub-página "Ver obrigações") é afetado por essa lista -- só a sub-aba Obrigações do
# Acompanhamento.
OBRIGACOES_REVISADAS_OPS = {'Calçada', 'Alianza GRU e Mauá'}

# covenant_tipo (46ª rodada, corrigida na 48ª/49ª): classifica cada item de Acompanhamento como
# 'ordinario' (o que já é checado no dia a dia -- IC, LTV, Fundo de Reserva, e os itens
# 'manual' de natureza financeira/de índice, ex.: Estrutura de Capital, Integralizações,
# Covenant Financeiro), 'obrigacao' (deveres de entrega/renovação -- seguro, laudo de
# avaliação, DFs/demonstrações financeiras, cessão fiduciária -- ver obligation_bucket_of/
# mine_obligation_items, e só pra operações em OBRIGACOES_REVISADAS_OPS, ver acima) ou None
# (fora da aba de Acompanhamento por completo).
#
# 48ª rodada, correção sobre a 46ª/47ª: o usuário apontou 2 problemas na 1ª versão --
# (1) "você trouxe informações de quorum de assembleias.. não faz sentido" -- Quórum de
# Assembleias é regra de votação de assembleia, não um dever de entrega com data/status pra
# monitorar, então sai da aba de Acompanhamento (None) -- mas continua aparecendo normalmente
# no painel de Itens de Acompanhamento da página de detalhe da operação (link pra subpágina),
# só não entra nos 2 blocos de Acompanhamento. O card genérico "Obrigações" (placeholder da
# subpágina, sem data/status próprios -- ver install_obrigacoes_quorum_placeholders) sai pelo
# mesmo motivo: virou redundante depois que os itens minerados abaixo trazem o dado de
# verdade linha a linha. (2) "aqui eu te falei em obrigações vamos trazer seguro, laudo,
# dfs e etc" -- as categorias 'seguro'/'laudo'/'df'/'cessao' (mine_obligation_items) agora
# entram como Obrigações de verdade, cada uma com seu próprio prazo/status.
def covenant_tipo(entry, op_name=None):
    if entry.get('_has_obrigacoes_subpage') or entry.get('_has_quorum_subpage'):
        return None
    if entry.get('_categoria') in ('garantia', 'seguro', 'laudo', 'df', 'cessao'):
        if op_name is not None and op_name not in OBRIGACOES_REVISADAS_OPS:
            return None
        return 'obrigacao'
    return 'ordinario'

# 41ª rodada: os 2 cards "Obrigações Pecuniárias" / "Quórum de Assembleias" (piloto Calçada,
# ver COVENANTS_MANUAL['Calçada'] e OBRIGACOES_PECUNIARIAS_BY_OP/QUORUM_ASSEMBLEIA_BY_OP acima)
# agora ficam instalados em TODAS as operações, mesmo sem conteúdo ainda -- pedido do usuário:
# "já pode colocar em todas operações esses dois cards [...] mesmo que ainda não tenha nenhuma
# informação cadastrada já vamos deixar isso instalado [...] depois colocamos as informações".
# Diferente da Calçada (onde os 2 tópicos REAPROVEITAM os slots de "Registro de Garantias"/
# "Seguro Patrimonial" via retitle, porque lá esse detalhamento SUBSTITUI o que existia), nas
# demais operações os cards são itens SINTÉTICOS ADICIONAIS (mesmo padrão de "Integralizações"
# na MSB Axis) -- não mexem nos covenants reais de garantia/seguro dessas operações, que
# continuam com seu exigido/atual/status normais. A sub-página abre mesmo sem dado (mostra
# "Sem dado disponível." -- ver topicsSubpageHtml no template) até o conteúdo real da operação
# ser adicionado a OBRIGACOES_PECUNIARIAS_BY_OP/QUORUM_ASSEMBLEIA_BY_OP.
def install_obrigacoes_quorum_placeholders(result):
    # 42ª rodada, ajuste pós-publicação: onde a operação já tinha "Registro de Garantias"/
    # "Seguro Patrimonial" com dado real cadastrado (categoria canônica 'garantia'/'seguro', ou
    # item extra com o mesmo título -- ex.: Residencial Jardins), esses 2 itens são REMOVIDOS --
    # pedido do usuário: os novos cards "Obrigações Pecuniárias"/"Quórum de Assembleias" que
    # acabamos de instalar em todas as operações VÃO SUBSTITUIR esse conteúdo (mesmo racional já
    # usado na Calçada, só que lá via retitle/_clear porque o detalhamento entrou na mesma
    # rodada; nas demais operações o detalhamento ainda não existe, então por ora os 2 itens
    # somem e os novos cards ficam como placeholder até a informação real ser cadastrada, op a
    # op). Filtra por TÍTULO (não por _categoria) pra pegar tanto os itens curados pelas 5
    # categorias canônicas quanto os itens extras com esse mesmo nome (Residencial Jardins).
    # Não afeta a Calçada, que já usa esses 2 slots SOB OUTRO NOME via retitle.
    LEGACY_TITLES = {'Registro de Garantias', 'Seguro Patrimonial'}
    result = [e for e in result if e.get('item') not in LEGACY_TITLES]
    has_obrigacoes = any(e.get('_has_obrigacoes_subpage') for e in result)
    has_quorum = any(e.get('_has_quorum_subpage') for e in result)
    if not has_obrigacoes:
        result.append({
            'item': 'Obrigações',
            'obs': 'Conteúdo ainda não cadastrado para esta operação.',
            '_categoria': 'manual',
            '_has_obrigacoes_subpage': True,
        })
    if not has_quorum:
        result.append({
            'item': 'Quórum de Assembleias',
            'obs': 'Conteúdo ainda não cadastrado para esta operação.',
            '_categoria': 'manual',
            '_has_quorum_subpage': True,
        })
    return result

# ---------- Indicadores parser (generic raw dated table, no field curation) ----------
def parse_indicadores_sheet(name, max_scan_rows=10, safety_cap=800, blank_break=15, max_col=60):
    ws = wb[name]
    max_r = min(ws.max_row, max_scan_rows + safety_cap + 5)
    max_c = min(ws.max_column, max_col)
    all_rows = list(ws.iter_rows(min_row=1, max_row=max_r, max_col=max_c, values_only=True))

    header_row = None; header_vals = None
    for r in range(1, min(max_scan_rows, len(all_rows))+1):
        row = all_rows[r-1]
        for v in row:
            if norm(v) == 'data':
                header_row = r; header_vals = row; break
        if header_row: break

    result = {'preamble': [], 'columns': [], 'records': []}

    # capture any non-empty rows before the header as a small raw "preamble" table
    # (e.g. Calçada's stock/sales summary block sitting above the monthly series)
    pre_end = (header_row - 1) if header_row else min(len(all_rows), 8)
    for r in range(1, pre_end+1):
        row = all_rows[r-1] if r-1 < len(all_rows) else []
        trimmed = [to_jsonable(v) for v in row]
        while trimmed and trimmed[-1] is None:
            trimmed.pop()
        if trimmed:
            result['preamble'].append(trimmed)

    if header_row is None:
        return result if result['preamble'] else None

    data_cols = [i for i,v in enumerate(header_vals) if norm(v)=='data']
    start_col = data_cols[0]
    end_col = data_cols[1] if len(data_cols) > 1 else len(header_vals)

    colmap = {}
    seen = {}
    for c in range(start_col, end_col):
        v = header_vals[c] if c < len(header_vals) else None
        if v in (None,''): continue
        key = str(v).strip()
        if key in seen:
            seen[key]+=1; key = f"{key}_{seen[key]}"
        else:
            seen[key]=0
        colmap[key] = c

    data_col_idx = colmap.get('Data')
    records = []
    blanks = 0
    for r in range(header_row+1, len(all_rows)+1):
        row = all_rows[r-1]
        data_val = row[data_col_idx] if (data_col_idx is not None and data_col_idx < len(row)) else None
        if data_val in (None,''):
            blanks += 1
            if blanks >= blank_break and records: break
        else:
            blanks = 0
            rec = {}
            for k,c in colmap.items():
                if c < len(row) and row[c] not in (None,''):
                    rec[k] = to_jsonable(row[c])
            records.append(rec)
    result['columns'] = list(colmap.keys())
    result['records'] = records
    return result

# ---------- Summary field extraction ----------
def find_papel_value(papel, *substrings, exclude=()):
    # try exact-ish match first (normalized key equality with first substring), then contains
    normed = {norm(k): v for k, v in papel.items()}
    for sub in substrings:
        if sub in normed:
            return normed[sub]
    # Correção (checagem do "Volume de Emissão" pedida pelo usuário -- achado ao investigar
    # inVista, que aparecia com R$26,7 MM, um valor claramente baixo demais perto do seu Saldo
    # Devedor de R$273 MM): o loop de "contains" abaixo ANTES iterava por CHAVE (linha da
    # planilha) e testava todos os `substrings` pra cada chave, retornando na 1ª chave que
    # batesse com QUALQUER substring -- então um substring mais GENÉRICO (ex.: "volume emissao",
    # sempre por último na lista, de propósito, como fallback) podia "ganhar" de um substring mais
    # ESPECÍFICO só porque a linha genérica aparecia antes na planilha. Caso real: inVista tem 2
    # linhas -- "Volume Emissão - Sênior (Cotas)" (26,7 MM, só a fatia sênior) ANTES de "Volume
    # Emissão - Total (Cotas)" (102,1 MM, o total de verdade) -- e como as 2 contêm "volume
    # emissao", a função sempre devolvia a 1ª (Sênior), nunca chegava na 2ª (Total), não importa
    # a ordem dos synonyms passados pela chamada. Fix: itera por SUBSTRING primeiro (respeitando a
    # ordem de prioridade que quem chama já passa), só then por chave -- um substring mais
    # específico, listado antes pela chamada, agora tem prioridade de verdade sobre um genérico
    # listado depois, não importa a ordem das linhas na planilha.
    for sub in substrings:
        for k, v in papel.items():
            nk = norm(k)
            if any(ex in nk for ex in exclude):
                continue
            if sub in nk:
                return v
    return None

def fmt_brl_str(v):
    if v is None or not isinstance(v,(int,float)): return None
    s = format(int(round(v)), ',').replace(',', '.')
    return 'R$ ' + s

# fmt_brl_maybe_multi (rodada de revisão geral de UI): algumas abas guardam "Volume Emissão"
# como vários números separados por espaço numa célula só (ex.: Habibs "75000000 50000000
# 25000000" -- total + valor de cada série, sem nenhuma formatação), em vez de um número puro
# -- daí caírem no ramo "else volume_emissao" de build_caracteristicas() sem NUNCA passar por
# fmt_brl_str, aparecendo cru no card de Características. Levantamento contra as 43 operações:
# não é só a Habibs -- Pirelli, ECLA, Lux, SKR, JALGP, PKK, Apil, LBV, Vitacon, IBL, Planta -
# Ed. Lara têm o mesmo padrão em Volume Emissão. Exatamente o tipo de inconsistência apontada
# pelo usuário ("características da operação... entro em outra operação e não tá formatado
# igual"). Detecta a célula com 2+ números puros separados por espaço e formata cada um em BRL,
# juntando com " | " (mesmo separador neutro já usado em "Cód. Cetip" pra múltiplos códigos, e
# no card comparativo da Alianza) -- não usa "+"/soma: em alguns casos o 1º valor É o total das
# séries seguintes (Habibs: 75.000.000 = 50.000.000 + 25.000.000; IBL: 97.000.000 = 65.000.000 +
# 22.000.000 + 10.000.000), mas nem sempre (Apil: "35000000 35000000" são 2 séries iguais, não
# total+parte) -- sem uma legenda por token vinda da planilha, afirmar soma seria arriscar uma
# conta errada. "|" só lista os valores, sem alegar relação nenhuma entre eles. Genérico: aplica
# em Volume Emissão E Volume Integralizado (mesmo padrão de campo, mesmo risco), não só onde já
# foi visto.
def fmt_brl_maybe_multi(v):
    if isinstance(v, (int, float)):
        return fmt_brl_str(v)
    if not isinstance(v, str):
        return v
    tokens = v.split()
    if len(tokens) < 2 or not all(re.fullmatch(r'\d+(\.\d+)?', t) for t in tokens):
        return v
    return ' | '.join(fmt_brl_str(float(t)) for t in tokens)

def fmt_pct_str(v, digits=2):
    if v is None or not isinstance(v,(int,float)): return None
    s = f"{v*100:.{digits}f}".replace('.', ',')
    return s + '%'

def clean_indexador(v):
    """Várias abas guardam o indexador com uma anotação técnica de defasagem
    (ex.: 'IPCA (M-2)', 'IPCA (M-1)') que é só informação interna de qual mês do
    índice é usado no cálculo -- sem valor pro leitor do portal e que só polui a
    exibição de 'Remuneração'. Remove esse sufixo '(M-N)' mantendo o indexador puro
    (ex.: 'IPCA (M-2)' -> 'IPCA'). Padrão geral, aplicado em todas as operações."""
    if not isinstance(v, str): return v
    return re.sub(r'\s*\(M-\d+\)\s*', '', v).strip()

def parse_pct_from_text(raw):
    """Algumas abas guardam 'Taxa de Juros' como texto anotado (ex.: '6,00% (Compramos a
    6,25%)') em vez de um float puro. Extrai o primeiro percentual do texto e devolve como
    fração (0.06), pra funcionar em qualquer lugar que já espera um número (fmtPct, etc)."""
    if isinstance(raw, (int, float)): return raw
    if not isinstance(raw, str): return None
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*%', raw)
    if not m: return None
    return float(m.group(1).replace(',', '.')) / 100

def infer_cadence_from_fluxo(fluxo_data):
    if not fluxo_data: return None
    recs = fluxo_data[0]['records']
    dates = sorted(r['data'] for r in recs if isinstance(r.get('data'), str))[:8]
    if len(dates) < 3: return None
    try:
        ds = [datetime.fromisoformat(d) for d in dates]
    except ValueError:
        return None
    gaps = [(ds[i+1]-ds[i]).days for i in range(len(ds)-1)]
    if not gaps: return None
    avg_gap = sum(gaps)/len(gaps)
    if 25 <= avg_gap <= 35: return 'Mensal'
    if 80 <= avg_gap <= 100: return 'Trimestral'
    if 170 <= avg_gap <= 190: return 'Semestral'
    if 350 <= avg_gap <= 380: return 'Anual'
    return None

def build_caracteristicas(papel, fluxo_data=None, op_name=None, fund_positions=None):
    """Curadoria de 'Características da Operação' por sinônimo (aplica-se às 49 abas,
    conteúdo de cada linha se adapta ao que a aba tiver — sem forçar '—')."""
    def fv(*subs, exclude=()):
        v = find_papel_value(papel, *subs, exclude=exclude)
        if v in (None,'','#REF!'): return None
        return v

    securitizadora = fv('securitizadora','administrador','emissor')
    af = fv('agente fiduciario')
    serie = fv('serie/emissao','series','serie', exclude=('tipo serie',))
    cetip = fv('codigo cetip','cetip')
    # 'volume emissao - total' (achado ao investigar inVista, ver comentário em find_papel_value):
    # cobre o padrão "Volume Emissão - Total (Cotas)" usado em FIIs com cota Sênior/Subordinada
    # -- tem que vir ANTES do fallback genérico 'volume emissao', que bateria primeiro com
    # "Volume Emissão - Sênior (Cotas)" (só a fatia sênior) sem essa prioridade.
    # Correção (achado ao conferir Ilog após publicar essa mudança): o synonym tinha ficado
    # como 'emissao - total' (sem o prefixo 'volume'), o que também batia com "Quantidade
    # Emissão - Total" (Ilog, valor 275.000 -- contagem de cotas emitidas, NÃO um valor em R$)
    # -- 275.000 é ridiculamente baixo perto do Saldo Devedor de R$78,7 MM da Ilog, o que
    # entregou o erro. Exigir o prefixo 'volume' (ou 'valor', já coberto por 'valor de
    # emissao' antes na lista) evita bater com "Quantidade Emissão - Total".
    # apply_papel_value_override (ver PAPEL_VALUE_OVERRIDE): mesmo ponto único usado por
    # build_summary(), pra Características e o quickstat/tabela de Operações nunca divergirem.
    # Correção (achado auditando JALGP, pedido do usuário "vamos ajustar a questão do Volume
    # de Emissão... tem vários errados"): faltava a variante com TRAVESSÃO ('volume emissao –
    # total', usada literalmente na aba JALGP: "Volume Emissão – Total") -- só tinha a com
    # hífen normal ('volume emissao - total'). Sem ela, caía direto no fallback genérico
    # 'volume emissao', que batia com a linha solta "Volume Emissão" de UMA sub-série (R$17,4
    # MM) em vez do total (R$58,5 MM = R$33,75 Sênior + R$24,75 Sub, confirmado por soma) --
    # exatamente o mesmo tipo de erro já corrigido em build_summary() antes, que já tinha essa
    # variante na lista (por isso o quickstat/Visão Geral já mostravam o valor certo enquanto
    # só Características ficava com o valor errado).
    volume_emissao = apply_papel_value_override(papel, op_name, 'valor_emissao',
        fv('valor de emissao','volume emissao total','volume emissao – total','volume emissao - total','volume emissao'))
    volume_integralizado = fv('volume integralizado','valor integralizado','montante integralizado')
    # Sinônimos alinhados com build_summary() (inclui 'pl atual - fundo'/'pl atual', que
    # faltavam aqui -- achado auditando CVPAR: sem eles, o fallback abaixo [operação sem
    # fund_positions] ficava sem "Saldo Devedor Atualizado" nenhum em Características, mesmo
    # com o valor certo já presente no summary/Visão Geral via 'PL Atual - Fundo').
    saldo_atual_total = apply_papel_value_override(papel, op_name, 'saldo_devedor',
        fv('montante atual cri','saldo devedor atualizado','saldo devedor - total','saldo devedor atual - consolidado','saldo devedor','pl atual - fundo','pl atual'))
    # saldo_atual (pedido do usuário: "a questão de saldo devedor que devemos usar é a visão
    # que está nas tabelas dos fundos, visão curva... temos a visão de saldo devedor na visão
    # geral, posição por fundo e características do ativo" -- as 3 têm que bater): mesma soma
    # que a Visão Geral/Posição por Fundo já usam (fp.saldo_curva_mm de fund_positions, em
    # milhões -- ver opSaldoDevedor() no portal_template.html), calculada aqui em Python pra
    # Características mostrar o MESMO número, não o Saldo Devedor TOTAL do CRI (que inclui
    # outros investidores quando % Mauá<100%, ex.: inVista 273MM total vs 255MM só Mauá). Cai
    # pro total acima (saldo_atual_total, já com os overrides de PAPEL_VALUE_OVERRIDE
    # aplicados) só quando a operação não tem posição de fundo listada no PPT -- mesmo
    # critério de fallback que opSaldoDevedor() usa no JS.
    if fund_positions:
        saldo_atual = sum((fp.get('saldo_curva_mm') or 0) * 1e6 for fp in fund_positions)
    else:
        saldo_atual = saldo_atual_total
    subordinacao = fv('subordinacao')
    data_emissao = fv('data de emissao')
    data_vencimento = fv('data de vencimento')
    indexador = clean_indexador(fv('indexador'))
    taxa = parse_pct_from_text(fv('taxa de juros'))
    # taxa_aquisicao (pedido do usuário: "tem que aparecer a mesma visualização em todos os
    # lugares que ela aparece... colocar tbm esses ajustes na característica do ativo e na
    # visão geral"): mesmo campo já extraído em parse_base_sheet/build_summary (ver comentário
    # lá) -- só populado pra Vista Faria Lima hoje.
    taxa_aquisicao = fv('taxa de juros (aquisicao)')
    juros_period = fv('atualizacao monetaria','periodicidade de juros','pagamento de juros')
    amortizacao_period = fv('periodicidade de amortizacao')
    if not amortizacao_period:
        amortizacao_period = infer_cadence_from_fluxo(fluxo_data)
    lockup = fv('lock up','lock-up','carencia')
    multa = fv('multa')

    remuneracao = None
    if indexador and isinstance(taxa,(int,float)):
        remuneracao = f"{indexador} + {fmt_pct_str(taxa)} a.a."
        if isinstance(taxa_aquisicao,(int,float)):
            remuneracao += f" (emissão) | {indexador} + {fmt_pct_str(taxa_aquisicao)} a.a. (aquisição)"
    elif indexador:
        remuneracao = str(indexador)

    # (pedido do usuário, ver comentário acima em saldo_atual): removida a nota "(XX% Mauá)"
    # que ficava embaixo do valor -- fazia sentido quando o número era o TOTAL do CRI (a nota
    # esclarecia a fatia da Mauá dentro dele); agora que o número JÁ é a fatia da Mauá (visão
    # curva, igual à Visão Geral/Posição por Fundo), repetir "(XX% Mauá)" do lado ficaria
    # redundante/confuso -- o mesmo raciocínio já usado no rótulo "Saldo Devedor % Mauá" da
    # tabela de Visão Geral (ver COLS no portal_template.html).
    saldo_cell = None
    if isinstance(saldo_atual,(int,float)):
        saldo_cell = fmt_brl_str(saldo_atual)

    rows = []
    def add(*cells):
        cells = [{'label':lbl,'text':str(val)} for (lbl,val) in cells if val not in (None,'')]
        if cells: rows.append(cells)

    add(('Securitizadora', securitizadora), ('AF', af))
    add(('Série', serie), ('Cód. Cetip', cetip))
    add(('Volume Emissão', fmt_brl_maybe_multi(volume_emissao)))
    add(('Volume Integralizado', fmt_brl_maybe_multi(volume_integralizado)))
    add(('Saldo Devedor Atualizado', saldo_cell))
    add(('Subordinação', fmt_pct_str(subordinacao) if isinstance(subordinacao,(int,float)) else subordinacao))
    add(('Data de Emissão', fmt_date_mesano(data_emissao) if data_emissao else None), ('Vencimento', fmt_date_mesano(data_vencimento) if data_vencimento else None))
    add(('Remuneração', remuneracao))
    # "Juros" às vezes cai no fallback de "Atualização Monetária" (quando a aba não tem uma
    # coluna própria de periodicidade de juros) e essa vem com sufixo "(M-2)" (defasagem de
    # mês de referência da correção monetária) -- correto pro campo de origem, mas confuso
    # sob o rótulo "Juros" (ex.: Residencial Jardins, "Mensal (M-2)"). Removido por ser um
    # texto que não pertence a esse campo; fix genérico (não específico da operação).
    juros_display = re.sub(r'\s*\(M-\d+\)\s*$', '', str(juros_period)).strip() if juros_period else juros_period
    add(('Juros', juros_display), ('Amortização', amortizacao_period))
    # Lock-up usava fmt_date_br (data cheia dd/mm/aaaa) enquanto Data de Emissão/Vencimento já
    # tinham sido padronizados pro formato abreviado Mês/AA (ver fmt_date_mesano acima) -- exatamente
    # a inconsistência que o usuário apontou ("características da operação... entro em outra
    # operação e não tá formatado igual"): BR Prop/WT Log/Calçada mostravam Lock-up como
    # "01/08/2025" cru enquanto Data de Emissão ao lado já saía "Ago/23". fmt_date_mesano cai de
    # volta pro texto original quando o valor não é uma data (Habibs/Localfrio guardam frase
    # descritiva tipo "Não há"/"Jul/26 (na hipótese de...)"), então nada quebra pros casos não-data.
    add(('Lock-up', fmt_date_mesano(lockup) if lockup else None))
    # "Multa" às vezes vem como fração numérica pura na planilha (ex.: 0.02), não como texto
    # já formatado/descritivo (a maioria das abas guarda uma fórmula/descrição em texto) --
    # sem formatar, aparecia cru tipo "0.02" em vez de "2,00%" (achado na Residencial Itaim,
    # 36ª rodada, mas também afeta Tellus River South/MSB Triu/MSB Axis/MSB Edson). Fix
    # genérico, mesmo padrão já usado em "Subordinação".
    add(('Multa', fmt_pct_str(multa) if isinstance(multa,(int,float)) else multa))
    return rows

def covenant_status_counts(covenants):
    counts = {'enquadrado':0,'verificar':0,'desenquadrado':0,'outro':0}
    for c in covenants:
        st = norm(c.get('status',''))
        if 'desenquadr' in st: counts['desenquadrado'] += 1
        elif 'enquadr' in st: counts['enquadrado'] += 1
        elif 'verificar' in st: counts['verificar'] += 1
        elif st: counts['outro'] += 1
    return counts

def derive_ltv_atual(fluxo_data, cutoff_date=None):
    """LTV atual = o do último registro 'realizado' do fluxo (onde o IC já foi apurado), pra bater
    com a linha correspondente na tabela de amortização mensal — em vez do campo estático do papel,
    que pode estar desatualizado em relação à data de referência.

    cutoff_date (string ISO 'AAAA-MM-DD'), quando informado, ignora linhas do fluxo com data
    posterior a ele -- ajuste pós-publicação (42ª rodada, achado na MSB Triu): a aba de fluxo
    de algumas operações vem com a série INTEIRA já desenhada até o vencimento (projeção 100%
    futura, sem nenhum "realizado" reportado ainda), e nos últimos meses dessa projeção a
    garantia declina até perto de zero (ex.: estoque totalmente vendido/entregue no cronograma
    projetado), fazendo o LTV "explodir" (chegou a 7.885,9% na Triu) -- sem cutoff, "o último
    registro com ic+ltv" pega essa cauda em vez do mês de fato mais recente. Usa o mesmo AS_OF
    do resto do portal (nunca faz sentido reportar um "LTV Atual" além do próprio mês de
    referência da carteira)."""
    best = None  # (data_iso, ltv)
    for fd in (fluxo_data or []):
        for r in fd['records']:
            if isinstance(r.get('ic'), (int, float)) and isinstance(r.get('ltv'), (int, float)) and isinstance(r.get('data'), str):
                if cutoff_date is not None and r['data'] > cutoff_date:
                    continue
                if best is None or r['data'] > best[0]:
                    best = (r['data'], r['ltv'])
    return best[1] if best else None

def derive_ic_atual(fluxo_data, cutoff_date=None):
    """Mesma lógica/linha do derive_ltv_atual() acima (último registro 'realizado' do fluxo,
    onde ic+ltv já foram apurados), só que devolvendo o 'ic' em vez do 'ltv' -- usado só pelo
    IC_ATUAL_SYNC_OPS pra sincronizar o "Atual" do covenant de IC/ICSD com o mês mais recente
    de verdade (ver nota em IC_ATUAL_SYNC_OPS).

    cutoff_date (string ISO 'AAAA-MM-DD'), quando informado, ignora linhas do fluxo com data
    posterior a ele. Achado na Residencial Itaim (36ª rodada): a aba de Fluxo já vem com uma
    linha seguinte (mês posterior) com IC e LTV preenchidos por fórmula, mas que ainda não é
    o período oficialmente fechado -- pegar literalmente "a última linha com os dois campos"
    nesse caso pulava um mês à frente do que o resto do painel (Highlights, "Atual" do LTV que
    já era confiável) reconhece como o período mais recente. cutoff_date vem da própria
    'Última Atualização' do covenant de IC/ICSD na aba base (find_covenant_ultima_atualizacao),
    que é a mesma referência que o card de Garantias usa -- então IC/LTV/Highlights ficam
    todos ancorados no mesmo período "fechado", em vez de um ficar um mês à frente dos outros."""
    best = None  # (data_iso, ic)
    for fd in (fluxo_data or []):
        for r in fd['records']:
            if isinstance(r.get('ic'), (int, float)) and isinstance(r.get('ltv'), (int, float)) and isinstance(r.get('data'), str):
                if cutoff_date is not None and r['data'] > cutoff_date:
                    continue
                if best is None or r['data'] > best[0]:
                    best = (r['data'], r['ic'])
    return best[1] if best else None

def apply_papel_value_override(papel, op_name, field, fallback):
    """Ponto único que aplica PAPEL_VALUE_OVERRIDE (ver comentário lá) -- usado tanto por
    build_summary() quanto build_caracteristicas() pros campos 'valor_emissao'/'saldo_devedor',
    pra garantir que os 2 lugares (summary/quickstat e Características) sempre concordem no
    mesmo número, em vez de cada um aplicar (ou esquecer de aplicar) a correção separadamente.
    `label` pode ser uma chave literal única (comportamento original) OU uma lista de chaves
    literais -- nesse caso soma todas (achado na Renda Residencial: não existe uma linha
    "Total" pra Volume Emissão na aba, só 'Valor Emissão (Sr)' + 'Valor de Emissão (Sub)'
    separadas -- diferente do Saldo Devedor, que já tinha 'Montante Atual - Operação' pronto)."""
    override = PAPEL_VALUE_OVERRIDE.get(op_name, {})
    label = override.get(field)
    if isinstance(label, (list, tuple)):
        vals = [papel.get(k) for k in label]
        if all(isinstance(v, (int, float)) for v in vals) and vals:
            return sum(vals)
    elif label:
        v = papel.get(label)
        if isinstance(v, (int, float)):
            return v
    return fallback

def build_summary(papel, covenants=None, fluxo_data=None, cutoff_date=None, op_name=None):
    covenants = covenants or []
    ltv_fluxo = derive_ltv_atual(fluxo_data, cutoff_date=cutoff_date)
    pct_maua = find_papel_value(papel, 'percentual maua','% maua')
    if pct_maua is None:
        v = find_papel_value(papel, '% do cri')
        pct_maua = v if isinstance(v, (int, float)) else None
    valor_emissao = apply_papel_value_override(papel, op_name, 'valor_emissao',
        find_papel_value(papel, 'valor de emissao','volume emissao total','volume emissao – total','volume emissao - total','volume emissao'))
    saldo_devedor = apply_papel_value_override(papel, op_name, 'saldo_devedor',
        find_papel_value(papel, 'montante atual cri','saldo devedor atualizado','saldo devedor - total','saldo devedor atual - consolidado','saldo devedor','pl atual - fundo','pl atual'))
    out = {
        'securitizadora': find_papel_value(papel, 'securitizadora','administrador','emissor'),
        'agente_fiduciario': find_papel_value(papel, 'agente fiduciario'),
        'serie': find_papel_value(papel, 'serie/emissao','series','serie','emissao / series'),
        'valor_emissao': valor_emissao,
        'saldo_devedor': saldo_devedor,
        'pct_maua': pct_maua,
        'data_emissao': find_papel_value(papel, 'data de emissao','data emissao'),
        'data_vencimento': find_papel_value(papel, 'data de vencimento','data vencimento'),
        'taxa_juros': parse_pct_from_text(find_papel_value(papel, 'taxa de juros')),
        # taxa_juros_aquisicao (pedido do usuário, ver comentário em parse_base_sheet sobre a
        # extração da 3ª coluna da linha "Taxa de Juros"): só populado quando a operação foi
        # comprada "fora da curva" a uma taxa diferente da taxa de emissão -- hoje só a Vista
        # Faria Lima (8,57% emissão / 9,44% aquisição, confirmado também no PDF consolidado).
        'taxa_juros_aquisicao': find_papel_value(papel, 'taxa de juros (aquisicao)'),
        'indexador': clean_indexador(find_papel_value(papel, 'indexador')),
        'concentracao': find_papel_value(papel, 'concentracao'),
        'ltv_atual': ltv_fluxo if ltv_fluxo is not None else find_papel_value(papel, 'ltv atual','ltv'),
        'duration': find_papel_value(papel, 'duration atual (anos)','duration (anos)','duration'),
    }
    out['covenant_counts'] = covenant_status_counts(covenants)
    out['n_covenants'] = len(covenants)
    return out

# ---------- Curadoria manual de campos extras/overrides em "Informações do Ativo" ----------
# Só usado quando a operação precisa de conteúdo que não sai limpo da extração automática de
# build_ativo_info() — rótulo customizado, valores combinados (R$/m² + R$/quarto) ou um campo
# novo que não é sinônimo de nada na aba-base (ex.: "Valor do Estoque Inicial", um número de
# referência FIXO na data de emissão do deal, não recalculado a cada rodada). Aplicado a
# TODOS os ativos/garantias daquela operação.
ATIVO_INFO_MANUAL = {
    'Calçada': {
        'descricao': [
            '222 Unidades Totais',
            '179 Unidades Garantia',
            'Bandeira: Square Design Hotel',
            'Operador: XR Advisor',
            'Inauguração: Jun/16',
        ],
        'valor_avaliacao_label': 'Laudo Bolsa Imobiliária RJ',
        'valor_avaliacao_valor_quarto': 613500,
        'valor_estoque_inicial': {
            'valor': 91000000,
            'valor_m2': 17170,
            'valor_quarto': 500000,
        },
    },
    'WT Log': {
        # A aba guarda ABL/Valor de Avaliação em pares "(100%)"/"(25%)" (fração ideal detida
        # pela Devedora), formato só dessa operação -- o find('abl total') genérico não bate
        # com "ABL (100%)" e o fallback (primeira coluna começando com "abl") pegava o valor
        # de 100% pro campo "ABL Adquirido", perdendo o par completo. Curado manualmente pra
        # trazer as 2 métricas (igual ao print de referência do usuário), mas nos MESMOS 2
        # campos/rótulos padrão do card ("ABL Total"/"ABL Adquirido") -- só o valor de
        # avaliação ganha uma linha extra (25%) porque o card só tem 1 linha de "Valor de
        # Avaliação" por padrão (ver valor_avaliacao_extra/apply_ativo_info_manual).
        'tipo_ativo': 'Galpão Logístico',
        'ativo': 'Condomínio WT Log RBR Franco da Rocha (Subcondomínios A e B / Galpões 100 e 200)',
        'abl_total': '122.230 m²',
        'abl_adquirido': '30.558 m² (25% - fração ideal da Devedora)',
        'descricao': [
            'Ano de entrega: 2021',
            'Classe AAA',
            'Pé direito: 12,0 m',
            'Capacidade do piso: 6 ton/m²',
        ],
        'valor_avaliacao': {'valor': 442800000, 'valor_m2': None},
        'valor_avaliacao_extra': [
            ['Valor de Avaliação (25%)', 'R$ 110.700.000 (R$ 3.622,67/m²)'],
        ],
    },
    'BR Prop': {
        # A "Informações da Garantia" bruta da aba ('Ativo', 'Descrição Garantia', etc.)
        # ainda reflete a garantia ANTIGA (Araucária/Centauri/Cupuaçu, locatários L'oreal e
        # M Cassab) -- em 2025/2026 ela foi integralmente substituída pelos galpões de
        # Cajamar (ver MANUAL_CONTENT/sobre_operacao). Curado manualmente pra refletir a
        # garantia atual, igual ao print de referência do usuário (34ª rodada).
        'tipo_ativo': 'Logístico',
        'ativo': 'Galpões Industriais Cajamar',
        'endereco': 'Rodovia Anhanguera, km 43 - Cajamar/SP',
        'abl_total': '86.950 m²',
        'descricao': [
            'Dois galpões AAA',
            'Vacância: 0%',
            'Contratos de locação com prazo superior a 10 anos e vencimento do CRI',
            'Locatários Antilhas, Girotrade, Yusen e JSL',
        ],
        'valor_avaliacao': {'valor': 231867693, 'valor_m2': 3990.9596729538916},
        'atualizacao_laudo': 'Anual – todo mês de Fevereiro',
    },
    'Residencial Itaim': {
        # A aba 'Residencial Itaim' tem um único ativo (Upper Itaim), mas o print de
        # referência do usuário (36ª rodada, ponto 5) usa um conjunto de campos totalmente
        # diferente do padrão fixo do card ("Proprietária"/"ABL Adquirido" não aparecem;
        # em vez disso há Incorporadora + ABL/Unidades separados em GARANTIA x
        # EMPREENDIMENTO + Entrega + Valor de Aquisição) -- não cabe nos campos fixos nem
        # no mecanismo de 'valor_avaliacao_extra' (que só acrescenta uma linha extra, não
        # troca o conjunto inteiro). Resolvido com 'ativo_info_fields' (mesmo espírito do
        # 'ativo_compare_fields' da Residencial Jardins/regra geral #33, só que pro card
        # empilhado padrão em vez do comparativo lado a lado) -- ver ativoInfoHtml() no
        # portal_template.html. ABL/Unidades (Garantia) batem com a aba ("Área Total"=3176,
        # "Unidades (Garantia)"=80); ABL (Empreendimento)=5.217 m² e "Lançamento do
        # projeto: Abr-14" não estão na planilha (só no laudo/print) -- curados à mão, tais
        # como o usuário passou, mesmo critério já usado noutras curadorias manuais.
        'tipo_ativo': 'Residencial',
        'ativo': 'Upper Itaim',
        'incorporadora': 'Canopus',
        'endereco': 'Rua João Cachoeira, 1.577 – Vila Nova Conceição/SP',
        'abl_garantia': '3.176 m²',
        'unidades_garantia': '80',
        'abl_empreendimento': '5.217 m²',
        'unidades_empreendimento': '122',
        'descricao': [
            'Prédio residencial na Vila Olímpia/SP',
            'Lançamento do projeto: Abr-14',
            'Entrega: Mai-16',
            '122 unidades no edifício',
            '80 unidades adquiridas na operação (garantia)',
            '40 m² por unidade adquirida',
        ],
        'entrega': 'Mai/16',
        'valor_aquisicao': 'R$ 45.400.000 (R$14.295/m²)',
        'valor_avaliacao_str': 'R$ 85.372.000 (R$26.880/m²)',
        'ativo_info_fields': [
            ['Tipo de Ativo', 'tipo_ativo'],
            ['Ativo', 'ativo'],
            ['Incorporadora', 'incorporadora'],
            ['Endereço', 'endereco'],
            ['ABL Total (Garantia)', 'abl_garantia'],
            ['Unidades (Garantia)', 'unidades_garantia'],
            ['ABL Total (Empreendimento)', 'abl_empreendimento'],
            ['Unidades (Empreendimento)', 'unidades_empreendimento'],
            ['Descrição', 'descricao'],
            ['Entrega', 'entrega'],
            ['Valor de Aquisição', 'valor_aquisicao'],
            ['Valor de Avaliação', 'valor_avaliacao_str'],
        ],
    },
    'MSB Triu': {
        # 42ª rodada, ponto 6 -- imagem de referência enviada pelo usuário. Mesmo mecanismo
        # 'ativo_info_fields' da Residencial Itaim (conjunto de campos totalmente customizado,
        # não cabe no card padrão Tipo de Ativo/Ativo/Proprietária/Endereço/ABL). O endereço
        # ("nº 1.722") diverge do valor bruto da aba ("1.772", provável erro de digitação na
        # planilha-fonte) -- segue a imagem enviada pelo usuário, mais recente.
        'tipo_ativo': 'Residencial',
        'incorporadora': 'MSB Sanchez',
        'ativo': 'TRIU 1722',
        'endereco': 'Rua Barão do Triunfo nº 1.722 – Campo Belo/SP',
        'area_terreno': '1.300 m²',
        'area_privativa': '6.970 m²',
        'unidades_area_media': '97 unidades (71 m²)',
        'tipologia': '92 unid. de 69 m², 2 unid. de 96 m², 2 unid. de 134 m² e 1 loja de 139 m²',
        'data_lancamento': 'Jun/23',
        'data_habitese': 'Abr/26',
        'ativo_info_fields': [
            ['Tipo de Ativo', 'tipo_ativo'],
            ['Incorporadora', 'incorporadora'],
            ['Ativo', 'ativo'],
            ['Endereço', 'endereco'],
            ['Área Terreno', 'area_terreno'],
            ['Área Privativa', 'area_privativa'],
            ['Nº Unidades (Área Média)', 'unidades_area_media'],
            ['Tipologia', 'tipologia'],
            ['Data Lançamento', 'data_lancamento'],
            ['Data Habite-se', 'data_habitese'],
        ],
    },
    'MSB Edson': {
        # 43ª rodada, ponto 7 -- "garantias estou enviando em anexo as informações que
        # precisão estar e para ajustar como está hoje": imagem de referência enviada pelo
        # usuário diverge da aba bruta em 3 campos (VGV Total R$207,1MM/Preço R$20,0 mil-m²
        # no anexo vs. R$211,2MM/R$20,4 mil-m² na aba; Previsão Habite-se Out/26 no anexo vs.
        # Dez/25 na aba) -- segue o anexo, mesmo racional já usado na Triu (endereço nº 1.722
        # vs. 1.772 da aba). Mesmo mecanismo 'ativo_info_fields' da Triu/Residencial Itaim.
        'tipo_ativo': 'Residencial',
        'incorporadora': 'MSB Sanchez',
        'ativo': 'Residencial vertical em desenvolvimento',
        'endereco': 'Rua Edson, nº 1.400 – Campo Belo/SP',
        'area_terreno': '2.000 m²',
        'area_privativa': '10.354 m²',
        'unidades_area_media': '44 unidades (235,3 m²)',
        'vgv_empreendimento': 'R$ 207.084.400 (R$ 20.000/m²)',
        'data_habitese': 'Out/26',
        'ativo_info_fields': [
            ['Tipo de Ativo', 'tipo_ativo'],
            ['Incorporadora', 'incorporadora'],
            ['Ativo', 'ativo'],
            ['Endereço', 'endereco'],
            ['Área Terreno', 'area_terreno'],
            ['Área Privativa', 'area_privativa'],
            ['Nº Unidades (área média)', 'unidades_area_media'],
            ['VGV Empreendimento', 'vgv_empreendimento'],
            ['Previsão Habite-se', 'data_habitese'],
        ],
    },
}

def apply_ativo_info_manual(op_name, ativo_info_list):
    manual = ATIVO_INFO_MANUAL.get(op_name)
    if not manual or not ativo_info_list:
        return
    for a in ativo_info_list:
        for simple_key in ('tipo_ativo', 'ativo', 'proprietaria', 'endereco', 'abl_total', 'abl_adquirido',
                           'incorporadora', 'abl_garantia', 'unidades_garantia', 'abl_empreendimento',
                           'unidades_empreendimento', 'entrega', 'valor_aquisicao', 'valor_avaliacao_str',
                           'area_terreno', 'area_privativa', 'unidades_area_media', 'tipologia',
                           'data_lancamento', 'data_habitese', 'vgv_empreendimento'):
            if simple_key in manual:
                a[simple_key] = manual[simple_key]
        if 'descricao' in manual:
            a['descricao'] = list(manual['descricao'])
        if 'valor_avaliacao_label' in manual:
            a['valor_avaliacao_label'] = manual['valor_avaliacao_label']
        if 'valor_avaliacao' in manual:
            a['valor_avaliacao'] = dict(manual['valor_avaliacao'])
        if 'valor_avaliacao_valor_quarto' in manual and a.get('valor_avaliacao'):
            a['valor_avaliacao']['valor_quarto'] = manual['valor_avaliacao_valor_quarto']
        if 'valor_avaliacao_extra' in manual:
            a['valor_avaliacao_extra'] = [list(x) for x in manual['valor_avaliacao_extra']]
        if 'valor_estoque_inicial' in manual:
            a['valor_estoque_inicial'] = dict(manual['valor_estoque_inicial'])
        if 'atualizacao_laudo' in manual:
            a['atualizacao_laudo'] = manual['atualizacao_laudo']
        # Conjunto de campos totalmente customizado (opt-in, hoje só Residencial Itaim) --
        # ver nota em ATIVO_INFO_MANUAL['Residencial Itaim'] e ativoInfoHtml() no template.
        if 'ativo_info_fields' in manual:
            a['ativo_info_fields'] = [list(x) for x in manual['ativo_info_fields']]

# ---------- "Acompanhamento de Estoque" (23ª/24ª rodada, card novo acima do Fluxo Mensal) ----------
# Específico da Calçada (deal virou de renda de hotel pra estoque de multipropriedade após a
# reestruturação — ver regra geral #15). Usuário mandou 2 imagens de referência (tabela
# "Acompanhamento de Estoque" — snapshot Estoque Inicial/Venda/Estoque Atual — e "Histórico de
# Vendas x Estoque" — por período) pra replicar como card novo, largura total, ACIMA do painel
# "Fluxo Mensal" (não dentro de Garantias, diferente da tentativa da 20ª rodada que foi revertida).
# Fonte: aba 'Calçada - Indicadores ' (nome com espaço no fim), que tem as 2 tabelas prontas:
#   - Tabela 1 (linhas 1-4): 1 linha por empreendimento + linha de total (bate com a linha única
#     aqui, só 1 empreendimento). Colunas: Estoque Inicial (nº/área/valor mínimo venda/valor/R$m²),
#     Venda (nº/área/valor/R$m²), Estoque Atual (nº/área/valor/R$m²/valor média vendas/R$m² média).
#   - Tabela 2 (linhas 25-35): histórico por mês, já com uma linha "2025" agregada pro ano
#     inteiro + linhas mensais de 2026. O usuário quer agrupado por TRIMESTRE em 2026 (ver imagem:
#     "1º Tri/26"/"2º Tri/26"), não por mês — agregado aqui somando os 3 meses de cada trimestre
#     (Jan-Mar, Abr-Jun); Jul/26 fica como mês isolado (3º tri ainda incompleto, só esse mês com
#     dado) e a linha de Total (linha 35 da aba) fecha a tabela.
# "Estoque Inicial" usa o valor CURADO de ATIVO_INFO_MANUAL (fixo/histórico — ver regra geral #16),
# não o bruto ao vivo da aba (que diverge: 179un/R$89,5MM ao vivo vs 182un/R$91MM curado) — mesma
# lógica já estabelecida, e "Estoque Atual" é recalculado a partir dele (Inicial − Venda), pra ficar
# consistente com o Valor do Estoque Inicial já mostrado em "Informações do Ativo".
ESTOQUE_UNIT_FLOOR = {'Calçada': 500000}  # VMD/piso por unidade (R$), usado pra recalcular Valor do Estoque Atual

def _estoque_period_row(ws, r, label):
    def cell(c): return ws.cell(row=r, column=c).value
    return {
        'periodo': label,
        'venda': {'n_unidades': cell(2) or 0, 'area': cell(3) or 0, 'valor_tabela': cell(4) or 0, 'valor_m2': cell(5) or 0},
        'definitiva': {'n_unidades': cell(6) or 0, 'valor_venda': cell(7) or 0, 'valor_recebido': cell(8) or 0,
                       'valor_a_receber': cell(9) or 0, 'amortizacao': cell(10) or 0, 'pct_calcada': cell(11) or 0},
        'provisoria': {'n_unidades': cell(12) or 0, 'valor_venda': cell(13) or 0, 'valor_recebido': cell(14) or 0,
                       'valor_a_receber': cell(15) or 0, 'amortizacao': cell(16) or 0, 'pct_calcada': cell(17) or 0},
    }

def _sum_estoque_periods(rows, label):
    out = {'periodo': label, 'venda': {}, 'definitiva': {}, 'provisoria': {}}
    for grp in ('venda', 'definitiva', 'provisoria'):
        for k in rows[0][grp]:
            out[grp][k] = sum(row[grp][k] for row in rows)
    area = out['venda']['area']
    out['venda']['valor_m2'] = (out['venda']['valor_tabela'] / area) if area else 0
    return out

def parse_estoque_calcada():
    if 'Calçada - Indicadores ' not in wb.sheetnames:
        return None
    ws = wb['Calçada - Indicadores ']
    def cell(r, c): return ws.cell(row=r, column=c).value

    manual_inicial = ATIVO_INFO_MANUAL.get('Calçada', {}).get('valor_estoque_inicial')
    floor = ESTOQUE_UNIT_FLOOR.get('Calçada')
    if manual_inicial and floor:
        inicial = {
            'n_unidades': round(manual_inicial['valor'] / floor),
            'area': round(manual_inicial['valor'] / manual_inicial['valor_m2']),
            'valor_minimo_venda': floor,
            'valor': manual_inicial['valor'],
            'valor_m2': manual_inicial['valor_m2'],
        }
    else:
        inicial = {
            'n_unidades': cell(3, 2), 'area': cell(3, 3), 'valor_minimo_venda': cell(3, 4),
            'valor': cell(3, 5), 'valor_m2': cell(3, 6),
        }
        floor = inicial['valor_minimo_venda']

    venda_snap = {'n_unidades': cell(3, 7), 'area': cell(3, 8), 'valor': cell(3, 9), 'valor_m2': cell(3, 10)}
    n_atual = inicial['n_unidades'] - venda_snap['n_unidades']
    area_atual = inicial['area'] - venda_snap['area']
    valor_atual = n_atual * floor
    atual = {
        'n_unidades': n_atual, 'area': area_atual, 'valor': valor_atual,
        'valor_m2': (valor_atual / area_atual) if area_atual else None,
        'valor_media_vendas': cell(3, 15), 'valor_media_vendas_m2': cell(3, 16),
    }

    snapshot = {'empreendimento': cell(3, 1), 'inicial': inicial, 'venda': venda_snap, 'atual': atual}

    row_2025 = _estoque_period_row(ws, 27, '2025')
    rows_q1 = [_estoque_period_row(ws, r, None) for r in (28, 29, 30)]
    rows_q2 = [_estoque_period_row(ws, r, None) for r in (31, 32, 33)]
    row_jul = _estoque_period_row(ws, 34, 'Jul/26')
    row_total = _estoque_period_row(ws, 35, 'Total')

    historico = [row_2025, _sum_estoque_periods(rows_q1, '1º Tri/26'), _sum_estoque_periods(rows_q2, '2º Tri/26'), row_jul, row_total]

    return {'snapshot': snapshot, 'historico': historico}

ESTOQUE_HIST_BY_OP = {'Calçada': parse_estoque_calcada()}

# ---------- "Mais informações operacionais do hotel" (28ª rodada, sub-página dedicada) ----------
# Específico da Calçada. A operação começou como deal de RENDA do hotel e migrou pra ESTOQUE de
# unidades após a reestruturação (ver regra geral #15/#16/#18/#21) — a view principal (Garantias/
# Fluxo Mensal) hoje é toda orientada a Estoque. O usuário pediu de volta as infos operacionais do
# hotel (removidas da view principal na 21ª rodada, ver regra geral #15 — "Performance do Hotel"),
# mas dessa vez como uma SUB-PÁGINA própria (não misturada com Garantias), acessada por um link
# em "Informações do Ativo".
# Fonte: aba 'Calçada' (a mesma aba-base do papel), numa área lateral própria à direita:
#   - "Histórico - Ocupação x Diária Média" (linha 3 = datas, uma coluna por mês, cresce pra
#     direita a cada rodada; linha 4 = Tx. Ocupação; linha 5 = Diária Média; linha 6 = RevPar —
#     RevPar já vem calculado na própria planilha, diferente da versão revertida da 20ª rodada
#     que calculava Tx.Ocupação × Diária Média no código). Pego dinamicamente TODOS os meses com
#     as 3 métricas preenchidas e uso só os últimos 6 (mesmo critério "últimos 6 meses com dado
#     real, dinâmico" já usado na tentativa da 20ª rodada).
#   - "Mini DRE" (localizado dinamicamente pelo texto "Mini DRE" na coluna 85 — a partir daí, a
#     linha de cabeçalho 2 linhas abaixo tem 1 coluna por mês + uma coluna com o texto literal
#     "Avg LTM"; ambas colunas mudam de posição a cada atualização mensal (a tabela cresce pra
#     direita), por isso procuro a data mais recente e o rótulo "Avg LTM" na linha de cabeçalho
#     em vez de fixar número de coluna — só os NÚMEROS DE LINHA das 9 linhas de item (logo abaixo
#     do cabeçalho) ficam fixos, já que aqui é a estrutura de linhas que não muda mês a mês).
MINI_DRE_ITEMS = [
    ('receitas', '(+) Receitas'), ('desp_operacional', '(-) Desp. Operacional'),
    ('gop', '(=) Lucro Operacional (GOP)'), ('desp_nao_operacional', '(-) Desp. Não Operacional + Imposto'),
    ('lucro_liquido', '(=) Lucro Líquido'), ('n_apartamentos', 'Nº Apartamentos'),
    ('resultado_apto', '(=) Resultado/Apto'), ('n_apto_garantia', 'Nº Apto Garantia'),
    ('resultado_garantia', '(=) Resultado Garantia'),
]

def parse_hotel_perf_calcada():
    if 'Calçada' not in wb.sheetnames:
        return None
    ws = wb['Calçada']

    chart_months = []
    c = 85
    empty_streak = 0
    while empty_streak < 6 and c < 400:
        d = ws.cell(row=3, column=c).value
        occ = ws.cell(row=4, column=c).value
        adr = ws.cell(row=5, column=c).value
        revpar = ws.cell(row=6, column=c).value
        if isinstance(d, datetime) and all(isinstance(v, (int, float)) for v in (occ, adr, revpar)):
            chart_months.append({'data': d.strftime('%Y-%m-%d'), 'ocupacao': occ, 'diaria_media': adr, 'revpar': revpar})
            empty_streak = 0
        else:
            empty_streak += 1
        c += 1
    chart_months.sort(key=lambda m: m['data'])
    chart = chart_months[-6:] if chart_months else []

    mini_dre = None
    title_row = None
    for r in range(1, min(ws.max_row, 200) + 1):
        if str(ws.cell(row=r, column=85).value or '').strip() == 'Mini DRE':
            title_row = r
            break
    if title_row:
        header_row = title_row + 2
        label_col = 85
        cur_col, ltm_col, cur_date = None, None, None
        for cc in range(label_col + 1, label_col + 12):
            v = ws.cell(row=header_row, column=cc).value
            if isinstance(v, datetime) and (cur_date is None or v > cur_date):
                cur_date, cur_col = v, cc
            elif isinstance(v, str) and 'avg ltm' in v.strip().lower():
                ltm_col = cc
        if cur_col and ltm_col:
            linhas = []
            for i, (key, label) in enumerate(MINI_DRE_ITEMS):
                r = header_row + 1 + i
                linhas.append({
                    'key': key, 'label': label,
                    'atual': ws.cell(row=r, column=cur_col).value,
                    'avg_ltm': ws.cell(row=r, column=ltm_col).value,
                })
            mini_dre = {'mes_atual': cur_date.strftime('%Y-%m-%d'), 'linhas': linhas}

    if not chart and not mini_dre:
        return None
    return {'chart': chart, 'mini_dre': mini_dre}

HOTEL_PERF_BY_OP = {'Calçada': parse_hotel_perf_calcada()}

# ---------- "Informações do Ativo" em formato comparativo lado a lado (31ª rodada) ----------
# Específico da Localfrio: 2 ativos (Armazéns Anhanguera/Itajaí), usuário pediu visão lado a
# lado (ver referência enviada) em vez do formato empilhado padrão de ativoInfoHtml() — usado
# pelas outras 6 operações multi-ativo (Superfrio, FII York, JALGP, Ilog, Apil, Vitacon), que
# NÃO devem ser afetadas por essa mudança (por isso o opt-in explícito via este dict, em vez
# de generalizar "se >1 ativo, usa comparativo" pra todas).
# Layout específico da aba 'Localfrio':
#   - 'Descrição' fica na linha ANTERIOR ao próprio rótulo 'Descrição' (não populada pelo
#     parser genérico de kv, que só junta bullets que começam com '-' antes do rótulo).
#   - 'Valor de mercado' (Laudo Apsis, "material de apoio") vem numa coluna-callout à parte
#     (coluna D), 2/3 linhas abaixo do rótulo 'Locatário' — não é um par rótulo/valor comum
#     de coluna A/B, por isso não aparece no dict `asset` que alimenta build_ativo_info().
# O usuário também pediu (mesma rodada) pra tirar o Laudo (Valor de Avaliação/Atualização)
# dessa visão — como aqui é uma tabela nova e dedicada, simplesmente não incluímos esses campos.
def parse_ativo_compare_localfrio():
    if 'Localfrio' not in wb.sheetnames:
        return None
    ws = wb['Localfrio']
    anchors = []
    for r in range(1, ws.max_row + 1):
        v = ws.cell(row=r, column=1).value
        if isinstance(v, str) and norm(v).startswith('tipo de ativo'):
            anchors.append(r)
    if len(anchors) < 2:
        return None

    out = []
    for i, r0 in enumerate(anchors[:2]):
        r_end = anchors[i+1] if i+1 < len(anchors) else ws.max_row + 1
        tipo_ativo = ws.cell(row=r0, column=2).value
        ativo = proprietaria = endereco = abl_total = descricao = locatario = None
        valor_mercado = valor_mercado_m2 = None
        for r in range(r0, r_end):
            label = ws.cell(row=r, column=1).value
            if not isinstance(label, str): continue
            nl = norm(label)
            if nl == 'ativo' and ativo is None:
                ativo = ws.cell(row=r, column=2).value
            elif nl.startswith('propriet'):
                proprietaria = ws.cell(row=r, column=2).value
            elif nl.startswith('endereco'):
                endereco = ws.cell(row=r, column=2).value
            elif nl == 'abl total':
                abl_total = ws.cell(row=r, column=2).value
            elif nl.startswith('descricao'):
                descricao = ws.cell(row=r-2, column=2).value
            elif nl.startswith('locatario'):
                locatario = ws.cell(row=r, column=2).value
                valor_mercado = ws.cell(row=r+2, column=4).value
                valor_mercado_m2 = ws.cell(row=r+3, column=4).value

        uf_m = re.search(r'([A-Z]{2})\s*$', str(endereco)) if endereco else None
        short_name = str(ativo).replace('Armazém ', '').strip() if ativo else None
        label_curto = f"{short_name} ({uf_m.group(1)})" if (short_name and uf_m) else (short_name or ativo)

        item = {
            'label': label_curto,
            'tipo_ativo': tipo_ativo, 'ativo': ativo, 'proprietaria': proprietaria,
            'endereco': endereco, 'abl_total': format_area_m2(abl_total) if abl_total else None,
            'descricao': descricao, 'locatario': locatario,
            'valor_mercado': valor_mercado, 'valor_mercado_m2': valor_mercado_m2,
        }
        if endereco:
            link = endereco_maps_link('Localfrio', endereco)
            if link: item['endereco_maps_url'] = link
        out.append(item)
    return out

# Residencial Jardins (35ª rodada) -- ponto 4: comparativo lado a lado dos 5 ativos do
# portfólio, igual ao print fornecido pelo usuário (Incorporador / Unidades Aquisição /
# Residenciais x Não Residenciais / Aquisição R$/m² / Avaliação R$/m², sem a linha
# "Estimativa CAPEX" que aparecia no print). Os valores de R$/m² do print não reconciliam
# de forma exata com nenhuma combinação simples encontrada nas abas 'Residencial Jardins'/
# 'Suporte Jardins' (aquisição/ABL bate certinho pro Terraço mas diverge ~0,03%-2,9% pros
# demais ativos, provavelmente por causa de uma área ligeiramente diferente usada só nesse
# quadro do relatório) -- usamos os números tais como o usuário passou no print, igual já
# se fez pra outros quadros "print" nesse portal (ver ATIVO_INFO_MANUAL/COVENANTS_MANUAL).
ATIVO_COMPARE_JARDINS = [
    {'label': 'Terraço Oscar Freire', 'incorporador': 'Sequoia', 'unidades': 28,
     'residenciais': 0, 'nao_residenciais': 28, 'aquisicao_m2': 13360, 'avaliacao_m2': 18517},
    {'label': 'Onze22', 'incorporador': 'Idea Zarvos', 'unidades': 71,
     'residenciais': 71, 'nao_residenciais': 0, 'aquisicao_m2': 12918, 'avaliacao_m2': 22551},
    {'label': 'Next Paulista', 'incorporador': 'Next Realty', 'unidades': 32,
     'residenciais': 29, 'nao_residenciais': 3, 'aquisicao_m2': 16888, 'avaliacao_m2': 22777},
    {'label': 'Next Franca', 'incorporador': 'Next Realty', 'unidades': 15,
     'residenciais': 15, 'nao_residenciais': 0, 'aquisicao_m2': 20593, 'avaliacao_m2': 18512},
    {'label': 'Next Haddock', 'incorporador': 'Next Realty', 'unidades': 22,
     'residenciais': 13, 'nao_residenciais': 9, 'aquisicao_m2': 23093, 'avaliacao_m2': 21158},
]
for _a in ATIVO_COMPARE_JARDINS:
    _a['unidades_fmt'] = str(_a['unidades'])
    _a['res_nao_res_fmt'] = f"{_a['residenciais']} / {_a['nao_residenciais']}"
    _a['aquisicao_m2_fmt'] = fmt_brl_str(_a['aquisicao_m2'])
    _a['avaliacao_m2_fmt'] = fmt_brl_str(_a['avaliacao_m2'])

# spec de campos custom (opt-in) consumido por ativoCompareHtml() no template -- ver
# regra geral #33; quando ausente, o template usa o conjunto fixo de campos da Localfrio.
ATIVO_COMPARE_FIELDS_BY_OP = {
    'Residencial Jardins': [
        ['Incorporador', 'incorporador'],
        ['Unidades Aquisição', 'unidades_fmt'],
        ['Residenciais / Não Residenciais', 'res_nao_res_fmt'],
        ['Aquisição (R$/m²)', 'aquisicao_m2_fmt'],
        ['Valor de Avaliação (R$/m²)', 'avaliacao_m2_fmt'],
    ],
}

# MSB Axis (37ª rodada) -- ponto 3: comparativo AXIS x SYNC, seguindo o racional do print
# enviado pelo usuário. Fonte: aba 'MSB Axis' linhas 36-46 (Endereço/Área Terreno/Nº
# Unidades por torre/Previsão Habite-se -- valores ao vivo, ex. Previsão Habite-se =
# Jul/27, diferente do "Ago/27" do print, que está desatualizado -- seguimos a planilha
# viva, mesmo precedente já usado em outras rodadas). Incorporadora/Data de Lançamento
# não estão na planilha -- curados do print (Incorporadora: MSB Sanchez; Data de
# Lançamento: Mar/24, derivado de "Meses desde Lançamento"=29 na aba Indicadores com Data
# Base 01/08/2026). Endereço da torre Sync também curado do print (planilha só tem o
# endereço do terreno/torre Axis).
# Ajuste pós-publicação: o print original (ponto 3) tem um quadro de linhas mais específico
# do que o que tínhamos posto no ar -- "Tipo de Ativo" é ÚNICO pro complexo todo
# ("Residencial", igual nas 2 colunas -- Sync também é residencial, só que studios, essa
# distinção fica na linha "Tipologia"), e faltavam as linhas "Área Privativa" e "Nº Unidades
# (Área Média)" que o print trazia. Área Privativa = soma das áreas das unidades de cada
# torre (aba 'MSB Axis', linhas 41/42: Axis = 40×131,16 + 20×136,02 + 1×115,94 = 8.082,74m²;
# Sync = 123×30,84 + 1×44,91 = 3.838,23m²) -- não confundir com Área Terreno (2.303m²,
# terreno único do empreendimento). Nº Unidades conta a loja térrea de cada torre (Axis
# 60+1=61, Sync 123+1=124), igual ao print.
ATIVO_COMPARE_MSB_AXIS = [
    {'label': 'AXIS', 'incorporadora': 'MSB Sanchez', 'ativo': 'Residencial',
     'endereco': 'Rua Doutor Jesuíno Maciel, nº 1.774 – Campo Belo/SP',
     'area_terreno': 2303, 'area_privativa': 40*131.16 + 20*136.02 + 1*115.94,
     'n_unidades': 61, 'area_media': 133,
     'tipologia': '40 unid. de 131 m², 20 unid. de 136 m² e 1 loja de 116 m²',
     'data_lancamento': 'Mar/24', 'previsao_habite_se': 'Jul/27'},
    {'label': 'SYNC', 'incorporadora': 'MSB Sanchez', 'ativo': 'Residencial',
     'endereco': 'Rua Pascal, nº 1.819 – Campo Belo/SP',
     'area_terreno': 2303, 'area_privativa': 123*30.84 + 1*44.91,
     'n_unidades': 124, 'area_media': 31,
     'tipologia': '123 studios de 30-31 m² e 1 loja de 45 m²',
     'data_lancamento': 'Mar/24', 'previsao_habite_se': 'Jul/27'},
]
for _a in ATIVO_COMPARE_MSB_AXIS:
    _a['area_terreno_fmt'] = format_area_m2(_a['area_terreno'])
    _a['area_privativa_fmt'] = format_area_m2(round(_a['area_privativa']))
    _a['n_unidades_fmt'] = f"{_a['n_unidades']} unidades ({_a['area_media']} m²)"
    _link = endereco_maps_link('MSB Axis', _a['endereco'])
    if _link:
        _a['endereco_html'] = f"<a href=\"{_link}\" target=\"_blank\" rel=\"noopener noreferrer\">{_a['endereco']} ↗</a>"
    else:
        _a['endereco_html'] = _a['endereco']

ATIVO_COMPARE_FIELDS_BY_OP['MSB Axis'] = [
    ['Tipo de Ativo', 'ativo'],
    ['Incorporadora', 'incorporadora'],
    ['Endereço', 'endereco_html'],
    ['Área Terreno', 'area_terreno_fmt'],
    ['Área Privativa', 'area_privativa_fmt'],
    ['Nº Unidades (Área Média)', 'n_unidades_fmt'],
    ['Tipologia', 'tipologia'],
    ['Data de Lançamento', 'data_lancamento'],
    ['Previsão Habite-se', 'previsao_habite_se'],
]

ATIVO_COMPARE_BY_OP = {'Localfrio': parse_ativo_compare_localfrio(), 'Residencial Jardins': ATIVO_COMPARE_JARDINS,
                        'MSB Axis': ATIVO_COMPARE_MSB_AXIS}

# ---------- "Informações de Locação dos Ativos" (35ª rodada, Residencial Jardins) ----------
# Ponto 5: a operação nasceu como deal de RENDA (recebíveis de locação dos 5 imóveis) e foi
# repactuada pra virar deal de ESTOQUE (venda das unidades) -- mesma migração já vista na
# Calçada (hotel -> estoque, ver regra geral #23/#24, sub-página "Mais informações
# operacionais do hotel"). Aqui replicamos o mesmo padrão (sub-página própria acessada por
# link em Garantias) só que com a tabela de performance de locação (Long-Stay/Short-Stay)
# no lugar do gráfico de ocupação do hotel. Fonte: aba 'Residencial Jardins', quadro
# 'Empreendimento/Valor Bruto LS/Vacância LS/Valor Bruto SS/Vacância LS+SS/Preço/m²',
# colunas AE:AJ, linhas 4-9 (5 ativos + linha "Total").
def parse_locacao_perf_jardins():
    if 'Residencial Jardins' not in wb.sheetnames:
        return None
    ws = wb['Residencial Jardins']
    rows = []
    total = None
    for r in range(4, 10):
        nome = ws.cell(row=r, column=31).value  # AE
        if not nome:
            continue
        item = {
            'empreendimento': nome,
            'valor_bruto_ls': to_jsonable(ws.cell(row=r, column=32).value),
            'vacancia_ls': to_jsonable(ws.cell(row=r, column=33).value),
            'valor_bruto_ss': to_jsonable(ws.cell(row=r, column=34).value),
            'vacancia_total': to_jsonable(ws.cell(row=r, column=35).value),
            'preco_m2': to_jsonable(ws.cell(row=r, column=36).value),
        }
        if norm(nome) == 'total':
            total = item
        else:
            rows.append(item)
    if not rows:
        return None
    return {'title': 'Informações de Locação dos Ativos', 'rows': rows, 'total': total}

LOCACAO_PERF_BY_OP = {'Residencial Jardins': parse_locacao_perf_jardins()}

# ---------- "Acompanhamento do Estoque" por ativo (35ª rodada, Residencial Jardins) ----------
# Ponto 6: mesmo card/posição já usados pra "Acompanhamento de Estoque" da Calçada (ver
# ESTOQUE_HIST_BY_OP/estoqueHistPanelHtml -- largura total, acima do Fluxo Mensal), mas com
# um formato de tabela diferente (por ativo, não por período), seguindo à risca as 2
# tabelas do print fornecido pelo usuário: "Aquisição x Atual (Estoque + Venda Não
# Quitada)" e "Acompanhamento Vendas x Carteira x Amortização". Os R$/m² do print usam uma
# área de aquisição por ativo que não reconcilia de forma exata com a planilha bruta (ver
# nota em ATIVO_COMPARE_JARDINS acima) -- números tais como o usuário passou no print.
ESTOQUE_POR_ATIVO_JARDINS = {
    'aquisicao_atual': {
        'rows': [
            {'label': 'Terraço Oscar Freire',
             'aq_un': 28, 'aq_area': 1138, 'aq_valor': 15200000, 'aq_m2': 13360, 'aq_aval': 21066656, 'aq_aval_m2': 18517,
             'at_un': 28, 'at_area': 1138, 'at_valor': 28167643, 'at_m2': 24758, 'at_med': 28167643, 'at_med_m2': 24758},
            {'label': 'Next Paulista',
             'aq_un': 32, 'aq_area': 922, 'aq_valor': 15570782, 'aq_m2': 16888, 'aq_aval': 21000394, 'aq_aval_m2': 22777,
             'at_un': 26, 'at_area': 808, 'at_valor': 21356507, 'at_m2': 26427, 'at_med': 20079337, 'at_med_m2': 24847},
            {'label': 'Next Franca',
             'aq_un': 15, 'aq_area': 466, 'aq_valor': 9596148, 'aq_m2': 20593, 'aq_aval': 8626592, 'aq_aval_m2': 18512,
             'at_un': 14, 'at_area': 441, 'at_valor': 10960271, 'at_m2': 24872, 'at_med': 10960271, 'at_med_m2': 24872},
            {'label': 'Next Haddock',
             'aq_un': 22, 'aq_area': 585, 'aq_valor': 13509439, 'aq_m2': 23093, 'aq_aval': 12377430, 'aq_aval_m2': 21158,
             'at_un': 22, 'at_area': 585, 'at_valor': 15131158, 'at_m2': 25865, 'at_med': 15131158, 'at_med_m2': 25865},
            {'label': 'Onze22',
             'aq_un': 71, 'aq_area': 1974, 'aq_valor': 25500000, 'aq_m2': 12918, 'aq_aval': 44515674, 'aq_aval_m2': 22551,
             'at_un': 69, 'at_area': 1917, 'at_valor': 40167914, 'at_m2': 20958, 'at_med': 40167914, 'at_med_m2': 20958},
        ],
        'total': {'label': 'Total',
             'aq_un': 168, 'aq_area': 5085, 'aq_valor': 79376369, 'aq_m2': 15611, 'aq_aval': 107586746, 'aq_aval_m2': 21159,
             'at_un': 159, 'at_area': 4888, 'at_valor': 115783494, 'at_m2': 23687, 'at_med': 114506324, 'at_med_m2': 23425},
    },
    'vendas': {
        'rows': [
            {'label': 'Terraço Oscar Freire',
             'vt_un': 0, 'vt_area': 0, 'vt_valor': 0, 'vt_m2': 0,
             've_un': 0, 've_pre': 0, 've_pos': 0, 'amex_pre': 0, 'amex_pos': 0,
             'vnq_un': 0, 'vnq_valor': 0},
            {'label': 'Next Paulista',
             'vt_un': 6, 'vt_area': 114, 'vt_valor': 2829290, 'vt_m2': 24847,
             've_un': 6, 've_pre': 1888890, 've_pos': 940400, 'amex_pre': 1637175, 'amex_pos': 0,
             'vnq_un': 0, 'vnq_valor': 0},
            {'label': 'Next Franca',
             'vt_un': 1, 'vt_area': 25, 'vt_valor': 600000, 'vt_m2': 23687,
             've_un': 1, 've_pre': 0, 've_pos': 600000, 'amex_pre': 0, 'amex_pos': 17757,
             'vnq_un': 0, 'vnq_valor': 0},
            {'label': 'Next Haddock',
             'vt_un': 0, 'vt_area': 0, 'vt_valor': 0, 'vt_m2': 0,
             've_un': 0, 've_pre': 0, 've_pos': 0, 'amex_pre': 0, 'amex_pos': 0,
             'vnq_un': 0, 'vnq_valor': 0},
            {'label': 'Onze22',
             'vt_un': 2, 'vt_area': 57, 'vt_valor': 794000, 'vt_m2': 13840,
             've_un': 2, 've_pre': 0, 've_pos': 794000, 'amex_pre': 0, 'amex_pos': 11749,
             'vnq_un': 0, 'vnq_valor': 0},
        ],
        'total': {'label': 'Total',
             'vt_un': 9, 'vt_area': 197, 'vt_valor': 4223290, 'vt_m2': 21485,
             've_un': 9, 've_pre': 1888890, 've_pos': 2334400, 'amex_pre': 1637175, 'amex_pos': 29506,
             'vnq_un': 0, 'vnq_valor': 0},
    },
}

ESTOQUE_POR_ATIVO_BY_OP = {'Residencial Jardins': ESTOQUE_POR_ATIVO_JARDINS}

# ---------- "Acompanhamento das Locações" por galpão (31ª rodada) ----------
# Mesma ideia/posição do painel já existente pra Evolution (locatariosPanelHtml, ver
# LOCATARIOS_CURATION acima), mas com colunas próprias (Galpão em vez de Locatário) — pedido
# do usuário: "colocar a planilha de acompanhamento das locações da mesma forma que na
# operação Evolution". Fonte: tabela lateral "Recebimentos - Locações" da aba 'Localfrio'
# (colunas O-R / 15-18), estruturada em blocos repetidos de 4 linhas (cabeçalho + Itajaí +
# Anhanguera + Total), um bloco por ano de reajuste, do mais recente pro mais antigo — usamos
# só o bloco mais recente (o primeiro encontrado). "Valor Contratado" e "Valor Pago" saem do
# mesmo número: o checkpoint da própria aba ("Todos os alugueis da CF entraram em Conta?")
# confirma que os dois batem 100% pra essa operação.
def parse_locacoes_localfrio():
    if 'Localfrio' not in wb.sheetnames:
        return None
    ws = wb['Localfrio']
    header_row = None
    for r in range(1, min(ws.max_row, 60) + 1):
        v = ws.cell(row=r, column=15).value
        if isinstance(v, str) and norm(v) == 'locatario':
            header_row = r
            break
    if header_row is None:
        return None

    reajuste_label = None
    marker = ws.cell(row=header_row - 1, column=18).value
    if isinstance(marker, str):
        m = re.search(r'(\d{2})\s*$', marker.strip())
        if m:
            reajuste_label = f"Jan/{int(m.group(1)) + 1:02d}"

    rows = []
    total_row = None
    r = header_row + 1
    while True:
        nome = ws.cell(row=r, column=15).value
        valor = ws.cell(row=r, column=16).value
        abl = ws.cell(row=r, column=17).value
        preco_m2 = ws.cell(row=r, column=18).value
        if nome is None: break
        if norm(str(nome)).startswith('total'):
            total_row = {'area': abl, 'valor_contratado': valor, 'valor_pago': valor, 'valor_m2': preco_m2}
            break
        galpao = re.sub(r'^im[oó]vel\s*', '', str(nome), flags=re.IGNORECASE).strip()
        rows.append({
            'galpao': galpao, 'area': abl, 'pct_ocupacao': 1.0,
            'valor_contratado': valor, 'valor_pago': valor, 'valor_m2': preco_m2,
            'reajuste': reajuste_label,
        })
        r += 1

    if not rows:
        return None
    return {'rows': rows, 'total': total_row}

MESES_ABREV_PT = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
def fmt_mes_ano_abrev(d):
    return f"{MESES_ABREV_PT[d.month-1]}/{d.year%100:02d}" if isinstance(d, datetime) else None

# WT Log tem uma tabela de "Acompanhamento" própria na mesma aba 'WT Log' (colunas O:W,
# a partir da linha do cabeçalho "Locatário") -- 1 linha por locatário (Mercado Livre,
# Caoa) + linha "Total", nos moldes da mesma tabela pedida pelo usuário nas outras
# operações (33ª rodada). Mesmo formato de saída de parse_locacoes_localfrio() (reaproveita
# locacoesGalpaoTableHtml no template), mas com "Locatário" como rótulo da 1ª coluna em vez
# de "Galpão" (aqui cada linha É um locatário, não um galpão) -- ver row_label.
def parse_locacoes_wtlog():
    if 'WT Log' not in wb.sheetnames:
        return None
    ws = wb['WT Log']
    header_row = None
    for r in range(1, min(ws.max_row, 20) + 1):
        v = ws.cell(row=r, column=16).value  # coluna P
        if isinstance(v, str) and norm(v) == 'locatario':
            header_row = r
            break
    if header_row is None:
        return None

    rows = []
    total_row = None
    r = header_row + 1
    while True:
        imovel = ws.cell(row=r, column=15).value       # O
        locatario = ws.cell(row=r, column=16).value     # P
        abl25 = ws.cell(row=r, column=18).value          # R: ABL (m²) 25%
        contratado = ws.cell(row=r, column=19).value     # S: Valor Contratado
        recebido = ws.cell(row=r, column=20).value       # T: Valor Recebido
        valor_m2 = ws.cell(row=r, column=21).value        # U: R$/m²
        reajuste_dt = ws.cell(row=r, column=22).value      # V: Reajuste
        if imovel is None and locatario is None:
            break
        if isinstance(imovel, str) and norm(imovel) == 'total':
            total_row = {'area': abl25, 'valor_contratado': contratado, 'valor_pago': recebido, 'valor_m2': valor_m2}
            break
        if locatario is None:
            break
        rows.append({
            'galpao': str(locatario).strip(),
            'area': abl25,
            'pct_ocupacao': None,
            'valor_contratado': contratado,
            'valor_pago': recebido,
            'valor_m2': valor_m2,
            'reajuste': fmt_mes_ano_abrev(reajuste_dt),
        })
        r += 1

    if not rows:
        return None
    total_area = (total_row or {}).get('area') or sum(x['area'] for x in rows if x['area'])
    for x in rows:
        if x['area'] and total_area:
            x['pct_ocupacao'] = x['area'] / total_area
    return {'rows': rows, 'total': total_row, 'row_label': 'Locatário'}

# BR Prop: pedido do usuário (34ª rodada, ponto 6) pra trazer a tabela de acompanhamento
# das locações dos galpões de Cajamar (garantia atual pós-substituição 2025/2026), no
# mesmo padrão das outras operações. A aba 'BR Prop' tem DUAS versões dessa tabela:
# - "Visão pós da AGE - 06/11/2025" (colunas O:X, linhas 17-20): 1 linha por
#   galpão/locatário com os valores/datas de reajuste mais atuais -- usada aqui como
#   fonte dos dados de cada linha.
# - "Detalhamento dos ativos" (colunas AD:AK, linhas 4-10): mesmos 4 galpões, mas já
#   vem com os rótulos e o agrupamento em subtotais prontos ("Subtotal - CF + AF" p/
#   Antilhas+Girotrade+Yusen, "Subtotal - CF" p/ JSL, "Total CF" geral) -- usada aqui só
#   como referência da estrutura/rótulos (os valores individuais dela são uma foto mais
#   antiga; os totais batem com a soma das linhas atuais).
# Como cada linha tem Galpão E Locatário como colunas distintas (ao contrário de
# Localfrio/WT Log, que só têm 1 rótulo por linha), usa row_label2 (ver regra geral #31 /
# locacoesGalpaoTableHtml no template).
def parse_locacoes_brprop():
    if 'BR Prop' not in wb.sheetnames:
        return None
    ws = wb['BR Prop']
    # (galpão bruto na aba -> rótulo curto, igual à tabela "Detalhamento dos ativos")
    GALPAO_LABEL = {
        'cajamar g200 - a / b': 'G200 – A/B',
        'cajamar g200 - c / d': 'G200 – C/D',
        'cajamar g100 - f': 'G100 – F',
        'cajamar g100 - a / b': 'G100 – A/B',
    }
    # a coluna O tem 3 tabelas empilhadas ("Visão antes da AGE", uma "Visão pós AGE"
    # intermediária/incompleta de 04/07/2025 com só 2 linhas, e a "Visão pós da AGE" de
    # 06/11/2025 com as 4 linhas finais) -- pega a ÚLTIMA ocorrência do cabeçalho
    # "Galpão"/"Locatário" (a mais recente), não a primeira.
    header_row = None
    for r in range(1, min(ws.max_row, 30) + 1):
        v = ws.cell(row=r, column=15).value  # coluna O
        if isinstance(v, str) and norm(v) == 'galpao' and 'age' in norm(ws.cell(row=r-1, column=15).value or ''):
            header_row = r
    if header_row is None:
        return None

    rows = []
    r = header_row + 1
    while True:
        galpao_raw = ws.cell(row=r, column=15).value      # O
        locatario = ws.cell(row=r, column=16).value        # P
        area = ws.cell(row=r, column=17).value              # Q: ABL m²
        contratado = ws.cell(row=r, column=18).value        # R: Aluguel Contratado
        recebido = ws.cell(row=r, column=19).value          # S: Aluguel Recebido
        valor_m2 = ws.cell(row=r, column=20).value            # T: Aluguel/m²
        reajuste_dt = ws.cell(row=r, column=22).value          # V: Próximo Reajuste
        if galpao_raw is None or locatario is None:
            break
        rows.append({
            'galpao': GALPAO_LABEL.get(norm(galpao_raw), str(galpao_raw).strip()),
            'locatario': str(locatario).strip(),
            'area': area,
            'pct_ocupacao': None,
            'valor_contratado': contratado,
            'valor_pago': recebido,
            'valor_m2': valor_m2,
            'reajuste': fmt_mes_ano_abrev(reajuste_dt),
        })
        r += 1

    if len(rows) < 4:
        return None

    def agg(items, label):
        area = sum(x['area'] for x in items)
        contratado = sum(x['valor_contratado'] for x in items)
        pago = sum(x['valor_pago'] for x in items)
        return {'_subtotal': True, 'label': label, 'area': area,
                'valor_contratado': contratado, 'valor_pago': pago,
                'valor_m2': (pago / area) if area else None}

    # agrupamento igual ao da tabela "Detalhamento dos ativos": os 3 primeiros galpões
    # (Antilhas/Girotrade/Yusen) formam o subtotal "CF + AF"; o 4º (JSL) é o subtotal "CF"
    # isolado; o total geral fecha como "Total CF".
    group_cf_af, jsl = rows[:3], rows[3:4]
    subtotal_cf_af = agg(group_cf_af, 'Subtotal - CF + AF')
    subtotal_cf = agg(jsl, 'Subtotal - CF')
    total_row = agg(rows, 'Total CF')
    total_area = total_row['area']
    for x in rows + [subtotal_cf_af, subtotal_cf]:
        if x.get('area') and total_area:
            x['pct_ocupacao'] = x['area'] / total_area

    out_rows = group_cf_af + [subtotal_cf_af] + jsl + [subtotal_cf]
    return {'rows': out_rows, 'total': total_row, 'row_label': 'Galpão', 'row_label2': 'Locatário'}

LOCACOES_GALPAO_BY_OP = {'Localfrio': parse_locacoes_localfrio(), 'WT Log': parse_locacoes_wtlog(),
                          'BR Prop': parse_locacoes_brprop()}

# "Acompanhamento das Locações" POR MODALIDADE (Residencial Itaim, 36ª rodada, ponto 6) --
# formato bem mais simples que locacoesGalpaoTableHtml (Galpão/Área/Valor Contratado/Valor
# Pago/Reajuste): só 4 colunas (Modalidade/Aluguel Bruto Ajustado/Ocupação/Preço por m²),
# batendo com o print de referência do usuário (Long-Stay/Short-Stay/Total). Não reaproveita
# locacoesGalpaoTableHtml (colunas não fazem sentido aqui -- não há "Área Locada"/"Valor
# Contratado" separado de "Pago"/"Reajuste") -- função irmã nova, própria pra esse formato,
# gated em op.locacoes_modalidade (mesmo padrão opt-in dos outros mecanismos "acompanhamento
# das locações"/"por ativo"). Fonte: aba 'Residencial Itaim', bloco "Acompanhamento por
# modalidade" (colunas O:R, a partir da linha com o cabeçalho "Modalidade") -- ignora a linha
# "Sub-total" (duplica os números do Long-Stay, não aparece no print de referência).
def parse_locacoes_modalidade_itaim():
    if 'Residencial Itaim' not in wb.sheetnames:
        return None
    ws = wb['Residencial Itaim']
    header_row = None
    for r in range(1, min(ws.max_row, 60) + 1):
        v = ws.cell(row=r, column=15).value  # coluna O
        if isinstance(v, str) and norm(v) == 'modalidade':
            header_row = r
            break
    if header_row is None:
        return None

    rows = []
    total_row = None
    r = header_row + 1
    while True:
        label = ws.cell(row=r, column=15).value       # O
        valor = ws.cell(row=r, column=16).value         # P: Aluguel Bruto Ajustado (R$)
        ocupacao = ws.cell(row=r, column=17).value       # Q: Ocupação (% do aluguel bruto total)
        preco_m2 = ws.cell(row=r, column=18).value         # R: Preço/m²
        if label is None:
            break
        # normaliza tirando hífen/pontuação também -- "Sub-total" (com hífen, como vem na
        # aba) não batia em norm() puro (só colapsa espaços, não hífen), então a linha
        # duplicada escapava do filtro e aparecia no card junto com "Long-Stay"/"Short-Stay".
        label_norm = re.sub(r'[^a-z0-9]+', ' ', norm(str(label))).strip()
        if label_norm in ('sub total', 'subtotal'):
            r += 1
            continue
        if label_norm == 'total':
            total_row = {'label': 'Total', 'valor': valor, 'ocupacao': ocupacao, 'preco_m2': preco_m2}
            break
        rows.append({'label': str(label).strip(), 'valor': valor, 'ocupacao': ocupacao, 'preco_m2': preco_m2})
        r += 1

    if not rows:
        return None
    return {'rows': rows, 'total': total_row}

LOCACOES_MODALIDADE_BY_OP = {'Residencial Itaim': parse_locacoes_modalidade_itaim()}

# ---------- Quebra de cálculo do covenant financeiro (Dívida Líquida/EBITDA) (31ª rodada) ----------
# Pedido do usuário: cadastrar o covenant nos Itens de Acompanhamento (ver COVENANTS_MANUAL
# 'Localfrio' acima, item extra "Convenants") e permitir clicar nele pra abrir uma sub-página
# com a tabela de quebra do cálculo (mesmo padrão de sub-página já usado pro hotel_perf da
# Calçada). Fonte: bloco "Movecta" na aba 'Localfrio', colunas L:R, linhas 33-52 — reconstrução
# do EBITDA contábil (eliminando IR/CSLL, depreciação/amortização e a SPE de Administração de
# Bens) e do Índice de Cobertura de Serviço da Dívida (Geração de Caixa / Juros e Amortização do
# CRI), ano a ano. Layout livre (usuário: "pode formatar seguindo o padrão, não precisa ser
# igual"); mantemos a estrutura de linhas da planilha (inclui os 2 "blocos" EBITDA->Geração de
# Caixa->ICSD) pra não perder a rastreabilidade do cálculo.
def parse_covenant_calc_localfrio():
    if 'Localfrio' not in wb.sheetnames:
        return None
    ws = wb['Localfrio']
    HEADER_ROW = 33
    LABEL_COL, FONTE_COL, FIRST_VAL_COL, LAST_VAL_COL = 12, 13, 14, 18  # L, M, N..R

    periods = []
    for c in range(FIRST_VAL_COL, LAST_VAL_COL + 1):
        v = ws.cell(row=HEADER_ROW, column=c).value
        periods.append(to_jsonable(v) if isinstance(v, (datetime, date)) else None)
    if not any(periods):
        return None

    ROW_SPECS = [
        (34, 'normal'), (35, 'normal'), (36, 'normal'), (37, 'normal'), (38, 'normal'),
        (39, 'normal'), (40, 'normal'), (41, 'normal'), (42, 'subtotal'),
        (44, 'normal'), (45, 'normal'), (46, 'normal'), (47, 'subtotal'),
        (49, 'normal'), (50, 'normal'), (51, 'ratio_highlight'), (52, 'status'),
    ]
    rows = []
    for r, kind in ROW_SPECS:
        label = ws.cell(row=r, column=LABEL_COL).value
        if not label:
            continue
        fonte = ws.cell(row=r, column=FONTE_COL).value
        values = []
        for c in range(FIRST_VAL_COL, LAST_VAL_COL + 1):
            values.append(to_jsonable(ws.cell(row=r, column=c).value))
        rows.append({'label': str(label).strip(), 'fonte': (str(fonte).strip() if fonte else None),
                     'kind': kind, 'values': values})
    if not rows:
        return None
    return {
        'title': 'Covenant Financeiro — Dívida Líquida/EBITDA',
        'subtitle': 'Reconstrução do EBITDA contábil e do Índice de Cobertura de Serviço da Dívida, ano a ano',
        'periods': periods,
        'has_fonte': True,
        'rows': rows,
        'footnote': 'Fonte: demonstrações financeiras (DFs), razão contábil (SAP) e fechamento mensal do CRI. '
                    'EBITDA elimina IR/CSLL (corrente e diferido), resultado financeiro, depreciação/amortização '
                    '(incl. efeito IFRS 16) e a SPE Localfrio Administração de Bens. Covenant: Dívida Líquida/EBITDA '
                    'com trajetória decrescente até ≤ 3,0x em 5 anos (AGT 29/08/2022).',
    }

COVENANT_CALC_BY_OP = {'Localfrio': parse_covenant_calc_localfrio()}

# Operações onde o card genérico "Indicadores" (dump bruto, sem curadoria, da aba
# "<Op> - Indicadores") fica escondido porque o mesmo dado já aparece curado em algum
# outro card (Calçada: a mesma aba 'Calçada - Indicadores ' já alimenta o card
# "Acompanhamento de Estoque", ver regra geral #18/#19 -- mostrar os dois ficava
# redundante). Continua ativo pra outras operações (MSB Triu/Axis/Edson) que não têm
# card curado equivalente.
# ---------- MSB Axis (37ª rodada) -- ponto 6: card "Acompanhamento da Carteira, Vendas
# e Estoque". Fonte: aba 'MSB Axis', quadro 'Acompanhamento de Vendas' (linhas 190-213,
# colunas O:V), valores fixos/consolidados (não dependem de navegação por período).
def parse_carteira_vendas_estoque_axis():
    """Ajuste pós-publicação (ponto 4): reformulado pra seguir EXATAMENTE o layout do print
    que o usuário mandou (2x) -- linhas por ANO (2024/2025/2026) com Quantidade AXIS/SYNC
    lado a lado, Área privativa e Valor da venda CONSOLIDADOS (soma das 2 torres), Preço
    médio/m² por torre; depois linha "Vendido" (mesmo formato), banner "Carteira Recebida/a
    Receber", e linha "Estoque". A 1ª versão (linhas por torre, colunas Vendido/Estoque)
    não seguia esse layout -- reconstruído do zero. Fonte: aba 'MSB Axis', linhas 196-213,
    colunas O:V (mesmo bloco 'Acompanhamento de Vendas' de antes, só que lido nas colunas
    certas p/ montar as linhas por ano: col S=Área Privativa, col V=Valor da Venda já vem
    pré-somado AXIS+SYNC na própria planilha)."""
    if 'MSB Axis' not in wb.sheetnames:
        return None
    ws = wb['MSB Axis']

    def g(r, c):
        return to_jsonable(ws.cell(row=r, column=c).value)

    anos = []
    # (linha AXIS, linha SYNC) por ano -- área privativa/valor da venda somam as 2 torres
    for ano, r_axis, r_sync in [(2024, 196, 201), (2025, 197, 202), (2026, 198, 203)]:
        area = (g(r_axis, 18) or 0) + (g(r_sync, 18) or 0)
        valor = g(r_axis, 22)  # coluna V já vem pré-somada (AXIS+SYNC) na planilha
        anos.append({
            'label': str(ano),
            'qtd_axis': g(r_axis, 17), 'qtd_sync': g(r_sync, 17),
            'area': area, 'valor': valor,
            'preco_axis': g(r_axis, 20), 'preco_sync': g(r_sync, 20),
        })

    vendido = {
        'label': 'Vendido',
        'qtd_axis': g(199, 17), 'qtd_sync': g(204, 17),
        'area': (g(199, 18) or 0) + (g(204, 18) or 0), 'valor': g(206, 19),
        'preco_axis': g(199, 20), 'preco_sync': g(204, 20),
    }
    estoque = {
        'label': 'Estoque',
        'qtd_axis': g(210, 17), 'qtd_sync': g(211, 17),
        'area': (g(210, 18) or 0) + (g(211, 18) or 0), 'valor': g(208, 19),
        'preco_axis': g(210, 20), 'preco_sync': g(211, 20),
    }

    carteira_recebida = g(213, 19)
    carteira_a_receber = g(213, 20)
    if carteira_recebida is None and carteira_a_receber is None:
        return None

    return {
        'anos': anos,
        'vendido': vendido,
        'estoque': estoque,
        'carteira_recebida': carteira_recebida,
        'carteira_a_receber': carteira_a_receber,
    }

CARTEIRA_VENDAS_ESTOQUE_BY_OP = {'MSB Axis': parse_carteira_vendas_estoque_axis()}

# ---------- MSB Axis (37ª rodada) -- ponto 7: sub-página com abertura mês a mês do card
# acima. Fonte: aba 'MSB Axis', colunas Z:AP, linhas 5 em diante -- para quando a série
# real termina (última linha com Área Estoque Total preenchida; linhas seguintes são
# meses futuros ainda sem fechamento).
def parse_carteira_detalhe_axis():
    if 'MSB Axis' not in wb.sheetnames:
        return None
    ws = wb['MSB Axis']
    rows = []
    for r in range(5, 190):
        data = ws.cell(row=r, column=26).value  # Z
        area_estoque_total = ws.cell(row=r, column=40).value  # AN
        if data is None:
            break
        if area_estoque_total is None:
            break
        rows.append({
            'data': to_jsonable(data),
            'axis_uni': to_jsonable(ws.cell(row=r, column=27).value),
            'axis_financeiro': to_jsonable(ws.cell(row=r, column=28).value),
            'axis_area': to_jsonable(ws.cell(row=r, column=29).value),
            'axis_preco_medio': to_jsonable(ws.cell(row=r, column=30).value),
            'axis_area_estoque': to_jsonable(ws.cell(row=r, column=31).value),
            'axis_preco_ltm': to_jsonable(ws.cell(row=r, column=32).value),
            'sync_uni': to_jsonable(ws.cell(row=r, column=33).value),
            'sync_financeiro': to_jsonable(ws.cell(row=r, column=34).value),
            'sync_area': to_jsonable(ws.cell(row=r, column=35).value),
            'sync_preco_medio': to_jsonable(ws.cell(row=r, column=36).value),
            'sync_area_estoque': to_jsonable(ws.cell(row=r, column=37).value),
            'sync_preco_ltm': to_jsonable(ws.cell(row=r, column=38).value),
            'preco_ltm_ponderado': to_jsonable(ws.cell(row=r, column=39).value),
            'area_estoque_total': to_jsonable(area_estoque_total),
            'sd_cri': to_jsonable(ws.cell(row=r, column=41).value),
            'loan_basis': to_jsonable(ws.cell(row=r, column=42).value),
        })
    if not rows:
        return None
    return rows

CARTEIRA_DETALHE_BY_OP = {'MSB Axis': parse_carteira_detalhe_axis()}

# ---------- MSB Axis (37ª rodada) -- ponto 8: IC em visão única (histórico + projetado),
# igual ao gráfico enviado pelo usuário. Fonte: aba 'MSB Axis - Indicadores', colunas
# B (Data) / X (IC Histórico + Projetado) / Z (IC Mínimo, constante 1,30x).
def parse_ic_projected_axis():
    sheet = 'MSB Axis - Indicadores'
    if sheet not in wb.sheetnames:
        return None
    ws = wb[sheet]
    rows = []
    for r in range(9, 66):
        data = ws.cell(row=r, column=2).value
        ic = ws.cell(row=r, column=24).value
        if data is None:
            continue
        if ic is None:
            break
        rows.append({'data': to_jsonable(data), 'ic': to_jsonable(ic)})
    if not rows:
        return None
    return {'series': rows, 'ic_minimo': 1.3}

IC_PROJECTED_BY_OP = {'MSB Axis': parse_ic_projected_axis()}

# ---------- MSB Edson (43ª rodada, ponto 10) -- mesmo gráfico de IC (histórico + projetado
# numa visão única, sem navegação por janela) usado na MSB Axis. Fonte: aba
# 'MSB Edson - Indicadores', mesmíssimo layout de colunas da aba da Axis/Triu: B (Data) / X
# (IC Histórico + Projetado) / Z (IC Mínimo, constante 1,50x aqui -- ver linha 6 da aba
# MSB Edson, 'índice de Cobertura', Exigido=1,5).
def parse_ic_projected_edson():
    sheet = 'MSB Edson - Indicadores'
    if sheet not in wb.sheetnames:
        return None
    ws = wb[sheet]
    rows = []
    for r in range(9, 66):
        data = ws.cell(row=r, column=2).value
        ic = ws.cell(row=r, column=24).value
        if data is None:
            continue
        if ic is None:
            break
        rows.append({'data': to_jsonable(data), 'ic': to_jsonable(ic)})
    if not rows:
        return None
    # 43ª rodada, ponto 10: nota metodológica pedida pelo usuário especificamente pra essa
    # operação (texto exato fornecido) -- não retroaplicada à MSB Axis (que usa o mesmíssimo
    # gráfico) por não ter sido pedida lá.
    nota = ("O IC do mês de referência corresponde ao menor índice verificado entre os meses "
            "da série projetada. O índice de cada mês projetado é a razão entre (i) o VPL do "
            "empreendimento e (ii) o Saldo Devedor dos CRI.")
    return {'series': rows, 'ic_minimo': 1.5, 'nota': nota}

IC_PROJECTED_BY_OP['MSB Edson'] = parse_ic_projected_edson()

# ---------- MSB Axis (37ª rodada) -- ponto 9: gráfico "Evolução Física da Obra"
# (Previsto/Realizado Mês + Acum.) substituindo o gráfico de LTV no fluxo mensal.
# Fonte: aba 'MSB Axis', colunas AR:AV, linhas 5 em diante.
def parse_obra_evolucao_axis(window=9):
    """Ajuste pós-publicação (ponto 6): a 1ª versão trazia a série INTEIRA, incluindo os
    meses futuros ainda sem execução (Realizado Mês = 0, do mês seguinte ao fechamento até
    o fim do cronograma previsto) -- por isso o gráfico publicado divergia do exemplo do
    usuário, que mostra só os ÚLTIMOS meses com dado real (Nov/25-Jul/26, 9 meses; valores
    conferidos batem exato com o exemplo: Previsto Acum. 45,7%/Realizado Acum. 46,6% em
    Jul/26). Corrigido: filtra só meses com Realizado Mês > 0 (execução de fato ocorrida) e
    janela pros últimos `window` (mesmo padrão de "janela recente" usado noutros gráficos
    do portal, ex. IC/LTV com buildBarChart)."""
    if 'MSB Axis' not in wb.sheetnames:
        return None
    ws = wb['MSB Axis']
    rows = []
    for r in range(5, 190):
        data = ws.cell(row=r, column=44).value  # AR
        realizado_mes = ws.cell(row=r, column=46).value  # AT
        if data is None:
            break
        if realizado_mes is None:
            break
        if not (isinstance(realizado_mes, (int, float)) and realizado_mes > 0):
            continue
        rows.append({
            'data': to_jsonable(data),
            'previsto_mes': to_jsonable(ws.cell(row=r, column=45).value),
            'realizado_mes': to_jsonable(realizado_mes),
            'previsto_acum': to_jsonable(ws.cell(row=r, column=47).value),
            'realizado_acum': to_jsonable(ws.cell(row=r, column=48).value),
        })
    if not rows:
        return None
    return rows[-window:] if window else rows

OBRA_EVOLUCAO_BY_OP = {'MSB Axis': parse_obra_evolucao_axis()}

# ---------- MSB Edson (43ª rodada, ponto 11) -- mesmo gráfico "Evolução Física da Obra" da
# MSB Axis, no lugar do gráfico de LTV. Fonte: aba 'MSB Edson', colunas X:AD, linhas 5 em
# diante (mesmo layout relativo da Axis, só que em colunas mais à esquerda: X=Data em vez de
# AR). Janela de 6 meses (não 9 como a Axis) -- é o que bate com o exemplo do usuário
# (fev/26-jul/26, Realizado Acum. final 87,9% -- conferido exato contra a aba).
def parse_obra_evolucao_edson(window=6):
    if 'MSB Edson' not in wb.sheetnames:
        return None
    ws = wb['MSB Edson']
    rows = []
    for r in range(5, 190):
        data = ws.cell(row=r, column=24).value  # X
        realizado_mes = ws.cell(row=r, column=27).value  # AA
        if data is None:
            break
        if realizado_mes is None:
            break
        if not (isinstance(realizado_mes, (int, float)) and realizado_mes > 0):
            continue
        rows.append({
            'data': to_jsonable(data),
            'previsto_mes': to_jsonable(ws.cell(row=r, column=25).value),
            'realizado_mes': to_jsonable(realizado_mes),
            'previsto_acum': to_jsonable(ws.cell(row=r, column=28).value),
            'realizado_acum': to_jsonable(ws.cell(row=r, column=30).value),
        })
    if not rows:
        return None
    return rows[-window:] if window else rows

OBRA_EVOLUCAO_BY_OP['MSB Edson'] = parse_obra_evolucao_edson()

# ---------- MSB Axis -- ajuste pós-publicação, ponto 1: card "Integralizações" / sub-página
# com a tabela de abertura por data. Fonte: aba 'MSB Axis', linhas 20-22 (resumo Emitido/
# Integralizado/A Integralizar, colunas E:H) + linhas 23-37 (tabela Data/Quantidade/PU de
# integralização/Valor integralizado, colunas E:H, cabeçalho na linha 23).
def parse_integralizacoes_axis():
    if 'MSB Axis' not in wb.sheetnames:
        return None
    ws = wb['MSB Axis']
    emitido = {'qtd': to_jsonable(ws.cell(row=20, column=6).value), 'valor': to_jsonable(ws.cell(row=20, column=8).value)}
    integralizado = {'qtd': to_jsonable(ws.cell(row=21, column=6).value), 'valor': to_jsonable(ws.cell(row=21, column=8).value)}
    a_integralizar = {'qtd': to_jsonable(ws.cell(row=22, column=6).value),
                       'valor_nominal': to_jsonable(ws.cell(row=22, column=7).value),
                       'valor_atual': to_jsonable(ws.cell(row=22, column=8).value)}
    rows = []
    r = 24
    while r <= ws.max_row:
        data = ws.cell(row=r, column=5).value
        if data is None:
            break
        rows.append({
            'data': to_jsonable(data),
            'quantidade': to_jsonable(ws.cell(row=r, column=6).value),
            'pu': to_jsonable(ws.cell(row=r, column=7).value),
            'valor': to_jsonable(ws.cell(row=r, column=8).value),
        })
        r += 1
    if not rows:
        return None
    return {'emitido': emitido, 'integralizado': integralizado, 'a_integralizar': a_integralizar, 'rows': rows}

INTEGRALIZACOES_BY_OP = {'MSB Axis': parse_integralizacoes_axis()}

# ---------- MSB Triu (43ª rodada, ponto 8) -- mesmo card/sub-página de Integralizações da
# MSB Axis. Fonte: aba 'MSB Triu', linhas 17-19 (resumo Emitido/Integralizado/A Integralizar,
# colunas E:H) + linhas 21+ (tabela Data/Quantidade/PU/Valor, mesmas colunas -- só 3 linhas:
# integralização inicial + 2 posteriores, já refletidas no texto de Sobre a Operação).
def parse_integralizacoes_triu():
    if 'MSB Triu' not in wb.sheetnames:
        return None
    ws = wb['MSB Triu']
    emitido = {'qtd': to_jsonable(ws.cell(row=17, column=6).value), 'valor': to_jsonable(ws.cell(row=17, column=8).value)}
    integralizado = {'qtd': to_jsonable(ws.cell(row=18, column=6).value), 'valor': to_jsonable(ws.cell(row=18, column=8).value)}
    a_integralizar = {'qtd': to_jsonable(ws.cell(row=19, column=6).value),
                       'valor_nominal': to_jsonable(ws.cell(row=19, column=7).value),
                       'valor_atual': to_jsonable(ws.cell(row=19, column=8).value)}
    rows = []
    r = 21
    while r <= ws.max_row:
        data = ws.cell(row=r, column=5).value
        if data is None:
            break
        rows.append({
            'data': to_jsonable(data),
            'quantidade': to_jsonable(ws.cell(row=r, column=6).value),
            'pu': to_jsonable(ws.cell(row=r, column=7).value),
            'valor': to_jsonable(ws.cell(row=r, column=8).value),
        })
        r += 1
    if not rows:
        return None
    return {'emitido': emitido, 'integralizado': integralizado, 'a_integralizar': a_integralizar, 'rows': rows}

INTEGRALIZACOES_BY_OP['MSB Triu'] = parse_integralizacoes_triu()

# ---------- MSB Edson (43ª rodada, ponto 8) -- idem. Fonte: aba 'MSB Edson', linhas 15-17
# (resumo, colunas E:H) + linhas 19+ (tabela, mesmas colunas).
def parse_integralizacoes_edson():
    if 'MSB Edson' not in wb.sheetnames:
        return None
    ws = wb['MSB Edson']
    emitido = {'qtd': to_jsonable(ws.cell(row=15, column=6).value), 'valor': to_jsonable(ws.cell(row=15, column=8).value)}
    integralizado = {'qtd': to_jsonable(ws.cell(row=16, column=6).value), 'valor': to_jsonable(ws.cell(row=16, column=8).value)}
    a_integralizar = {'qtd': to_jsonable(ws.cell(row=17, column=6).value),
                       'valor_nominal': to_jsonable(ws.cell(row=17, column=7).value),
                       'valor_atual': to_jsonable(ws.cell(row=17, column=8).value)}
    rows = []
    r = 19
    while r <= ws.max_row:
        data = ws.cell(row=r, column=5).value
        if data is None:
            break
        rows.append({
            'data': to_jsonable(data),
            'quantidade': to_jsonable(ws.cell(row=r, column=6).value),
            'pu': to_jsonable(ws.cell(row=r, column=7).value),
            'valor': to_jsonable(ws.cell(row=r, column=8).value),
        })
        r += 1
    if not rows:
        return None
    return {'emitido': emitido, 'integralizado': integralizado, 'a_integralizar': a_integralizar, 'rows': rows}

INTEGRALIZACOES_BY_OP['MSB Edson'] = parse_integralizacoes_edson()

# ---------- MSB Triu (42ª rodada) -- ponto 7: card "Acompanhamento da Carteira, Vendas e
# Estoque", mesmo padrão visual da MSB Axis, mas SEM a divisão AXIS/SYNC (a Triu tem uma
# única torre) -- por isso os campos aqui vêm "achatados" (qtd/area/valor/preco, sem sufixo
# _axis/_sync) e o dict carrega 'dual': False pro template saber que é o layout de 1 coluna
# só de quantidade/preço (ver carteiraVendasEstoquePanelHtml no portal_template.html).
# Fonte: aba 'MSB Triu', bloco 'Acompanhamento de Vendas' (linhas 108-120, colunas O:S).
def parse_carteira_vendas_estoque_triu():
    if 'MSB Triu' not in wb.sheetnames:
        return None
    ws = wb['MSB Triu']

    def g(r, c):
        return to_jsonable(ws.cell(row=r, column=c).value)

    anos = []
    for ano, r in [(2023, 110), (2024, 111), (2025, 112), (2026, 113)]:
        anos.append({'label': str(ano), 'qtd': g(r, 16), 'area': g(r, 17), 'valor': g(r, 18), 'preco': g(r, 19)})

    vendido = {'label': 'Vendido', 'qtd': g(114, 16), 'area': g(114, 17), 'valor': g(114, 18), 'preco': g(114, 19)}
    # Estoque AFI (linha 117) não tem a própria coluna de preço médio na planilha -- mas AFI/
    # Vendável/Permuta/SCPista usam todos o MESMO preço médio/m² do empreendimento (confirmado:
    # valor/área de cada bucket bate com o preço médio de "Vendido"), por isso calculado aqui em
    # vez de deixado em branco.
    estoque_afi_valor = g(117, 18)
    estoque_afi_area = g(117, 17)
    estoque_afi_preco = (estoque_afi_valor / estoque_afi_area) if (estoque_afi_valor and estoque_afi_area) else vendido.get('preco')
    estoque_afi = {'label': 'Estoque AFI', 'qtd': g(117, 16), 'area': estoque_afi_area, 'valor': estoque_afi_valor, 'preco': estoque_afi_preco}
    estoque_vendavel = {'label': "Estoque 'vendável'", 'qtd': g(118, 16), 'area': g(118, 17), 'valor': g(118, 18), 'preco': g(118, 19)}
    unidades_scpistas = {'label': 'Unidades SCPistas', 'qtd': g(120, 16), 'area': g(120, 17), 'valor': g(120, 18), 'preco': g(120, 19)}
    unidades_permuta = {'label': 'Unidades permuta', 'qtd': g(119, 16), 'area': g(119, 17), 'valor': g(119, 18), 'preco': g(119, 19)}

    # 'Carteira Recebida'/'Carteira a Receber' (linha 121-122 da aba) refletem o último
    # recálculo da planilha, que já inclui a receita de Ago/26 (R$ 1.726.103,36, ver aba
    # 'MSB Triu - Indicadores', linha de 01/08/2026) -- 1 mês à FRENTE do AS_OF do portal
    # (Jul/26). Ajustado aqui pra refletir o corte de Jul/26 (mesmo mês de referência de todo
    # o resto do portal): subtrai essa receita de Carteira Recebida e soma a Carteira a
    # Receber. O resultado bate exato com 'saldo a integralizar (pré-setembro)' da aba
    # Indicadores (célula C6 = 5.178.310,09), confirmando o corte.
    carteira_recebida_bruta = g(122, 18)
    carteira_a_receber_bruta = g(122, 19)
    receita_ago26 = 1726103.36
    carteira_recebida = (carteira_recebida_bruta - receita_ago26) if carteira_recebida_bruta else None
    carteira_a_receber = (carteira_a_receber_bruta + receita_ago26) if carteira_a_receber_bruta is not None else None

    return {
        'dual': False,
        'anos': anos,
        'vendido': vendido,
        'estoque': estoque_afi,
        'estoque_sub': [estoque_vendavel, unidades_scpistas, unidades_permuta],
        'carteira_recebida': carteira_recebida,
        'carteira_a_receber': carteira_a_receber,
    }

CARTEIRA_VENDAS_ESTOQUE_BY_OP['MSB Triu'] = parse_carteira_vendas_estoque_triu()

# ---------- MSB Triu (42ª rodada) -- ponto 7: sub-página com abertura mês a mês do card
# acima, mesmo padrão da MSB Axis (mas layout de torre única -- ver 'dual': False). Fonte:
# aba 'MSB Triu', colunas X:AG, linhas 5 em diante. Corta no 1º mês sem "Vendas mês (#uni)"
# populado (planilha crua já vem com a série completa desenhada até 2026, mas só os meses
# até o AS_OF (Jul/26) têm dado real -- os seguintes ficam em branco na própria aba).
def parse_carteira_detalhe_triu():
    if 'MSB Triu' not in wb.sheetnames:
        return None
    ws = wb['MSB Triu']
    rows = []
    for r in range(5, 200):
        data = ws.cell(row=r, column=24).value  # X
        vendas_mes = ws.cell(row=r, column=25).value  # Y
        if data is None or vendas_mes is None:
            break
        rows.append({
            'data': to_jsonable(data),
            'uni': to_jsonable(vendas_mes),
            'uni_acum': to_jsonable(ws.cell(row=r, column=26).value),  # Z
            'financeiro': to_jsonable(ws.cell(row=r, column=27).value),  # AA
            'area': to_jsonable(ws.cell(row=r, column=28).value),  # AB
            'preco_medio': to_jsonable(ws.cell(row=r, column=29).value),  # AC
            'preco_ltm': to_jsonable(ws.cell(row=r, column=30).value),  # AD
            'area_estoque': to_jsonable(ws.cell(row=r, column=31).value),  # AE
            'sd_cri': to_jsonable(ws.cell(row=r, column=32).value),  # AF
            'loan_basis': to_jsonable(ws.cell(row=r, column=33).value),  # AG
        })
    if not rows:
        return None
    return rows

CARTEIRA_DETALHE_BY_OP['MSB Triu'] = parse_carteira_detalhe_triu()

# ---------- MSB Edson (43ª rodada, ponto 9) -- mesmo card "Acompanhamento da Carteira,
# Vendas e Estoque" das outras 2 operações MSB (torre única, 'dual': False), com 2 diferenças
# pedidas pelo usuário (imagem de referência): (1) o dado-fonte de vendas na aba MSB Edson é
# MENSAL (bloco 'Acompanhamento de Vendas', linhas 58-64, colunas O:S), não anual como Axis/
# Triu -- agregado por ano aqui pra bater com o mesmo formato visual das outras 2 operações
# (conferido: os 4 anos, "Vendido" e "Estoque" batem exatos com a imagem, célula a célula);
# (2) linhas extras "% Total" (participação de Quantidade/Área sobre o total) logo abaixo de
# "Vendido" e de "Estoque" -- não existem em Axis/Triu, fonte: linhas 67/69, colunas P/Q.
def parse_carteira_vendas_estoque_edson():
    if 'MSB Edson' not in wb.sheetnames:
        return None
    ws = wb['MSB Edson']

    def g(r, c):
        return to_jsonable(ws.cell(row=r, column=c).value)

    from collections import OrderedDict
    by_year = OrderedDict()
    r = 58
    while True:
        data = ws.cell(row=r, column=15).value
        # Guarda contra linha não-data (não só None) -- achado na planilha de Ago/26 (teste de
        # atualização mensal, ponto único BR Prop): uma nova venda foi lançada nessa mesma aba
        # em Ago/26 (linha 65, "2026-08-31"), empurrando o bloco de rótulos "Vendido"/"Estoque"
        # (antes fixo nas linhas 66-69) uma linha pra baixo -- sem essa guarda, o loop batia na
        # string 'Vendido' (perdeu o None que antes parava o loop 1 linha antes) e quebrava com
        # AttributeError. Isso NÃO corrige os offsets fixos abaixo (g(66,...) etc, que passam a
        # apontar pra linha errada quando o bloco desloca) -- só evita o crash; se/quando essa
        # aba for atualizada de verdade em produção, os offsets precisam ser revistos.
        if not isinstance(data, datetime):
            break
        year = data.year
        b = by_year.setdefault(year, {'qtd': 0, 'area': 0.0, 'valor': 0.0})
        b['qtd'] += ws.cell(row=r, column=16).value or 0
        b['area'] += ws.cell(row=r, column=17).value or 0
        b['valor'] += ws.cell(row=r, column=18).value or 0
        r += 1
    anos = []
    for year, b in by_year.items():
        preco = (b['valor']/b['area']) if b['area'] else None
        anos.append({'label': str(year), 'qtd': to_jsonable(b['qtd']), 'area': to_jsonable(round(b['area'], 2)),
                     'valor': to_jsonable(round(b['valor'], 2)), 'preco': to_jsonable(preco)})

    vendido = {'label': 'Vendido', 'qtd': g(66, 16), 'area': g(66, 17), 'valor': g(66, 18), 'preco': g(66, 19)}
    pct_vendido = {'qtd': g(67, 16), 'area': g(67, 17)}
    estoque = {'label': 'Estoque', 'qtd': g(68, 16), 'area': g(68, 17), 'valor': g(68, 18), 'preco': g(68, 19)}
    pct_estoque = {'qtd': g(69, 16), 'area': g(69, 17)}
    # Carteira Recebida/a Receber (linha 71, colunas R/S): valor AO VIVO da aba -- diverge um
    # pouco do anexo enviado pelo usuário (R$ 37.791.041,71/R$ 8.160.943,13 aqui vs.
    # R$ 34.230.484/R$ 9.769.401 no anexo). Diferente do caso da Triu (onde achamos a
    # referência EXATA de onde vinha o corte), aqui não achamos nenhuma célula na planilha
    # batendo com os valores do anexo (busca no workbook inteiro, sem match) -- e todo o
    # resto da imagem (os 4 anos, Vendido, Estoque) bate exato com a aba ao vivo, então não é
    # um "anexo mais atualizado". Segue o valor ao vivo da aba, mesmo racional já usado no
    # resto do portal ("planilha viva" prevalece sobre print, exceto quando o usuário pede
    # expressamente pra usar o valor do anexo, como na Informações da Garantia desta mesma
    # operação, ponto 7).
    carteira_recebida = g(71, 18)
    carteira_a_receber = g(71, 19)
    return {
        'dual': False, 'anos': anos, 'vendido': vendido, 'estoque': estoque,
        'pct_vendido': pct_vendido, 'pct_estoque': pct_estoque,
        'carteira_recebida': carteira_recebida, 'carteira_a_receber': carteira_a_receber,
    }

CARTEIRA_VENDAS_ESTOQUE_BY_OP['MSB Edson'] = parse_carteira_vendas_estoque_edson()

# ---------- MSB Edson (43ª rodada, ponto 9) -- sub-página do card acima, mas AQUI a "quebra"
# não é mês a mês (a aba não tem abertura mensal com SD CRI/Loan Basis/Preço LTM como Axis/
# Triu) -- é a "Tabela de Unidades" já pronta na própria aba (linhas 4-54, colunas O:V):
# 1 linha por unidade (Status/Unidade/Área privativa/Valor de Tabela/Data Venda/Valor de
# Venda/Preço R$/m²/Tabela Longa-Curta-À Vista), com "Total" (linha 49) e subtotais por
# status (linhas 50-54: Vendida/Estoque/Permuta/SCP/Equity) no rodapé -- exatamente o layout
# do anexo enviado pelo usuário (mesmo título "Tabela de Unidades"), conferido linha a linha.
def parse_unidades_edson():
    if 'MSB Edson' not in wb.sheetnames:
        return None
    ws = wb['MSB Edson']

    def g(r, c):
        return to_jsonable(ws.cell(row=r, column=c).value)

    rows = []
    r = 5
    while True:
        status = ws.cell(row=r, column=15).value
        if status is None or status == 'Total':
            break
        rows.append({
            'status': status,
            'unidade': g(r, 16),
            'area': g(r, 17),
            'valor_tabela': g(r, 18),
            'data_venda': g(r, 19),
            'valor_venda': g(r, 20),
            'preco': g(r, 21),
            'tabela': g(r, 22),
        })
        r += 1
    if not rows:
        return None
    total_row = r
    total = {'label': 'Total', 'unidade': g(total_row, 16), 'area': g(total_row, 17),
             'valor_tabela': g(total_row, 18), 'valor_venda': g(total_row, 20)}
    subtotals = []
    sr = total_row + 1
    while True:
        status = ws.cell(row=sr, column=15).value
        if status is None:
            break
        subtotals.append({'label': status, 'unidade': g(sr, 16), 'area': g(sr, 17),
                           'valor_tabela': g(sr, 18), 'valor_venda': g(sr, 20), 'preco': g(sr, 21)})
        sr += 1
    return {'rows': rows, 'total': total, 'subtotals': subtotals}

UNIDADES_DETALHE_BY_OP = {'MSB Edson': parse_unidades_edson()}

# ---------- MSB Triu (42ª rodada) -- ponto 8: no lugar do gráfico de IC (a operação não tem
# um covenant de índice de cobertura de verdade monitorado no "Fluxo Mensal" -- o "IC
# Gerencial" da aba é só um cálculo interno, não um covenant formal, por isso não faz sentido
# tratá-lo como o gráfico de IC padrão), o usuário pediu 2 gráficos no lugar: "Histórico de
# Amortização" (barras, só meses já realizados) e "Acompanhamento LTV" (série de LTV
# projetado ESTÁVEL, não o LTV bruto do fluxo -- que "explode" perto do vencimento porque a
# garantia declina até goal zero num cronograma 100% projetado, ver LTV Atual 7.885,9% que
# aparecia antes desse ajuste). Fonte: aba 'MSB Triu - Indicadores', cabeçalho na linha 8
# (col B=Data, W=Amortização, AB=LTV 'flat').
def parse_amort_ltv_flat_triu():
    sheet = 'MSB Triu - Indicadores'
    if sheet not in wb.sheetnames:
        return None
    ws = wb[sheet]
    rows = []
    for r in range(9, 200):
        data = ws.cell(row=r, column=2).value  # B
        if data is None:
            break
        amort = ws.cell(row=r, column=23).value  # W
        ltv_flat = ws.cell(row=r, column=28).value  # AB
        rows.append({
            'data': to_jsonable(data),
            'amortizacao': to_jsonable(amort) if isinstance(amort, (int, float)) else None,
            'ltv_flat': to_jsonable(ltv_flat) if isinstance(ltv_flat, (int, float)) else None,
        })
    if not rows:
        return None
    return rows

AMORT_LTV_FLAT_BY_OP = {'MSB Triu': parse_amort_ltv_flat_triu()}

# ---------- Obrigações Pecuniárias / Quórum de Assembleias (38ª rodada, teste piloto Calçada) --
# Conteúdo colado pelo usuário direto da CCB (Cédula de Crédito Bancário) e do Termo de
# Securitização -- não vem da planilha (não existe uma fonte columnar pra isso), por isso é
# dado literal aqui, no mesmo espírito do MANUAL_CONTENT/COVENANTS_MANUAL logo abaixo. Aberto
# numa sub-página própria a partir do item "Obrigações Pecuniárias"/"Quórum de Assembleias" em
# Itens de Acompanhamento (ver COVENANTS_MANUAL['Calçada']['retitle'] acima, flags
# _has_obrigacoes_subpage/_has_quorum_subpage). Cada item leva o texto (com o prazo/regra) e a
# cláusula de origem (ref), pro usuário conseguir ir direto na fonte se precisar conferir.
OBRIGACOES_PECUNIARIAS_BY_OP = {
    # 41ª rodada (correção pós-publicação): tirado o banner de premissa (o usuário pediu pra
    # remover, "'nota' saiu do item) e as datas viraram ISO reais (antes eram texto "mmm/aaaa"),
    # pra poder reaproveitar EXATAMENTE a mesma régua de urgência de Itens de Acompanhamento
    # (ver daysBetween/covenantUrgency no template: ≤30 dias = Verificar, vencido = Desenquadrado,
    # senão Enquadrado -- calculado em cima de AS_OF, hoje 2026-07-31) em vez de um "Verificar"
    # fixo. 'ultimo' voltou (o usuário pediu a referência da data anterior, no mesmo formato de
    # .covitem-dates: "últ. atualização X · próxima Y").
    # Âncoras usadas pra estimar as datas: itens de relatório periódico (Demonstrações, IR do
    # Avalista, Demonstrativo semestral) consideram exercício social encerrado em 31/dez
    # (premissa padrão, ainda a confirmar); o Seguro usa a Data de Emissão do CCB (20/12/2019,
    # já mapeada em op.summary.data_emissao) como âncora do ciclo anual da apólice -- pedido do
    # usuário ("você já tem essa informação").
    'Calçada': {
        'fonte': 'CCB (Cédula de Crédito Bancário), Cláusula 4.1.1 (obrigações de fazer) e Cláusula 9.1(e) (obrigação de não fazer)',
        'items': [
            {'label': 'Demonstrações Financeiras Auditadas', 'text': 'Até 5 meses após o encerramento do exercício social (ou data da AGO, o que ocorrer primeiro).', 'ref': 'CCB, Cláusula 4.1.1(i)(a)', 'ultimo': '2026-05-31', 'proximo': '2027-05-31'},
            {'label': 'Balancete trimestral da Emitente e da Hotel Vogue', 'text': 'Até o 45º dia após o fim de cada trimestre.', 'ref': 'CCB, Cláusula 4.1.1(i)(b)', 'ultimo': '2026-05-15', 'proximo': '2026-08-14'},
            {'label': 'Atas societárias (AGO, RCA, conselho fiscal)', 'text': 'Em até 10 dias úteis da realização.', 'ref': 'CCB, Cláusula 4.1.1(i)(c)'},
            {'label': 'Comunicação de inadimplemento ou de Evento de Vencimento Antecipado', 'text': 'Próprio ou da Hotel Vogue, em até 5 dias úteis do conhecimento do fato.', 'ref': 'CCB, Cláusula 4.1.1(i)(d)'},
            {'label': 'Cópia de notificações judiciais/extrajudiciais recebidas', 'text': 'Em até 5 dias úteis do recebimento.', 'ref': 'CCB, Cláusula 4.1.1(i)(e)'},
            {'label': 'Informações complementares solicitadas pela Securitizadora', 'text': 'Em até 10 dias.', 'ref': 'CCB, Cláusula 4.1.1(i)(f)'},
            {'label': 'Declaração de IR do Avalista', 'text': 'Anualmente, em até 4 meses do fim do exercício.', 'ref': 'CCB, Cláusula 4.1.1(i)(g)', 'ultimo': '2026-04-30', 'proximo': '2027-04-30'},
            {'label': 'Demonstrativo contábil semestral', 'text': 'Despesas de condomínio, IPTU e foro do imóvel, até o 5º dia útil do semestre.', 'ref': 'CCB, Cláusula 4.1.1(xviii)', 'ultimo': '2026-07-08', 'proximo': '2027-01-08'},
            {'label': 'Reduzir capital social', 'text': 'Vedado reduzir capital social (exceto para absorver prejuízos) ou sofrer redução do patrimônio líquido da Emissora abaixo de R$ 50.000.000,00.', 'ref': 'CCB, Cláusula 9.1(e) — obrigação negativa/Vencimento Antecipado, não faz parte do bloco de reporte acima'},
            {'label': 'Relatório periódico sobre o hotel', 'text': 'Conforme Anexo VIII da CCB.', 'ref': 'CCB, Cláusula 4.1.1(xix)'},
            {'label': 'Manter seguro vigente do Imóvel', 'text': 'Endossado à Securitizadora em até 30 dias da emissão; comprovante anual e comprovante de renovação 30 dias antes do vencimento da apólice. Importância segurada mínima: R$ 108.000.000,00 (corrigida pelo IPCA).', 'ref': 'CCB, Cláusula 4.1.1(vi), com o tratamento de sinistro/indenização na Cláusula 4.1.1(vii)', 'ultimo': '2025-12-20', 'proximo': '2026-12-20'},
        ],
    },
    # 44ª rodada (Alianza GRU e Mauá): mesmo mecanismo piloto da Calçada acima, conteúdo colado
    # pelo usuário direto do Termo de Securitização (TS) -- todas as referências do usuário
    # citam "TS X.X.X", nenhuma CCB aqui. 'ultimo'/'proximo' preenchidos só pras 3 obrigações de
    # prazo PERIÓDICO (mesmo racional da Calçada, mesmas âncoras já usadas noutros pontos desta
    # operação): Laudo de avaliação usa o próprio ciclo anual "todo mês de Junho" já cadastrado
    # em Garantias (build_alianza_ativo_compare); DFs completas usa exercício social encerrado
    # em 31/dez + 90 dias corridos (=31/mar); Aditamento semestral usa as datas fixas do próprio
    # texto do usuário (15/jun e 15/dez). As demais obrigações (itens de vencimento antecipado,
    # disparados por evento -- cross-default, protesto, sinistro, reorganização societária) não
    # têm prazo fixo, então ficam sem 'ultimo'/'proximo', igual aos itens equivalentes da
    # Calçada (ex.: "Comunicação de inadimplemento").
    'Alianza GRU e Mauá': {
        'fonte': 'Termo de Securitização, Cláusula 6.4.2 (obrigações de fazer / eventos de vencimento antecipado) e Cláusulas 6.4.6/6.4.7 (obrigações de informação)',
        'obs': 'Eventos de vencimento antecipado, seguro e obrigações periódicas de informação previstos no Termo de Securitização — ver detalhamento completo.',
        'items': [
            {'label': 'Registro da Alienação Fiduciária de Imóvel', 'text': 'Registro em cartório em até 45 dias.', 'ref': 'TS, Cláusula 6.4.2(a)'},
            {'label': 'Cross-default', 'text': 'Vencimento antecipado de obrigação financeira em valor superior a R$ 0,5 MM individual ou R$ 1 MM agregado.', 'ref': 'TS, Cláusula 6.4.2(o)'},
            {'label': 'Protesto de títulos', 'text': 'Protesto em valor superior a R$ 0,5 MM individual ou R$ 1 MM agregado, com cura em até 15 dias.', 'ref': 'TS, Cláusula 6.4.2(q)'},
            {'label': 'Reorganização societária', 'text': 'Mudança de controle ou transferência de ativos igual ou superior a R$ 1 MM sem prévia anuência.', 'ref': 'TS, Cláusula 6.4.2(r)'},
            {'label': 'Sinistro sem indenização', 'text': 'Sinistro total ou parcial sem pagamento de indenização em até 180 dias.', 'ref': 'TS, Cláusula 6.4.2(w)/(x)'},
            {'label': 'Ônus ou gravame não autorizado', 'text': 'Constituição de ônus ou gravame sobre bens/direitos sem autorização, com cura em até 30 dias.', 'ref': 'TS, Cláusula 6.4.2(y)'},
            # 49ª rodada: "Renovação" e "Endosso" da apólice de seguro eram 2 itens separados
            # nessa lista (cláusulas distintas do TS) -- o usuário pediu pra juntar em 1 só
            # ("Seguro do Ativo"), com a mesma data que a linha "Endosso do Seguro" já mostra na
            # aba de Acompanhamento (última 01/08/2025, próxima 01/08/2026). Texto combina as 2
            # obrigações (renovar + endossar), ref cita as 2 cláusulas de origem.
            # 'status': 'Enquadrado' (correção pós-publicação, 49ª rodada): esse item é o MESMO
            # covenant da linha "Endosso do Seguro" minerada na aba de Acompanhamento (mesma
            # fonte, mesmas datas ultimo/proximo, ver build_alianza_covenants) -- sem 'status'
            # explícito aqui, renderTopicItems recalculava um status PRÓPRIO só pela proximidade
            # da data (≤30 dias = "Verificar"), diferente do status real ("Enquadrado") que a
            # aba de Acompanhamento mostra pro mesmo item -- 2 telas, 2 respostas pro mesmo dado
            # (usuário: "o seguro nas obrigações aparece enquadrado e na aba do ativo aparece
            # como verificar [...] está diferente"). 'status' explícito aqui faz esta sub-página
            # usar o MESMO dado real da planilha em vez de reinventar um por conta própria.
            {'label': 'Seguro do Ativo', 'text': 'Manter a apólice sempre vigente, com renovação em até 15 dias do vencimento (pela Securitizadora, caso não renovada antes pela Devedora) e endosso à Emissora como única beneficiária em até 30 dias da contratação/renovação.', 'ref': 'TS, Cláusulas 6.4.2(aa) e 6.4.2(bb)', 'ultimo': '2025-08-01', 'proximo': '2026-08-01', 'status': 'Enquadrado'},
            {'label': 'Laudo de avaliação', 'text': 'Entrega anual.', 'ref': 'TS, Cláusula 6.4.6.1', 'ultimo': '2026-06-30', 'proximo': '2027-06-30'},
            {'label': 'Demonstrações Financeiras completas', 'text': 'Envio em até 90 dias do encerramento do exercício social.', 'ref': 'TS, Cláusula 6.4.7.2', 'ultimo': '2026-03-31', 'proximo': '2027-03-31'},
            {'label': 'Aditamento semestral da Cessão Fiduciária', 'text': 'Celebrado em 15/jun e 15/dez de cada ano, com registro em cartório em até 10 dias da celebração.', 'ref': 'Contrato de Cessão Fiduciária, Cláusula 1.1.3', 'ultimo': '2026-06-15', 'proximo': '2026-12-15'},
        ],
    },
}
QUORUM_ASSEMBLEIA_BY_OP = {
    'Calçada': {
        'fonte': 'Termo de Securitização, Cláusula Décima Sétima — Assembleia Geral de Titulares de CRI',
        'sections': [
            {
                'title': 'Convocação',
                'items': [
                    {'text': 'Pode ser convocada pela Emissora, pelo Agente Fiduciário, pela CVM e/ou por Investidores que representem, no mínimo, 10% dos CRI em Circulação.', 'ref': 'TS, Cláusula 17.3'},
                    {'text': 'Edital publicado 3 vezes: antecedência mínima de 15 dias para a 1ª convocação e 8 dias para a 2ª (20 dias em caso de liquidação do Patrimônio Separado). A 2ª convocação não pode ser feita junto com a 1ª.', 'ref': 'TS, Cláusulas 17.4 e 17.5'},
                ],
            },
            {
                'title': 'Instalação',
                'compare': True,
                'items': [
                    {'label': '1ª convocação', 'text': 'Presença de titulares que representem, no mínimo, metade mais um dos CRI em Circulação.', 'ref': 'TS, Cláusula 17.6(i)'},
                    {'label': '2ª convocação', 'text': 'Instala-se com qualquer número de CRI em Circulação presentes.', 'ref': 'TS, Cláusula 17.6(ii)'},
                ],
            },
            {
                'title': 'Deliberação (quórum geral)',
                'compare': True,
                'items': [
                    {'label': '1ª convocação', 'text': 'Maioria dos CRI em Circulação (base total).', 'ref': 'TS, Cláusula 17.12(a)'},
                    {'label': '2ª convocação', 'text': 'Maioria dos CRI em Circulação presentes, desde que presentes votantes representando pelo menos 20% dos CRI em Circulação.', 'ref': 'TS, Cláusula 17.12(b)'},
                ],
            },
            {
                'title': 'Quórum qualificado — 90% dos CRI em Circulação',
                'ref': 'TS, Cláusula 17.13',
                'intro': 'Exigido para deliberar sobre:',
                'ordered': True,
                'highlight': True,
                'items': [
                    {'text': 'Alteração das datas de pagamento de principal e Remuneração.'},
                    {'text': 'Alteração da Remuneração ou do principal dos CRI.'},
                    {'text': 'Alteração do prazo de vencimento dos CRI.'},
                    {'text': 'Quaisquer alterações na CCB que mudem as condições dos Créditos Imobiliários.'},
                    {'text': 'Alteração dos eventos de liquidação do Patrimônio Separado.'},
                    {'text': 'Criação de hipóteses de resgate antecipado/amortização extraordinária, e/ou alteração dos Eventos de Vencimento Antecipado (do TS ou da CCB).'},
                    {'text': 'Alteração de qualquer quórum de deliberação previsto no TS.'},
                    {'text': 'Renúncia prévia a direitos dos titulares ou perdão temporário (waiver) de obrigações da Emissora e/ou da Devedora.'},
                ],
            },
        ],
    },
    # 44ª rodada (Alianza GRU e Mauá): mesmo mecanismo piloto acima, texto colado pelo usuário
    # direto do TS (Cláusulas 14.3 a 14.9, Assembleia Geral de Titulares/AGT). 'Instalação' e
    # 'Falta de quórum' viram sec.compare (2 cenários lado a lado, mesmo tratamento visual já
    # usado em 'Instalação'/'Deliberação' da Calçada); 'Deliberação qualificada' é a seção mais
    # crítica de operar (mexe em juros/prazo/amortização/vencimento antecipado), então ganha
    # sec.highlight igual ao quórum de 90% da Calçada.
    'Alianza GRU e Mauá': {
        'fonte': 'Termo de Securitização, Cláusulas 14.3 a 14.9 — Assembleia Geral de Titulares de CRI',
        'obs': 'Regras de convocação, instalação e deliberação da Assembleia Geral de Titulares de CRI — ver detalhamento completo.',
        'sections': [
            {
                'title': 'Convocação',
                'items': [
                    {'text': 'Pode ser convocada por titulares que representem, no mínimo, 10% dos CRI em Circulação.', 'ref': 'TS, Cláusula 14.3(d)'},
                ],
            },
            {
                'title': 'Instalação',
                'compare': True,
                'items': [
                    {'label': '1ª convocação', 'text': 'Presença de titulares que representem, no mínimo, 2/3 dos CRI em Circulação.', 'ref': 'TS, Cláusula 14.4'},
                    {'label': '2ª convocação', 'text': 'Instala-se com presença de titulares que representem, no mínimo, 20% dos CRI em Circulação.', 'ref': 'TS, Cláusula 14.4'},
                ],
            },
            {
                'title': 'Deliberação (quórum padrão)',
                'items': [
                    {'text': 'Aprovação por maioria simples (50% + 1) dos votos dos titulares presentes.', 'ref': 'TS, Cláusula 14.8'},
                ],
            },
            {
                'title': 'Deliberação qualificada — 75% dos presentes',
                'ref': 'TS, Cláusula 14.9',
                'intro': 'Exigido em 1ª e 2ª convocação para deliberar sobre:',
                'ordered': True,
                'highlight': True,
                'items': [
                    {'text': 'Alteração da Remuneração (juros) dos CRI.'},
                    {'text': 'Alteração do prazo de vencimento dos CRI.'},
                    {'text': 'Alteração das condições de amortização dos CRI.'},
                    {'text': 'Alteração das hipóteses de vencimento antecipado.'},
                    {'text': 'Pagamento antecipado (resgate antecipado/amortização extraordinária) dos CRI.'},
                ],
            },
            {
                'title': 'Falta de quórum',
                'compare': True,
                'items': [
                    {'label': 'Evento automático', 'text': 'A Emissora declara o vencimento antecipado independentemente de deliberação em Assembleia.', 'ref': 'TS, Cláusula 6.4.4'},
                    {'label': 'Evento não automático', 'text': 'A Emissora não declara o vencimento antecipado na falta do quórum de instalação/deliberação.', 'ref': 'TS, Cláusula 6.4.5'},
                ],
            },
        ],
    },
}

INDICADORES_HIDE = {'Calçada', 'MSB Axis', 'MSB Triu', 'MSB Edson'}

# ---------- Conteúdo manual por operação (Sobre a Operação / Highlights) ----------
# Curado à mão, operação por operação, conforme revisão com o usuário — não vem da planilha nem do PPT.
MANUAL_CONTENT = {
    'Evolution': {
        'sobre_operacao': [
            "Operação lastreada em créditos imobiliários oriundos de contratos de locação, tendo como Devedora o FUNDO DE INVESTIMENTO IMOBILIÁRIO – FII REC RENDA IMOBILIÁRIA, lastreada nas locações dos imóveis para Elo Participações/Banco Digio (Alphaville/Barueri) e Corteva Agriscience/CTVA Proteção de Cultivos. A operação conta com CF dos recebíveis de locação (Contrato de Cessão Fiduciária de Direitos Creditórios).",
            "Emitida em 12/12/2019, no valor de R$ 63 milhões, remuneração IPCA + 6,25% a.a., com amortização mensal.",
            "Covenants financeiros monitorados a partir de 10/jan/2025: Índice de Cobertura ≥ 1,20x (média dos últimos 3 meses do fluxo de recebíveis depositado na Conta do Patrimônio Separado / média dos últimos 3 meses das parcelas de Amortização Programada + Juros Remuneratórios dos CRI), apurado mensalmente.",
        ],
        'highlights': [
            "O IC médio apurado no mês foi de 1,25x acima do mínimo de 1,20x.",
            "Foi comunicada a intenção do Banco Digio S.A. em descontinuar a locação dos conjuntos que hoje ocupa (701 a 704 – 7º andar). Considerando o impacto da saída desse inquilino, o IC spot seria de 1,05x, enquanto a média móvel (3 meses) ficaria em 1,20x.",
        ],
    },
    'Calçada': {
        'sobre_operacao': [
            "Operação lastreada em créditos imobiliários oriundos de CCB emitida pela Calçada Empreendimentos Imobiliários S.A., destinada ao financiamento da construção do empreendimento hoteleiro \"Square Design Hotel\", na Barra da Tijuca/RJ. A operação conta com AFI do imóvel, AF de Quotas, CF dos recebíveis do hotel (Arrecadação + Conta Vinculada) e Fundo de Reserva.",
            "Emitida em Dez/19, no valor de até R$ 30,0 milhões, remuneração IPCA + 12,00% a.a., com vencimento final prorrogado para Dez/29 (originalmente Dez/24, prorrogado em 60 meses via Assembleia dez/24-jan/25). A operação prevê amortização extraordinária obrigatória (Cash Sweep) sempre que houver venda direta de uma das unidades do empreendimento: o VMD (o maior entre R$ 500 mil ou 85% do preço de venda) é direcionado à amortização extraordinária do saldo devedor, respeitado o percentual mínimo de amortização ordinária obrigatória de cada semestre, conforme cronograma de Saldo Devedor Máximo.",
            "Covenants monitorados: Fluxo Mínimo da Conta Vinculada e Valor Mínimo do Fundo de Reserva.",
        ],
        'highlights': [
            "A amortização do mês foi de R$ 691 Mil.",
            "No mês de Jul/26 tivemos 1 venda por R$ 600.000 (R$ 20 mil/m²).",
            "Amortização acumulada de R$ 19,4 MM, sendo R$ 5,7 MM de principal e R$ 13,7 MM de correção monetária, atendendo ao saldo devedor máximo definido para Jun/27 (R$ 28,5 MM); sendo o próximo definido em Dez/27 (R$ 24,4 MM).",
            "Dos valores a receber referente as vendas definitivas temos uma previsão de amortização futura de R$ 2,6 MM.",
        ],
    },
    'Localfrio': {
        'sobre_operacao': [
            "Operação lastreada em créditos imobiliários oriundos de Contratos de Locação (sale-leaseback) firmados entre a Localfrio Administração de Bens Ltda.  e a Localfrio S.A. Armazéns Gerais Frigoríficos, tendo como lastro 2 imóveis de armazenagem frigorífica (1 em São Paulo/SP e 1 em Itajaí/SC). A operação conta com AFI dos imóveis, AF das quotas da Cedente, CF da conta vinculada e Fiança dos fiadores/acionistas.",
            "Emitida em Nov/19, no valor de R$100,0 milhões (R$80,0 MM Sênior – 54ª série + R$20,0 MM Subordinada – 55ª série), remuneração IPCA + 6,00% a.a. (Sênior), com amortização mensal conforme cronograma (vencimento final Dez/31). A operação conta com Fundo de Reserva (originalmente 5 PMTs, reduzido para 3 PMTs em 2024) e Fundo de Despesas como colchão de liquidez.",
            "Os covenants financeiros monitorados desde 2022 são: Dívida Líquida/EBITDA, com trajetória decrescente até ≤ 3,0x em 5 anos.",
        ],
        'highlights': [
            "O IC gerencial do mês foi de 1,16x.",
        ],
    },
    'WT Log': {
        'sobre_operacao': [
            "Operação lastreada em Créditos Imobiliários representados por CCI, oriundos de Notas Comerciais emitidas pela FDR Independência Desenvolvimento Imobiliário Ltda., tendo como lastro a fração ideal de 25% de 2 imóveis de armazenagem/logística em Franco da Rocha/SP. A operação conta com AFI dos imóveis, AF das quotas da PMG Desenvolvimento, CF de recebíveis de locação e Aval dos Avalistas.",
            "Emitida em Jan/23, no valor de R$30,0 milhões, remuneração IPCA + 8,14% a.a., com amortização mensal conforme cronograma (vencimento final Dez/35). A operação conta com Fundo de Reserva (mínimo de 3 PMTs) e Fundo de Despesas (mínimo 12 meses de despesas recorrentes) como colchão de liquidez.",
            "Os covenants financeiros monitorados são: LTV máximo de 50% e Índice de Cobertura mínimo de 1,25x.",
        ],
        'highlights': [
            "O IC apurado no mês foi de 1,76x, acima do mínimo de 1,25x.",
        ],
    },
    'BR Prop': {
        'sobre_operacao': [
            "Operação lastreada em créditos imobiliários oriundos da 18ª emissão de debêntures da BR Properties S.A., tendo como lastro dos CRI. Em 2025/2026 a garantia foi integralmente substituída por 5 módulos do Condomínio de Galpões BRPR Cajamar I, com os recebíveis de locação de Yusen Logistics, Girotrade e JSL.",
            "Emitida em Ago/23, no valor original de R$80,0 milhões, majorado para R$90,0 milhões via exercício parcial da opção de lote adicional, remuneração 100% CDI + 2,00% a.a., com pagamento mensal de juros sem carência (vencimento final Ago/31).",
            "Os covenants financeiros monitorados são: LTV máximo de 50%; índice de cobertura ≥1,20x e dívida líquida/propriedades para investimento <50%.",
        ],
        'highlights': [
            "O IC verificado no mês foi de 1,52x, acima do mínimo de 1,20x.",
        ],
    },
    'Residencial Jardins': {
        # ponto 2 da 35ª rodada -- texto reenviado pelo usuário depois do resto da rodada
        # já ter sido publicado.
        'sobre_operacao': [
            "Operação lastreada em debêntures simples, com garantia real, série única, da Promontoria Imóveis 5 S.A., representadas por CCI. Garantias: alienação fiduciária de ações da Devedora (Fiduciantes: FIP Multiapartamentos 1 + Promontoria Imóveis 3), alienação fiduciária de 5 imóveis residenciais individualmente (Next Haddock, Next Paulista, Next França, Onze 22 e Terraço) e cessão fiduciária de recebíveis (aluguéis e vendas dos imóveis).",
            "Emitida em 22/09/2022, no valor de R$58.420.000. Amortização por Saldo Devedor Máximo em marcos semestrais. Conta com Fundo de Reserva e Fundo de Despesas.",
            "Os covenants financeiros monitorados são: índice de cobertura > 1,25x, LTV < 60% e Saldo Devedor Máximo.",
        ],
        'highlights': [
            "O ICSD médio apurado no mês de Jul/26 foi de 2,07x, acima do mínimo de 1,25x.",
            "Portfólio 100% locado:<br>➢ Terraço OF – 100% locado para a Viva<br>➢ Next Paulista – 100% locado para a Viva<br>➢ Next Franca – 100% locado para a Viva<br>➢ Next Haddock – 100% locado para a Viva<br>➢ Onze22 – 100% locado para a Viva",
            "Venda escriturada no mês: Onze22 – 1 unidade.",
            "Fundo de Reserva foi recomposto após o fechamento de Jul/26.",
        ],
    },
    'Residencial Itaim': {
        # ponto 2 da 36ª rodada -- texto reenviado pelo usuário depois do resto da rodada
        # já publicado.
        'sobre_operacao': [
            "Operação lastreada em debêntures simples, com garantia real, série única, da Promontoria Imóveis 4 S.A., representadas por CCI. Garantias: alienação fiduciária de ações da Devedora (Fiduciantes: FIP Multiapartamentos 1 + Promontoria Imóveis 3), alienação fiduciária de imóveis (70 unidades autônomas do Edifício Residencial Üpper Itaim Bibi, Rua João Cachoeira nº 1.577, Vila Nova Conceição/SP) e cessão fiduciária de recebíveis (aluguéis e vendas).",
            "Emitida em 11/12/2020, no valor de R$33.611.000,00, vencimento em 21/12/2026. Conta com Fundo de Reserva e Fundo de Despesas.",
            "Covenants/mecanismos monitorados: LTV < 60% e ICSD > 1,3x.",
        ],
        'highlights': [
            "O IC apurado no mês de Jul/26 foi de 2,34x, acima do mínimo de 1,30x.",
            "Ocupação atual do portfólio está em 100%.",
            "Fundo de reserva foi recomposto após o fechamento de Jul/26.",
        ],
    },
    'MSB Axis': {
        # 37ª rodada, pontos 1/2.
        'highlights': [
            "No mês o aporte na SPE pelos SCPistas foi no valor de R$ 2,0MM, além da receita do empreendimento no valor de R$ 533.305.",
            "O IC apurado no mês foi de 1,30x, considerando aportes adicionais da MSB de R$ 43,7MM para suprir a exposição de caixa do projeto.",
        ],
        'sobre_operacao': [
            "Emissão de nota comercial no montante de R$ 95,0 MM, devida pela MSB Valência Emp. Imob. Ltda, para o desenvolvimento de empreendimento residencial composto por duas torres: Axis (60 unidades de aprox. 133 m²) e Sync (123 studios de aprox. 31 m²), no Campo Belo.",
            "Integralização inicial de R$ 48,4 MM, destinada à quitação da permuta da Devedora com a Brio. Integralizações/liberações posteriores para a Devedora conforme necessidade/evolução da obra.",
            "Pagamento de prêmio inicial ao investidor de R$ 1,9 MM (2,0% do volume emitido).",
            "Covenants: (i) índice de cobertura (razão entre VPL do empreendimento e saldo devedor dos CRI) > 1,30x; (ii) proporção estrutura de capital (razão entre equity aportado e exposição de caixa) > 20%.",
            "Aprovado em Fev/26 a obrigação de aportes mensais de equity, no valor de R$ 2,0 MM cada, pari passu com liberações dos CRI, de Nov/25 até Out/26.",
        ],
    },
    'MSB Triu': {
        # 42ª rodada, ponto 2 e 3 -- mesmo padrão da MSB Axis (operação irmã, mesmo
        # incorporador/estrutura, no Campo Belo).
        'highlights': [
            "Durante o mês foi amortizado R$ 1,7MM.",
            "Não houve vendas no mês. Saldo em carteira para repasse de R$ 5,2MM.",
        ],
        'sobre_operacao': [
            "Emissão de nota comercial no montante de R$ 40,0 MM, devida pela SPE Barcelona Emp. Imob. Ltda, para o desenvolvimento de empreendimento residencial, com 96 unidades de aprox. 71 m², no Campo Belo.",
            "Integralização inicial de R$ 25,0 MM, seguida por mais duas integralizações (em Dez/24 e Jul/25) de aprox. R$ 5,0 MM cada. Liberações para a Devedora conforme necessidade/evolução da obra.",
            "Pagamento de prêmio inicial ao investidor de R$ 1,0 MM (2,5% do volume emitido).",
            "Emissão do Habite-se em Abr/26 (2 meses após a previsão inicial).",
            "Aumento de 50 bps na remuneração dos CRI a partir de Dez/25.",
        ],
    },
    'MSB Edson': {
        # 43ª rodada, ponto 6 -- operação vencida em 15/05/2026 (ver 'Data de Vencimento'
        # na aba MSB Edson), nova operação em estruturação pra substituir/rolar essa.
        'highlights': [
            "Operação vencida desde 15/05/2026.",
            "Estruturação da nova operação em andamento.",
        ],
    },
    'Alianza GRU e Mauá': {
        # 44ª rodada -- texto ditado pelo usuário (pontos 3 e 4), reenviado por completo depois
        # que o texto original veio cortado no meio da frase na 1ª tentativa (covenant de ICSD).
        # O usuário confirmou explicitamente (msg seguinte) que o bullet de highlight sobre o
        # laudo de avaliação, que veio DUPLICADO/cortado na mensagem original ("Atualização do
        # laudo de avaliação, com aumento do" sem completar, repetido logo depois já completo
        # com os valores), pode ficar só na versão completa -- "não precisa mexer em nada aqui
        # ainda [...] esses pontos vão ser atualizados no futuro com as infos de agosto".
        'sobre_operacao': [
            "Operação lastreada em créditos imobiliários oriundos da aquisição, pelo Alianza Urban Hub Renda FII, de dois ativos localizados em Guarulhos/SP e em Mauá/SP. A operação conta com a CF dos recebíveis de locação e AFI de ambos ativos.",
            "Compartilhamento de Garantias entre o CRI Guarulhos (435ª Série) e o CRI Mauá (447ª Série), com mecanismo de sobejo cruzado, excedentes da excussão de uma garantia redirecionados à outra, e Fundo de Reserva com base dinâmica de 3 parcelas futuras de serviço da dívida.",
            "Os covenants financeiros monitorados são: ICSD ≥ 1,30x (recebíveis de locação / serviço mensal dos CRI), apurado mensalmente; e LTV ≤ 60%, verificado com laudo anual.",
        ],
        'highlights': [
            "O IC foi de 1,36x na visão consolidada (Mauá + GRU), acima do mínimo de 1,30x.<br>✓ Visão Segregada: Mauá – 1,13x | GRU – 1,75x.",
            "No mês de Jul/26 ocorreu o reajuste do valor de aluguel do inquilino AGI para R$ 331.514 (R$ 24,77/m²).",
            "No mês de Jul/26 ocorreu o reajuste do valor de aluguel do inquilino Platinum Log para R$ 104.856 (R$ 29,80/m²).",
            "Atualização do laudo de avaliação, com aumento do valor do imóvel de R$ 81,7 MM (R$ 3.870/m²) para R$ 88,6 MM (R$ 4.201/m²).",
        ],
    },
}

# ---------- Alianza GRU e Mauá: consolidação de 2 séries numa única operação (44ª rodada) ----------
# Pedido do usuário: "Alianza GRU" e "Alianza Mauá" compartilham garantias/cascata/Fundo de
# Reserva (ver mecanismo de sobejo cruzado em MANUAL_CONTENT['Alianza GRU e Mauá']
# ['sobre_operacao']) -- na prática são uma operação só, então em vez de 2 abas separadas no
# portal (como o loop genérico faria por padrão), as 2 são excluídas de EXCLUDED_OPERATIONS
# (ver acima) e montadas aqui, à mão, numa única entrada 'Alianza GRU e Mauá'. Sempre GRU
# primeiro, Mauá depois nas tabelas comparativas (ordem usada pelo usuário no print de
# referência de Características).

def parse_alianza_ic_historico():
    """Histórico mensal alinhado de IC Mauá/IC GRU/IC Total (item 10). A aba 'Alianza - Fluxo'
    tem 3 blocos de colunas em paralelo -- Consolidado (D:K), Alianza Mauá (N:AC) e Alianza
    Guarulhos (AF:AU) -- CADA UM com sua PRÓPRIA coluna de Data, porque as 2 séries têm
    cadências de pagamento diferentes (Mauá emitida Mar/22, GRU emitida Jan/22 -- as linhas não
    estão alinhadas por data entre os blocos). Agrupa cada bloco pelo (ano,mês) da SUA PRÓPRIA
    coluna de Data e alinha os 3 por mês-calendário -- único jeito de comparar lado a lado.
    Verificado batendo exatamente contra os 6 meses do print de referência do usuário (fev-jul/
    26): Total 1,39/1,48/1,37/1,50/1,33/1,36x; Mauá 1,09/1,13/1,03/1,19/1,04/1,13x; GRU 1,89/
    2,13/1,93/2,02/1,84/1,75x."""
    if 'Alianza - Fluxo' not in wb.sheetnames:
        return []
    ws = wb['Alianza - Fluxo']
    def cidx(letter):
        return column_index_from_string(letter)
    def group_by_month(data_col, val_col):
        buckets = {}
        dc, vc = cidx(data_col), cidx(val_col)
        for r in range(2, ws.max_row + 1):
            d = ws.cell(row=r, column=dc).value
            if not isinstance(d, (datetime, date)):
                continue
            v = ws.cell(row=r, column=vc).value
            if isinstance(v, (int, float)):
                buckets[(d.year, d.month)] = v
        return buckets
    total = group_by_month('D', 'H')
    ic_min = group_by_month('D', 'I')
    maua = group_by_month('N', 'Z')
    gru = group_by_month('AF', 'AR')
    months = sorted(set(total) | set(maua) | set(gru))
    out = []
    for (y, m) in months:
        key = (y, m)
        rec = {'data': f"{y:04d}-{m:02d}-01"}
        if key in total: rec['ic_total'] = round(total[key], 6)
        if key in maua: rec['ic_maua'] = round(maua[key], 6)
        if key in gru: rec['ic_gru'] = round(gru[key], 6)
        if key in ic_min: rec['ic_minimo'] = round(ic_min[key], 6)
        if 'ic_total' in rec or 'ic_maua' in rec or 'ic_gru' in rec:
            out.append(rec)
    return out

def parse_alianza_ic_historico_realizado():
    """Mesmo motivo do cutoff_date em derive_ltv_atual (MSB Triu, ver nota lá): a aba de fluxo
    já vem com a série INTEIRA desenhada até o vencimento (2032), mas só o IC é apurado mês a
    mês com base no aluguel de fato recebido -- além do mês de referência (AS_OF, Jul/26) os 3
    campos (ic_total/ic_maua/ic_gru) caem pra 0 (sem projeção de IC futura nessa aba). Corta em
    AS_OF pra não misturar meses "realizados" com uma cauda de zeros no gráfico/covenant."""
    hist = parse_alianza_ic_historico()
    cutoff = to_jsonable(as_of) if 'as_of' in globals() and as_of is not None else None
    if cutoff is None:
        return hist
    return [r for r in hist if r['data'] <= cutoff]

def parse_alianza_juros_amortizacao_consolidado():
    """Juros/Amortização consolidados (Mauá + GRU somados) pra tabela de amortização mensal
    (46ª rodada, "alianza é um exemplo [...] tem que ver a visão consolidado dos dois igual já
    tinhamos ajustado anteriormente" -- mesmo espírito do item 10/parse_alianza_ic_historico,
    aplicado agora à tabela de fluxo). O bloco Consolidado (D:K) de 'Alianza - Fluxo' NÃO tem
    Juros/Amortização (só existem nos blocos por série, Mauá N:AC e GRU AF:AU) -- por isso
    esses 2 campos ficavam de fora da tabela depois do corte de colunas da 45ª/46ª rodada.

    Cada bloco por série tem Juros/Amortização em DOSE dupla (ex. Mauá: R/S/T/U em TAXA --
    conferido R+S+T=U -- e V/W/X no MESMO período em R$ -- conferido V+W=X). Usa a dupla em
    R$ (a única que dá pra somar Mauá+GRU com sentido -- taxa não soma entre 2 séries com
    saldos diferentes) e agrupa por (ano,mês) da PRÓPRIA coluna de Data de cada bloco (mesma
    técnica de parse_alianza_ic_historico, já que as 2 séries têm cadências diferentes).
    Chaves de saída ('juros_rs'/'amortizacao_rs') propositalmente DIFERENTES de 'juros'/
    'amortizacao' (que em todo o resto do app guardam a versão em taxa, não em R$) -- ver
    FLUXO_COLS no template, essas 2 colunas extras só aparecem pra operações que de fato têm
    esse dado (só a Alianza, por ora)."""
    if 'Alianza - Fluxo' not in wb.sheetnames:
        return []
    ws = wb['Alianza - Fluxo']
    def cidx(letter):
        return column_index_from_string(letter)
    def group_by_month(data_col, val_col):
        buckets = {}
        dc, vc = cidx(data_col), cidx(val_col)
        for r in range(2, ws.max_row + 1):
            d = ws.cell(row=r, column=dc).value
            if not isinstance(d, (datetime, date)):
                continue
            v = ws.cell(row=r, column=vc).value
            if isinstance(v, (int, float)):
                buckets[(d.year, d.month)] = buckets.get((d.year, d.month), 0) + v
        return buckets
    juros_maua = group_by_month('N', 'W')
    amort_maua = group_by_month('N', 'V')
    juros_gru = group_by_month('AF', 'AO')
    amort_gru = group_by_month('AF', 'AN')
    # TAI (correção da mesma rodada -- "falta a tai tbm"): não dá pra somar como Juros/
    # Amortização (é taxa, não R$), então traz as 2 séries por torre separadas (TAI Mauá/TAI
    # GRU) em vez de uma única "TAI" que precisaria de uma média ponderada não verificada.
    tai_maua = group_by_month('N', 'AA')
    tai_gru = group_by_month('AF', 'AS')
    months = sorted(set(juros_maua) | set(amort_maua) | set(juros_gru) | set(amort_gru) | set(tai_maua) | set(tai_gru))
    # SEM corte em AS_OF aqui (diferente do IC/LTV): Juros/Amortização/TAI por série já vêm
    # 100% projetados até o vencimento (2032), igual Saldo Devedor/PMT do bloco Consolidado --
    # cortar em AS_OF deixava a tabela com Saldo Devedor/PMT indo até 2032 mas Juros/
    # Amortização parando em Jul/26, an inconsistência real reportada pelo usuário ("não tem
    # valores de juros e amortização até o final").
    out = []
    for (y, m) in months:
        data_str = f"{y:04d}-{m:02d}-01"
        key = (y, m)
        jr = (juros_maua.get(key, 0) or 0) + (juros_gru.get(key, 0) or 0)
        ar = (amort_maua.get(key, 0) or 0) + (amort_gru.get(key, 0) or 0)
        tm = tai_maua.get(key)
        tg = tai_gru.get(key)
        if jr or ar or tm is not None or tg is not None:
            rec = {'data': data_str, 'juros_rs': round(jr, 2), 'amortizacao_rs': round(ar, 2)}
            if tm is not None: rec['tai_maua'] = round(tm, 6)
            if tg is not None: rec['tai_gru'] = round(tg, 6)
            out.append(rec)
    return out

def build_alianza_locacao():
    """Item 9 -- 'Informação Locações', 2 grupos (Mauá primeiro, GRU depois -- mesma ordem do
    print de referência do usuário) + 1 total por grupo, SEM total geral no fim (mesmo layout
    do print). Fontes:
    - 'Alianza Mauá': tabela única (linhas 5-8, total pré-calculado na linha 10). Correção
      pontual: as colunas 'Próx. Reajuste' de AGI Log/LF Armazenagem vêm TROCADAS entre si na
      planilha bruta (AGI->ago/26, LF->jul/27) -- contradiz o próprio highlight do usuário
      ("reajuste do AGI ocorreu em jul/26", logo o PRÓXIMO reajuste é jul/27, não ago/26) e o
      print de referência enviado (AGI->jul/27, LF->ago/26); usa aqui os valores corrigidos
      (AGI->Jul/27, LF->Ago/26), os outros campos batem 100% com a aba ao vivo.
    - 'Alianza GRU': CORREÇÃO PÓS-PUBLICAÇÃO (45ª rodada, ponto extra) -- a versão anterior
      usava a tabela "Informações de Locação - Atualizado" (linhas 16-22 da aba), lendo isso
      como o dado mais recente/correto. O usuário apontou o oposto: "esse acompanhamento das
      locações está com informações erradas [...] o que vc colocou no portal já é uma
      atualização que vai vir mais pra frente" -- ou seja, a tabela "Atualizado" da aba já
      reflete uma troca de locatários (saída de Évidência Textil, entrada de Expak/Apetito
      Foods, reajuste do Platinum Log pra R$29,80/m²) que ainda NÃO se aplica no mês de
      referência do portal (Jul/26); o dado certo pra Jul/26 é a 1ª tabela ("Informações de
      Locação", linhas 5-9), a mesma que aparece no print de referência do usuário. Volta a
      usar essa 1ª tabela, com os valores EXATOS do print (Platinum Log a R$27,96/m² -- o
      valor pré-reajuste -- e Mult Bev com próx. reajuste Dez/27; a aba ao vivo tem esses 2
      campos já atualizados pra além de Jul/26, então usa o print como fonte nesses 2 pontos
      pontuais, igual à correção já feita pro AGI/LF Log da Mauá acima). Évidência Textil
      aparece no print já como "Vago" (sem valor de aluguel recebido na tabela viva desse
      período), não como locatário nomeado."""
    # nota: locacoesGalpaoTableHtml() (template) lê r.galpao pra 1ª coluna das linhas normais
    # (r.label só é usado nas linhas de total/subtotal) -- por isso as linhas de locatário
    # abaixo usam a chave 'galpao' (o rótulo da coluna em si, "Locatário", vem de row_label).
    gru_area_total = 21161.41
    rows = [
        {'galpao': 'AGI Log', 'area': 13383.01, 'pct_ocupacao': 13383.01/27468.43,
         'valor_contratado': 331514.21, 'valor_pago': 331514.21, 'valor_m2': 24.771274175241594,
         'reajuste': 'Jul/27'},
        {'galpao': 'LF Armazenagem', 'area': 10243.74, 'pct_ocupacao': 10243.74/27468.43,
         'valor_contratado': 226629.89, 'valor_pago': 226629.89, 'valor_m2': 22.12374484319204,
         'reajuste': 'Ago/26'},
        {'galpao': 'CIV Center', 'area': 1721, 'pct_ocupacao': 1721/27468.43,
         'valor_contratado': 32085.3, 'valor_pago': 32085.3, 'valor_m2': 18.643404997094713,
         'reajuste': 'Mar/27'},
        {'galpao': 'Vago', 'area': 2120.68, 'pct_ocupacao': 2120.68/27468.43,
         'valor_contratado': None, 'valor_pago': None, 'valor_m2': None, 'reajuste': None},
        {'_grouptotal': True, 'label': 'Total Mauá', 'area': 27468.43,
         'pct_ocupacao': (27468.43-2120.68)/27468.43,
         'valor_contratado': 590229.40, 'valor_pago': 590229.40, 'valor_m2': 23.28527778599679},
        {'galpao': 'Mercearia Chama', 'area': 10549.18, 'pct_ocupacao': 10549.18/gru_area_total,
         'valor_contratado': 323002.01, 'valor_pago': 323002.01, 'valor_m2': 30.618684106252807,
         'reajuste': 'Mai/27'},
        {'galpao': 'Mult Bev Distribuição', 'area': 5275.0, 'pct_ocupacao': 5275.0/gru_area_total,
         'valor_contratado': 144130.37, 'valor_pago': 144130.37, 'valor_m2': 27.32329289099526,
         'reajuste': 'Dez/27'},
        {'galpao': 'Platinum Log', 'area': 3581.0, 'pct_ocupacao': 3581.0/gru_area_total,
         'valor_contratado': 104856.7, 'valor_pago': 104856.7, 'valor_m2': 27.96,
         'reajuste': 'Jul/27'},
        {'galpao': 'Vago', 'area': 1756.23, 'pct_ocupacao': 1756.23/gru_area_total,
         'valor_contratado': None, 'valor_pago': None, 'valor_m2': None, 'reajuste': None},
        {'_grouptotal': True, 'label': 'Total GRU', 'area': gru_area_total,
         'pct_ocupacao': (gru_area_total-1756.23)/gru_area_total,
         'valor_contratado': 571989.08, 'valor_pago': 571989.08, 'valor_m2': 29.57},
    ]
    return {'row_label': 'Locatário', 'rows': rows, 'total': None}

# Item 6 -- "Características da Operação", 2 colunas GRU/Mauá. Estrutura igual ao print de
# referência do usuário (mesma tabela visual de ATIVO_COMPARE_BY_OP/.ativo-compare-table, ver
# caracteristicasCompareHtml no template), mas com valores REAIS da planilha ao vivo no lugar
# dos valores de exemplo do print (Securitizadora/AF "Opea | Oliveira Trust" no print é
# claramente um placeholder de template -- as 2 abas mostram "Riza Sec"/"Vortx" pras 2 séries;
# Data de Emissão|Vencimento e Lock-up também vêm como um único valor compartilhado no print,
# mas na aba ao vivo cada série tem sua própria data -- usa os valores reais de cada uma).
# LTV/Duration ficam DE FORA dessa tabela de propósito: o LTV "solo" de cada série (Mauá
# 67,9%, GRU 37,7%) não reflete o LTV de verdade da operação, que é CONSOLIDADO por causa do
# compartilhamento de garantias (52,5%, já mostrado nos cards/quickstats) -- misturar os 2
# aqui confundiria mais do que ajudaria.
ALIANZA_CARACTERISTICAS_COMPARE = [
    {'label': 'GRU', 'securitizadora_af': 'Riza Sec | Vortx',
     'emissao_serie_cetip': '4ºE | 435ºS | 22A0253223',
     'volume_emissao': 'R$ 29.500.000', 'volume_integralizado': 'R$ 29.500.000',
     'saldo_devedor_pct': 'R$ 33.381.301 (100%)', 'subordinacao': 'Não há',
     'data_emissao_vencimento': 'Jan/22 | Jan/32', 'remuneracao': 'IPCA + 7,20%',
     'juros_amortizacao': 'Mensal | Mensal', 'lockup': 'Jan/26',
     'multa': 'Fluxo descontado pela taxa de 5%'},
    {'label': 'Mauá', 'securitizadora_af': 'Riza Sec | Vortx',
     'emissao_serie_cetip': '4ºE | 447ºS | 22C0050625',
     'volume_emissao': 'R$ 50.500.000', 'volume_integralizado': 'R$ 50.500.000',
     'saldo_devedor_pct': 'R$ 56.707.260 (100%)', 'subordinacao': 'Não há',
     'data_emissao_vencimento': 'Mar/22 | Fev/32', 'remuneracao': 'IPCA + 7,20%',
     'juros_amortizacao': 'Mensal | Mensal', 'lockup': 'Mar/26',
     'multa': 'Fluxo descontado pela taxa de 5%'},
]
ALIANZA_CARACTERISTICAS_FIELDS = [
    ['Securitizadora | AF', 'securitizadora_af'],
    ['Emissão | Série | Cód. Cetip', 'emissao_serie_cetip'],
    ['Volume Emissão', 'volume_emissao'],
    # 'Volume Integralizado' removida (correção pós-publicação, 45ª rodada, ponto 2 -- usuário
    # circulou essa linha de vermelho no exemplo e pediu pra tirar; o valor é idêntico ao de
    # 'Volume Emissão' nas 2 séries, então era só redundância).
    ['Saldo Devedor Atualizado (% do CRI)', 'saldo_devedor_pct'],
    ['Subordinação', 'subordinacao'],
    ['Data de Emissão | Vencimento', 'data_emissao_vencimento'],
    ['Remuneração', 'remuneracao'],
    ['Juros | Amortização', 'juros_amortizacao'],
    ['Lock-up', 'lockup'],
    ['Multa', 'multa'],
]

# Item 8 -- "Garantias", 2 ativos (Mauá/Guarulhos), valores EXATOS do anexo enviado pelo
# usuário ("estou te enviando em anexo as informações que precisam ser cadastradas"), não da
# aba ao vivo: o ABL Total do anexo (29.631 m² Mauá / 21.098 m² GRU) diverge um pouco do ABL
# bruto da aba (29.723 m² Mauá) -- uma busca na planilha inteira por um valor próximo de
# 29.631 não achou a origem exata da diferença (nem uma 2ª métrica de área nas abas-base), e a
# instrução do usuário pra essa seção específica ("como mostrar as informações") é o sinal
# mais forte de "use os valores como mandei", mesmo padrão de outras curadorias manuais deste
# portal quando o usuário sinaliza explicitamente os valores do anexo. Área do Terreno e
# Valor de Avaliação batem exatos com a aba ao vivo (54.126/63.257 m²; R$83,5MM/R$88,6MM).
ATIVO_COMPARE_ALIANZA = [
    {'label': 'Mauá', 'tipo_ativo': 'Galpão Logístico', 'proprietaria': 'Alianza Urban Hub FII',
     'ativo': 'Mauá', 'endereco': 'Av. Papa João XXIII, nº 3.580, Mauá/SP',
     'abl_total': '29.631 m²', 'abl_garantia': '29.631 m²', 'area_terreno': '54.126 m²',
     'valor_avaliacao': 'R$ 83.509.000 (R$ 2.809/m²)', 'atualizacao_laudo': 'Anual – todo mês de Junho'},
    {'label': 'Guarulhos', 'tipo_ativo': 'Galpão Logístico', 'proprietaria': 'Alianza Urban Hub FII',
     'ativo': 'Guarulhos', 'endereco': 'Estrada da Olaria, nº 600, Guarulhos/SP',
     'abl_total': '21.098 m²', 'abl_garantia': '21.098 m²', 'area_terreno': '63.257 m²',
     'valor_avaliacao': 'R$ 88.644.000 (R$ 4.201/m²)', 'atualizacao_laudo': 'Anual – todo mês de Junho'},
]
for _a in ATIVO_COMPARE_ALIANZA:
    _link = endereco_maps_link('Alianza GRU e Mauá', _a['endereco'])
    _a['endereco_html'] = f"<a href=\"{_link}\" target=\"_blank\" rel=\"noopener noreferrer\">{_a['endereco']} ↗</a>" if _link else _a['endereco']
ATIVO_COMPARE_BY_OP['Alianza GRU e Mauá'] = ATIVO_COMPARE_ALIANZA
ATIVO_COMPARE_FIELDS_BY_OP['Alianza GRU e Mauá'] = [
    ['Tipo de Ativo', 'tipo_ativo'],
    ['Proprietária', 'proprietaria'],
    ['Ativo', 'ativo'],
    ['Endereço', 'endereco_html'],
    ['ABL Total', 'abl_total'],
    ['ABL Garantia', 'abl_garantia'],
    ['Área do Terreno', 'area_terreno'],
    ['Valor de Avaliação', 'valor_avaliacao'],
    ['Atualização do Laudo', 'atualizacao_laudo'],
]

def build_alianza_covenants():
    """Itens de Acompanhamento consolidados. Cada aba-base, quando curada isoladamente por
    curate_covenants(), só produz 3 categorias canônicas de fato (LTV/IC/Fundo de Reserva --
    'AF Imóvel'/'Endosso do Seguro'/'Laudo de Avaliação'/'DFs Anuais' não batem nos padrões de
    covenant_bucket_of(), mesmo comportamento -- oculto por padrão -- de toda operação do
    portal; ver mine_obligation_items mais abaixo, que reaproveita esse texto bruto por uma via
    separada, específica pra Obrigações). LTV e IC saem SUBSTITUÍDOS por 1 item CONSOLIDADO cada
    (pedido explícito do usuário no
    ponto 6 duplicado: "no itens de acompanhamento, trazer a visão do IC consolidado, IC maua e
    IC GRU [...] no mesmo card, porque o que vale pra operação é o IC consolidado" -- visão
    segregada entra no campo 'obs' do próprio item, mesmo card). Fundo de Reserva continua 2x
    (1 por série -- valores exigido/atual realmente diferentes, não devem ser somados/
    escolhidos um só)."""
    base_maua = parse_base_sheet('Alianza Mauá')
    base_gru = parse_base_sheet('Alianza GRU')
    cur_maua = curate_covenants(base_maua['covenants'])
    cur_gru = curate_covenants(base_gru['covenants'])
    out = []
    ic_hist = parse_alianza_ic_historico_realizado()
    ic_atual = ic_hist[-1]['ic_total'] if ic_hist else None
    ic_ultima = find_covenant_ultima_atualizacao(base_maua['covenants'], 'ic')
    ic_proxima = None
    for c in base_maua['covenants']:
        if covenant_bucket_of(c.get('item', '')) == 'ic':
            ic_proxima = c.get('proxima_atualizacao'); break
    out.append({
        'item': 'Verificação do IC', '_categoria': 'ic', '_is_ratio': True,
        'exigido': 1.30, 'atual': round(ic_atual, 6) if ic_atual is not None else None,
        'status': 'Enquadrado' if (ic_atual is None or ic_atual >= 1.30) else 'Desenquadrado',
        'obs': 'Visão segregada: Mauá – 1,13x · GRU – 1,75x.',
        'ultima_atualizacao': ic_ultima, 'proxima_atualizacao': ic_proxima,
    })
    ltv_ultima = find_covenant_ultima_atualizacao(base_maua['covenants'], 'ltv')
    ltv_proxima = None
    for c in base_maua['covenants']:
        if covenant_bucket_of(c.get('item', '')) == 'ltv':
            ltv_proxima = c.get('proxima_atualizacao'); break
    out.append({
        'item': 'Verificação do LTV', '_categoria': 'ltv', '_is_pct': True, '_pct_decimals': 1,
        'exigido': 0.60, 'atual': 0.5252273895894931,
        'status': 'Enquadrado',
        'obs': 'LTV consolidado (garantias compartilhadas entre as 2 séries).',
        'ultima_atualizacao': ltv_ultima, 'proxima_atualizacao': ltv_proxima,
    })
    # 49ª rodada: sufixo da série Mauá encurtado de "(Mauá)" pra "(MA)", pareando com "(GRU)"
    # (3 letras) -- pedido do usuário ao revisar a Alianza: "aproveitando a interação diminuir
    # o texto de Mauá.. já tínhamos padronizado o texto geral para não ficar grande". Aplicado
    # em todo item por série desta operação (Fundo de Reserva e, mais abaixo, Laudo de
    # Avaliação), não só onde foi citado, pra manter os dois rótulos "(GRU)"/"(MA)" consistentes
    # entre si.
    SERIE_SUF = {'GRU': 'GRU', 'Mauá': 'MA'}
    for cur, suf in ((cur_gru, 'GRU'), (cur_maua, 'Mauá')):
        for c in cur:
            if c.get('_categoria') == 'reserva':
                e = dict(c); e['item'] = f"{e['item']} ({SERIE_SUF[suf]})"
                out.append(e)
    # 48ª rodada: mesma mineração de Obrigações (seguro/laudo/DF/cessão -- ver
    # obligation_bucket_of/mine_obligation_items) aplicada às 2 abas-base da Alianza, que o
    # docstring desta função já apontava como tendo esses itens ocultos ("'AF Imóvel'/'Endosso
    # do Seguro'/'Laudo de Avaliação'/'DFs Anuais' não batem nos padrões [...] oculto por
    # padrão"). Endosso do Seguro e DFs Anuais são a MESMA obrigação pras 2 séries (mesma
    # apólice/mesma demonstração cobre o consolidado) -- mostra 1 vez só quando o conteúdo é
    # idêntico entre GRU e Mauá; Laudo de Avaliação tem próxima data diferente por série, então
    # mostra as 2, com sufixo (mesmo padrão já usado acima pro Fundo de Reserva -- ver SERIE_SUF).
    mined_by_series = {'GRU': mine_obligation_items(base_gru['covenants']),
                        'Mauá': mine_obligation_items(base_maua['covenants'])}
    by_item = {}
    for suf, items in mined_by_series.items():
        for c in items:
            by_item.setdefault(c['item'], []).append((suf, c))
    for item, entries in by_item.items():
        if len(entries) == 2 and entries[0][1].get('proxima_atualizacao') == entries[1][1].get('proxima_atualizacao') \
                and entries[0][1].get('obs') == entries[1][1].get('obs'):
            out.append(dict(entries[0][1]))
        else:
            for suf, c in entries:
                e = dict(c); e['item'] = f"{e['item']} ({SERIE_SUF[suf]})"
                out.append(e)
    # 49ª rodada: "Aditamento Semestral da CF" (Cessão Fiduciária) pedido pelo usuário como item
    # de Obrigações -- não vem da tabela bruta "Itens de Acompanhamento" das abas GRU/Mauá (ela
    # não tem essa linha), só existia até aqui dentro do texto da sub-página "Ver obrigações"
    # (OBRIGACOES_PECUNIARIAS_BY_OP['Alianza GRU e Mauá'], item "Aditamento semestral da Cessão
    # Fiduciária", Cláusula 1.1.3 do Contrato de CF) -- mesmas datas reaproveitadas aqui pra
    # também virar uma linha rastreável na aba de Acompanhamento. _acomp_only=True pelo mesmo
    # motivo dos demais itens minerados (seguro/laudo/DFs, ver mine_obligation_items): fica só
    # na aba de Acompanhamento, sem virar um card a mais no painel de Itens de Acompanhamento da
    # página de detalhe (ajuste já pedido antes pelo usuário -- "já tínhamos ajustado esse ponto
    # para deixar tudo dentro de Obrigações").
    out.append({
        'item': 'Aditamento Semestral da Cessão Fiduciária', '_categoria': 'cessao',
        'exigido': 'OK', 'atual': 'OK', 'status': 'Enquadrado',
        'obs': 'Celebrado em 15/jun e 15/dez de cada ano, com registro em cartório em até 10 dias da celebração.',
        'ultima_atualizacao': '2026-06-15', 'proxima_atualizacao': '2026-12-15',
        '_acomp_only': True,
    })
    out.append({
        'item': 'Obrigações', '_categoria': 'manual',
        'obs': OBRIGACOES_PECUNIARIAS_BY_OP.get('Alianza GRU e Mauá', {}).get(
            'obs', 'Conteúdo ainda não cadastrado para esta operação.'),
        '_has_obrigacoes_subpage': True,
    })
    out.append({
        'item': 'Quórum de Assembleias', '_categoria': 'manual',
        'obs': QUORUM_ASSEMBLEIA_BY_OP.get('Alianza GRU e Mauá', {}).get(
            'obs', 'Conteúdo ainda não cadastrado para esta operação.'),
        '_has_quorum_subpage': True,
    })
    for entry in out:
        entry['_tipo'] = covenant_tipo(entry, 'Alianza GRU e Mauá')
    return out

def build_alianza_consolidado():
    """Monta a operação consolidada 'Alianza GRU e Mauá' inteira (todos os 12 itens do pedido
    do usuário), reaproveitando o parsing genérico de cada aba-base (parse_base_sheet) onde faz
    sentido e conteúdo curado à mão onde o dado não é uma simples soma/leitura (ver funções e
    comentários acima)."""
    base_maua = parse_base_sheet('Alianza Mauá')
    base_gru = parse_base_sheet('Alianza GRU')
    manual = MANUAL_CONTENT.get('Alianza GRU e Mauá', {})

    # ---- Fluxo consolidado (Consolidado, colunas D:K de 'Alianza - Fluxo') -- mesma função
    # genérica de sempre: como o bloco Consolidado é o 1º par de colunas "Data" da aba, e o 2º
    # par de "Data" (Mauá) marca onde o bloco Consolidado termina, parse_fluxo_sheet já recorta
    # exatamente esse intervalo sem precisar de nenhum código novo. Alimenta o quickstat de
    # LTV Atual, o gráfico "Acompanhamento LTV" (item 11) e a tabela de amortização
    # consolidada (item 12, colunas Quantidade/PU/Juros/Amortização/TAI ficam de fora porque o
    # bloco Consolidado não as tem -- só existem nos blocos por série).
    fluxo_recs = parse_fluxo_sheet('Alianza - Fluxo') or []
    # Juros/Amortização consolidados (46ª rodada, ver parse_alianza_juros_amortizacao_
    # consolidado acima) -- mescla por (ano,mês) no registro mensal do bloco Consolidado (que
    # já tem exatamente 1 registro por mês-calendário).
    juros_amort_by_month = {}
    for r in parse_alianza_juros_amortizacao_consolidado():
        y, m = r['data'][:4], r['data'][5:7]
        juros_amort_by_month[(y, m)] = r
    for rec in fluxo_recs:
        d = rec.get('data')
        if d:
            extra = juros_amort_by_month.get((d[:4], d[5:7]))
            if extra:
                rec['juros_rs'] = extra['juros_rs']
                rec['amortizacao_rs'] = extra['amortizacao_rs']
                if 'tai_maua' in extra: rec['tai_maua'] = extra['tai_maua']
                if 'tai_gru' in extra: rec['tai_gru'] = extra['tai_gru']
    fluxo_data = [{'sheet': 'Alianza - Fluxo (Consolidado)', 'records': fluxo_recs}] if fluxo_recs else []
    # cutoff_date=AS_OF (mesmo motivo da MSB Triu, ver nota em derive_ltv_atual): a série do
    # bloco Consolidado já vem 100% projetada até o vencimento (2032), então "o último registro
    # com ic+ltv" sem corte pegaria a cauda da projeção (perto do vencimento a garantia já foi
    # amortizada quase a zero) em vez do mês de fato mais recente (Jul/26).
    as_of_cutoff = to_jsonable(as_of)
    ltv_atual = derive_ltv_atual(fluxo_data, cutoff_date=as_of_cutoff)
    if ltv_atual is None and fluxo_recs:
        ltv_recs_tmp = [r for r in fluxo_recs if isinstance(r.get('ltv'), (int, float)) and r.get('data') and r['data'] <= as_of_cutoff]
        ltv_atual = ltv_recs_tmp[-1]['ltv'] if ltv_recs_tmp else None
    saldo_devedor = None
    sd_recs = [r for r in fluxo_recs if isinstance(r.get('saldo_devedor'), (int, float)) and r.get('data') and r['data'] <= as_of_cutoff]
    if sd_recs:
        saldo_devedor = sd_recs[-1]['saldo_devedor']

    # ---- Item 1: cards consolidados ----
    summary = {
        'securitizadora': 'Riza Sec', 'agente_fiduciario': 'Vortx',
        'serie': '435ª (GRU) / 447ª (Mauá)',
        'valor_emissao': 29500000 + 50500000,
        'saldo_devedor': saldo_devedor,
        # pct_maua (correção pós-publicação, 45ª rodada, ponto 4 -- "faltou colocar o % da
        # Mauá padrão em todas as operações"): mesma semântica usada em toda outra operação
        # (find_papel_value(...,'percentual maua','% maua') com fallback pra '% do CRI' —
        # ver build_summary/parse_base_sheet). As 2 séries próprias (GRU e Mauá) não têm coluna
        # "% Mauá" dedicada nas suas abas de papel, então cada uma cai no mesmo fallback: "%
        # do CRI" = 100% pras 2 (confirmado lendo direto a aba, find_papel_value(base_gru/maua
        # ['papel'], '% do cri') = 1 nas 2). Consolidado herda o mesmo 100%.
        'pct_maua': 1,
        'data_emissao': None,
        'data_vencimento': 'Jan/32 (GRU) · Fev/32 (Mauá)',
        'taxa_juros': 0.072,
        'indexador': 'IPCA',
        'concentracao': 'Logístico',
        'ltv_atual': ltv_atual if ltv_atual is not None else 0.5252273895894931,
        'duration': 4.1,
    }

    # ---- Item 2: Posição por Fundo segregada, 1 tabela só ----
    fund_positions = []
    for suf, key in (('GRU', 'Alianza GRU'), ('Mauá', 'Alianza Mauá')):
        for fp in FUND_POSITIONS_BY_OP.get(key, []):
            fp2 = dict(fp)
            fp2['tranche'] = f"{fp2.get('tranche') or ''} ({suf})".strip()
            fund_positions.append(fp2)
    fund_positions.sort(key=lambda r: r.get('saldo_curva_mm') or 0, reverse=True)

    covenants = build_alianza_covenants()

    ativo_info_garantias = (base_maua['garantias'] or []) + (base_gru['garantias'] or [])

    op = {
        'group': 'MCCI',
        'papel': None,
        'garantias': ativo_info_garantias,
        'covenants': covenants,
        'caracteristicas': [],
        'caracteristicas_compare': ALIANZA_CARACTERISTICAS_COMPARE,
        'caracteristicas_compare_fields': ALIANZA_CARACTERISTICAS_FIELDS,
        'sobre_operacao': manual.get('sobre_operacao', []),
        'highlights': manual.get('highlights', []),
        'locatarios': None,
        'ativo_info': [],
        'summary': {**summary, 'covenant_counts': covenant_status_counts(covenants), 'n_covenants': len(covenants)},
        'fluxo': fluxo_data,
        'indicadores': [],
        'fund_positions': fund_positions,
        'estoque_hist': None,
        'hotel_perf': None,
        'ativo_compare': ATIVO_COMPARE_BY_OP.get('Alianza GRU e Mauá'),
        'ativo_compare_fields': ATIVO_COMPARE_FIELDS_BY_OP.get('Alianza GRU e Mauá'),
        'locacoes_galpao': build_alianza_locacao(),
        'locacoes_modalidade': None,
        'covenant_calc': None,
        'locacao_perf': None,
        'estoque_por_ativo': None,
        'carteira_vendas_estoque': None,
        'carteira_detalhe': None,
        'ic_projected': None,
        'obra_evolucao': None,
        'integralizacoes': None,
        'unidades_detalhe': None,
        'obrigacoes_pecuniarias': OBRIGACOES_PECUNIARIAS_BY_OP.get('Alianza GRU e Mauá'),
        'quorum_assembleia': QUORUM_ASSEMBLEIA_BY_OP.get('Alianza GRU e Mauá'),
        'amort_ltv_flat': None,
        # campo extra (só usado por esta operação -- ver renderFluxoCharts no template):
        # item 10 (3-barras IC Mauá/GRU/Total). O chip extra "LTV Máximo" (ltv_max_ref) da 44ª
        # rodada foi removido na 45ª -- ver comentário no template, LTV voltou ao padrão-único
        # "LTV Atual" de toda outra operação.
        'ic_by_group': parse_alianza_ic_historico_realizado(),
    }
    return op

# ---------- Main ----------
result = {
    'meta': {},
    'groups': [],
    'operations': {},
}

# global meta from Resumo
ws = wb['Resumo']
resumo_rows = list(ws.iter_rows(min_row=1, max_row=10, values_only=True))
as_of = resumo_rows[3][0] if len(resumo_rows) > 3 else None
# Correção pós-publicação (8ª rodada, reorganização geral, ponto 3): a célula de referência da
# aba "Resumo" ainda está datada de agosto/2026, mas o conteúdo cadastrado nesse ciclo é de
# julho/2026 (confirmado pelo usuário: "eu sei que a planilha está com a data de agosto, mas
# informações que estou cadastrando são de julho") -- a planilha-fonte em si ainda não foi
# corrigida na origem. Override manual até a próxima planilha já vir com a data certa; MONTH_KEY
# é o identificador do snapshot mensal usado pelo seletor de mês no front-end (ver __PORTFOLIO_
# DATA_JSON__ / MONTHS no template).
AS_OF_OVERRIDE = date(2026, 7, 31)
MONTH_KEY = '2026-07'
as_of = AS_OF_OVERRIDE
premissa_cdi = None
for i,row in enumerate(resumo_rows):
    if row[0] and 'premissa cdi' in norm(row[0]):
        premissa_cdi = resumo_rows[i+1][0] if i+1 < len(resumo_rows) else None
result['meta'] = {
    'as_of_date': to_jsonable(as_of),
    'premissa_cdi': premissa_cdi,
    'source_file': 'Acompanhamento de Ativos_2026.08.xlsx',
}

for code, ops in base_ops_by_group:
    result['groups'].append({'code': code, 'operations': ops})
    for op in ops:
        if op == 'Alianza GRU e Mauá':
            # marcador inserido no lugar de 'Alianza Mauá'/'Alianza GRU' (ver EXCLUDED_
            # OPERATIONS/base_ops_by_group acima) -- monta a operação consolidada inteira
            # (todos os campos já no formato final) em vez do parsing genérico de 1 aba.
            result['operations'][op] = build_alianza_consolidado()
            continue
        base = parse_base_sheet(op)
        fluxo_names = find_fluxo(op)
        fluxo_data = []
        for fn in fluxo_names:
            recs = parse_fluxo_sheet(fn)
            if recs:
                fluxo_data.append({'sheet': fn, 'records': recs})

        indic_names = find_indicadores(op)
        indic_data = []
        for iname in indic_names:
            idata = parse_indicadores_sheet(iname)
            if idata and (idata['records'] or idata['preamble']):
                indic_data.append({'sheet': iname, **idata})
        if op in INDICADORES_HIDE:
            indic_data = []

        # último "IC Mínimo" conhecido no fluxo, usado como fallback do exigido na
        # curadoria de covenants quando a própria tabela de covenants não traz o valor
        ic_minimo_fallback = None
        for fd in fluxo_data:
            for r in reversed(fd['records']):
                if isinstance(r.get('ic_minimo'), (int,float)):
                    ic_minimo_fallback = r['ic_minimo']; break
            if ic_minimo_fallback is not None: break

        locatarios = build_locatarios_table(op)
        ativo_info = [build_ativo_info(a) for a in base['garantias']]
        ativo_info = [a for a in ativo_info if a]
        # apply_ativo_info_manual ANTES do link do Maps: pra operações cujo "endereço" só
        # existe no conteúdo curado à mão (ex.: BR Prop -- a aba bruta não tem uma linha de
        # endereço, o galpão de Cajamar veio inteiro de ATIVO_INFO_MANUAL), fazer o link
        # primeiro deixava a.get('endereco') vazio e o card ficava sem link nenhum, nem o
        # fallback de busca genérica -- fix geral, não específico da BR Prop.
        apply_ativo_info_manual(op, ativo_info)
        for a in ativo_info:
            if a.get('endereco') and not a.get('endereco_maps_url'):
                link = endereco_maps_link(op, a['endereco'])
                if link: a['endereco_maps_url'] = link

        manual = MANUAL_CONTENT.get(op, {})

        fund_positions = FUND_POSITIONS_BY_OP.get(op, [])

        ltv_atual_sync = derive_ltv_atual(fluxo_data) if op in LTV_ATUAL_SYNC_OPS else None
        if op in IC_ATUAL_SYNC_OPS:
            # ver nota em derive_ic_atual(): corta no mesmo período que o próprio covenant de
            # IC/ICSD já reconhece como o mais recente fechado, pra não pular um mês à frente
            # de uma linha de fluxo pré-calculada por fórmula mas ainda não oficial.
            ic_cutoff = find_covenant_ultima_atualizacao(base['covenants'], 'ic')
            ic_atual_sync = derive_ic_atual(fluxo_data, cutoff_date=ic_cutoff)
        else:
            ic_atual_sync = None

        # covenant_counts/health do card de resumo (chip "Enquadrada"/"Verificar"/etc no topo
        # da página, cor do "dot" na sidebar) precisa vir da mesma lista CURADA que aparece no
        # card "Itens de Acompanhamento" -- não da lista bruta da planilha. Antes usava
        # base['covenants'] (bruto), que inclui itens que nunca chegam a aparecer na tela
        # (ex. MSB Axis: "Comprovação de aporte", "Cópia de balancetes anuais", etc., alguns
        # com status "Verificar") -- o resultado era um chip de saúde que não batia com o que
        # os 3 cards efetivamente mostrados diziam (usuário viu status "Verificar"/"Sem
        # covenants" no topo enquanto os 3 itens do card só mostravam "Enquadrado"). Curando
        # a lista uma vez e reaproveitando pros dois usos resolve isso de forma genérica.
        covenants_curated = curate_covenants(base['covenants'], ic_minimo_fallback, op_name=op, ltv_atual_sync=ltv_atual_sync, ic_atual_sync=ic_atual_sync)

        result['operations'][op] = {
            'group': code,
            'papel': base['papel'],
            'garantias': base['garantias'],
            'covenants': covenants_curated,
            'caracteristicas': build_caracteristicas(base['papel'], fluxo_data, op_name=op, fund_positions=fund_positions),
            'sobre_operacao': manual.get('sobre_operacao', []),
            'highlights': manual.get('highlights', []),
            'locatarios': locatarios,
            'ativo_info': ativo_info,
            'summary': build_summary(base['papel'], covenants_curated, fluxo_data, cutoff_date=to_jsonable(as_of) if op in LTV_ATUAL_CUTOFF_OPS else None, op_name=op),
            'fluxo': fluxo_data,
            'indicadores': indic_data,
            'fund_positions': fund_positions,
            'estoque_hist': ESTOQUE_HIST_BY_OP.get(op),
            'hotel_perf': HOTEL_PERF_BY_OP.get(op),
            'ativo_compare': ATIVO_COMPARE_BY_OP.get(op),
            'ativo_compare_fields': ATIVO_COMPARE_FIELDS_BY_OP.get(op),
            'locacoes_galpao': LOCACOES_GALPAO_BY_OP.get(op),
            'locacoes_modalidade': LOCACOES_MODALIDADE_BY_OP.get(op),
            'covenant_calc': COVENANT_CALC_BY_OP.get(op),
            'locacao_perf': LOCACAO_PERF_BY_OP.get(op),
            'estoque_por_ativo': ESTOQUE_POR_ATIVO_BY_OP.get(op),
            'carteira_vendas_estoque': CARTEIRA_VENDAS_ESTOQUE_BY_OP.get(op),
            'carteira_detalhe': CARTEIRA_DETALHE_BY_OP.get(op),
            'ic_projected': IC_PROJECTED_BY_OP.get(op),
            'obra_evolucao': OBRA_EVOLUCAO_BY_OP.get(op),
            'integralizacoes': INTEGRALIZACOES_BY_OP.get(op),
            'unidades_detalhe': UNIDADES_DETALHE_BY_OP.get(op),
            'obrigacoes_pecuniarias': OBRIGACOES_PECUNIARIAS_BY_OP.get(op),
            'quorum_assembleia': QUORUM_ASSEMBLEIA_BY_OP.get(op),
            'amort_ltv_flat': AMORT_LTV_FLAT_BY_OP.get(op),
        }

# ---------- Documentos por operação (base pra chat de consulta) ----------
# extract_documents.py roda separado (só quando a pasta de documentos muda) e grava
# documents_data.json: {"<Operação>": [{"filename":..., "text":...}, ...]}.
# Aqui só fragmentamos (chunk) o texto já extraído e anexamos em cada operação.
def chunk_text(text, chunk_size=900, overlap=150):
    """Fragmenta em pedaços de ~chunk_size chars, tentando cortar em quebra de
    parágrafo/frase perto do limite, com sobreposição pra não perder contexto
    de fronteira entre chunks."""
    text = text.strip()
    if not text:
        return []
    chunks = []
    pos = 0
    n = len(text)
    while pos < n:
        end = min(pos + chunk_size, n)
        if end < n:
            # tenta cortar num parágrafo ou frase perto do fim do chunk
            cut = text.rfind('\n\n', pos, end)
            if cut == -1 or cut <= pos + chunk_size * 0.4:
                cut = text.rfind('. ', pos, end)
            if cut != -1 and cut > pos + chunk_size * 0.4:
                end = cut + 1
        chunk = text[pos:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        pos = max(end - overlap, pos + 1)
    return chunks

CPF_FORMATTED_RE = re.compile(r'\d{3}\.\d{3}\.\d{3}-\d{2}')
CPF_PLAIN_RE = re.compile(r'(?<!\d)\d{11}(?!\d)')

def redact_cpf(text):
    """Remove CPFs (documento de identificação de pessoa física, formatado ou
    em sequência de 11 dígitos) do texto antes de ele entrar na base do chat
    de documentos — são dados de terceiros (signatários), não relevantes
    para a análise da operação."""
    text = CPF_FORMATTED_RE.sub('[CPF removido]', text)
    text = CPF_PLAIN_RE.sub('[CPF removido]', text)
    return text

DOCUMENTS_DATA_PATH = '/tmp/work/documents_data.json'
documents_data = {}
documents_data_extracted_at = None
if os.path.exists(DOCUMENTS_DATA_PATH):
    with open(DOCUMENTS_DATA_PATH, 'r', encoding='utf-8') as f:
        documents_data = json.load(f)
    # Data da última extração (pedido do usuário, indiretamente: reclamou que o agente
    # "não traz resposta" sem saber que a pasta de documentos só é reprocessada manualmente
    # -- mostrar essa data no painel evita que alguém confunda "sem documentos novos aqui"
    # com "a pasta está vazia", quando na real é só uma foto desatualizada).
    documents_data_extracted_at = to_jsonable(datetime.fromtimestamp(os.path.getmtime(DOCUMENTS_DATA_PATH)))

# Obrigações identificadas em documentos (atas/aditamentos) -- pedido do usuário: "quero que
# a IA entenda quais foram as últimas atas, se os documentos foram editados, os prazos... tem
# alguma pendência?". Diferente de op.obrigacoes_pecuniarias (que vem de linhas fixas da
# planilha "Itens de Acompanhamento" -- seguro, laudo, DF, cessão -- itens RECORRENTES de
# monitoramento), isso aqui é extraído lendo o texto de atas/aditamentos: obrigações
# pontuais criadas por uma assembleia específica (ex.: "prazo de 30 dias pra aditar X"),
# cada uma citando o arquivo-fonte e o trecho exato. Hoje é uma leitura manual (feita ao
# processar os documentos, mesmo esforço de quando a pasta é reprocessada) -- não é extração
# automática por IA ainda, mas já cobre o caso de uso pedido (ata da Alianza de 16/07/2026:
# prazo de 30 dias pra cumprir o Anexo II, mas o Anexo II não está nos documentos indexados
# -- não dá pra confirmar cumprimento).
OBLIGATIONS_DATA_PATH = '/tmp/work/obligations_data.json'
obligations_data = {}
if os.path.exists(OBLIGATIONS_DATA_PATH):
    with open(OBLIGATIONS_DATA_PATH, 'r', encoding='utf-8') as f:
        obligations_data = json.load(f)

# Documentos da Operação -- checagem de completude vs. o que está na pasta (pedido do
# usuário, 45ª rodada: "você vai lá no termo de securitização, vê todos os documentos que
# compõem esse termo de securitização... verificar, pô, aqui na pasta eu vi que tá faltando
# o documento"). Igual a obligations_data.json, é uma leitura manual registrada em JSON --
# não é extração automática por IA ainda -- mas a arquitetura (este loop + o painel no
# front-end) é genérica: assim que uma operação tiver documents_meta.json preenchido (mesmo
# que seja adicionada depois, com mais pastas de documentos chegando), o painel "Documentos
# da Operação" aparece sozinho, sem precisar de nenhum código novo. Cada instrumento traz
# sua própria cadeia de aditamentos conhecida (número, data, se está ou não na pasta) --
# monta-se aqui, em Python, o resumo (versão mais recente disponível na pasta vs. a mais
# recente conhecida) e a lista de gaps, pro front-end só precisar renderizar.
DOCUMENTS_META_PATH = '/tmp/work/documents_meta.json'
documents_meta = {}
if os.path.exists(DOCUMENTS_META_PATH):
    with open(DOCUMENTS_META_PATH, 'r', encoding='utf-8') as f:
        documents_meta = json.load(f)


def build_doc_instrumentos(meta_entry):
    """Recebe a entrada de documents_meta.json de uma operação (ou None) e devolve a lista
    de instrumentos já com o resumo calculado (presente_na_pasta, versão mais recente na
    pasta vs. mais recente conhecida, gap em texto pronto pro front-end)."""
    if not meta_entry:
        return None
    out = []
    for instr in meta_entry.get('instrumentos', []):
        adits = instr.get('aditamentos_conhecidos', [])
        presentes = [a for a in adits if a.get('presente_na_pasta')]
        original_presente = bool(instr.get('original_presente_na_pasta'))
        tem_algo_na_pasta = bool(presentes) or original_presente
        mais_recente_conhecido = adits[-1]['numero'] if adits else None
        mais_recente_presente = presentes[-1] if presentes else None
        completo = original_presente and not any(not a.get('presente_na_pasta') for a in adits)
        faltando_nums = [a['numero'] for a in adits if not a.get('presente_na_pasta')]
        gap_parts = []
        if not original_presente:
            gap_parts.append('o instrumento original')
        if faltando_nums:
            nums_txt = ', '.join(f"{n}º" for n in faltando_nums)
            gap_parts.append(f"o(s) aditamento(s) {nums_txt}")
        gap_txt = ('Faltam na pasta: ' + ' e '.join(gap_parts) + '.') if gap_parts else None
        out.append({
            'tipo': instr.get('tipo'),
            'nome': instr.get('nome'),
            'nome_curto': instr.get('nome_curto'),
            'data_original': instr.get('data_original'),
            'original_presente_na_pasta': original_presente,
            'aditamentos_conhecidos': adits,
            'presente_na_pasta': tem_algo_na_pasta,
            'completo': completo,
            'versao_mais_recente_na_pasta': (
                f"{mais_recente_presente['numero']}º Aditamento" +
                (f" ({fmt_data_br(mais_recente_presente['data'])})" if mais_recente_presente.get('data') else " (s/ data confirmada)")
                if mais_recente_presente else ('Original' if original_presente else None)
            ),
            'mais_recente_conhecido_numero': mais_recente_conhecido,
            'gap': gap_txt,
            'nota': instr.get('nota'),
        })
    return {
        'instrumentos': out,
        'metodologia_nota': meta_entry.get('metodologia_nota'),
    }


def fmt_data_br(iso):
    if not iso:
        return None
    try:
        y, m, d = iso.split('-')
        return f"{d}/{m}/{y}"
    except Exception:
        return iso

# A pasta de documentos no computador do usuário nem sempre tem o mesmo nome da chave
# interna da operação no portal (ex.: a chave é "BR Prop", abreviada, mas a pasta real
# em Operações/ é "BR Properties", por extenso) -- extract_documents.py grava
# documents_data.json com o nome real da pasta, então precisa desse alias pra achar os
# documentos certos (34ª rodada). Ver também a lição geral sobre nome de pasta != nome
# da operação no portal (WT Log, 33ª rodada — lá o mismatch foi corrigido renomeando a
# pasta em vez de alias, porque a pasta real não tinha nem espaço).
DOCUMENTS_OP_ALIAS = {'BR Prop': 'BR Properties', 'Residencial Jardins': 'Residencial Jardins FL2',
                       'Residencial Itaim': 'Residencial Itaim FL2',
                       # 44ª rodada -- confirmado pelo usuário: a pasta real em Operações/ é
                       # "Alianza GRU e Maua" (sem acento no á final), diferente da chave
                       # "Alianza GRU e Mauá" usada no portal.
                       'Alianza GRU e Mauá': 'Alianza GRU e Maua'}

for op_name, op_data in result['operations'].items():
    docs = documents_data.get(DOCUMENTS_OP_ALIAS.get(op_name, op_name), [])
    chunks_out = []
    for doc in docs:
        clean = redact_cpf(doc['text'])
        for i, ch in enumerate(chunk_text(clean)):
            chunks_out.append({'filename': doc['filename'], 'chunk_idx': i, 'text': ch})
    op_data['doc_chunks'] = chunks_out
    op_data['doc_files'] = [d['filename'] for d in docs]
    op_data['doc_extracted_at'] = documents_data_extracted_at
    obrig_entry = obligations_data.get(DOCUMENTS_OP_ALIAS.get(op_name, op_name))
    op_data['doc_obligations_reviewed'] = bool(obrig_entry and obrig_entry.get('reviewed'))
    all_items = (obrig_entry or {}).get('items', [])
    # atual=true (da assembleia mais recente) vs atual=false (histórico/superado) -- pedido
    # explícito do usuário: "não faz sentido trazer uma obrigação identificada de uma ata
    # antiga... se uma ata aconteceu recentemente, essas obrigações antigas já foram
    # superadas". A separação já vem pronta de obligations_data.json (campo 'atual', decidido
    # na revisão manual de qual é a ata mais recente de cada operação) -- aqui só dividimos em
    # 2 listas pro front-end não precisar filtrar de novo em vários lugares.
    op_data['doc_obligations_current'] = [it for it in all_items if it.get('atual')]
    # Histórico em ordem cronológica DECRESCENTE (49ª rodada, pedido explícito do usuário: "faz
    # mais sentido começar pela ordem de Cronologia... 2024, 2023, 2022 e 2021" -- não fazia
    # sentido abrir o histórico pela ata mais ANTIGA). fonte_data vem em ISO (AAAA-MM-DD), então
    # ordena como string mesmo, decrescente; item sem fonte_data (raro) vai pro final.
    op_data['doc_obligations_historico'] = sorted(
        [it for it in all_items if not it.get('atual')],
        key=lambda it: it.get('fonte_data') or '',
        reverse=True,
    )
    op_data['doc_obligations_latest_ata_data'] = (obrig_entry or {}).get('latest_ata_data')
    op_data['doc_obligations_latest_ata_arquivo'] = (obrig_entry or {}).get('latest_ata_arquivo')
    # doc_obligations_nota_revisor removido da renderização (49ª rodada, pedido explícito do
    # usuário: "eu te falei para tirar esse aviso de todas as operações.. vc n ajustou em
    # todas" -- mesmo tratamento já dado ao metodologia_nota na 47ª rodada: o texto de
    # observacao_reviewer continua existindo aqui nos dados/JSON pra quem olhar o pipeline
    # diretamente, só não aparece mais na tela). Campo mantido no build_data.py (não removido)
    # só por retrocompatibilidade -- ver portal_template.html, renderDocObrigSubview: a variável
    # revisorNota/seu <div> foram removidos de lá.
    op_data['doc_obligations_nota_revisor'] = (obrig_entry or {}).get('observacao_reviewer')

    meta_entry = documents_meta.get(DOCUMENTS_OP_ALIAS.get(op_name, op_name))
    op_data['doc_instrumentos'] = build_doc_instrumentos(meta_entry)

    # Redundância pedida pelo usuário ("quero sempre que aconteça essa redundância de
    # informações para precaver que o agente consulte documentos de versões antigas, e acabe
    # tomando decisões erradas"): as obrigações ATUAIS (da ata mais recente) também entram na
    # aba Acompanhamento, num sub-bloco PRÓPRIO ("Via Assembleia", _tipo='obrigacao_assembleia' --
    # ver ACOMP_TABS no JS). Correção pós-publicação (pedido explícito: "eu quero que tenha uma
    # 'pasta' só com as obrigações via assembleia [...] acho que tudo junto pode acabar deixando
    # passar algo"): antes essas entravam misturadas em _tipo='obrigacao' (junto com
    # seguro/laudo/DF/cessão), só com uma tag "Via Assembleia" no texto -- o usuário achou
    # arriscado demais (fácil de passar batido no meio da lista); agora ficam num sub-bloco
    # totalmente segregado. _acomp_only=True (mesmo padrão dos itens minerados de seguro/laudo/
    # DF) -- não aparece no card "Itens de Acompanhamento" da página de detalhe (essa operação já
    # tem sua própria sub-página "Obrigações Identificadas em Documentos", acessível pelo chat),
    # só na aba Acompanhamento. Histórico (atual=False) NÃO entra aqui -- só na sub-página
    # dedicada -- pra não listar como "pendência ativa" algo que já foi superado por uma ata mais
    # nova.
    for it in op_data['doc_obligations_current']:
        obs_parts = [it['descricao']]
        obs_parts.append(
            f"Documento de cumprimento identificado na pasta: {it['documento_cumprimento']}."
            if it.get('documento_cumprimento')
            else "Nenhum documento de cumprimento identificado na pasta até o momento."
        )
        if it.get('nota'):
            obs_parts.append(it['nota'])
        fonte_data = it.get('fonte_data')
        # 'item' (pedido explícito: "trazer brevemente por um título qual é o conteúdo da
        # obrigação"): antes era só "Obrigação da Assembleia de DD/MM/AAAA" -- um rótulo genérico
        # que não dizia nada sobre o CONTEÚDO (a data já aparece na coluna Última Atualização,
        # então repeti-la aqui não ajudava). Usa o campo 'titulo' curado manualmente em
        # obligations_data.json (resume o que a obrigação é: qual instrumento, qual entrega);
        # cai pro rótulo antigo só se essa curadoria ainda não tiver sido feita pra algum item.
        fallback_item = f"Obrigação da Assembleia de {fmt_date_br(fonte_data)}" if fonte_data else 'Obrigação identificada em ata'
        synthetic = {
            'item': it.get('titulo') or fallback_item,
            'obs': ' '.join(obs_parts),
            '_tipo': 'obrigacao_assembleia',
            '_acomp_only': True,
            '_origem': 'assembleia',
            'ultima_atualizacao': fonte_data,
        }
        if it.get('verificacao') == 'cumprido':
            synthetic['status'] = 'Enquadrado'  # cumprido não deve mostrar "vencido" por prazo já passado
        elif it.get('prazo'):
            synthetic['proxima_atualizacao'] = it['prazo']
        op_data.setdefault('covenants', []).append(synthetic)

result['meta']['fund_positions_source'] = 'Apresentação PPT "Operações Estruturadas 07.2026", páginas "Portfólio Atual" (7 fundos: MCCI, MCCE, MCRE, MCRED, MCFA, MCEQ, MCCL)'
result['meta']['fund_positions_note'] = (
    'Uma mesma operação pode ser detida por mais de um fundo, cada um com posição, tranche e taxa próprias. '
    'Operações sem posição listada no PPT (CVPAR, UMC, Tarjab, Windsor, Lotus, WT Morumbi) não constam '
    'nas tabelas de Portfólio Atual do PPT na data de referência — podem estar fora do período coberto ou sob '
    'outra estrutura. Um ativo do PPT (FII Grand Mercure) não tem aba correspondente nesta '
    'planilha e por isso não aparece no portal. "Vogue Square" no PPT é o mesmo ativo da aba "Calçada" '
    '(mesmo emissor Habitasec, vencimento Dez/29, taxa IPCA+12% e %CRI 85,7% — confirmado com o usuário).'
)

with open('/tmp/work/portfolio_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, )

import os
print('Wrote', os.path.getsize('/tmp/work/portfolio_data.json'), 'bytes')
print('N operations:', len(result['operations']))
