import streamlit as st
from textwrap import dedent

import utils as U

Defaults = U.Defaults

st.write("# Streamlit REPL ✨")

st.write("""
Made with :heart: using `replite`: &nbsp; *An embeddable REPL, powered by JupyterLite.*
""")

with st.sidebar:
    st.write("## ⚙️ Parameters")

    options = dict()

    options["toolbar"] = st.checkbox(
        label="Show Toolbar ⚙️",
        value=Defaults.ShowToolbar,
    )

    options["language"] = st.radio(
        label="Programming Language",
        options=Defaults.LanguageOptions,
        index=1,
    )

    options["theme"] = st.radio(
        label="Choose Theme",
        options=Defaults.ReplThemeOptions,
        index=0,
    )

    st.write("---")

    U.add_about_section()

toolbar = int(options.get("toolbar", Defaults.ShowToolbar))
kernel = str(options.get("language", Defaults.DefaultLanguage)).lower()
theme = options.get("theme", Defaults.DefaultReplTheme)

iframeurl = f"https://replite.vercel.app/retro/consoles/?toolbar={toolbar}&kernel={kernel}&theme={theme}"

st.success(dedent("""### Enjoy the REPL! 🎈🎉

> GitHub: https://github.com/jtpio/replite

Run the following line in the REPL to install a purely-python library (for example: `genespeak`).
See [micropip API docs][#micropip-api-docs] for more details.

- [Creating a Pyodide Package](https://pyodide.org/en/stable/development/new-packages.html#creating-a-pyodide-package)
- [Pyodide Package Recipe: `meta.yaml` file](https://pyodide.org/en/stable/development/meta-yaml.html)

[#micropip-api-docs]: https://pyodide.org/en/stable/usage/api/micropip-api.html

```python
import micropip; await micropip.install("genespeak"); import genespeak as gp; pkg = gp; print(f"{pkg.__name__} version: {pkg.__version__}")
```

"""))

st.components.v1.iframe(iframeurl, height=500, scrolling=True)
