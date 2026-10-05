# HW1 — Funny lexer: regex → ε-NFA → DFA → minimization

## Что это

Лексер для учебного языка Funny. На входе — текст программы, на выходе — список токенов.

Внутри: регулярные выражения → ε-НКА по Томпсону → ДКА через subset construction → полный ДКА с ловушкой → минимальный ДКА по Хопкрофту.

## Что реализовано

1. Регулярные выражения токенов Funny.
2. Построение общего ε-НКА по конструкции Томпсона.
3. Преобразование ε-НКА → ДКА методом subset construction.
4. Добавление явной ловушки и удаление недостижимых состояний.
5. Минимизация ДКА методом Хопкрофта.
6. Сериализация DFA и минимального DFA в JSON.
7. Maximal munch / longest match для лексического анализа.
8. Приоритет правил: если несколько токенов принимают одинаковую максимальную лексему, выигрывает правило с меньшим номером.
9. Тесты на крайние случаи.

## Требования

Python 3.10+. Внешние библиотеки не нужны.

## Запуск

```bash
python3 main.py build
```

Создаёт:

- `output/nfa_stats.json`
- `output/dfa.json`
- `output/dfa_min.json`

Проверка тестов:

```bash
python3 main.py test
```

Проверка одной строки:

```bash
python3 main.py scan "function f(x) returns r { r = x + 1; }"
```

## Структура

- `lexer_spec.py` — список токенов.
- `automata.py` — regex parser, Thompson NFA, subset construction, Hopcroft minimization, scanner.
- `main.py` — CLI.
- `tests/run_tests.py` — тесты.
- `output/` — результаты построения.
- `REPORT.md` — краткий отчёт.

## Токены

```text
IDENT      [A-Za-z_][A-Za-z0-9_]*
INT        0|[1-9][0-9]*
WS         [ \t\r\n]+
COMMENT    //[^\n]*
```

Ключевые слова:

```text
function returns uses while if else true false
assert assume invariant length
```

Операторы и разделители:

```text
+ - * / == != <= >= < > = , ; ( ) [ ] { }
```

Алфавит — ASCII 0..127. WS и COMMENT пропускаются.

## Размеры автоматов

```text
NFA states: 1247
DFA states: 342
Minimal DFA states: 88
```