import sys, math, collections
train_set = []
test_set = []
learning_rate = float(sys.argv[1])
dim = 4
weights = [0 for i in range(dim)]
bias = 1

train_file = str(sys.argv[2])
file = open(train_file, "r")          
for line in file:
  values = line.rstrip('\n').split(',')
  train_set.append(([float(x) for x in values[:dim]], values[dim]))
file.close()


if len(sys.argv) == 4:                                      ## if we have file with test set
  test_file = str(sys.argv[3])
  file = open(test_file, "r")
  for line in file:
    values = line.rstrip('\n').split(',')
    test_set.append(([float(x) for x in values[:dim]], values[dim]))
  file.close()
else:                                                       ## if not - ask for vector
  print('Our dimension is '+ str(dim) + '. Please input vector and type to estimate, e.g \'5.6,3.0,4.5,1.5,Iris-versicolor\'')
  values = input().rstrip('\n').split(',')
  test_set.append(([float(x) for x in values[:dim]], values[dim]))

error = 1
while error != 0:
  #print("////////////////")
  error = 0
  for item in train_set:
    net = sum([x*y for x,y in zip(item[0],weights)]) - bias
    y = 0 if net < 0 else 1
    d = 0 if item[1] == 'Iris-setosa' else 1
    error = error + abs(d-y)
    weights = [w+learning_rate*(d-y)*x for w,x in zip(weights,item[0])]
    bias = bias - learning_rate*(d-y)
  #print("New error "+str(error))

for item in test_set:
  net = sum([x*y for x,y in zip(item[0],weights)]) - bias
  y = 'Iris-setosa' if net < 0 else 'Iris-versicolor'
  print("////////////////")
  print("Expected: "+item[1])
  print("Got: "+y)