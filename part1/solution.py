import re
import sys
from pg_sample_texts import DIV_COMM, MAG_CART
 
documents = [DIV_COMM, MAG_CART]
 
# PREPARE OUR REGEXES FOR METADATA SEARCHES #
title_search = re.compile(r"""
                          (?:title:\s*) #look for 'title: ' in the original text.
                          (?P<title>        #then capture the following group which we'll
                                            #call title and can access with that name later
 
                          (                 #title consists of words, which are
                            (
                              \S*           #one or more non-white spaces
                              (\ )?         #followed by zero or 1 spaces 
                                            # note how we have to use a slash to escape
                                            # the space character, since re.VERBOSE mode ignores
                                            # unescaped whitespace in your pattern.
 
                            )+              # title has 1 or more such words
                          )
                          (                 #and this set of words can optionally be followed
                            (\n(\ )+)       #by a new line character, plus a few spaces
                            (\S*(\ )?)*     #and then one or more additional words
                          )*                #and this * means the title can encompass
                          )""",             #however many extra lines we need
                          re.IGNORECASE | re.VERBOSE)  #note the #appearance of | above. 
                                            #This allows us to set multiple flags to our regex. 
                                            #See: http://docs.python.org/dev/howto/regex.html#compilation-flags
author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)
illustrator_search = re.compile(r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)
 
#prepare regexes for user supplied keywords
kws = dict.fromkeys([kw for kw in sys.argv[1:]], None) 
 
#compile your regex patterns
for kw in kws:
  kws[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE) 
                                  #border the kw with boundary chars
                                  #and set 'pattern' for this kw to comp
                                  #we'll also ignore case, so we can match
                                  # whether or not search word appears as first
                                  # word in sentence.
 
# Now we'll iterate over our documents and report on them
# In what follows, remember that if our metadata searches come up empty
# they will have a value of None. Since None evaluates to False in if statements
# we can test if, say, author has a non-none value, and if it does, we'll
# reassign author to be the string that was pulled in by the author group
# and we'll print this at the end. Otherwise, we'll retain the value of None
# for this variable.
for i,doc in enumerate(documents):
  author = re.search(author_search, doc)
  if author:
    author = author.group('author')
  translator = re.search(translator_search, doc)
  if translator:
    translator = translator.group('translator')
  illustrator = re.search(illustrator_search, doc)
  if illustrator:
    illustrator = illustrator.group('illustrator')
  title = re.search(title_search, doc).group('title')
  print "***" * 25
  print "Here's the info for doc {}:".format(i)
  print "Title:  {}".format(author)
  print "Author(s): {}".format(title)
  print "Translator(s): {}".format(translator)
  print "Illustrator(s): {}".format(illustrator)
  print "\n****KEYWORD REPORT****\n\n"
  for kw in kws:
    print "\"{0}\": {1}".format(kw, len(re.findall(kws[kw], doc)))
  print '\n\n'