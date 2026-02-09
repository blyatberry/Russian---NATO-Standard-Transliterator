# Russian---NATO-Standard-Transliterator

This tool transliterates Russian in **both directions**:

- Cyrillic -> Latin (BGN/PCGN in NATO/STANAG 3689 context)
- Latin -> Cyrillic (with heuristics for ambiguous reverse mapping)

Files:

- `russian_nato_transliterator.py`
- `russian_nato_transliterator_gui.py` (German UI)
- `russian_nato_transliterator_gui_en.py` (English UI)
-  NATOtransliterator.apk (Android App)

## Requirements

- Python 3.10+ (standard library only)

Optional, make executable:

```bash
chmod +x russian_nato_transliterator.py
```

## Quick Start (CLI)

Russian -> NATO transliteration:

```bash
python3 russian_nato_transliterator.py --direction ru2lat --text "Ельцин, Подъезд, Берёза, Тюмень"
```

NATO transliteration -> Russian:

```bash
python3 russian_nato_transliterator.py --direction lat2ru --text "Yel'tsin, Pod\"yezd, Beryoza, Tiumen'"
```

Automatic direction detection:

```bash
python3 russian_nato_transliterator.py --direction auto --text "Съешь ещё этих мягких французских булок"
```

## Start GUI

German GUI:

```bash
python3 russian_nato_transliterator_gui.py
```

English GUI:

```bash
python3 russian_nato_transliterator_gui_en.py
```

GUI features:

- Side-by-side input and output text areas
- Direction selector: `Auto`, `RU -> LAT`, `LAT -> RU`
- Optional ASCII mode for `ru2lat` (`ë` -> `yo`)
- Load/save text files
- Swap texts and copy output to input

## Input and Output (CLI)

Input sources:

- `--text "..."` direct input
- `--input-file <file>` UTF-8 text file
- `stdin` (pipe) if neither `--text` nor `--input-file` is provided

Output:

- Defaults to `stdout`
- optional with `--output-file <file>`

Pipe example:

```bash
echo "Берёза и Ёлка" | python3 russian_nato_transliterator.py --direction ru2lat
```

## Key Options

- `--direction {ru2lat,lat2ru,auto}` transliteration direction (default: `auto`)
- `--ascii` for `ru2lat` only: replace `ë/Yë` with ASCII `yo/Yo`
- `--text` input text
- `--input-file` input file (UTF-8)
- `--output-file` output file (UTF-8)

## Implemented Core Rules (ru2lat)

- `Е/е` -> `Ye/ye` at word start or after vowel/`й`/`ь`/`ъ`, otherwise `E/e`
- `Ё/ё` -> `Yë/yë` at word start or after vowel/`й`/`ь`/`ъ`, otherwise `Ë/ë`
- `Ю/ю` -> `Yu/yu` or `Iu/iu` (context dependent)
- `Я/я` -> `Ya/ya` or `Ia/ia` (context dependent)
- `Ь/ь` -> `'`
- `Ъ/ъ` -> `"`
- Digraphs like `ж/х/ц/ч/ш/щ` -> `zh/kh/ts/ch/sh/shch`

## Reverse Transliteration (lat2ru)

Reverse transliteration has inherent ambiguity. The tool uses heuristics:

- `y` may map to `й` or `ы`
- `e` may map to `е` or `э`
- ASCII `yo` is interpreted as `ё`

For deterministic output, input should follow the expected BGN/PCGN conventions.


