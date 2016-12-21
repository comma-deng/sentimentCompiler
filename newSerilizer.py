# encoding=utf-8
import Queue
import sys
from pyltp import Segmentor

sentiment_dict = {}
count=0
with open("/home/cm/pyfiles/dict/sentimentDict.txt",'r') as f:
  lines = f.readlines()
  for line in lines:
    split_result = line.split()
    word = split_result[0]
    value = float(split_result[1])
    sentiment_dict[word] = value
	

with open("/home/cm/pyfiles/dict/fanZhuanCi.txt",'r') as f:
  lines = f.readlines()
  for line in lines:
    word = line
    value = -1.0
    sentiment_dict[word] = value

sentence = sys.argv[1]
segmentor = Segmentor()
segmentor.load_with_lexicon('/home/cm/pyfiles/ltpmodel/ltp_data/cws.model','/home/cm/pyfiles/dict/外部词典.txt')
words = segmentor.segment(sentence)
words = list(words)
print '\t'.join(words)


from pyltp import Postagger
postagger = Postagger() 
postagger.load('/home/cm/pyfiles/ltpmodel/ltp_data/pos.model')  
postags = postagger.postag(words)  
print '\t'.join(postags)
postagger.release()

from pyltp import Parser
parser = Parser() 
parser.load('/home/cm/pyfiles/ltpmodel/ltp_data/parser.model')  
arcs = parser.parse(words, postags)  
print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
parser.release()  

word_infos=[]
for i in range(len(words)):
  word_infos.append(postags[i] + '|' + str(i) + '|' + str(sentiment_dict.get(words[i],0.0)))

relation_tree = []    
for i in range(len(arcs)):
  relation_tree.append([])

position_relation_list =[]

head_node = 0
for i in range(len(arcs)):
  if(arcs[i].head != 0):
    relation_tree[arcs[i].head-1].append(i+1);
  else:
    head_node = i+1

print(relation_tree)

for i in range(len(arcs)):
  if len(relation_tree[i]) == 0:
    if(arcs[i].head > i+1): #如果父节点在当前节点右边
      position_relation_list.append([i+1,str(arcs[i].relation)]) 
    else:
      position_relation_list.append([i,str(arcs[i].relation)]) 
    continue;
  subtree_list = []
  queue = Queue.Queue() #遍历子树
  for node in relation_tree[i]:
    queue.put(node)
  while(queue.empty()==False):
    temp = queue.get()
    subtree_list.append(temp)
    for node in relation_tree[temp-1]:
      queue.put(node)
  subtree_list.append(i+1) #加入当前节点
  max_pos = max(subtree_list)
  min_pos = min(subtree_list)-1
  if(arcs[i].head > i+1): #如果父节点在当前节点右边
    position_relation_list.append([max_pos,str(arcs[i].relation)])
    position_relation_list.append([max_pos,')']) 
    position_relation_list.append([min_pos,'('])
  else:  #如果父节点在当前节点左边
    position_relation_list.append([max_pos,')'])
    position_relation_list.append([min_pos,'('])
    position_relation_list.append([min_pos,str(arcs[i].relation)])



print " ".join("%d:%s" %(p_l[0],p_l[1]) for p_l in position_relation_list)
  
position_relation_list.sort(key = lambda x:x[0])

print " ".join("%d:%s" %(p_l[0],p_l[1]) for p_l in position_relation_list)

#因为插入顺序是从左至右的，故同一位置上插入多个） 和依存符号，或者是单个的‘）’，必然是父亲节点的先插入，但父节点的括号应该在子节点的右边，故要交换。另外，同一位置上如果有‘（’，那么‘（’必然是在‘）’后插入的，这里不必交换。
i=0
order_list = [-1]
for i in range(len(position_relation_list)-1):
  if(position_relation_list[i][0] != position_relation_list[i+1][0]):
    order_list.append(i)

order_list.append(len(position_relation_list)-1)
print(order_list)

i=0


for i in range(len(order_list)-1):
  symbol_dict = {'(':0,')':0}
  syn = None
  for j in range(order_list[i]+1,order_list[i+1]+1): #统计“）”和“（”数目
    if(symbol_dict.get(position_relation_list[j][1])!=None):  
      symbol_dict[position_relation_list[j][1]]+=1
    else:
      syn =  position_relation_list[j][1]

  #重新排列，同一位置上如果有同时有“（” “）” 依存符号 必然是按 ） 依存符号 （ 的顺序排列。且依存符号只可能有一个。
  for j in range(symbol_dict[')']): 
    position_relation_list[order_list[i]+1+j][1] = ')'

  if(syn!=None):
    position_relation_list[order_list[i]+1+symbol_dict[')']][1] = syn
  
  for j in range(symbol_dict['(']):
    position_relation_list[order_list[i+1]-j][1] = '('

i=0
print('\n')
print(str(symbol_dict['(']) + "   " + str(symbol_dict[')']) + "   ")
print " ".join("%d:%s" %(p_l[0],p_l[1]) for p_l in position_relation_list)

#插入依存符号和括号
for i in range(len(position_relation_list)):
  position_relation_list[i][0] += i
  words.insert(position_relation_list[i][0],position_relation_list[i][1])
  word_infos.insert(position_relation_list[i][0],position_relation_list[i][1])

print " ".join("%d:%s" %(p_l[0],p_l[1]) for p_l in position_relation_list)

print " ".join(words)
print " ".join(word_infos)

f = open(r'/home/cm/pyfiles/text/序列化文本.txt','w')
f.write(' '.join(word_infos))
f.close()

