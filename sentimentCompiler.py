# encoding=utf-8

import ply.lex as lex


tokens = ['WORD']

reserved ={
'wp':'POS_WP',
'n':'POS_N',
'nd':'POS_N',
'nh':'POS_N',
'ni':'POS_N',
'nl':'POS_N',
'ns':'POS_N',
'nt':'POS_N',
'nz':'POS_N',
'v':'POS_V',
'd':'POS_D',
'u':'POS_U',
'a':'POS_A',
'r':'POS_R',
'p':'POS_P',
'm':'POS_M',
'q':'POS_Q',
'ROOT':'SYN_ROOT',
'SBV':'SYN_SBV',		
'ADV':'SYN_ADV',
'VOB':'SYN_VOB',
'ATT':'SYN_ATT',
'RAD':'SYN_RAD',
'HED':'SYN_HED',
'WP':'SYN_WP',
'COO':'SYN_COO',
'POB':'SYN_POB',
'CMP':'SYN_CMP',
'FOB':'SYN_FOB',
'(':'LEFT',
')':'RIGHT'
}


tokens = tokens + list(set(reserved.values()))

def t_ID(t):
    r'[A-Z][A-Z_]*|\(|\)'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

t_ignore = ' \t'

def t_WORD(t):
  r'[^ ]+\|[^ ]+\|[^ ]+'
  print(t.value)
  temp = t.value.split('|')
  value = []
  value.append(t.value)
  value.append(int(temp[1]))
  value.append(float(temp[2]))
  t.value = value
  t.type = reserved.get(temp[0],'WORD')
  return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

#data = 'ROOT n|0|0.4 SBV d|1|1.3 ADV v|2|0.8 n|3|0.0 SBV v|4|-0.4 n|5|-0.1  VOB u|6|0.0 RAD ATT n|7|0.0 VOB wp|8|0.0 WP HED'

f = open('/home/cm/pyfiles/text/序列化文本.txt')
data = f.readline()
f.close()

print(data)
lexer.input(data)

while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)


import ply.yacc as yacc

def p_sentence_root_stc_hed(p):
  'sentence : sentence SYN_HED'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_sentece_left_sentence_right(p):
  'sentence : LEFT sentence RIGHT'
  p[0] = ['sentence',p[2][1],p[2][2]] 

def p_sentence_stc_wpphrase_wp(p):
  'sentence : sentence wpphrase SYN_WP'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_sentence_sbvphrase(p): #主谓句
  'sentence : sbvphrase'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_sentence_vobphrase(p):#动宾句
  'sentence : vobphrase'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_sentence_nphrase(p):#定中结构句（多么漂亮的彩虹啊）
  'sentence : nphrase'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_sentence_fobphrase(p):
  'sentence : fobphrase'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_sentence_vphrase(p):
  'sentence : vphrase'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_wpphrase_wp(p):
  'wpphrase : POS_WP'
  p[0] =['wpphrase',p[1][1],p[1][2]]

def p_sbvphrase_nphrase_sbv_vphrase(p):#主谓结构,此处主语为名词
  'sbvphrase : nphrase SYN_SBV vphrase'
  p[0] = ['sbvphrase',p[3][1],p[3][2]]

def p_sbvphrase_nphrase_sbv_vphrase_error(p):#主谓结构,此处主语为名词
  'sbvphrase : nphrase SYN_SBV error'
  p[0] = ['sbvphrase',p[3][1],p[3][2]]
  print('error in sbv')

def p_sbvphrase_nphrase_sbv_aphrase(p):#主谓结构，此处谓语为形容词
  'sbvphrase : nphrase SYN_SBV aphrase'
  p[0] =['sbvphrase',p[2][1],p[3][2]]


def p_sbvphrase_LEFT_RIGHT(p):
  'sbvphrase : LEFT sbvphrase RIGHT'
  p[0] = ['sbvphrase',p[2][1],p[2][2]]

def p_vobphrase_sbvphrase_nphrase_vob(p):
  'vobphrase : sbvphrase nphrase SYN_VOB'
  p[0] = ['vobphrase',p[2][1],p[1][2]*p[2][2]]

def p_vobphrase_sbvphrase_nphrase_vob_error(p):
  'vobphrase : sbvphrase error SYN_VOB'
  print('error in VOB!')

def p_vobphrase_sbvphrase_aphrase_vob(p):
  'vobphrase : sbvphrase aphrase SYN_VOB'
  p[0] = ['vobphrase',p[1][1],p[1][2]*p[2][2]]

def p_vobphrase_vphrase_nphrase_SYN_VOB(p):#动宾结构
  'vobphrase : vphrase nphrase SYN_VOB'
  p[0] = ['vobphrase',p[1][1],p[1][2]*p[2][2]]

def p_vobphrase_vphrase_aphrase_vob(p):  #动宾结构，宾语为形容词（pyltp会把一些名词当形容词处理。比如美丽）
  'vobphrase : vphrase aphrase SYN_VOB'
  p[0] = ['vobphrase',p[1][1],p[1][2]*p[2][2]]

def p_vobphrase_vobphrase_uphrase_rad(p):#动宾结构后加语气词
  'vobphrase : vobphrase uphrase SYN_RAD'
  p[0] = ['vobphrase',p[1][1],p[1][2]]

def p_vobphrase_vobphrase_vphrase_coo(p):
  'vobphrase : vobphrase vphrase SYN_COO'
  p[0] = ['vobphrase',p[1][1],p[1][2]+p[2][2]]

def p_vobphrase_LEFT_RIGHT(p):
  'vobphrase : LEFT vobphrase RIGHT'
  p[0] = ['vobphrase',p[2][1],p[2][2]]

def p_fobphrase_nphrase_fob_pobphrase_adv_vphrase(p):
  'fobphrase : nphrase SYN_FOB pobphrase SYN_ADV vphrase'
  p[0] = ['fobphrase',p[5][1],p[1][2]*p[5][2]]


def p_nphrase_aphrase_att_nphrase(p): #定中结构
  'nphrase : aphrase SYN_ATT nphrase'
  p[0] =['nphrase',p[3][1],p[1][2]*p[3][2]]

def p_nphrase_nphrase_nphrase_att(p):
  'nphrase : nphrase SYN_ATT nphrase'
  p[0] = ['nphrase',p[1][1],p[1][2]]

def p_nphrase_nphrase_uphrase_rad(p):#定中结构，右边是语气词（感叹句）
  'nphrase : nphrase uphrase SYN_RAD'
  p[0] =['nphrase',p[1][1],p[1][2]*p[2][2]]

def p_nphrase_nphrase_uphrase_rad_error(p):
  'nphrase : nphrase error SYN_RAD'
  print('error in RAD!')  

def p_nphrase_n(p):
  'nphrase : POS_N'
  p[0] = ['nphrase',p[1][1],p[1][2]]

def p_nphrase_r(p): #名词性词组也可以是代词
  'nphrase : POS_R'
  p[0] = ['nphrase',p[1][1],p[1][2]]

def p_nphrase_vobphrase_att_nphrase(p):
  'nphrase : vobphrase SYN_ATT nphrase'
  p[0] = ['nphrase',p[3][1],p[1][2]+p[3][2]]

def p_nphrase_vobphrase_att_nphrase_error(p):
  'nphrase : vobphrase SYN_ATT error'
  print('error in vob att nphrase')

def p_nphrase_pos_m__att_nphrase(p): #数词修饰名词（ltp会把“一个”作为数词）
  'nphrase : POS_M SYN_ATT nphrase'
  p[0] = ['nphrase',p[3][1],p[3][2]]

def p_nphrase_mqphrase_att_nphrase(p): #数量词修饰名词
  'nphrase : mqphrase SYN_ATT nphrase'
  p[0] = ['nphrase',p[3][1],p[3][2]]

def p_nphrase_left_right(p):
  'nphrase : LEFT nphrase RIGHT'
  p[0] =['nphrase',p[2][1],p[2][2]]

def p_vphrase_dphrase_adv_vphrase(p):
  'vphrase : dphrase SYN_ADV vphrase'
  p[0] = ['vphrase',p[3][1],p[1][2]*p[3][2]]

def p_vphrase_pobphrase(p):
  'vphrase : pobphrase SYN_POB vphrase'
  p[0] = ['vphrase',p[3][1],p[1][2]*p[3][2]]

'''
#加入本条规则后，分析“打人的事是不对的”，会提示aphrase出现语法错误.原因知道了，是括号的关系。
def p_vhrase_vphrase_vphrase_cmp(p):
  'vphrase :  vphrase vphrase SYN_CMP'
  p[0] = ['vphrase',p[1][1],p[1][2]*p[2][2]]
'''

def p_posv_posv_cmp(p):
  'vphrase : POS_V POS_V SYN_CMP'
  p[0] = ['vphrase',p[1][1],p[1][2]*p[2][2]]

def p_vphrase_v(p):
  'vphrase : POS_V'
  p[0] = ['vphrase',p[1][1],p[1][2]]

def p_vphrase_vphrase_uphrase_rad(p):
  'vphrase : vphrase uphrase SYN_RAD'
  p[0] = ['vphrase',p[1][1],p[1][2]]

def p_vphrase_LEFT_RIGHT(p):
  'vphrase : LEFT vphrase RIGHT'
  p[0] = ['vphrase',p[2][1],p[2][2]]

def p_dphrase_d(p):
  'dphrase : dphrase SYN_ADV pobphrase'
  p[0] = ['dphrase',p[1][1],p[1][2]*p[3][2]]

def p_dhrase_d(p):
  'dphrase : POS_D'
  p[0] = ['dphrase',p[1][1],p[1][2]]


def p_uphrase_u(p):
  'uphrase : POS_U'
  p[0] = ['uphrase',p[1][1],p[1][2]]


def p_aphrase_aphrase_uphrase_SYN_RAD(p): #带‘的’的形容词短语
  'aphrase : aphrase uphrase SYN_RAD'
  p[0] = ['aphrase',p[1][1],p[1][2]]
  

def p_aphrase_aphrase_uphrase_SYN_RAD_error(p):
  'aphrase : aphrase error SYN_RAD'
  print('error in uphrase aphrase RAD!')

def p_aphrase_d_ADV_a(p):
  'aphrase : dphrase SYN_ADV aphrase'#副词+形容词的形容词短语
  p[0] = ['aphrase',p[1][1],p[1][2]*p[3][2]]

def p_aphrase_a(p):
  'aphrase : POS_A'
  p[0] = ['aphrase',p[1][1],p[1][2]]

def p_aphrase_LEFT_RIGHT(p):
  'aphrase : LEFT aphrase RIGHT'
  p[0] = ['aphrase',p[2][1],p[2][2]]

def p_pobphrase_p_pob_nphrase(p):
  'pobphrase : POS_P nphrase SYN_POB'
  p[0] = ['pobphrase',p[2][1],p[2][2]]

def p_pobphrase_LEFT_RIGHT(p):
  'pobphrase : LEFT pobphrase RIGHT'
  p[0] = ['pobphrase',p[2][1],p[2][2]]

def p_mqphrase_m_att_q(p):
  'mqphrase : POS_M SYN_ATT POS_Q'
  p[0] = ['mqphrase',p[1][1],p[1][2]]

def p_error(p):
  print("Syntax error in input:" + str(p))

parser = yacc.yacc()
result = parser.parse(data)  
print(result)

