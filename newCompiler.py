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

f = open('./text/序列化文本.txt')
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

################### 句子主干部分 ###########################

def p_final_sentece_hed_sentence(p):
  'final_sentence : SYN_HED LEFT sentence RIGHT'
  p[0] = ['final_sentence',p[3][1],p[3][2]] 

def p_sentence_sub_sentence(p): #单句
  'sentence : sub_sentence'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_sentence_coo_sentence(p):  #不同主语的并列复合句
  'sentence : coo_sentence SYN_WP POS_WP'
  p[0] = ['sentence',p[1][1],p[1][2]]

def p_coo_sentence_recursive(p):
  'coo_sentence : sub_sentence SYN_COO LEFT coo_sentence RIGHT'
  p[0] = ['sentence',p[1][1],p[1][2] + p[4][2]]

def p_coo_sentence_definition(p): 
  'coo_sentence : sub_sentence SYN_COO LEFT sentence_content RIGHT'
  p[0] = ['coo_sentence',p[1][1],p[1][2] + p[4][2]]


def p_sub_sentence_sentence_content_wp(p):
  'sub_sentence : sentence_content SYN_WP POS_WP'
  p[0] = ['sub_sentence',p[1][1],p[1][2]]

def p_senetence_subject(p): #仅主语
  'sentence_content : subject'
  p[0] = ['sentence_content',p[1][1],p[1][2]]

def p_sentence_content_subject_sbv_predicate(p):  #主谓
  'sentence_content : subject SYN_SBV predicate'  
  p[0] = ['sentence_content', p[1][1], p[1][2]+p[3][2]]

def p_sentence_content_subject_sbv_predicate_vob_object(p): #主谓宾
  'sentence_content : subject SYN_SBV predicate SYN_VOB object'
  p[0] = ['sentence_content', p[1][1], p[1][2]+p[3][2]*p[5][2]]

def p_sentence_content_left_subject_right_wp_sbv_predicate_vob_object(p): #主谓宾,但是主语和谓语用逗号分开
  'sentence_content : LEFT subject SYN_WP POS_WP RIGHT SYN_SBV predicate SYN_VOB object'
  p[0] = ['sentence_content', p[2][1], p[2][2]+p[7][2]*p[9][2]]

def p_sentence_content_predicate_vob_object(p):  #谓宾(祈使句)
  'sentence_content : predicate SYN_VOB object'
  p[0] = ['sentence_content',p[1][2],p[1][2]*p[3][2]]

def p_subject(p):
  '''subject : nphrase
             | vphrase
             | vobphrase
             | aphrase
             | sbv_vob_phrase'''
  p[0] = ['subject',p[1][1],p[1][2]]

def p_predicate(p):
  '''predicate : vphrase
               | aphrase'''
  p[0] = ['predicate',p[1][1],p[1][2]] 

def p_object(p):
  '''object : nphrase
            | aphrase
            | vphrase
            | vobphrase
            | sbvphrase
            | sbv_vob_phrase'''
  p[0] = ['object',p[1][1],p[1][2]]


###################### sbvphrase ########################

def p_sbvphrase(p):  #必然有左右括号。
  'sbvphrase : LEFT subject SYN_SBV vphrase RIGHT'
  p[0] = ['sbvphrase',p[2][1],p[2][2]+p[4][2]]
  

###################### vobphrase ########################
def p_innervob_left_innervob_right(p):#动宾结构，必须分层处理。不分层会出问题。vobphrase -> vphrase . SYN_VOB object ,ply选择继续移入。这里的vobphrase来自于attphrase的展开。attphrase又来自于nphrase，nphrase来自于predicate的展开。
  'vobphrase : LEFT innervob RIGHT'
  p[0] = ['vobphrase',p[2][1],p[2][2]]

def p_innervob_left_innervob_wp_right(p):#动宾结构做分句
  'vobphrase : LEFT innervob SYN_WP POS_WP RIGHT'
  p[0] = ['vobphrase',p[2][1],p[2][2]]

def p_innervob_vphrase_nphrase_SYN_VOB(p):
  'innervob : vphrase SYN_VOB object'
  p[0] = ['innervob',p[2][1],p[1][2]*p[3][2]]

def p_innervob_innervob_uphrase_rad(p):#动宾结构后加语气词
  'innervob : innervob SYN_RAD uphrase'
  p[0] = ['innervob',p[1][1],p[1][2]]

def p_innervob_c_adv_innervob(p):  #连词加到innervob前面，“并吃瓜”
  'innervob : POS_C SYN_ADV innervob'
  p[0] = ['innervob',p[3][1],p[3][2]]

################# sbv_vob_phrase ##########################
#主谓宾结构
def p_sbv_vob_phrase(p):
  'sbv_vob_phrase : LEFT subject SYN_SBV vphrase SYN_VOB object RIGHT'
  p[0] = ['sbv_vob_phrase',p[2][1],p[2][2] + p[4][2] * p[6][2]]
  
###################### nphrase ##########################

def p_nphrase_attphrase_att_nphrase(p): 
  'nphrase : attphrase SYN_ATT nphrase'
  p[0] = ['nphrase',p[1][1],p[1][2]+p[3][2]]

def p_nphrase_attphrase_vphrase(p):  #动词当名词用，"工作","改革"
  'nphrase : attphrase SYN_ATT vphrase'
  p[0] = ['nphrase',p[1][1],p[1][2]*p[3][2]]

def p_nphrase_attphrase_aphrase(p):#形容词当名词用，“喜悦”
  'nphrase : attphrase SYN_ATT aphrase'
  p[0] = ['nphrase',p[1][1],p[1][2]*p[3][2]]

def p_nphrase_p_lad_nphrase(p): #名词短语左边附加介词，”与某某“
  'nphrase : POS_P SYN_LAD nphrase'
  p[0] = ['nphrase',p[3][1],p[3][2]]

def p_nphrase_c_lad_nphrase(p):  #名词短语左边附加连词，”和某某“
  'nphrase : POS_C SYN_LAD nphrase'
  p[0] = ['nphrase',p[3][1],p[3][2]]

def p_nphrase_nphrase_nphrase_coo(p): #名词短语并列
  'nphrase : nphrase SYN_COO nphrase'
  p[0] = ['nphrase',p[1][1],p[1][2]+p[3][2]]

def p_nphrase_m_att_q(p): #数量词短语作为名词成分存在。不会有括号把它扩住
  'nphrase : POS_M SYN_ATT POS_Q'
  p[0] = ['nphrase',p[1][1],p[1][2]]

def p_nphrase_a_a_coo(p): #“繁荣稳定”
  'nphrase : POS_A SYN_COO POS_A'
  p[0] = ['nphrase',p[1][1],p[1][2]+p[3][2]]

def p_nphrase_nphrase_uphrase_rad(p):#定中结构，右边是语气词（感叹句）
  'nphrase : nphrase SYN_RAD uphrase'
  p[0] =['nphrase',p[1][1],p[1][2]]

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


#################### vphrase ############################

def p_vphrase_dphrase_adv_vphrase(p):
  'vphrase : dphrase SYN_ADV vphrase'
  p[0] = ['vphrase',p[3][1],p[1][2]*p[3][2]]

def p_vphrase_aphrase_adv_vphrase(p): #形容词修饰动词
  'vphrase : aphrase SYN_ADV vphrase'
  p[0] = ['vphrase',p[3][1],p[1][2]*p[3][2]]

def p_vphrase_attphrase_vphrase(p):
  'vphrase : attphrase SYN_ATT vphrase'
  p[0] = ['vphrase',p[2][1],p[1][2]*p[3][2]]

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
  'vphrase : POS_V SYN_CMP vphrase'
  p[0] = ['vphrase',p[1][1],p[1][2]*p[3][2]]

def p_vphrase_v(p):
  'vphrase : POS_V'
  p[0] = ['vphrase',p[1][1],p[1][2]]

def p_vphrase_vphrase_uphrase_rad(p): #动词加的/地/了
  'vphrase : vphrase SYN_RAD uphrase'
  p[0] = ['vphrase',p[1][1],p[1][2]]

def p_vphrase_c_lad_vphrase(p): #动词短语左接连词 “和现代化“
  'vphrase : POS_C SYN_LAD vphrase'
  p[0] = ['vphrase',p[3][1],p[3][2]]

def p_vphrase_vphrase_coo_vphrase(p):  #动词并列
  'vphrase : vphrase SYN_COO vphrase'
  p[0] = ['vphrase',p[1][1],p[1][2]+p[3][2]]

def p_vphrase_LEFT_RIGHT(p):
  'vphrase : LEFT vphrase RIGHT'
  p[0] = ['vphrase',p[2][1],p[2][2]]

def p_vphrase_vobphrase_vphrase_coo(p): #连动词，上街买菜
  'vphrase : vphrase SYN_COO vobphrase'
  p[0] = ['vobphrase',p[1][1],p[1][2]+p[3][2]]

#################### dphrase ########################
def p_dphrase_d(p):  #副词短语
  'dphrase : POS_D'
  p[0] = ['dphrase',p[1][1],p[1][2]]

def p_dphrase_LEFT_dphrase_RIGHT(p):
  'dphrase : LEFT inner_dphrase RIGHT'
  p[0] = ['dphrase',p[2][1],p[2][2]]

def p_dphrase_d_adv_pobphrase(p):
  'inner_dphrase  : POS_D SYN_ADV pobphrase'
  p[0] = ['dphrase',p[1][1],p[1][2]*p[3][2]]

def p_dphrase_uphrase_rad(p):
  'inner_dphrase : POS_D SYN_RAD uphrase'
  p[0] = ['dphrase',p[1][1],p[1][2]]

###################### uphrase #######################

def p_uphrase_u(p):
  'uphrase : POS_U'
  p[0] = ['uphrase',p[1][1],p[1][2]]


###################### aphrase #######################

def p_aphrase_aphrase_uphrase_SYN_RAD(p): #带‘的’的形容词短语
  'aphrase : aphrase SYN_RAD uphrase'
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


####################### pobphrase #####################

def p_pobphrase_p_pob_nphrase(p):  #介宾短语
  'inner_pobphrase : POS_P SYN_POB object'
  p[0] = ['pobphrase',p[3][1],p[3][2]]

def p_pobphrase_wpphrase(p):  #可能有逗号分割
  'inner_pobphrase : inner_pobphrase SYN_WP POS_WP'
  p[0] = ['pobphrase',p[1][1],p[1][2]]

def p_pobphrase_LEFT_RIGHT(p):
  'pobphrase : LEFT inner_pobphrase RIGHT'
  p[0] = ['pobphrase',p[2][1],p[2][2]]


################# attphrase #############################

def p_attphrase_definition(p): #可以做定语的短语。
  '''attphrase : POS_M 
               | mqphrase 
               | rmqphrase 
               | vobphrase 
               | aphrase 
               | nphrase 
               | vphrase 
               | rqphrase 
               | POS_B 
               | sbv_vob_phrase 
 	       | sbvphrase '''
  p[0] = ['attphrase',p[1][1],p[1][2]]


################ 数量词短语 #####################################

def p_mqphrase_m_att_q(p): #数量词短语做定语成分，如果它是做定语成分的，必然会有括号把它扩住。
  'mqphrase : LEFT POS_M SYN_ATT POS_Q RIGHT'
  p[0] = ['mqphrase',p[2][1],p[2][2]]

def p_rqphrase_left_r_att_q_right(p): #这件/这把
  'rqphrase : LEFT POS_R SYN_ATT POS_Q RIGHT'
  p[0] = ['rqphrase',p[2][1],p[2][2]]

def p_rmqphrase_definition_1(p):#这一把
  'rmqphrase : LEFT LEFT POS_R SYN_ATT POS_M RIGHT SYN_ATT POS_Q RIGHT'
  p[0] = ['rmqphrase',p[2][1],p[3][2]]

def p_error(p):
  print("Syntax error in input:" + str(p))


parser = yacc.yacc()
result = parser.parse(data)  
print(result)




