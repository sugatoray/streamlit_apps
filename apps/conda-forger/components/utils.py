import streamlit as st
import os
import shutil
import subprocess
from textwrap import dedent
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from parse import parse, compile, Parser
from faker import Faker


# read in environment variale "ST_USE_WIDE_LAYOUT"
def use_wide_layout(watchvariable: str = "ST_USE_WIDE_LAYOUT", value: str = "0") -> bool:
    # Default is False (ST_USE_WIDE_LAYOUT = "0")
    return bool(os.environ.get(watchvariable, value) == "1")
    

@st.cache_data
def use_debug_mode(watchvariable: str = "ST_DEBUG_MODE", value: str = "0") -> bool:
    # Default is False (ST_DEBUG_MODE = "0")
    return bool(os.environ.get(watchvariable, value) == "1")


@st.cache_data
def is_streamlit_cloud(watchvariable: str = "ST_IS_STREAMLIT_CLOUD") -> bool:
    """If running in the Streamlit Cloud, set environment variable
    (the same as ``watchvariable``) to 1.
    """
    return bool(os.environ.get(watchvariable, "0") == "1")


@st.cache_data
@dataclass
class Defaults:
    DEFAULT_PACKAGE_SOURCE: str = "PyPI"
    DEFAULT_RECIPES_DIR: str = ".scrap"
    TIME_OUT: int = 20
    MAX_TIME_OUT: int = 60
    APP_DIR: str = os.environ.get("ST_APP_DIR", os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    APP_URL: str = r"https://share.streamlit.io/sugatoray/streamlit_apps/master/apps/conda-forger/app.py"
    APP_URL_SHORT: str = r"https://tinyurl.com/conda-forger"
    APP_REPO_URL: str = r"https://github.com/sugatoray/streamlit_apps/blob/master/apps/conda-forger/app.py"
    APP_CODE_BADGE: str = r"https://img.shields.io/static/v1?logo=github&style=flat&color=blue&label=code&message={message}%20⭐"
    ON_ST_CLOUD: bool = is_streamlit_cloud()
    USE_DEBUG_MODE: bool = use_debug_mode()
    USE_WIDE_LAYOUT: bool = use_wide_layout()
    # Cannot assign a mutable dictionary to a dataclass field directly: need field + default_factory 
    # APP_CONFIG: dict = field(default_factory=lambda : dict(
    #         page_title = "Conda-Forger App :zap:",
    #         page_icon = ":zap:",
    #         layout = "wide" if use_wide_layout() else "centered",
    #         initial_sidebar_state = "auto",
    #         menu_items = None,
    #     )
    # )


def create_recipes_dir(recipes_dir: Optional[str] = None, app_dir: Optional[str] = None) -> str:
    if recipes_dir is None:
        recipes_dir = Defaults.DEFAULT_RECIPES_DIR
    if app_dir is None:
        app_dir = Defaults.APP_DIR
    recipes_dir = os.path.join(app_dir, recipes_dir)
    os.environ["RECIPES_DIR"] = recipes_dir
    if not os.path.exists(recipes_dir):
        os.makedirs(recipes_dir)
    if not os.path.isdir(recipes_dir):
        os.makedirs(recipes_dir)
    return recipes_dir


@st.cache
def create_command(options: Dict[str, Any], 
    package_name: str = "", 
    package_version: str = "", 
    github_repo_url: str = "", 
    github_release_tag: str = "") -> str:
    """Creates command with ``grayskull`` utility for PyPI package or GitHub package repository."""
    recipes_dir = os.environ.get('RECIPES_DIR')
    
    IS_PYPI = source_is_pypi(options)
    IS_GITHUB = source_is_github(options)

    strict_conda_forge = f" --strict-conda-forge" if options.get("strict-conda-forge", False) else ""

    if IS_PYPI:
        version_contraint = f'=={package_version}' if package_version else ''
        command = f'grayskull pypi "{package_name}{version_contraint}"{strict_conda_forge} -o {recipes_dir} --maintainers ADD_YOUR_GITHUB_ID_HERE'
        return command

    elif IS_GITHUB:
        release_tag = f' --tag "{github_release_tag}"' if github_release_tag else ''
        command = f'grayskull pypi "{github_repo_url}"{release_tag}{strict_conda_forge} -o {recipes_dir} --maintainers ADD_YOUR_GITHUB_ID_HERE'
        return command


def show_recipe(package_name: str, recipes_dir: str = None) -> str:
    if recipes_dir is None:
        recipes_dir = os.environ.get('RECIPES_DIR')
    st.success("### Recipe 🎁")
    recipe_path = os.path.join(
        recipes_dir, package_name, "meta.yaml")  # type: ignore
    recipe = ""
    with open(recipe_path, "r") as f:
        recipe = f.read()
        st.code(recipe, language="yaml")
    return recipe


def clearall(recipes_dir: str = None) -> None:
    if recipes_dir is None:
        recipes_dir = os.environ.get('RECIPES_DIR')
    if os.path.isdir(recipes_dir):
        shutil.rmtree(recipes_dir)
    create_recipes_dir(recipes_dir=recipes_dir)


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


@st.cache
def generate_message_as_image(message: str, height: int = 600, width: int = 1200, bgcolor: str = "0288d1", textcolor: str = "fff") -> str:
    import urllib
    message = urllib.parse.quote_plus(message)
    image_url = f"https://fakeimg.pl/{width}x{height}/{bgcolor}/{textcolor}/?text={message}"
    return image_url


def show_message(message: str="Not Yet Implemented!", **kwargs):
    url = generate_message_as_image(message, **kwargs)
    st.write(f"![message]({url})")


def run_command(command: str, timeout: Optional[int]=None):
    if timeout is None:
        timeout = Defaults.TIME_OUT
    result = subprocess.run(
        command,
        capture_output=True,
        shell=True,
        timeout=timeout,
        check=True,
    )
    return result


def source_is_github(options: Dict[str, Any]) -> bool:
    """Checks if the source is from GitHub and returns True or False."""
    return options.get("source", Defaults.DEFAULT_PACKAGE_SOURCE).lower() == "github"


def source_is_pypi(options: Dict[str, Any]) -> bool:
    """Checks if the source is from PyPI and returns True or False."""
    return options.get("source", Defaults.DEFAULT_PACKAGE_SOURCE).lower() == "pypi"


@st.cache
def show_not_implemented_banner():
    msg_params = dict(height=300, width=700, bgcolor="fa5043", textcolor="fff")
    show_message("Not Yet Implemented!", **msg_params)


PAT: Parser = compile("https://github.com/{owner}/{repo}/{extra}")

# @st.cache(allow_output_mutation=True)
def parse_github_url(url: str) -> Dict[str, str]:
    """Extract GitHub ``owner`` and ``repository`` from URL."""
    url = url + "/extra" if url[-1]!="/" else url + "extra"
    parsed = PAT.parse(url).named
    return parsed


def dummy_package_name():
    """Returns a dummy package name in the format ``alpha-beta``."""
    fk = Faker()
    return f"{fk.domain_word()}-{fk.domain_word()}"
