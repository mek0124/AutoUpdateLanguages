# AutoUpdate Languages

A package that automatically maintains an updated list of programming languages by scraping programminglanguages.info.

## Installation

```bash
pip install autoupdate-languages
```

## Usage

```python
from autoupdate_languages import AutoUpdateLanguages

app = AutoUpdateLanguages()
asyncio.run(app.start())
```

<!-- fix codebase for command below to work -->
<!-- Or from command line:
```bash
autoupdate-languages
``` -->

## Features
- Automatically updates language list monthly
- Lightweight and easy to use