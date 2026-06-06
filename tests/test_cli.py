from __future__ import annotations

import json

from video_plan_editor.cli import main
from video_plan_editor.builder import scaffold_plan
from video_plan_editor.models import PresetName, EditPlan, TimelineItem, Role


def test_scaffold_prints_valid_json(capsys):
    rc = main(["scaffold", "como fazer pão", "--preset", "suave"])
    out = capsys.readouterr().out
    assert rc == 0
    data = json.loads(out)
    assert data["style"]["preset"] == "suave"
    assert data["source"]["kind"] == "topic"


def test_validate_returns_1_on_error(tmp_path, capsys):
    plan = scaffold_plan("assunto x", PresetName.acao)  # timeline vazia -> erro
    path = tmp_path / "plan.json"
    path.write_text(plan.model_dump_json(), encoding="utf-8")
    rc = main(["validate", str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "empty_timeline" in out


def test_validate_returns_0_when_valid(tmp_path, capsys):
    plan = scaffold_plan("assunto x", PresetName.acao)
    plan.timeline.append(TimelineItem(id="s1", role=Role.hook))
    path = tmp_path / "plan.json"
    path.write_text(plan.model_dump_json(), encoding="utf-8")
    rc = main(["validate", str(path)])
    assert rc == 0


def test_resumo_prints_markdown(tmp_path, capsys):
    plan = scaffold_plan("assunto x", PresetName.viral)
    plan.timeline.append(TimelineItem(id="s1", role=Role.hook))
    path = tmp_path / "plan.json"
    path.write_text(plan.model_dump_json(), encoding="utf-8")
    rc = main(["resumo", str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert out.startswith("# ")
    assert "Timeline" in out
