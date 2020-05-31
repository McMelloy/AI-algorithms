import sys, math, collections
train_set = []
test_set = []
k = int(sys.argv[1])
train_file = str(sys.argv[2])

file = open(train_file, "r")                                ## reading training set
for line in file:
  train_set.append(line.rstrip('\n').split(','))
file.close()

if len(sys.argv) == 4:                                      ## if we have file with test set
  test_file = str(sys.argv[3])
  file = open(test_file, "r")
  for line in file:
    test_set.append(line.rstrip('\n').split(','))
  file.close()
else:                                                       ## if not - ask for vector
  print('Please input 4D vector, e.g \'5.1,3.5,1.4,0.2\'')
  test_set.append(input().split(','))

for te_set in test_set:
  distance = dict.fromkeys(range(105)) ## storing distance to all neighbors
  i = 0
  for tr_set in train_set: 
    curr_dist = math.sqrt((float(tr_set[0])-float(te_set[0]))**2+(float(tr_set[1])-float(te_set[1]))**2
    +(float(tr_set[2])-float(te_set[2]))**2+(float(tr_set[3])-float(te_set[3]))**2)
    distance[i] = curr_dist
    i+=1

  distance = collections.OrderedDict(sorted(distance.items(), key=lambda t: t[1],reverse=True)) ## sorting to find out which neighbors are nearest

  types = []
  for it in range(k):
    types.append(train_set[distance.popitem()[0]][4]) ## storing types of k nearest neighbors

  print()
  print('Estimated type: '+te_set[4])
  print('Computed type: '+collections.Counter(types).most_common()[0][0]) ## taking the most common type in k nearest neighbors