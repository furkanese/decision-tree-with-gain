from __future__ import division
import numpy as np
import arff
thetree = np.load('my_file1.npy').item()
dataset = arff.load(open('testingD.arff', 'r'))
testdata = dataset['data']
testattr = dataset['attributes']
print('okundu')
def find_index(the_testattr,k):
att_index = 0
for i in range (0, len(the_testattr)):
if the_testattr[i][0] == k:
att_index = i
break
return att_index
def visit(node,the_data,parent_index, parent=None):
result = 'XXX'
for k,v in node.iteritems():
if isinstance(v, dict):
loc_index = find_index(testattr,k)
'''
Gezmeye devam sarti:
- gelen ozellik attr listesinde ana ozellik olmali
- alt ozellik data ile eslesmeli
'''
if loc_index != 0 or the_data[parent_index] == k:
the_result = visit(v,the_data,loc_index, k)
return the_result
else:
'''
Devam edilecek branch yok ise buraya gelir
- Sonuc data ile ayniysa sonuc doner
- Degilse default deger verilir
'''
if(the_data[parent_index] == k):
result = str(v)
return result
else:
return result
rescount =0
count = 0
for a in testdata:
res = visit(thetree,a,0)
if res == a[274]:
rescount += 1
count += 1
(totdata,totattr) = np.shape(testdata)
success = rescount * 100 / totdata
print success
print rescount
print count