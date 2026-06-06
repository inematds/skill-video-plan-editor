# video_plan_editor/cli.py
from __future__ import annotations

import argparse
import sys

from .builder import scaffold_plan
from .models import EditPlan, PresetName
from .resumo import render_resumo
from .validate import validate_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vpe", description="video-plan-editor")
    sub = parser.add_subparsers(dest="command", required=True)

    sc = sub.add_parser("scaffold", help="Gera um plano-esqueleto a partir do input")
    sc.add_argument("input", help="assunto, link de página ou link de vídeo")
    sc.add_argument("--preset", required=True, choices=[p.value for p in PresetName])
    sc.add_argument("--title", default=None)

    va = sub.add_parser("validate", help="Valida um plano-edicao.json")
    va.add_argument("plan", help="caminho do plano JSON")

    rs = sub.add_parser("resumo", help="Renderiza RESUMO.md de um plano")
    rs.add_argument("plan", help="caminho do plano JSON")

    args = parser.parse_args(argv)

    if args.command == "scaffold":
        plan = scaffold_plan(args.input, PresetName(args.preset), title=args.title)
        print(plan.model_dump_json(indent=2))
        return 0

    if args.command == "validate":
        plan = EditPlan.model_validate_json(_read(args.plan))
        issues = validate_plan(plan)
        for issue in issues:
            print(f"[{issue.severity}] {issue.code}: {issue.message}")
        return 1 if any(i.severity == "error" for i in issues) else 0

    if args.command == "resumo":
        plan = EditPlan.model_validate_json(_read(args.plan))
        print(render_resumo(plan), end="")
        return 0

    return 2


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    sys.exit(main())
