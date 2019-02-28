s = ''
with open("../d_pet_pictures.txt") as f:
  s = f.read()

s = s.split('\n')[1:]
s = [(str(i), l.split(' ')) for i, l in enumerate(s)]
vert_images = {i: l[2:] for (i, l) in s if l[0] == "V"}
horiz = {i: l[2:] for (i, l) in s if l[0] == "V"}

def uniq(l1, l2):
  return len(set(l1 + l2))

verts = {}

def pair_verts():
  used = set()
  for i in vert_images:
    max_index = ""
    max_tags = 0
    for j in vert_images:
      tag_count = uniq(vert_images[i], vert_images[j])
      if tag_count > max_tags:
        max_tags = tag_count
        max_index = j
    verts[i + " " + j] = list(set(vert_images[i] + vert_images[j]))
    used.add(i)
    used.add(j)

pair_verts()

slides = dict(horiz, **verts)
slide_names = list(slides.keys())
slide_names.sort(key=lambda k: len(slides[k]))

def score(names):
  s = 0
  for i in range(0, len(names) - 1):
    s1 = names[i]
    s2 = names[i+1]
    s1_tags = set(slides[s1])
    s2_tags = set(slides[s2])
    s += min(len(s1_tags - s2_tags), len(s1_tags & s2_tags), len(s2_tags - s1_tags))
  return s

print(score(slide_names))