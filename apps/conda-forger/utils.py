import streamlit as st
import os
import shutil
from textwrap import dedent
from typing import Optional, Dict, Any
from dataclasses import dataclass

DEFAULT_PACKAGE_SOURCE = "PyPI"
DEFAULT_RECIPES_DIR = ".scrap"


def use_debug_mode(watchvariable: str = "ST_DEBUG_MODE", value: str = "0") -> bool:
    # Default is False (ST_DEBUG_MODE = "0")
    return bool(os.environ.get(watchvariable, value) == "1")


def is_streamlit_cloud(watchvariable: str = "ST_IS_STREAMLIT_CLOUD") -> bool:
    """If running in the Streamlit Cloud, set environment variable
    (the same as ``watchvariable``) to 1.
    """
    return bool(os.environ.get(watchvariable, "0") == "1")


@st.cache
@dataclass
class Defaults:
    DEFAULT_PACKAGE_SOURCE: str = "PyPI"
    DEFAULT_RECIPES_DIR: str = ".scrap"
    APP_DIR: str = os.environ.get("ST_APP_DIR", os.path.abspath(os.path.dirname(__file__)))
    APP_URL: str = r"https://share.streamlit.io/sugatoray/streamlit_apps/master/apps/conda-forger/app.py"
    APP_URL_SHORT: str = r"https://tinyurl.com/conda-forger"
    ON_ST_CLOUD: bool = is_streamlit_cloud()
    USE_DEBUG_MODE: bool = use_debug_mode()

# @st.cache
def create_recipes_dir(recipes_dir: Optional[str] = None, app_dir: Optional[str] = None):
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


def create_command(package_name: str, options: Dict[str, Any], package_version: str = ""):
    recipes_dir = os.environ.get('RECIPES_DIR')
    version_contraint = f'=={package_version}' if package_version else ''
    strict_conda_forge = f"--strict-conda-forge" if options.get(
        "strict-conda-forge", False) else ""
    command = f'grayskull pypi "{package_name}{version_contraint}" {strict_conda_forge} -o {recipes_dir} --maintainers ADD_YOUR_GITHUB_ID_HERE'
    return command


def show_recipe(package_name: str, recipes_dir: str = None):
    if recipes_dir is None:
        recipes_dir = os.environ.get('RECIPES_DIR')
    st.success("### Recipe")
    recipe_path = os.path.join(
        recipes_dir, package_name, "meta.yaml")  # type: ignore
    recipe = ""
    with open(recipe_path, "r") as f:
        recipe = f.read()
        st.code(recipe, language="yaml")
    return recipe


def clearall(recipes_dir: str = None):
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


def generate_message_as_image(message: str, height: int = 600, width: int = 1200, bgcolor: str = "0288d1", textcolor: str = "fff"):
    import urllib
    message = urllib.parse.quote_plus(message)
    image_url = f"https://fakeimg.pl/{width}x{height}/{bgcolor}/{textcolor}/?text={message}"
    return image_url

def show_message(message: str="Not Yet Implemented!", **kwargs):
    url = generate_message_as_image(message, **kwargs)
    st.write(f"![message]({url})")
