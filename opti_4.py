import itertools
import sys
import random
from collections import defaultdict

s = ''
with open("b_lovely_landscapes.txt") as f:
  s = f.read()

s = s.split('\n')[1:-1]
s = [(str(i), l.split(' ')) for i, l in enumerate(s)]
print(len(s))

tags = set.union(*[set(t) for i, t in s])

slides = {i: set(l[2:]) for (i, l) in s}
slide_names = list(slides.keys())

slides_by_tag = defaultdict(set)
for s in slide_names:
  for t in slides[s]:
    slides_by_tag[t].add(s)

final = []

relevant_tags = set(t for t in slides_by_tag.keys() if len(slides_by_tag[t]) > 1)
relevant_slides = {i: slides[i] & relevant_tags for i in slide_names}
relevant_slides = {i: relevant_slides[i] for i in relevant_slides.keys() if len(relevant_slides[i]) > 0}
current = next(iter(relevant_slides.keys()))
slides_used = set()
slides_not_used = set(relevant_slides.keys())

try:
  while len(slides_not_used) > 0:
    final.append(current)
    slides_used.add(current)
    slides_not_used.remove(current)
    next_possibilites = set.union(*(slides_by_tag[t] for t in relevant_slides[current])) - slides_used
    if len(next_possibilites) > 0:
      current = next(iter(next_possibilites))
    else:
      current = next(iter(slides_not_used))
except StopIteration:
  pass


def score_2(k1, k2):
  s1_tags = slides[k1]
  s2_tags = slides[k2]
  return min(len(s1_tags - s2_tags), len(s1_tags & s2_tags), len(s2_tags - s1_tags))


def score(names):
  s = 0
  for i in range(0, len(names) - 1):
    s1 = names[i]
    s2 = names[i+1]
    s1_tags = slides[s1]
    s2_tags = slides[s2]
    s += min(len(s1_tags - s2_tags), len(s1_tags & s2_tags), len(s2_tags - s1_tags))
  return s

print(score(final))

with open("b_sols", "w") as f:
  f.write("%d\n" % len(final))
  for name in final:
    f.write(name + "\n")