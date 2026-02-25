import re

class Pattern:
    def __init__(self, text):
        self.text = text
        self.sections = {}
        self.total_marks_distribution = {}
        self.internal_choices = 0
        self.attempt_rule = None

    def analyze(self):
        lines = self.text.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()

            # Detect section (SECTION A, PART-B, etc.)
            section_match = re.match(
                r"(SECTION|PART)\s*[-:]?\s*([A-Z])",
                line,
                re.IGNORECASE
            )
            if section_match:
                current_section = section_match.group(2).upper()
                self.sections[current_section] = {
                    "questions": 0,
                    "marks_distribution": {}
                }
                continue

            # Detect attempt rules
            if re.search(r"(Attempt|Answer)\s+(any|all)", line, re.IGNORECASE):
                self.attempt_rule = line

            # Detect OR
            if re.search(r"\bOR\b", line, re.IGNORECASE):
                self.internal_choices += 1

            # Detect marks (multiple formats)
            marks_match = re.search(
                r"\((\d+)\)|\[(\d+)\]|(\d+)\s*Marks?|(\d+)\s*M\b|[-:]\s*(\d+)",
                line,
                re.IGNORECASE
            )

            if marks_match and current_section:
                mark = next(int(g) for g in marks_match.groups() if g)

                self.sections[current_section]["questions"] += 1

                sec_dist = self.sections[current_section]["marks_distribution"]
                sec_dist[mark] = sec_dist.get(mark, 0) + 1

                self.total_marks_distribution[mark] = (
                    self.total_marks_distribution.get(mark, 0) + 1
                )

    def summary(self):
        return {
            "sections": self.sections,
            "total_marks_distribution": self.total_marks_distribution,
            "internal_choices": self.internal_choices,
            "attempt_rule": self.attempt_rule
        }