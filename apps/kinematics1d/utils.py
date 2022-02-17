import streamlit as st
import urllib
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional
from textwrap import dedent


@st.cache
@dataclass
class Defaults:
    APP_URL: str = r"https://share.streamlit.io/sugatoray/streamlit_apps/master/apps/kinematics1d/app.py"
    APP_URL_SHORT: str = r"https://tinyurl.com/st-kinematics1d-demo"


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


def show_math_steps(steps: List[str]):
    """Shows mathematical steps from a list of math expressions as LaTeX.
    """
    for i, step in enumerate(steps):
        st.latex(r"\begin{aligned}" + "\n" +
                 step + "\n" + r"\end{aligned}")
        if i < len(steps) - 1:
            html_text = '<div style="text-align: center"> ⏬ </div>'
            st.write(html_text,
                     unsafe_allow_html=True)


def display_result(result: Dict[str, Any], known: Optional[List[str]]=None):
    """Displays evaluated parameters from the result."""
    if known is None:
        known = []

    def unknown_marker(x, unknown_label: str = r" $^{\color{red}(?)}$", known_label: str = ""):
        return known_label if ((x in known) or (not known)) else unknown_label

    cells = [
        (
            r"$\Delta x$" + unknown_marker(x="Dx"),
            f" `{result.get('Dx')}`",
            r"$\scriptsize \text{m}$",
        ),
        (
            r"$a$" + unknown_marker(x="a"),
            f" `{result.get('a')}`",
            r"$\scriptsize \text{m}/\text{s}^{2}$",
        ),
        (
            r"$v_{avg}$" + unknown_marker(x="v_avg"),
            f" `{result.get('v_avg')}`",
            r"$\scriptsize \text{m/s}$",
        ),
        (
            r"$v_{i}$" + unknown_marker(x="vi"),
            f" `{result.get('vi')}`",
            r"$\scriptsize \text{m/s}$",
        ),
        (
            r"$v_{f}$" + unknown_marker(x="vf"),
            f" `{result.get('vf')}`",
            r"$\scriptsize \text{m/s}$",
        ),
        (
            r"$t$" + unknown_marker(x="t"),
            f" `{result.get('t')}`",
            r"$\scriptsize \text{s}$",
        ),
    ]
    l1 = '| ' + ' | '.join([h for h, _, _ in cells]) + ' |'
    l2 = ':---:'.join("|" * (len(cells) + 1))
    l3 = '| ' + ' | '.join([v for _, v, _ in cells]) + ' |'
    l4 = '| ' + ' | '.join([u for _, _, u in cells]) + ' |'

    st.markdown(f"""
    | Params {l1}
    |:---{l2}
    | **Values** {l3}
    | **Units** {l4}

    """)

    st.write("\n")

    st.warning("#### Parameters as JSON")
    st.json(result)
