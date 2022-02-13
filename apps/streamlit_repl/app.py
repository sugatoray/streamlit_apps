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
"""))

st.components.v1.iframe(iframeurl, height=500, scrolling=True)
