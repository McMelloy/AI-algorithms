import sys, math, collections, re, numpy
latin_letters = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
alphabet = dict(zip(range(26),sorted(latin_letters)))
weights = [list(numpy.zeros(26)),list(numpy.zeros(26)),list(numpy.zeros(26))]
bias = list(numpy.ones(3))
learning_rate = 0.5
ENG = 0
GER = 1
POL = 2

def normalize(vector):
  module = math.sqrt(sum(map(lambda x: x**2, vector)))
  return [x/module for x in vector]

def read_text(filename, language): #reads text and outputs vector of all latin letters
  letters = re.findall(r'[qwertyuiopasdfghjklzxcvbnm]', open(filename, encoding="utf-8").read().lower())
  count = collections.Counter(letters)
  letters_appearence = sorted([(letter,count[letter]) for letter in latin_letters], key=lambda t: t[0])
  return (normalize([x[1] for x in letters_appearence]),language)

def test(item):
  y = numpy.zeros(3)
  for lang in [ENG, GER, POL]:
    net = numpy.sign(sum([x*y for x,y in zip(item[0],weights[lang])]) - bias[lang])
    y[lang] = 0 if net < 0 else 1
  if y[0] == 1:
    y = 'English'
  elif y[1] == 1:
    y = 'German'
  elif y[2] == 1:
    y = 'Polish'
  else:
    y = 'Error'
  print("Expected: "+item[1])
  print("Result: "+y)

train_set = []
for lang in ['English','German','Polish']:
  for x in range(1,11):
    train_set.append(read_text('lang/'+lang+'/'+str(x)+'.txt',lang))

test_set = []
if len(sys.argv) == 1:
  for lang in ['English','German','Polish']:
    for x in range(1,4):
      test_set.append(read_text('lang.test/'+lang+'/'+str(x)+'.txt',lang))
else:
  test_set.append(read_text(sys.argv[1],'Unknown(user input)'))


error = 1
while error != 0:
  error = 0
  for lang in [ENG, GER, POL]:
    for item in train_set:
      net = sum([x*y for x,y in zip(item[0],weights[lang])]) - bias[lang]
      y = 0 if net < 0 else 1
      if lang == ENG:
        d = 1 if item[1] == 'English' else 0
      elif lang == GER:
        d = 1 if item[1] == 'German' else 0
      elif lang == POL:
        d = 1 if item[1] == 'Polish' else 0
      error = error + abs(d-y)
      weights[lang] = [w+learning_rate*(d-y)*x for w,x in zip(weights[lang],item[0])]
      bias[lang] = bias[lang] - learning_rate*(d-y)

for item in test_set:
  test(item)