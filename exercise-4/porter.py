def tokenize(text):
  return text.split()

# call this using is_consonant(word, i)
def is_consonant(word, index):
	if word[index] in ['a', 'e', 'i', 'o', 'u']:
		return False
	if word[index] == 'y':
		if index == 0:
			return True
		else:
			return not is_consonant(word, index - 1)
	return True


def is_vowel(word, index):
	return not is_consonant(word, index)


def measure(word):
	cvs = ""
	for i in range(len(word)):
		if is_consonant(word, i):
			cvs = cvs + "c"
		else:
			cvs = cvs + "v"

	return cvs.count("vc")


def contains_vowel(word):
	for index in range(len(word)):
		if not is_consonant(word, index):
			return True
	return False


def ends_in_double_consonant(word):
	if len(word) >= 2 and is_consonant(word, len(word) - 1):
		if word[-1] == word[-2]:
			return True
	return False


def ends_in_cvc(word):
	if len(word) >= 3:
		if is_consonant(word, len(word) - 3) and not is_consonant(word, len(word) - 2) and is_consonant(word, len(word) - 1) and word[-1] not in ['w', 'x', 'y']:
			return True
	return False

def replace(word, suffix, replacement):
  return word[:-len(suffix)] + replacement

def ends(word, suffix):
  return word[-len(suffix):] == suffix


def step_1a(word):

  if word[-4:] == "sses":
    # remember, Porter algorithm matches
    # the longest suffix in each step
    # and then finishes the step
    # without checking the other rules
    return word[:-4] + "ss"
  elif word[-3:] == "ies":
    return word[:-3] + "i"
  elif word[-2:] == "ss":
    return word
  elif word[-1:] == "s":
    return word[:-1]

  return word

def step_1b(word):

  if ends(word, "eed"):
    if measure(word[:-3]) > 0:
      return replace(word, "eed", "ee")
    else:
      return word
  elif ends(word, "ed"):
    if contains_vowel(word[:-2]):
      stem = replace(word, "ed", "")
      return step_1b_helper(stem)
    else:
      return word
  elif ends(word, "ing"):
    if contains_vowel(word[:-3]):
      stem = replace(word, "ing", "")
      return step_1b_helper(stem)
    else:
      return word

  return word

def step_1b_helper(word):

  # notice how we're iterating through a list of lists here
  for suffix_pair in [ [ "at", "ate" ],
                       [ "bl", "ble" ],
                       [ "iz", "ize" ] ]:
    suffix = suffix_pair[0]
    replacement = suffix_pair[1]
    if ends(word, suffix):
      return replace(word, suffix, replacement)

  if ends_in_double_consonant(word) and word[len(word) - 1] not in [ "l", "s", "z"]:
    return word[:-1]

  if measure(word) == 1 and ends_in_cvc(word):
    return word + "e"

  return word

def step_1c(word):
  if word[-1] == "y":
    if contains_vowel(word[:-1]):
      return replace(word, "y", "i")

  return word

def step_2(word):
  for suffix_pair in [ [ "ational", "ate" ],
                       [ "tional", "tion" ],
					             [ "enci", "ence" ],
					             [ "anci", "ance" ],
					             [ "izer", "ize" ],
					             [ "abli", "able" ],
					             [ "alli", "al" ],
					             [ "entli", "ent" ],
					             [ "eli", "e" ],
			          		   [ "ousli", "ous" ],
			          		   [ "ization", "ize" ],
		          			   [ "ation", "ate" ],
			          		   [ "ator", "ate" ],
			          		   [ "alism", "al" ],
				          	   [ "iveness", "ive" ],
				          	   [ "fulness", "ful" ],
				          	   [ "ousness", "ous" ],
				          	   [ "aliti", "al" ],
				          	   [ "iviti", "ive" ],
                       [ "biliti", "ble" ] ]:
    suffix = suffix_pair[0]
    replacement = suffix_pair[1]
    if ends(word, suffix):
      if measure(word[:-len(suffix)]) > 0:
        return replace(word, suffix, replacement)
  return word

def step_3(word):
  for suffix_pair in [ [ "icate", "ic" ],
                       [ "ative", "" ],
					             [ "alize", "al" ],
					             [ "iciti", "ic" ],
					             [ "ical", "ic" ],
					             [ "ful", "" ],
                       [ "ness", "" ] ]:
    suffix = suffix_pair[0]
    replacement = suffix_pair[1]
    if ends(word, suffix):
      if measure(word[:-len(suffix)]) > 0:
        return replace(word, suffix, replacement)
  return word

def step_4(word):
  for suffix_pair in [ [ "al", "" ],
                       [ "ance", "" ],
					             [ "ence", "" ],
					             [ "er", "" ],
					             [ "ic", "" ],
					             [ "able", "" ],
					             [ "ible", "" ],
					             [ "ant", "" ],
					             [ "ement", "" ],
			          		   [ "ment", "" ],
			          		   [ "ent", "" ],
		          			   [ "ou", "" ],
			          		   [ "ism", "" ],
			          		   [ "ate", "" ],
				          	   [ "iti", "" ],
				          	   [ "ous", "" ],
				          	   [ "ive", "" ],
                       [ "ize", "" ] ]:
    suffix = suffix_pair[0]
    replacement = suffix_pair[1]
    if ends(word, "ion") and word[-4] in ["s", "t"]:
      if measure(word[:-len(suffix)]) > 1:
        return replace(word, "ion", "")
    elif ends(word, suffix):
      if measure(word[:-len(suffix)]) > 1:
        return replace(word, suffix, replacement)
  return word

def step_5a(word):
  if word[-1] == "e":
    if measure(word[:-1]) > 1:
      return word[:-1]
    elif measure(word[:-1]) == 1:
      if not ends_in_cvc(word[:-1]):
        return word[:-1]
  return word

def step_5b(word):
  if measure(word[:-1]) > 1 and ends_in_double_consonant(word) and word[-1] == "l":
    return word[:-1]
  return word

def stem(word):
  stem = step_1a(word)
  stem = step_1b(stem)
  stem = step_1c(stem)
  stem = step_2(stem)
  stem = step_3(stem)
  stem = step_4(stem)
  stem = step_5a(stem)
  stem = step_5b(stem)

  return stem

result = [ { word : stem(word) } for word in tokenize("I agreed with the greatest minds of my generalization destroyed by caresses")]
print(result)
