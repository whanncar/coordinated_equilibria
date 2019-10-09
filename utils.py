

# Get k-tuples of elements of s
def get_ordered_tuples(s, k):

  result = []

  if k == 1:
    for x in s:
      y = []
      y.append(x)
      result.append(y)
    return result

  for x in s:
    smaller = get_ordered_tuples(s, k - 1)
    for y in smaller:
      y.append(x)
      result.append(y)
  return result

