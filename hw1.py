from __future__ import division
import arff, numpy as np
import math
import time
print time.localtime()
dataset = arff.load(open('training_subsetD.arff', 'r'))
print('okundu')
print time.localtime()
# Class bilgisinin yeri
class_place = 274
# ozellik listemizi aliyoruz
all_data = []
attributes = np.array(all_data, dtype=object)
attributes = dataset['attributes']
# datayi aliyoruz
data = np.array(dataset['data'])
# data icerisinde bos olan elemanlari en yaygin elemanlar ile dolduruyoruz
# datanin sayisini aliyoruz
(totalData, totalAttribute) = np.shape(data)
word_counter = {}
for i in range(0, totalAttribute):
for j in range(0, totalData):
if data[j][i] in word_counter:
word_counter[data[j][i]] += 1
elif data[j][i] is not None:
word_counter[data[j][i]] = 1
popular_word = sorted(word_counter, key=word_counter.get, reverse=True)
for k in range(0, totalData):
if data[k][i] is None:
data[k][i] = popular_word[0]
word_counter.clear()
print('Data duzenlendi')
def find_from_attributes(attribute, target):
# toplam ozellik sayimizi buluyoruz
totalattributecount = len(attribute)
index = 0
for i in range(0, totalattributecount):
if attribute[i][0].find(target) != -1:
index = i
if index == 0:
index = -1
return index
def get_attribute_entropy(thedata, subattribute, indexattr):
# datanin sayisini aliyoruz
(totdata, b) = np.shape(thedata)
T = 0
F = 0
for i in range(0, totdata):
# verdigimiz alt deger dogru ise Class kontrolu yapiliyor.
if subattribute in thedata[i][indexattr]:
if thedata[i][b-1] == 'True':
T += 1
else:
F += 1
if T != 0 and F != 0:
m = T / totdata
n = F / totdata
entropy = - m * math.log(m, 2) - n * math.log(n, 2)
else:
entropy = 1
return entropy
def get_total_entropy(thedata):
# Verilen datanin entropisini almaya yarar
# datanin sayisini aliyoruz
(totaldata, b) = np.shape(thedata)
global class_place
T = 0
F = 0
for i in range(0, totaldata):
if thedata[i][b-1] == 'True':
T += 1
else:
F += 1
if T != 0 and F != 0:
m = T / totaldata
n = F / totaldata
entropy = - m * math.log(m, 2) - n * math.log(n, 2)
else:
entropy = 1
return entropy
def get_freq(thedata,targetattribute,mainattributeindex):
# Verilen data icerisindeki attributelarin alt elemanlarinin frekans degerini bulur
(data_count,data_length) = np.shape(thedata)
freq = 0
for i in range(0,data_count):
if thedata[i][mainattributeindex] == targetattribute:
freq += 1
freq = freq / data_count
return freq
def get_gain(thedata, theattributes, mainattributeindex):
# Datayi bolersek elde edecegimiz kazanci bulur
total_gain = get_total_entropy(thedata)
for i in range(0, len(theattributes[mainattributeindex][1])):
total_gain += -(get_freq(thedata, theattributes[mainattributeindex][1][i], mainattributeindex) *
get_attribute_entropy(thedata, theattributes[mainattributeindex][1][i], mainattributeindex))
return total_gain
def get_max_gain(thedata, theattributes):
max = 0.0
index = 0
attra = ''
for i in range(0, (len(theattributes) - 1)):
gain = (get_gain(thedata, theattributes, i))
if gain > max:
max = gain
attra = theattributes[i][0]
index = i
return index, attra, maxdef divide_data(thedata, attr_index, target):
# verilen datayi gelen attribute a gore boler
(data_count, data_length) = np.shape(thedata)
dats = np.ndarray([data_count, data_length-1], dtype=object)
countx = 0
county = 0
for k in range(0, data_count):
if thedata[k][attr_index] == target:
for l in range(0,data_length):
if l != attr_index:
dats[countx][county] = thedata[k][l]
county += 1
county = 0
countx += 1
resultdats = np.ndarray([countx, data_length-1], dtype=object)
for ix in range(0, countx):
for iy in range(0, data_length-1):
resultdats[ix][iy] = dats[ix][iy]
return resultdats
def find_results(thedata, theattributes):
# sonuclari tutacagimiz bir dizi olusturuyoruz
(dataCount, AttrCount) = np.shape(thedata)
resultIndex = find_from_attributes(theattributes, "Class")
results = np.empty([dataCount], dtype=object)
for i in range(0, dataCount):
results[i] = data[i][resultIndex]
return results
def control_results(current_results):
countt = 0
countf = 0
for i in current_results:
if i == 'True':
countt += 1
elif i == 'False':
countf += 1
if countt > 0 and countf == 0:
return True
elif countt == 0 and countf > 0:
return True
else:
return False
def tree_build(thedata, theattributes, mainattr):
# print('agaca geldi')
global class_place
treshold = 700000
current_results = find_results(thedata, theattributes)
result_ctrl = control_results(current_results)
(data_count, data_length) = np.shape(thedata)
if result_ctrl == True:
# Eger butun sonuclar True ya da False ise
return current_results[0]
elif len(theattributes) == 0:
# Attr yoksa en yaygin datayi koy
(totalData, totalAttribute) = np.shape(thedata)
clss = totalAttribute - 1
fcount = 0
tcount = 0
for j in range(0, totalData):
if thedata[j][clss] == 'True':
tcount += 1
else:
fcount += 1
if tcount > fcount:
return 'True'
else:
return 'False'
else:
# En yuksek gaini seceriz ve gideriz
index, attrb, maxgain = get_max_gain(thedata, theattributes)
# bir sozluk(node) olusturuyoruz
mytree = {attrb: {}}
for subatts in theattributes[index][1]:
# data listesi bolunuyor
subdata = divide_data(thedata, index, subatts)
# kullanilmis olan attribute listeden cikiyor
newattr = [item for item in theattributes if item[0] != attrb]
class_place = find_from_attributes(newattr, "Class")
(new_data_count, data_length) = np.shape(subdata)
if new_data_count == 0:
# Eger data yoksa
(totalData, totalAttribute) = np.shape(thedata)
clss = totalAttribute - 1
fcount = 0
tcount = 0
for j in range(0, totalData):
if thedata[j][clss] == 'True':
tcount += 1
else:
fcount += 1
if tcount > fcount:
return 'True'
else:
return 'False'
else:
# pruning
deviation = chi_square(thedata, theattributes, index)
print deviation
fcount = 0
tcount = 0
if deviation > treshold:
(totalData, totalAttribute) = np.shape(thedata)
clss = totalAttribute - 1
for j in range(0, totalData):
if thedata[j][clss] == 'True':
tcount += 1
else:
fcount += 1
if tcount > fcount:
return 'True'
else:
return 'False'
else:
# pruning olamadigi icin bolmeye devam et
subtree = tree_build(subdata, newattr, mainattr)
mytree[attrb][subatts] = subtree
return mytree
def chi_square(thedata,theattributes, attr_index):
# data,ozellikler,bolunecek ozellik
deviation = 0
# ilk olarak o anki toplam class degerlerine bakiyoruz
trcount = 0
flcount = 0
subtrcount = 0
subflcount = 0
current_results = find_results(thedata, theattributes)
for res in current_results:
if res == 'True':
trcount += 1
else:
flcount += 1
# alt ozelliklere gore datayi bolersek olacak sonuca bakiyoruz
for subatts in theattributes[attr_index][1]:
subdata = divide_data(thedata, attr_index, subatts)
current_results = find_results(thedata, theattributes)
for res in current_results:
if res == 'True':
subtrcount += 1
else:
subflcount += 1
if subtrcount > 0:
deviation += (trcount - subtrcount) * (trcount - subtrcount) / subtrcount
if subflcount > 0:
deviation += (flcount - subflcount) * (flcount - subflcount) / subflcount
return deviation
tree = tree_build(data,attributes,"Class")
print tree
print time.localtime()
# numpy ile save
np.save('my_file1.npy', tree)