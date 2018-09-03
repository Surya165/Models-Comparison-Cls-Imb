#centroid list as i/p and o/p as list of tuplels of centroid and label
import math
"""
def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)
"""
def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		d1 = instance1[x] - instance2[x]
		if d1 < 0:
			d1= d1 * (-1)
		distance += d1
	return (distance)

def labeller(d_list,c_list):
	label_list = []
	#print('size of d_list is '+str(len(d_list)))
	mitotic_list = []
	nonmitotic_list = []
	for i in range(len(d_list)):
		d_tuple = [d_list[i],0]
		label_list.append(d_tuple)

	c = len(c_list)
	d = len(d_list)
	removableList = []
	#print("dlist",d_list)
	misCount = 0
	for i in range(c):
		a = c_list[i][0]
		b = c_list[i][1]
		list1 = []
		list1.append(a)
		list1.append(b)
		prev = 9999999
		prev_index = 0
		for j in range(d):
			list2 = []
			m = d_list[j][0]
			n = d_list[j][1]
			list2.append(m)
			list2.append(n)
			Distance = euclideanDistance(list1,list2,2)
			if prev > Distance:
				prev = Distance
				prev_index = j
		if prev <= 160.0:
			misCount += 1
			label_list[prev_index][1] = 1
			mitotic_list.append(label_list[prev_index][0])
			removableList.append(label_list[prev_index][0])
			print(str(label_list[prev_index][0]) + "->" + str(label_list[prev_index][1]) + " given centroid " , (a,b) , " distance " , prev)

	#print("removableList",removableList)
	dummy_list = []
	for i in d_list:
		#print('i',i)
		if i not in removableList and ( i[0] != 584  and i[1] != 2003 ):
			dummy_list.append(i)

	#print(dummy_list)
	misCount = len(c_list) - misCount
	return (c_list,dummy_list,misCount)
