import itertools
import sys
import random
from collections import defaultdict

s = ''
with open("d_pet_pictures.txt") as f:
  s = f.read()

s = s.split('\n')[1:]
s = [(str(i), l.split(' ')) for i, l in enumerate(s)]

tags = set.union(*[set(t) for i, t in s])

vert_images = {i: set(l[2:]) for (i, l) in s if l[0] == "V"}
horiz = {i: set(l[2:]) for (i, l) in s if l[0] == "H"}
print(len(vert_images))

seed = 13401359
def next_rand():
  global seed
  seed = (seed * 22695477 + 1) % 2**32
  return seed

def uniq(l1, l2):
  return len(set(l1 + l2))

verts = {}

def similarity(l1, l2):
  return len(l1 & l2)

def make_scorer(f):
  def scorer(lst):
    score = 0
    for i in range(0, len(lst) - 1):
      score += f(lst[i], lst[i+1])
    return score
  return scorer

def local_order(lst, scorer):
  q_max = None
  q_max_score = 0
  for q in itertools.permutations(lst):
    q_score = scorer(q)
    if q_score > q_max_score:
      q_max_score = q_score
      q_max = q
  return q

def local_opti(lst, n, scorer):
  for i in range(0, len(lst) - n + 1):
    lst[i:i+n] = local_order(lst[i:i+n], scorer)
  return lst

def score(names):
  s = 0
  for i in range(0, len(names) - 1):
    s1 = names[i]
    s2 = names[i+1]
    s1_tags = slides[s1]
    s2_tags = slides[s2]
    s += min(len(s1_tags - s2_tags), len(s1_tags & s2_tags), len(s2_tags - s1_tags))
  return s


def pair_verts():
  vert_keys = list(vert_images.keys())
  vert_keys.sort(key=lambda i: len(vert_images[i]))
  def score(i1, i2):
    return similarity(vert_images[i1], vert_images[i2])
  local_opti(vert_keys, 5, make_scorer(score))
  
  for i in range(0, len(vert_keys) // 2):
    k1 = vert_keys[i]
    k2 = vert_keys[-i-1]
    verts[k1 + " " + k2] = vert_images[k1] | vert_images[k2]
    
pair_verts()

print(len(verts))
print("verticals paired")

slides = dict(horiz, **verts)
slide_names = list(slides.keys())

print("before opti: %d\n" % score(slide_names))

finals = [""] * len(slide_names)

def score_2(k1, k2):
  s1_tags = slides[k1]
  s2_tags = slides[k2]
  return min(len(s1_tags - s2_tags), len(s1_tags & s2_tags), len(s2_tags - s1_tags))

finals[0] = slide_names[0]
slides_used = defaultdict(bool)
slides_used[finals[0]] = True
for index in range(1, len(slide_names)):
  s1 = finals[index - 1]
  max_score = 0
  max_name = ''
  for j in range(0, 100):
    new_i = 0
    while slides_used[slide_names[new_i]]:
      new_i = random.randint(1, len(slide_names) - 1)
      # new_i = (next_rand() % (len(slide_names) - 2)) + 1
    s2 = slide_names[new_i]
    if score_2(s1, s2) > max_score:
      max_score = score_2(s1, s2)
      max_name = s2
  if max_name == '':
    for s in slide_names:
      if not slides_used[s]:
        max_name = s
        break
  finals[index] = max_name
  slides_used[max_name] = True




# local_opti(slide_names, 5, score)

# for i in range(0, len(slide_names) - 1):
#   max_next = score_2(slide_names[i], slide_names[i+1])
#   max_index = i+1
#   for j in range(i+2, min(i+1001, len(slide_names))):
#     if score_2(slide_names[i], slide_names[j]) > max_next:
#       max_next = score_2(slide_names[i], slide_names[j])
#       max_index = j
#   tmp = slide_names[i+1]
#   slide_names[i+1] = slide_names[j]
#   slide_names[j] = tmp

print(score(finals))

with open("d_sols_3", "w") as f:
  f.write("%d\n" % len(finals))
  for name in finals:
    f.write(name + "\n")