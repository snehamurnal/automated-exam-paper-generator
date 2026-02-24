from pattern_analyzer import analyze_pattern

sample_text = """
SECTION - A
Q1) Define DBMS - 2 Marks
Q2. Explain normalization 5M

PART B:
4. Explain transactions (10)
5. Describe ER model : 10
"""

result = analyze_pattern(sample_text)

print(result)