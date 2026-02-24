import re

def analyze_pattern(text):
    lines = text.split("\n")
    
    pattern_data = {
        "sections": {},
        "total_marks_distribution": {},
        "internal_choices": 0
    }

    current_section = None

    for line in lines:
        line = line.strip()

        # Detect Section (like "Section A")
        section_match = re.match(
    r"(SECTION|PART)\s*[-:]?\s*([A-Z])",
    line,
    re.IGNORECASE
)
        if section_match:
            current_section = section_match.group(2).upper()
            pattern_data["sections"][current_section] = {
                "questions": 0,
                "marks_distribution": {}
            }
            continue

        # Detect multiple mark formats
        marks_match = re.search(
            r"\((\d+)\)|\[(\d+)\]|(\d+)\s*Marks?|(\d+)\s*M\b|[-:]\s*(\d+)",
            line,
            re.IGNORECASE
        )

        if marks_match and current_section:
            # Extract whichever group matched
            mark = next(int(group) for group in marks_match.groups() if group)

            pattern_data["sections"][current_section]["questions"] += 1

            # Section-wise distribution
            section_dist = pattern_data["sections"][current_section]["marks_distribution"]
            section_dist[mark] = section_dist.get(mark, 0) + 1

            # Overall distribution
            overall_dist = pattern_data["total_marks_distribution"]
            overall_dist[mark] = overall_dist.get(mark, 0) + 1

        # Detect internal choice (OR)
        if re.search(r"\bOR\b", line, re.IGNORECASE):
            pattern_data["internal_choices"] += 1

    return pattern_data