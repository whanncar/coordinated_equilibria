

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



# Get list of permutations of given list s
def get_all_permutations(s):
	# Base cases
	if len(s) == 0:
		return []
	if len(s) == 1:
		return [[s[0]]]
	# Other cases
	result = []
	for i in range(len(s)):
		first = s.pop(i)
		subperms = get_all_permutations(s)
		for j in range(len(subperms)):
			result.append([first] + subperms[j])
		s.insert(i, first)
	return result



# Get product of given list s of lists
def get_list_product(s):
	# Base cases
	if len(s) == 0:
		return []
	if len(s) == 1:
		result = []
		for i in range(len(s[0])):
			result.append([s[0][i]])
		return result
	# Other cases
	result = []
	first = s.pop(0)
	subproduct = get_list_product(s)
	for i in range(len(first)):
		for j in range(len(subproduct)):
			point = [first[i]]
			for k in range(len(subproduct[j])):
				point.append(subproduct[j][k])
			result.append(point)
	return result
			




# Get transpose of matrix m
def get_transpose(m):
	result = []
	# Get dimensions of m
	old_num_rows = len(m)
	old_num_cols = len(m[0])
	# Set dimensions of m transpose
	num_rows = old_num_cols
	num_cols = old_num_rows
	# Populate m transpose
	for i in range(num_rows):
		result.append([])
		for j in range(num_cols):
			result[-1].append(m[j][i])
	return result

