# Suffixtrees
A C code that implements suffix trees.
Given a set of documents, the code builds a suffix tree to perform the following operations.

1)List all the occurrences of a query-string in the set of documents.

2)List only the first occurrence of a given query-string in every document. If the query-string is not present, find the first occurrence of the longest substring of the query-string.
3)For a given query-string (query of words), list the documents ranked by the relevance.Stories that have exact query string have highest rank.Stories that have all words of querystring have higher relevance than those which have a subset of the words.

