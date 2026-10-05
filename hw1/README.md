# HW1 — Funny lexer: regex → ε-NFA → DFA → minimization

Учебная реализация HW1 без внешних Python-зависимостей.

## Что реализовано

1. Регулярные выражения токенов Funny.
2. Построение общего ε-НКА по конструкции Томпсона.
3. Преобразование ε-НКА → ДКА методом subset construction.
4. Добавление явной ловушки и удаление недостижимых состояний.
5. Минимизация ДКА методом Хопкрофта.
6. Сериализация DFA и минимального DFA в JSON.
7. Maximal munch / longest match для лексического анализа.
8. Приоритет правил: если несколько токенов принимают одинаковую максимальную лексему, выигрывает правило с меньшим номером.
9. Тесты на крайние случаи из задания.

## Требования

Python 3.10+.

Внешние библиотеки не нужны.

## Запуск

Из каталога проекта:

```bash
python main.py build
```

Будут созданы:

- `output/nfa_stats.json`
- `output/dfa.json`
- `output/dfa_min.json`

Проверка:

```bash
python main.py test
```

Или напрямую:

```bash
python tests/run_tests.py
```

Проверка строки:

```bash
python main.py scan "function f(x) returns r { r = x + 1; }"
```

## Структура

- `lexer_spec.py` — спецификация токенов.
- `automata.py` — regex parser, Thompson NFA, subset construction, Hopcroft minimization и scanner.
- `main.py` — CLI.
- `tests/run_tests.py` — автоматические проверки.
- `output/` — результаты построения.

## Регулярные выражения

Используются:

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

Операторы/разделители:

```text
+ - * / == != <= >= < > = , ; ( ) [ ] { }
```

Алфавит — ASCII 0..127.

`WS` и `COMMENT` являются skip-токенами.

## Важное замечание про `00` и `01`

Регулярное выражение `INT = 0|[1-9][0-9]*` не принимает `00` или `01` как один `INT`.

Но при обычном maximal-munch сканировании:

```text
00 -> INT("0"), INT("0")
01 -> INT("0"), INT("1")
```

Поэтому эти строки не являются ошибкой на уровне лексера: они разбиваются на два корректных токена. Если преподаватель требует считать `00`/`01` целиком ошибкой, нужен отдельный диагностический rule перед `INT`, например `0[0-9]+`, который помечается как ERROR. В текущей версии оставлено строгое поведение по заданному `INT`.

## Longest match

Например:

```text
==  → EQ
=   → ASSIGN
<=  → LE
<   → LT
function → FUNCTION
functionality → IDENT
```

Причина последнего случая: `function` и `functionality` имеют разные длины, поэтому longest match выбирает весь `functionality`, после чего состояние принимает `IDENT`.

## Отчёт

После:

```bash
python main.py build
```

команда печатает:

```text
NFA states: ...
DFA states: ...
Minimal DFA states: ...
```

Эти числа следует вставить в краткий отчёт вместе с описанием ловушки.

Минимизация выполняется после того, как ДКА сделан полным: для отсутствующих переходов добавляется явное rejecting trap state. Это соответствует требованию задания о покрытии всего ASCII-алфавита.

## Почему структура соответствует HW1

Pipeline:

```text
regex rules
   ↓
Thompson
   ↓
ε-NFA
   ↓
epsilon-closure + subset construction
   ↓
DFA
   ↓
complete + remove unreachable
   ↓
Hopcroft
   ↓
minimal total DFA
```

Состояние DFA хранит информацию о наиболее приоритетном принимающем правиле. Это позволяет использовать тот же автомат как основу для будущего лексера HW2/P02.
