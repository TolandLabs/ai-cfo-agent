from dataclasses import dataclass
import pandas as pd

COLUMNS = ["month", "department", "category", "actual", "budget"]

@dataclass(frozen=True)
class Finding:
    month: str
    department: str
    kind: str
    amount: float

def load_and_validate(path):
    df = pd.read_csv(path)
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    df = df[COLUMNS].copy()
    df["month"] = pd.to_datetime(df.month, format="%Y-%m-%d", errors="raise")
    if df.month.dt.day.ne(1).any():
        raise ValueError("Month must start on day 1")
    if df.department.isna().any() or df.department.astype(str).str.strip().eq("").any():
        raise ValueError("Invalid department")
    if not df.category.isin(["revenue", "expense"]).all():
        raise ValueError("Invalid category")
    for col in ("actual", "budget"):
        df[col] = pd.to_numeric(df[col], errors="raise")
        if df[col].isna().any() or not df[col].map(lambda x: float("-inf") < x < float("inf")).all() or df[col].lt(0).any():
            raise ValueError(f"Invalid {col}")
    if df.duplicated(["month", "department", "category"]).any():
        raise ValueError("Duplicate records")
    return df

def analyze(df, threshold=0.1):
    if threshold < 0:
        raise ValueError("Threshold must be nonnegative")
    findings = []
    for row in df.itertuples(index=False):
        adverse = row.actual - row.budget if row.category == "expense" else row.budget - row.actual
        if adverse > 0 and (row.budget == 0 or adverse / row.budget >= threshold):
            kind = "expense overspend" if row.category == "expense" else "revenue shortfall"
            findings.append(Finding(row.month.strftime("%Y-%m"), row.department, kind, float(adverse)))
    findings.sort(key=lambda x: x.amount, reverse=True)
    revenue = df.loc[df.category.eq("revenue"), "actual"].sum()
    expense = df.loc[df.category.eq("expense"), "actual"].sum()
    budget_rev = df.loc[df.category.eq("revenue"), "budget"].sum()
    budget_exp = df.loc[df.category.eq("expense"), "budget"].sum()
    return {"revenue": float(revenue), "expense": float(expense),
            "operating_result": float(revenue - expense),
            "budget_result": float(budget_rev - budget_exp), "findings": findings}

def briefing(data):
    lines = ["# CFO Executive Briefing", "", "Synthetic-data demonstration; not an audited statement.",
             "", "## Operating summary",
             f"- Revenue: ${data['revenue']:,.2f}",
             f"- Expenses: ${data['expense']:,.2f}",
             f"- Operating result: ${data['operating_result']:,.2f}",
             f"- Budget operating result: ${data['budget_result']:,.2f}",
             f"- Variance: ${data['operating_result'] - data['budget_result']:+,.2f}",
             "", "## Adverse variance findings"]
    if not data["findings"]:
        lines.append("No findings exceeded the threshold.")
    for finding in data["findings"]:
        lines.append(f"- {finding.month} | {finding.department} | {finding.kind}: ${finding.amount:,.2f} adverse")
    lines.extend(["", "## Management follow-up",
                  "Validate variances against source transactions, timing, coding and assumptions."])
    return "\n".join(lines) + "\n"
