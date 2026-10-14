import argparse
from pathlib import Path
from .core import load_and_validate, analyze, briefing

def main():
    parser = argparse.ArgumentParser(description="Generate a CFO executive briefing")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="executive_brief.md")
    parser.add_argument("--threshold", type=float, default=0.1)
    args = parser.parse_args()
    result = briefing(analyze(load_and_validate(args.input), args.threshold))
    Path(args.output).write_text(result, encoding="utf-8")
    print(f"Created {args.output}")

if __name__ == "__main__":
    main()
