#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from lexer_spec import RULES, ALPHABET
from automata import build_combined_nfa, nfa_to_dfa, complete_dfa, trim_unreachable, hopcroft_minimize, serialize_dfa, scan

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"

def build():
    nfa = build_combined_nfa(RULES)
    dfa = nfa_to_dfa(nfa, ALPHABET)
    dfa = complete_dfa(dfa)
    dfa = trim_unreachable(dfa)
    mini = hopcroft_minimize(dfa)
    OUT.mkdir(exist_ok=True)
    (OUT / "nfa_stats.json").write_text(json.dumps({
        "states": len(nfa.states),
        "alphabet_size": len(ALPHABET),
        "accepting_states": len(nfa.accepts),
    }, indent=2), encoding="utf-8")
    (OUT / "dfa.json").write_text(json.dumps(serialize_dfa(dfa), indent=2), encoding="utf-8")
    (OUT / "dfa_min.json").write_text(json.dumps(serialize_dfa(mini), indent=2), encoding="utf-8")
    print(f"NFA states: {len(nfa.states)}")
    print(f"DFA states: {len(dfa.states)}")
    print(f"Minimal DFA states: {len(mini.states)}")
    print(f"Trap state(s): explicit total DFA includes rejecting sink(s); see dfa_min.json")
    return nfa, dfa, mini

def main():
    ap = argparse.ArgumentParser(description="HW1: Funny regex -> NFA -> DFA -> minimal DFA")
    ap.add_argument("command", nargs="?", choices=["build", "scan", "test"], default="build")
    ap.add_argument("text", nargs="?", help="text for scan")
    args = ap.parse_args()

    _, dfa, mini = build()
    if args.command == "scan":
        if args.text is None:
            ap.error("scan requires TEXT")
        print(json.dumps(scan(mini, args.text), ensure_ascii=False, indent=2))
    elif args.command == "test":
        import subprocess, sys
        raise SystemExit(subprocess.call([sys.executable, str(ROOT/"tests"/"run_tests.py")]))

if __name__ == "__main__":
    main()
