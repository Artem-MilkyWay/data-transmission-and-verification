#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lexer_spec import RULES, ALPHABET
from automata import build_combined_nfa, nfa_to_dfa, complete_dfa, trim_unreachable, hopcroft_minimize, scan

def kinds(text, dfa):
    return [x["kind"] for x in scan(dfa, text) if "kind" in x]

def has_error(text, dfa):
    return any("error" in x for x in scan(dfa, text))

def main():
    nfa = build_combined_nfa(RULES)
    dfa = trim_unreachable(complete_dfa(nfa_to_dfa(nfa, ALPHABET)))
    mini = hopcroft_minimize(dfa)

    checks = [
        ("empty", "", [], False),
        ("spaces", "   \t\r\n", [], False),
        ("zero", "0", ["INT"], False),
        ("leading zero 00", "00", ["INT", "INT"], False),
        ("leading zero 01", "01", ["INT", "INT"], False),
        ("underscore", "_x9", ["IDENT"], False),
        ("keyword", "function", ["FUNCTION"], False),
        ("keywords", "returns while if else assert assume invariant length",
         ["RETURNS","WHILE","IF","ELSE","ASSERT","ASSUME","INVARIANT","LENGTH"], False),
        ("keyword prefix is IDENT", "functionality", ["IDENT"], False),
        ("operators", "()[]{},; + - * / == != <= >= < > =",
         ["LPAREN","RPAREN","LBRACKET","RBRACKET","LBRACE","RBRACE",
          "COMMA","SEMICOLON","PLUS","MINUS","STAR","SLASH",
          "EQ","NE","LE","GE","LT","GT","ASSIGN"], False),
        ("comment", "// hello world", [], False),
        ("comment then token", "// c\nx", ["IDENT"], False),
        ("longest match", "a==b<=10", ["IDENT","EQ","IDENT","LE","INT"], False),
        ("unknown ascii", "@", [], True),
        ("non-ascii", "é", [], True),
    ]

    ok = 0
    for name, text, expected, err in checks:
        got = kinds(text, mini)
        got_err = has_error(text, mini)
        good = got == expected and got_err == err
        print(("PASS" if good else "FAIL"), name, "->", got,
              "error=" + str(got_err))
        ok += good

    print(f"\n{ok}/{len(checks)} checks passed")
    print(f"states: NFA={len(nfa.states)}, DFA={len(dfa.states)}, MIN={len(mini.states)}")
    return 0 if ok == len(checks) else 1

if __name__ == "__main__":
    raise SystemExit(main())
