#!/usr/bin/env python3
"""Fail-closed structural audit for Paper A.

This audit is intentionally narrow. It verifies that the manuscript retains the
prespecified evidentiary boundaries, carries the expected citations, and does
not contain a small set of prohibited overclaims. It does not assess legal
correctness, prose quality, or the truth of external sources.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_HEADINGS = (
    "## Abstract",
    "## 1. Introduction",
    "## 2. Legal testbed: Saudi Arabia’s 2026 Copyright Law",
    "## 3. Related work and the missing evidence layer",
    "## 4. IPEL architecture",
    "## 5. Methods",
    "## 6. Results",
    "## 7. Discussion",
    "## 8. Threats to validity",
    "## 9. Falsification and future work",
    "## 10. Conclusion",
    "## Declarations",
    "## References",
)

# Each in-text token must have a corresponding bibliography token. This is a
# deterministic coverage gate for the current draft, not a general citation
# parser.
CITATION_PAIRS = (
    ("Samuelson 2023", "Samuelson P (2023)"),
    ("Guadamuz 2024", "Guadamuz A (2024)"),
    ("de la Durantaye 2025", "de la Durantaye K (2025)"),
    ("Sag and Yu 2025", "Sag M, Yu PK (2025)"),
    ("European Union 2019", "European Union (2019)"),
    ("Agency for Cultural Affairs 2024", "Agency for Cultural Affairs (Japan) (2024)"),
    ("United States Copyright Office 2025", "United States Copyright Office (2025)"),
    ("United Kingdom Government 2026", "United Kingdom Government (2026)"),
    ("Bender and Friedman 2018", "Bender EM, Friedman B (2018)"),
    ("Mitchell et al. 2019", "Mitchell M, Wu S"),
    ("Gebru et al. 2021", "Gebru T, Morgenstern J"),
    ("Pushkarna, Zaldivar, and Kjartansson 2022", "Pushkarna M, Zaldivar A, Kjartansson O (2022)"),
    ("Longpre et al. 2024", "Longpre S, Mahari R"),
    ("CAWG 2025", "CAWG (Creator Assertions Working Group) (2025)"),
    ("TDM·AI n.d.", "TDM·AI (n.d.)"),
    ("C2PA 2026", "C2PA (Coalition for Content Provenance and Authenticity) (2026)"),
    ("Cobbe, Lee, and Singh 2021", "Cobbe J, Lee MSA, Singh J (2021)"),
    ("Raji et al. 2020", "Raji ID, Smart A"),
    ("Di Porto 2023", "Di Porto F (2023)"),
    ("Guitton, Tamò-Larrieux, and Mayer 2023", "Guitton C, Tamò-Larrieux A, Mayer S (2023)"),
    ("Francesconi and Governatori 2023", "Francesconi E, Governatori G (2023)"),
    ("Witt et al. 2024", "Witt A, Huggins A, Governatori G et al. (2024)"),
    ("Saudi Arabia 2026a", "Saudi Arabia (2026a)"),
    ("Saudi Arabia 2026b", "Saudi Arabia (2026b)"),
    ("Saudi Arabia 2026c", "Saudi Arabia (2026c)"),
)

AUDIT_SOURCE_TOKENS = (
    "Samuelson",
    "Guadamuz",
    "de la Durantaye",
    "Sag, M.",
    "European Union",
    "Agency for Cultural Affairs",
    "United States Copyright Office",
    "United Kingdom Government",
    "Bender, E. M.",
    "Mitchell, M.",
    "Gebru, T.",
    "Pushkarna, M.",
    "Longpre, S.",
    "CAWG",
    "TDM·AI",
    "C2PA",
    "Cobbe, J.",
    "Raji, I. D.",
    "Di Porto",
    "Guitton, C.",
    "Francesconi, E.",
    "Witt, A.",
    "Saudi Arabia (2026a)",
    "Saudi Arabia (2026b)",
    "Saudi Arabia (2026c)",
)

REQUIRED_BOUNDARIES = (
    "not automated copyright compliance",
    "no human-effect result is claimed",
    "legal_conclusion=false",
    "0/4 Article 30(3) core fields",
    "IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED",
    "This is not an impossibility theorem",
    "A tamper-evident false assertion remains false",
    "not authenticate a human response before intake",
)

REQUIRED_RESULTS = (
    "Cases with semantic loss | 0/5",
    "Changed leaf paths | 0",
    "Article 30(3) tuple preserved | 5/5",
    "PASS / REVIEW / FAIL outcome preserved | 5/5",
    "False-equivalence attacks resisted | 2/2",
    "assertion.dataHash.mismatch",
    "assertion.hashedURI.mismatch",
    "claimSignature.mismatch",
    "0.90.16 and 0.78.0",
)

# These patterns target affirmative overclaims. Negative or limiting sentences
# are intentionally not matched.
FORBIDDEN_PATTERNS = (
    r"\bIPEL (?:proves|ensures|guarantees|determines) (?:legal|lawful|copyright|compliance)",
    r"\bC2PA (?:proves|ensures|guarantees) (?:legal|lawful|compliance)",
    r"\bindependent implementations? (?:confirmed|validated|agreed|established)",
    r"\bvalidated by independent (?:experts|reviewers|adjudicators)",
    r"\bhuman (?:study|results?|reviewers?) (?:showed|shows|demonstrated|confirmed|proved)",
    r"\bcryptographically blind\b",
    r"\bexpert-validated ground truth\b",
    r"\bensures lawful training\b",
)


def _contains_all(text: str, tokens: Iterable[str]) -> tuple[bool, list[str]]:
    missing = [token for token in tokens if token not in text]
    return not missing, missing


def audit_texts(draft: str, reference_audit: str, claim_matrix: str) -> dict[str, object]:
    checks: list[Check] = []

    ok, missing = _contains_all(draft, REQUIRED_HEADINGS)
    checks.append(Check("required_sections", ok, "missing=" + repr(missing)))

    word_count = len(re.findall(r"\b[\w’'-]+\b", draft))
    checks.append(Check("minimum_manuscript_length", word_count >= 4500, f"word_count={word_count}"))

    missing_citations: list[str] = []
    missing_bibliography: list[str] = []
    for in_text, bibliography in CITATION_PAIRS:
        if in_text not in draft:
            missing_citations.append(in_text)
        if bibliography not in draft:
            missing_bibliography.append(bibliography)
    checks.append(Check("in_text_citation_coverage", not missing_citations, "missing=" + repr(missing_citations)))
    checks.append(Check("manuscript_bibliography_coverage", not missing_bibliography, "missing=" + repr(missing_bibliography)))

    missing_audit_sources = [token for token in AUDIT_SOURCE_TOKENS if token not in reference_audit]
    checks.append(Check("reference_audit_coverage", not missing_audit_sources, "missing=" + repr(missing_audit_sources)))

    ok, missing = _contains_all(draft, REQUIRED_BOUNDARIES)
    checks.append(Check("mandatory_boundaries", ok, "missing=" + repr(missing)))

    ok, missing = _contains_all(draft, REQUIRED_RESULTS)
    checks.append(Check("committed_result_values", ok, "missing=" + repr(missing)))

    overclaims: list[str] = []
    for pattern in FORBIDDEN_PATTERNS:
        match = re.search(pattern, draft, flags=re.IGNORECASE)
        if match:
            overclaims.append(match.group(0))
    checks.append(Check("forbidden_overclaims_absent", not overclaims, "matches=" + repr(overclaims)))

    placeholder_terms = ("References — working list", "citation needed", "TODO CITATION", "TBD SOURCE")
    placeholders = [term for term in placeholder_terms if term.lower() in draft.lower()]
    checks.append(Check("citation_placeholders_absent", not placeholders, "matches=" + repr(placeholders)))

    matrix_requirements = (
        "Claims reserved for Paper B",
        "IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED",
        "Human-effect claims are prohibited",
        "0/4 core fields were delegated in the tested mapping",
    )
    ok, missing = _contains_all(claim_matrix, matrix_requirements)
    checks.append(Check("claim_matrix_boundaries", ok, "missing=" + repr(missing)))

    doi_count = len(re.findall(r"https://doi\.org/10\.", draft))
    checks.append(Check("bibliographic_identifier_floor", doi_count >= 14, f"doi_count={doi_count}"))

    passed = all(check.passed for check in checks)
    return {
        "audit_version": "paper-a-claim-citation-audit-v1",
        "passed": passed,
        "word_count": word_count,
        "check_count": len(checks),
        "failed_checks": [check.name for check in checks if not check.passed],
        "checks": [asdict(check) for check in checks],
        "scope_limit": (
            "Structural claim/citation audit only; not legal validation, source-truth verification, "
            "peer review, plagiarism detection, or prose-quality assessment."
        ),
    }


def audit_files(draft_path: Path, references_path: Path, matrix_path: Path) -> dict[str, object]:
    for path in (draft_path, references_path, matrix_path):
        if not path.is_file():
            return {
                "audit_version": "paper-a-claim-citation-audit-v1",
                "passed": False,
                "failed_checks": ["required_file_missing"],
                "missing_file": str(path),
            }
    return audit_texts(
        draft_path.read_text(encoding="utf-8"),
        references_path.read_text(encoding="utf-8"),
        matrix_path.read_text(encoding="utf-8"),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, default=Path("manuscript/PAPER_A_DRAFT.md"))
    parser.add_argument("--references", type=Path, default=Path("manuscript/PAPER_A_REFERENCES.md"))
    parser.add_argument("--matrix", type=Path, default=Path("manuscript/PAPER_A_CLAIM_EVIDENCE_MATRIX.md"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = audit_files(args.draft, args.references, args.matrix)
    serialized = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return 0 if report.get("passed") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
