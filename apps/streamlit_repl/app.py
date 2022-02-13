import streamlit as st
from textwrap import dedent

import utils as U

Defaults = U.Defaults

st.write("# Streamlit Python REPL ✨")

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

# iframeurl = U.prepare_url(
#     base="https://replite.vercel.app/retro/consoles/",
#     params=dict(toolbar=toolbar, kernel=kernel, theme=theme)
# )

iframeurl = f"https://replite.vercel.app/retro/consoles/?toolbar={toolbar}&kernel={kernel}&theme={theme.replace(' ', '+')}"

st.success(dedent("""### Enjoy the REPL! 🎈🎉

> GitHub: https://github.com/jtpio/replite

"""))

st.info("### Installing Python Packages")

with st.expander(label="Click to see more", expanded=False):
    st.write(dedent('''
    Run the following line in the REPL to install a purely-python library (for example: `genespeak`).
    See [micropip API docs][#micropip-api-docs] for more details.

    - [Creating a Pyodide Package](https://pyodide.org/en/stable/development/new-packages.html#creating-a-pyodide-package)
    - [Pyodide Package Recipe: `meta.yaml` file](https://pyodide.org/en/stable/development/meta-yaml.html)

    [#micropip-api-docs]: https://pyodide.org/en/stable/usage/api/micropip-api.html

    ```python
    import micropip; await micropip.install("genespeak"); import genespeak as gp; pkg = gp; print(f"{pkg.__name__} version: {pkg.__version__}")
    ```

    or,

    ```python
    import micropip; await micropip.install("genespeak")
    ```
    or,

    ```python
    async def mpinstall(libname: str, libspec: str=None):
        """Installs pure-python libraries using micropip.

        Usage:

            await mpinstall("emoji");
            await mpinstall("genespeak");
            await mpinstall("genespeak", libspec="==0.0.8") # this fails for now

        """
        import micropip
        import importlib
        import warnings
        lib = libname + "" if libspec is None else libspec
        try:
            await micropip.install(lib)
        except Exception as e:
            msg = f"Exception occured while installing with version specification. Installing latest version of {libname}."
            warnings.warn(msg)
            await micropip.install(libname)
        pkg = importlib.import_module(libname)
        print(f"{pkg.__name__} version: {pkg.__version__}")

    await mpinstall("genespeak")
    await mpinstall("emoji")
    ```

    ''')
    )

    st.warning("#### URL Used")
    st.write(dedent(f"""
    **`replite` app url**:
    > {iframeurl}
    """))

st.components.v1.iframe(iframeurl, height=500, scrolling=True)
