import itertools
import sys
import random
from collections import defaultdict

s = ''
with open("b_lovely_landscapes.txt") as f:
  s = f.read()

s = s.split('\n')[1:]
s = [(str(i), l.split(' ')) for i, l in enumerate(s)]

tags = set.union(*[set(t) for i, t in s])

slides = {i: set(l[2:]) for (i, l) in s}
slide_names = list(slides.keys())

slides_by_tag = defaultdict(int)
for s in slide_names:
  for t in slides[s]:
    slides_by_tag[t] += 1

relevant_tags = set(t for t in slides_by_tag.keys() if slides_by_tag[t] > 1)
relevant_slides = [s & relevant_tags for s in slides]

final = []

def uniq(l1, l2):
  return len(set(l1 + l2))

verts = {}


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

print(score(slide_names))
