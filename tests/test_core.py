import pytest
from cfo_agent.core import load_and_validate, analyze, briefing

def test_analysis(tmp_path):
    path = tmp_path / "financials.csv"
    path.write_text("month,department,category,actual,budget\n2026-07-01,Sales,revenue,90,100\n2026-07-01,Ops,expense,120,100\n")
    analysis = analyze(load_and_validate(path))
    assert analysis["operating_result"] == -30
    assert len(analysis["findings"]) == 2
    assert analysis["findings"][0].kind == "expense overspend"
    assert "Ops" in briefing(analysis)

def test_bad_input(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("month,department,category,actual,budget\n2026-07-01,Ops,expense,-1,10\n")
    with pytest.raises(ValueError):
        load_and_validate(path)
