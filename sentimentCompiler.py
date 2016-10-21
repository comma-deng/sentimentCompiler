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
'i':'POS_I',
'c':'POS_C',
'j':'POS_J',
'b':'POS_B',
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
'LAD':'SYN_LAD',
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

def p_sentence_sentencepart(p):
  'sentence : sentence_part'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_sentece_sentence_sentencepart(p):  #复合句的情感值等于两句分句相加
  'sentence : sentence sentence_part'
  p[0] = ['sentence',p[1][1],p[1][2] + p[2][2]]

def p_sentencepart_stc_wpphrase_wp(p):  #第一种情况：分句是第一个分句。第二种情况 ： 分句是第一个分句之后的分句。
  '''sentence_part : sentence_part wpphrase SYN_WP
                   | sentence_part SYN_COO wpphrase SYN_WP'''
  p[0] = ['sentence_part',p[1][1],p[1][2]]


def p_sentencepart_sbvphrase(p): #主谓句
  'sentence_part : sbvphrase'
  p[0] = ['sentence_part',p[1][1],p[1][2]]

def p_sentencepart_vobphrase(p):#动宾句
  'sentence_part : vobphrase'
  p[0] = ['sentence_part',p[1][1],p[1][2]]

def p_sentencepart_nphrase(p):#定中结构句（多么漂亮的彩虹啊）
  'sentence_part : nphrase'
  p[0] = ['sentence_part',p[1][1],p[1][2]]

def p_sentencepart_fobphrase(p): #前置宾语句
  'sentence_part : fobphrase'
  p[0] = ['sentence_part',p[1][1],p[1][2]]

def p_sentencepart_vphrase(p):
  'sentence_part : vphrase'
  p[0] = ['sentence_part',p[1][1],p[1][2]]

def p_wpphrase_wp(p):
  'wpphrase : POS_WP'
  p[0] =['wpphrase',p[1][1],p[1][2]]

def p_sbvphrase_nphrase_sbv_vphrase(p):#主谓结构,此处主语为名词
  'sbvphrase : nphrase SYN_SBV vphrase'
  p[0] = ['sbvphrase',p[3][1],p[3][2]]

def p_sbvphrase_nphrase_sbv_vphrase_error(p):#错误
  'sbvphrase : nphrase SYN_SBV error'
  print('error in sbv')

def p_sbvphrase_nphrase_sbv_aphrase(p):#主谓结构，此处谓语为形容词
  'sbvphrase : nphrase SYN_SBV aphrase'
  p[0] =['sbvphrase',p[2][1],p[3][2]]

def p_sbvphrase_vphrase_sbv_vphrase(p): #主谓结构，主语是动词。“工作”
  'sbvphrase : vphrase SYN_SBV vphrase'
  p[0] = ['sbvphrase',p[1][1],p[1][2]]

def p_sbvphrase_vobphrase_sbv_vphrase(p): #主语是 动宾结构 “完成祖国统一是大势所趋”
  'sbvphrase : vobphrase SYN_SBV vphrase'
  p[0] = ['sbvphrase',p[1][1],p[1][2]]


def p_sbvphrase_LEFT_RIGHT(p):
  'sbvphrase : LEFT sbvphrase RIGHT'
  p[0] = ['sbvphrase',p[2][1],p[2][2]]

def p_vobphrase_c_adv_vobphrase(p):  #连词加到vobphrase前面，“并吃瓜”
  'vobphrase : POS_C SYN_ADV vobphrase'
  p[0] = ['vobphrase',p[3][1],p[3][2]]

def p_vobphrase_sbvphrase_nphrase_vob(p):
  'vobphrase : sbvphrase nphrase SYN_VOB'
  p[0] = ['vobphrase',p[2][1],p[1][2]*p[2][2]]

def p_vobphrase_sbvphrase_vobphrase_vob(p): #主宾句接动宾句做宾语，“中国政府顺利恢复对香港行使主权”
  'vobphrase : sbvphrase vobphrase SYN_VOB'
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

def p_vobphrase_vobphrase_vphrase_coo(p): #连动词，上街买菜
  'vobphrase : vphrase vobphrase SYN_COO'
  p[0] = ['vobphrase',p[1][1],p[1][2]+p[2][2]]


def p_vobphrase_v_v_vob(p): #两个动词之间也可能是动宾关系，“推向前进”
  'vobphrase : POS_V POS_V SYN_VOB'
  p[0] = ['vobphrase',p[1][1],p[1][2]*p[2][2]]

def p_vobphrase_vphrase_vobphrase_vob(p): #动词接一个动宾句做宾语，“继续把建设有中国特色社会主义事业推向前进”
  'vobphrase : vphrase vobphrase SYN_VOB'
  p[0] = ['vobphrase',p[1][1],p[1][2]*p[2][2]]

def p_vobphrase_vphrase_sbvphrase_vob(p): #“完成祖国统一”
  'vobphrase : vphrase sbvphrase SYN_VOB'
  p[0] = ['vobphrase',p[1][1],p[1][2]*p[2][2]]

def p_vobphrase_pobphrase_adv_vobphrase(p): #介宾结构修饰动宾结构
  'vobphrase : pobphrase SYN_ADV vobphrase'
  p[0] = ['vobphrase',p[1][1],p[1][2]*p[3][2]]

def p_vobphrase_LEFT_RIGHT(p):
  'vobphrase : LEFT vobphrase RIGHT'
  p[0] = ['vobphrase',p[2][1],p[2][2]]

def p_fobphrase_nphrase_fob_vphrase(p): #前置宾语：凶手被抓住了
  'fobphrase : nphrase SYN_FOB vphrase'
  p[0] = ['fobphrase',p[1][1],p[1][1]*p[3][1]]
 
def p_nphrase_attphrase_att_nphrase(p): #为何这中间没有依存符号？这是为了单定语和多重定语的统一。attphrase中包含了依存符号。
  'nphrase : attphrase nphrase'
  p[0] = ['nphrase',p[1][1],p[1][2]]

def p_nphrase_attphrase_vphrase(p):  #动词当名词用，"工作"
  'nphrase : attphrase vphrase'
  p[0] = ['nphrase',p[1][1],p[1][2]]


def p_nphrase_p_lad_nphrase(p): #名词短语左边附加介词，”与某某“
  'nphrase : POS_P SYN_LAD nphrase'
  p[0] = ['nphrase',p[3][1],p[3][2]]

def p_nphrase_c_lad_nphrase(p):  #名词短语左边附加连词，”和某某“
  'nphrase : POS_C SYN_LAD nphrase'
  p[0] = ['nphrase',p[3][1],p[3][2]]


def p_nphrase_nphrase_nphrase_coo(p): #名词短语并列
  'nphrase : nphrase nphrase SYN_COO'
  p[0] = ['nphrase',p[1][1],p[1][1]+p[2][1]]


def p_nphrase_attphrase_att_q(p): #数量词短语作为名词成分存在。不会有括号把它扩住
  'nphrase : POS_M SYN_ATT POS_Q'
  p[0] = ['nphrase',p[1][1],p[1][2]]

def p_nphrase_a_a_coo(p): # “繁荣稳定”
  'nphrase : POS_A POS_A SYN_COO'
  p[0] = ['nphrase',p[1][1],p[1][2]+p[2][2]]

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

def p_nphrase_j(p):#缩略词可以做名词成分
  'nphrase : POS_J'
  p[0] = ['nphrase',p[1][1],p[1][2]]

def p_nphrase_i(p):#成语可以做名词成分
  'nphrase : POS_I'
  p[0] = ['nphrase',p[1][1],p[1][2]]

def p_nphrase_left_right(p):
  'nphrase : LEFT nphrase RIGHT'
  p[0] =['nphrase',p[2][1],p[2][2]]

def p_vphrase_dphrase_adv_vphrase(p):
  'vphrase : dphrase SYN_ADV vphrase'
  p[0] = ['vphrase',p[3][1],p[1][2]*p[3][2]]

def p_vphrase_aphrase_adv_vphrase(p): #形容词修饰动词
  'vphrase : aphrase SYN_ADV vphrase'
  p[0] = ['vphrase',p[3][1],p[1][2]*p[3][2]]

def p_vphrase_pobphrase(p):
  'vphrase : pobphrase SYN_ADV vphrase'
  p[0] = ['vphrase',p[3][1],p[1][2]*p[3][2]]

'''
#加入本条规则后，分析“打人的事是不对的”，会提示aphrase出现语法错误.原因知道了，是括号的关系。
def p_vhrase_vphrase_vphrase_cmp(p):
  'vphrase :  vphrase vphrase SYN_CMP'
  p[0] = ['vphrase',p[1][1],p[1][2]*p[2][2]]
'''

def p_posv_posv_cmp(p): #动补结构
  'vphrase : POS_V POS_V SYN_CMP'
  p[0] = ['vphrase',p[1][1],p[1][2]*p[2][2]]

def p_vphrase_v(p):
  'vphrase : POS_V'
  p[0] = ['vphrase',p[1][1],p[1][2]]

def p_vphrase_vphrase_uphrase_rad(p): #动词加的/地
  'vphrase : vphrase uphrase SYN_RAD'
  p[0] = ['vphrase',p[1][1],p[1][2]]

def p_vphrase_c_lad_vphrase(p): #动词短语左接连词 “和现代化“
  'vphrase : POS_C SYN_LAD vphrase'
  p[0] = ['vphrase',p[3][1],p[3][2]]

def p_vphrase_LEFT_RIGHT(p):
  'vphrase : LEFT vphrase RIGHT'
  p[0] = ['vphrase',p[2][1],p[2][2]]

def p_dphrase_d_adv_pobphrase(p):
  'dphrase : dphrase SYN_ADV pobphrase'
  p[0] = ['dphrase',p[1][1],p[1][2]*p[3][2]]

def p_dphrase_d(p):  #副词短语
  'dphrase : POS_D'
  p[0] = ['dphrase',p[1][1],p[1][2]]

def p_dphrase_uphrase_rad(p):
  'dphrase : dphrase uphrase SYN_RAD'
  p[0] = ['dphrase',p[1][1],p[1][2]]

def p_dphrase_LEFT_dphrase_RIGHT(p):
  'dphrase : LEFT dphrase RIGHT'
  p[0] = ['dphrase',p[2][1],p[2][2]]

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

def p_aphrase_a(p): #形容词短语
  'aphrase : POS_A'
  p[0] = ['aphrase',p[1][1],p[1][2]]

def p_aphrase_LEFT_RIGHT(p):
  'aphrase : LEFT aphrase RIGHT'
  p[0] = ['aphrase',p[2][1],p[2][2]]

def p_pobphrase_p_pob_nphrase(p):  #介宾短语
  'pobphrase : POS_P objphrase SYN_POB'
  p[0] = ['pobphrase',p[2][1],p[2][2]]

def p_pobphrase_wpphrase(p):  #可能有逗号分割
  'pobphrase : pobphrase wpphrase SYN_WP'
  p[0] = ['pobphrase',p[1][1],p[1][2]]

def p_pobphrase_LEFT_RIGHT(p):
  'pobphrase : LEFT pobphrase RIGHT'
  p[0] = ['pobphrase',p[2][1],p[2][2]]

def p_mqphrase_m_att_q(p): #数量词短语做修饰成分，如果它是做修饰成分的，必然会有括号把它扩住。
  'mqphrase : LEFT POS_M SYN_ATT POS_Q RIGHT'
  p[0] = ['mqphrase',p[2][1],p[2][2]]

def p_rqphrase_left_r_att_q_right(p): #这件/这把
  'rqphrase : LEFT POS_R SYN_ATT POS_Q RIGHT'
  p[0] = ['rqphrase',p[2][1],p[2][2]]

def p_rmqphrase_definition_1(p):#这一
  'rmqphrase : LEFT LEFT POS_R SYN_ATT POS_M RIGHT SYN_ATT POS_Q RIGHT'
  p[0] = ['rmphrase',p[3][1],p[3][2]]

def p_attphrase_definition(p): #可以做定语的短语。之所以把SYN_ATT也放到attphrase中，是为了实现多重定语。
  '''attphrase : POS_M SYN_ATT
               | mqphrase SYN_ATT
               | rmqphrase SYN_ATT
               | vobphrase SYN_ATT
               | aphrase SYN_ATT
               | nphrase SYN_ATT
               | vphrase SYN_ATT
               | rqphrase SYN_ATT
               | POS_R SYN_ATT
               | POS_B SYN_ATT'''
  p[0] = ['attphrase',p[1][1],p[1][2]]

def p_obj_definition(p): #可以在介宾结构中做宾语的短语
  'objphrase : sentence_part'
  p[0] = ['objphrase',p[1][1],p[1][2]]


def p_attphrase_repeat(p):  #多重定语
  'attphrase : attphrase SYN_ATT attphrase SYN_ATT'
  p[0] = ['attphrase',p[1][1],p[1][2]+p[3][2]]

def p_error(p):
  print("Syntax error in input:" + str(p))

parser = yacc.yacc()
result = parser.parse(data)  
print(result)

