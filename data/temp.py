from pattern_analyzer import Pattern

text = """
SECTION A
Attempt any 2 questions.
Q1) Define DBMS - 2 Marks
Q2) Explain normalization 5M
OR

PART B
Answer all questions.
Q3) Explain transactions (10)
"""

p = Pattern(text)
p.analyze()
print(p.summary())