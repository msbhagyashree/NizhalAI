"""ss: the Strands Workshop to Ship kit.

Run in your project folder.

Commands:
  ss init                  Set up the project
  ss blocks                Show the Strands toolbox
  ss block <name>          Run one toolbox block
  ss status                Show project status
  ss bedrock               Test Bedrock and Amazon Translate
  ss run "message"         Run the NizhalAI agent
  ss cases check           Validate evaluation cases
  ss cases show            Display evaluation cases
  ss cases approve         Sign off reviewed cases
  ss measure               Evaluate agent against baseline
  ss video                 Record the demo
  ss ship                  Prepare submission files
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
PROJECT_T = KIT / "project"
EXAMPLES = KIT / "examples"
BLOCKS = KIT / "blocks"

MODEL_DEFAULT = "global.amazon.nova-2-lite-v1:0"
REGION_DEFAULT = "ap-southeast-2"

BLOCK_FILES = {
    "tools": "b01_tools",
    "mcp": "b02_mcp",
    "hooks": "b03_hooks",
    "interventions": "b04_interventions",
    "graph": "b05_graph",
    "swarm": "b06_swarm",
    "agents-as-tools": "b07_agents_as_tools",
    "sessions": "b08_sessions",
    "decider": "b09_decider",
    "shell": "b10_shell",
    "harness": "b11_harness",
    "evals": "b12_evals",
    "voice": "b13_voice",
    "guardrails": "b14_guardrails",
}

BLOCK_STATUS = {
    "decider": "KEY",
    "guardrails": "KEY",
    "voice": "DOC (needs a microphone)",
}

GITIGNORE = [
    ".venv/",
    "__pycache__/",
    "results/_raw/",
    "*.webm",
]


def _copy(
    src: Path,
    dst: Path,
    done: list,
    skipped: list,
    overwrite: bool = False,
) -> None:
    if src.is_dir():
        for p in sorted(src.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                _copy(
                    p,
                    dst / p.relative_to(src),
                    done,
                    skipped,
                    overwrite,
                )
        return

    if dst.exists() and not overwrite:
        skipped.append(str(dst))
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    done.append(str(dst))


def cmd_init(a) -> int:
    if not PROJECT_T.is_dir():
        raise SystemExit(
            "init runs from the installed kit: "
            "use the installed ss command."
        )

    root, done, skipped = Path.cwd(), [], []

    _copy(
        KIT / "ship_kit",
        root / "ship_kit",
        done,
        skipped,
        overwrite=a.update,
    )

    if a.update:
        print(f"Refreshed ship_kit/ ({len(done)} files). Nothing else touched.")
        return 0

    if a.example:
        src = EXAMPLES / a.example

        if not src.is_dir():
            names = sorted(
                p.name for p in EXAMPLES.iterdir() if p.is_dir()
            )
            raise SystemExit(
                f"Unknown example {a.example!r}; "
                f"choose one of {', '.join(names)}"
            )

        agent_src = src / "agent"
        seed = src / "cases.seed.jsonl"
        video = src / "video.json"
    else:
        agent_src = PROJECT_T / "agent"
        seed = PROJECT_T / "cases.seed.jsonl"
        video = PROJECT_T / "video.json"

    _copy(agent_src, root / "agent", done, skipped)
    _copy(seed, root / "cases.jsonl", done, skipped)
    _copy(video, root / "video.json", done, skipped)

    for f in ("requirements.txt", "FAILURES.md"):
        _copy(PROJECT_T / f, root / f, done, skipped)

    for sub in ("steering", "hooks", "agents"):
        _copy(
            PROJECT_T / sub,
            root / ".kiro" / sub,
            done,
            skipped,
        )

    gi = root / ".gitignore"
    have = gi.read_text(encoding="utf-8").splitlines() if gi.exists() else []
    add = [x for x in GITIGNORE if x not in have]

    if add:
        gi.write_text(
            "\n".join(have + add) + "\n",
            encoding="utf-8",
        )

    (root / "results").mkdir(exist_ok=True)

    print(
        ("Worked example: " + a.example)
        if a.example
        else "Generic starter"
    )
    print(f"Copied {len(done)} files.")

    if skipped:
        print(
            f"Kept {len(skipped)} existing files (never overwritten):\n  "
            + "\n  ".join(skipped)
        )

    print("Next: test Bedrock, then run the agent or explore the toolbox.")
    return 0


def cmd_blocks(_a) -> int:
    for name, f in BLOCK_FILES.items():
        doc = (
            (BLOCKS / f"{f}.py")
            .read_text(encoding="utf-8")
            .split('"""')[1]
            .strip()
            .splitlines()[0]
        )

        print(
            f"{name:16} "
            f"{BLOCK_STATUS.get(name, 'LIVE'):24} "
            f"{doc[:90]}"
        )

    print(
        "\nRun one: ss block <name>. "
        "Read the code: " + str(BLOCKS)
    )
    return 0


def cmd_block(a) -> int:
    f = BLOCK_FILES.get(a.name)

    if not f:
        raise SystemExit(
            f"Unknown block {a.name!r}; "
            f"choose one of: {', '.join(BLOCK_FILES)}"
        )

    return subprocess.call(
        [sys.executable, str(BLOCKS / f"{f}.py")],
        cwd=str(BLOCKS),
    )


def _here() -> None:
    if not (Path.cwd() / "agent").is_dir():
        raise SystemExit(
            "No agent/ here. Run the command from your project folder."
        )

    sys.path.insert(0, str(Path.cwd()))


def cmd_status(_a) -> int:
    from . import cases

    model = os.environ.get("SHIP_MODEL", MODEL_DEFAULT)
    region = os.environ.get("AWS_REGION", REGION_DEFAULT)

    print(f"model    {model}  region {region}")
    print(
        f"agent/   "
        f"{'yes' if Path('agent').is_dir() else 'no'}"
    )

    if Path("cases.jsonl").exists():
        c = cases.check(cases.load())

        print(
            "cases    "
            + ", ".join(
                f"{k} {v}" for k, v in c["counts"].items()
            )
            + ("" if c["ok"] else "  -> cases check needed")
        )

    m = Path("results/measure.json")

    if m.exists():
        r = json.loads(m.read_text(encoding="utf-8"))
        print(
            f"measure  {r['when']}: "
            f"gate {'PASSED' if r['passed'] else 'NOT PASSED'}"
        )

    v = Path("results/video_run.json")

    if v.exists():
        r = json.loads(v.read_text(encoding="utf-8"))
        print(f"video    {r['file']} ({r['seconds']} s)")

    return 0


def cmd_bedrock(_a) -> int:
    from strands import Agent
    from strands.models import BedrockModel

    mid = os.environ.get("SHIP_MODEL", MODEL_DEFAULT)
    reg = os.environ.get("AWS_REGION", REGION_DEFAULT)

    try:
        out = Agent(
            model=BedrockModel(model_id=mid, region_name=reg),
            callback_handler=None,
        )("Reply with the single word: ready")

        print(f"Bedrock OK  {mid} in {reg}: {str(out).strip()[:40]}")

    except Exception as e:
        msg = str(e)
        print(f"Bedrock FAILED for {mid} in {reg}: {msg[:300]}")

        if "credential" in msg.lower() or "token" in msg.lower():
            print(
                "Check your Bedrock API key environment variable "
                "and authentication configuration."
            )
        elif (
            "access" in msg.lower()
            or "payment" in msg.lower()
            or "marketplace" in msg.lower()
        ):
            print(
                "Check Bedrock model access and permissions."
            )

        return 1

    try:
        import boto3

        t = boto3.client(
            "translate",
            region_name=reg,
        ).translate_text(
            Text="Drink water.",
            SourceLanguageCode="en",
            TargetLanguageCode="ta",
        )

        print(f"Translate OK  en->ta: {t['TranslatedText']}")

    except Exception as e:
        print(
            "Translate FAILED "
            f"(Tamil fallback may not work): {str(e)[:200]}"
        )
        return 1

    return 0


def cmd_run(a, rest) -> int:
    _here()

    return subprocess.call(
        [sys.executable, "-m", "agent.app", *rest]
    )


def cmd_cases(a) -> int:
    from . import cases

    cs = cases.load()

    if a.action == "approve":
        n = cases.approve(
            cs,
            a.by,
            a.ids.split(",") if a.ids else None,
        )
        cases.save(cs)
        print(f"Signed off {n} cases as {a.by}.")
        return 0

    if a.action == "show":
        for c in cs:
            e = c.get("expected", {})

            job = c.get("job", "unknown")
            lang = c.get("lang", "en")
            escalation = e.get("escalation", "none")
            risk = e.get("risk_level", "N/A")

            temp = c.get("temp_c")
            humidity = c.get("rh")

            if temp is not None and humidity is not None:
                conditions = f"{temp}C/{humidity}%"
            else:
                conditions = "NizhalAI"

            if c.get("signed_off_by"):
                status = "SIGNED " + c["signed_off_by"]
            else:
                status = "UNSIGNED"

            print(
                f"{c.get('id', '?'):12} "
                f"{lang:3} "
                f"{job[:18]:18} "
                f"{conditions:12} "
                f"{risk:8} "
                f"{escalation:10} "
                f"{status}"
            )

            print(f"{'':12} {c.get('text', '')}")

        return 0

    r = cases.check(cs)

    print(
        "counts: "
        + ", ".join(
            f"{k} {v}" for k, v in r["counts"].items()
        )
    )

    for error in r["errors"]:
        print("ERROR " + error)

    for warning in r["below_minimum"]:
        print("BELOW MINIMUM " + warning)

    if r["unsigned"]:
        print(
            f"UNSIGNED {len(r['unsigned'])}: "
            "review each case before signing it off."
        )

    print("OK" if r["ok"] else "NOT READY")

    return 0 if r["ok"] else 1


def cmd_measure(a) -> int:
    _here()

    from . import measure

    return measure.main(a.limit, a.workers)


def cmd_video(a) -> int:
    _here()

    from . import video

    r = video.record(a.spec)

    print(json.dumps(r, ensure_ascii=False, indent=2))

    return (
        0
        if r["under_3_min"]
        and all(s["exit"] == 0 for s in r["scenes"])
        else 1
    )


def cmd_ship(_a) -> int:
    from . import submit

    return submit.main()


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    ap = argparse.ArgumentParser(
        prog="ss",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("init")
    p.add_argument("--example")
    p.add_argument("--update", action="store_true")

    sp.add_parser("blocks")

    p = sp.add_parser("block")
    p.add_argument("name")

    sp.add_parser("status")
    sp.add_parser("bedrock")

    sp.add_parser("run", add_help=False)

    p = sp.add_parser("cases")
    p.add_argument(
        "action",
        choices=["check", "show", "approve"],
        nargs="?",
        default="check",
    )
    p.add_argument("--by")
    p.add_argument("--ids")

    p = sp.add_parser("measure")
    p.add_argument("--limit", type=int)
    p.add_argument("--workers", type=int, default=3)

    p = sp.add_parser("video")
    p.add_argument("--spec", default="video.json")

    sp.add_parser("ship")

    if argv[:1] == ["run"]:
        return cmd_run(None, argv[1:])

    a = ap.parse_args(argv)

    commands = {
        "init": cmd_init,
        "blocks": cmd_blocks,
        "block": cmd_block,
        "status": cmd_status,
        "bedrock": cmd_bedrock,
        "cases": cmd_cases,
        "measure": cmd_measure,
        "video": cmd_video,
        "ship": cmd_ship,
    }

    return commands[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
