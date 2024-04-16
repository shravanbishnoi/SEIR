# Search Engine and Information Retrieval Course
Explore my Search Engine and Information Retrieval course repository! Dive into assignments reinforcing theory and projects applying practical skills. Contribute and collaborate to enhance this learning hub. 
🚀 #InformationRetrieval #SearchEngine

This repository is organized to showcase my work throughout the course, and it will be regularly updated with new assignments and projects.

## Course Advisor: Dr. Amit Singhal (Computer Scientist, Founder Sitare University)

## Table of Contents
- In this course we will learn how do search engines work and retrieve user satisfiable information when queried.
    - Architecture of a Search Engine
        - Text Acquisition
        - Text Transformation
        - Index Creation
        - Ranking
        - User Interaction
        - Evaluation
     - Crawls and feeds
     - Processing text
        - Tokenization
        - Stop words
        - Stemming
        - POS tagging
        - N-Grams
        - Page Ranks
     - Ranking and Indexes
        - Inverted Indices
        - Compression
        - Encoding
        - Skip Pointers
        - Merging
        - Map Reduce
      - Queries and Interfaces
      - MRS
        - Scoring
        - Term weighting
        - Vector Space Model
        - Document length normalisation
       - Evalution
        - Relevance
        - Pooling
        - Query logs
        - Efficiency metrics
        - Significance tests
          
## Assignments:
    - Relevance Assessment

## About the Course

This course covers various aspects of search engines, information retrieval, and related topics. It includes theoretical concepts as well as hands-on assignments and projects to deepen understanding and practical skills.

## Projects

1. Webpage Python Project (projects/Webpage Python Project/):
   Write a python program that takes a URL on the command line, fetches the page, and outputs (as clearly demarked sections)
    - Page Title (without any HTML tags)
    - Page Body (without any html tags)
    - All the URLs that the page points/links to
    - Don't use any HTML parsing libraries, do Python from scratch
2. Web-document Similarity project
    - Count the frequency of every word (a word is a sequence of alphanumeric characters, case does NOT matter) in the body of your document.
    - Write a 64 bit hash function for a word using polynomial rolling hash function.
       hash(s) = s[0] + s[1].p  + s[2].
       p^2   + ..... + s[n-1].p^(n-1)   mod m
    - Here s[i] is the ASCII for letter i in a word, use p = 53 and m = 2^64
    - Compute Simhash for the document.
    - Modify your program to take two URLs from the web on the command line, print how many bits are common in their simhashes.
