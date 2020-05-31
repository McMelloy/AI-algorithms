import collections, numpy
train_data = []
test_data = []
outcomes = {"unacc": 0, "acc": 0, "good": 0, "vgood": 0}
outcomes_probability = {"unacc": 0, "acc": 0, "good": 0, "vgood": 0} # for determining which is the highest
d = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0} # number of possible attributes of value (for each column)
predicted_actual = [numpy.zeros(4),numpy.zeros(4),numpy.zeros(4),numpy.zeros(4)] # table for classifier evaluation

# aux methods

def probability(outcome): # probability of outcome(unacc/acc/good/vgood) in all data
  return outcomes[outcome]/len(train_data)

def probability_param(column, param, outcome): # probability of outcome if the column(e.g column 2) has certain parameter(e.g 'vhigh')
  count = 0
  for line in train_data:
    if line[column] == param and line[6] == outcome:
      count += 1
  if count == 0:
    return (count + 1)/(outcomes[outcome] + d[column])
  return count/outcomes[outcome]

def find_max_probability(): # determining which of outcomes has the highest possibility for test data
  max_value = max(outcomes_probability.values())
  return list(outcomes_probability.keys())[list(outcomes_probability.values()).index(max_value)]

# Forming data

file = open("car.data", "r")          
for line in file:
  values = line.rstrip('\n').split(',')
  train_data.append(values)
  outcomes[values[-1]] += 1
file.close()

file = open("car.test.data", "r")
for line in file:
  values = line.rstrip('\n').split(',')
  test_data.append(values)
file.close()

for column in range(6):
  count = collections.Counter([x[column] for x in train_data])
  d[column] = len(count)

# classifying process

for line in test_data:
  for outcome in outcomes.keys():
    p = probability(outcome)
    for column in range(len(line)-1):
      p *= probability_param(column, line[column], outcome)
    outcomes_probability[outcome] = p

  denominator = sum(outcomes_probability.values())
  for outcome in outcomes.keys():
    outcomes_probability[outcome] /= denominator

  predicted_outcome = find_max_probability()
  #print(outcomes_probability)
  #print(predicted_outcome)
  predicted_actual [list(outcomes.keys()).index(predicted_outcome)][list(outcomes.keys()).index(line[6])] += 1 

# Evaluating classifier 

outcomes_index = {"unacc": 0, "acc": 1, "good": 2, "vgood": 3}
print("\n'Predicted-Actual' Table\n" + str(predicted_actual))

ACCURACY = sum([predicted_actual[i][i] for i in range(4)])/sum(sum(predicted_actual))
print("\nAccuracy\n" + str(ACCURACY))

OUTCOMES_PRECISION = {"unacc": 0, "acc": 0, "good": 0, "vgood": 0}
OUTCOMES_RECALL = {"unacc": 0, "acc": 0, "good": 0, "vgood": 0}
OUTCOMES_F = {"unacc": 0, "acc": 0, "good": 0, "vgood": 0}

for outcome in outcomes_index:
  OUTCOMES_PRECISION[outcome] = predicted_actual[outcomes_index[outcome]][outcomes_index[outcome]]/sum([predicted_actual[i][outcomes_index[outcome]] for i in range(4)])
  OUTCOMES_RECALL[outcome] = predicted_actual[outcomes_index[outcome]][outcomes_index[outcome]]/sum([predicted_actual[outcomes_index[outcome]][i] for i in range(4)])
  OUTCOMES_F[outcome] = 2 * OUTCOMES_PRECISION[outcome] * OUTCOMES_RECALL[outcome] / (OUTCOMES_PRECISION[outcome] + OUTCOMES_RECALL[outcome])

print("\nPrecision\n" + str(OUTCOMES_PRECISION))
print("\nRecall\n" + str(OUTCOMES_RECALL))
print("\nF-Measure\n" + str(OUTCOMES_F))
