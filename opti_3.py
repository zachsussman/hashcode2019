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

def get_by_tags(slide_names, depth):
  if depth >= 5:
    return slide_names
  slides_by_tag = defaultdict(int)
  for s in slide_names:
    for t in slides[s]:
      slides_by_tag[t] += 1
  most_common = max(list(slides_by_tag.keys()), key=lambda t: slides_by_tag[t])
  l1 = [s for s in slide_names if most_common in slides[s]]
  l2 = [s for s in slide_names if most_common not in slides[s]]
  if len(l1) == len(slide_names):
    return slide_names
  elif len(l1) == 0:
    return slide_names
  else:
    print("%d slides have tag %s" % (len(l1), most_common))
    return get_by_tags(l1, depth + 1) + get_by_tags(l2, depth + 1)

slide_names = get_by_tags(slide_names, 1)


def score_2(k1, k2):
  s1_tags = slides[k1]
  s2_tags = slides[k2]
  return min(len(s1_tags - s2_tags), len(s1_tags & s2_tags), len(s2_tags - s1_tags))


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

print(score(slide_names))

# with open("c_sols_3", "w") as f:
#   f.write("%d\n" % len(slide_names))
#   for name in slide_names:
#     f.write(name + "\n")