import sys, math, collections, random
iris_set = [] # each iris is: [([coordinates],class), centroid]
centroids = [] 
k = int(sys.argv[1])

# aux methods

def distance(coordinates1, coordinates2):
  dist = [a - b for a, b in zip(coordinates1, coordinates2)]
  dist = sum(map(lambda x:x*x,dist))
  return math.sqrt(dist)

def find_nearest(coordinates):
  curr_min = sys.maxsize
  curr_nearest = 0
  for centroid in centroids:
    dist = distance(centroid, coordinates)
    if dist < curr_min:
      curr_min = dist
      curr_nearest = centroids.index(centroid)
  return curr_nearest

def adjust_centoid(centroid):
  centroid_index = centroids.index(centroid)
  all_assigned = []
  for iris in iris_set:
    if iris[1] == centroid_index:
      all_assigned.append(iris[0][0])
  if(len(all_assigned)>0):
    centroids[centroid_index] = [round(sum(column)/len(all_assigned),8) for column in zip(*all_assigned)]

def print_all():
  for iris in iris_set:
    print(str(iris_set.index(iris)) + " assigned to " + str(iris[1]) + ", distance = " + str(distance(iris[0][0],centroids[iris[1]])))

def print_rand():
  iris = iris_set[random.randint(0,len(iris_set))]
  print(str(iris_set.index(iris)) + " assigned to " + str(iris[1]))
  for i in range(k):
    print( "Distance to " + str(i) + " = " + str(distance(iris[0][0],centroids[i])))

def print_homogenity():
  for i in range(k):
    print()
    all_assigned = []
    for iris in iris_set:
      if iris[1] == i:
        all_assigned.append(iris[0][1])
    print(str(i) + " -> " + str(collections.Counter(all_assigned)))

# Forming data

file = open("irisORIG.data", "r")          
for line in file:
  values = line.rstrip('\n').split(',')
  iris_set.append([([float(x) for x in values[:-1]], values[-1]), k])
file.close()

for i in range(k):
  centroids.append(iris_set[random.randint(0,len(iris_set)-1)][0][0])

# Doing iterations

print(centroids)

changeCountdown = 2
while changeCountdown>0:
  changedIn = False
  for iris in iris_set:
    new_nearest = find_nearest(iris[0][0])
    if new_nearest != iris[1]:
      changedIn = True
      iris[1] = new_nearest
  if changedIn:
    changeCountdown = 2
    for centroid in centroids:
      adjust_centoid(centroid)
  if not changedIn:
    changeCountdown = changeCountdown - 1
  print_all()
  
print(centroids) 
print_homogenity()

    

