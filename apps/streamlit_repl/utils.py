import streamlit as st
import urllib
from dataclasses import dataclass
from typing import List, Tuple
from textwrap import dedent


@st.cache
@dataclass
class Defaults:
    ShowToolbar: bool = True
    LanguageOptions: Tuple[str] = ("Julia", "Python", "R",) # type: ignore
    DefaultLanguage: str = "Python"
    ReplThemeOptions: Tuple[str] = (
        "JupyterLab Light",
        "JupyterLab Dark",
    )  # type: ignore
    DefaultReplTheme: str = "JupyterLab Light"
    APP_URL: str = r"https://share.streamlit.io/sugatoray/streamlit_apps/master/apps/streamlit_repl/app.py"
    APP_URL_SHORT: str = r"https://tinyurl.com/streamlit-repl-demo"


def add_about_section():
    """Adds an About section to the app."""

    st.write("## ℹ️ About")
    st.info(
        dedent(
            f"""
        This web [app][#streamlit-app] is maintained by [Sugato Ray][#linkedin].
        You can follow me on social media:
        - [@sugatoray | LinkedIn][#linkedin]
        - [@sugatoray | Twitter][#twitter]
        - [@sugatoray | GitHub][#github]
        [#linkedin]: https://www.linkedin.com/in/sugatoray/
        [#twitter]: https://twitter.com/sugatoray
        [#github]: https://github.com/sugatoray
        [#streamlit-app]: {Defaults.APP_URL}
        Short URL: {Defaults.APP_URL_SHORT}
        """
        )
    )


def prepare_url(base: str, params: Dict):
    """Return an encoded url."""
    tail = urllib.parse.urlencode(**params)
    url = urllib.parse.urljoin(base, tail)
    return url
