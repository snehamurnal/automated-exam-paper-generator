import re
from collections import defaultdict


class PaperAnalyzer:
    """
    Analyzes question paper text and extracts:
    - Section-wise question count
    - Marks distribution per section
    - Total marks distribution
    - Internal choices (OR detection)
    """

    # -------------------------
    # Precompiled Regex Patterns
    # -------------------------

    SECTION_PATTERN = re.compile(
        r"(SECTION|PART)\s*[-:]?\s*([A-Z])",
        re.IGNORECASE
    )

    MARKS_PATTERN = re.compile(
        r"\((\d+)\)|\[(\d+)\]|(\d+)\s*Marks?|(\d+)\s*M\b|[-:]\s*(\d+)",
        re.IGNORECASE
    )

    ATTEMPT_PATTERN = re.compile(
        r"(Attempt|Answer)\s+(any|all)",
        re.IGNORECASE
    )

    OR_PATTERN = re.compile(r"\bOR\b", re.IGNORECASE)

    # -------------------------
    # Constructor
    # -------------------------

    def __init__(self, text):
        self.text = text
        self.sections = {}
        self.total_marks_distribution = defaultdict(int)
        self.internal_choices = 0

    # -------------------------
    # Public Method
    # -------------------------

    def analyze(self):
        current_section = None

        for line in self.text.split("\n"):
            line = line.strip()
            if not line:
                continue

            # Detect Section
            section = self._detect_section(line)
            if section:
                current_section = section
                continue

            # Detect Attempt Instructions
            self._detect_attempt_instruction(line)

            # Detect OR
            if self._detect_or(line):
                self.internal_choices += 1

            # Detect Marks
            mark = self._detect_marks(line)
            if mark and current_section:
                self._update_distributions(current_section, mark)

        return self._generate_output()

    # -------------------------
    # Detection Methods
    # -------------------------

    def _detect_section(self, line):
        match = self.SECTION_PATTERN.match(line)
        if match:
            section_name = match.group(2).upper()

            if section_name not in self.sections:
                self.sections[section_name] = {
                    "questions": 0,
                    "marks_distribution": defaultdict(int)
                }

            return section_name
        return None

    def _detect_marks(self, line):
        match = self.MARKS_PATTERN.search(line)
        if match:
            for group in match.groups():
                if group:
                    return int(group)
        return None

    def _detect_attempt_instruction(self, line):
        # Future scope: store attempt rules
        if self.ATTEMPT_PATTERN.search(line):
            pass

    def _detect_or(self, line):
        return bool(self.OR_PATTERN.search(line))

    # -------------------------
    # Update Logic
    # -------------------------

    def _update_distributions(self, section, mark):
        section_obj = self.sections[section]

        section_obj["questions"] += 1
        section_obj["marks_distribution"][mark] += 1
        self.total_marks_distribution[mark] += 1

    # -------------------------
    # Output Formatting
    # -------------------------

    def _generate_output(self):
        return {
            "sections": {
                sec: {
                    "questions": data["questions"],
                    "marks_distribution": dict(data["marks_distribution"])
                }
                for sec, data in self.sections.items()
            },
            "total_marks_distribution": dict(self.total_marks_distribution),
            "internal_choices": self.internal_choices
        }


# -------------------------
# Example Usage
# -------------------------

if __name__ == "__main__":
    sample_text = """
    SECTION A
    Q1. Define AI. (2 Marks)
    Q2. Explain ML. (5 Marks)
    Q3. Short notes on NLP. (5 Marks)

    SECTION B
    Q4. Explain Deep Learning. (10 Marks)
    Q5. Case study on AI ethics. (10 Marks)
    OR
    """

    analyzer = PaperAnalyzer(sample_text)
    result = analyzer.analyze()

    print(result)