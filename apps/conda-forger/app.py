import os
import streamlit as st
from textwrap import dedent

from components import utils as U
from components import appfactory as A
from components.downloader import FileDownloader

Defaults = U.Defaults
APP_CODE_BADGE = Defaults.APP_CODE_BADGE

# This must be the first Streamlit command used 
# in your app, and must only be set once.
st.set_page_config(**U.APP_CONFIG)

def main():
    options = dict()

    os.environ["RECIPES_DIR"] = os.path.join(
        Defaults.APP_DIR, Defaults.DEFAULT_RECIPES_DIR)

    recipes_dir = U.create_recipes_dir(recipes_dir=None, app_dir=Defaults.APP_DIR)


    st.header("Conda Forger App :zap:")

    st.write(dedent(f"""
        Create **conda-forge** recipes lightning-fast online! :zap:

        > *Powered by* [**`grayskull`**](https://github.com/conda-incubator/grayskull) ❤️
        
        """))

    st.warning(dedent(f"""    
        :bulb: ***If you like the app, please consider leaving a :star: at the GitHub repository.*** 
        [![GitHub App Code]({APP_CODE_BADGE.format(message="streamlit-conda-forger")})][#code-conda-forger-app]

        [#code-conda-forger-app]: {Defaults.APP_REPO_URL}
        """))

    with st.expander("Instruction: How to create a conda-forge package", expanded=False):
        st.write(dedent(open(os.path.join(Defaults.APP_DIR, "instruction.md"))
                            .read()
                            .replace("# Instruction", "")
                            .replace("# ", "### ")
                        )
                )

    if options.get("debug-mode", False):
        st.write("**Recipes Directory:**")
        st.code(os.environ.get("RECIPES_DIR"))

    options = A.make_sidebar(recipes_dir=recipes_dir)

    tip = dedent(f"""If the recipe generation fails, you may want to try with 
    a higher timeout (`>{options.get("timeout")},<={A.MAX_TIME_OUT}` seconds).
    """)

    st.info(f"### Tip 💡\n{tip}")

    IS_PYPI = U.source_is_pypi(options)
    IS_GITHUB = U.source_is_github(options)
    options["IS_PYPI"] = IS_PYPI
    options["IS_GITHUB"] = IS_GITHUB

    if IS_PYPI or IS_GITHUB:

        options, generate, clear_workspace = A.update_app_options(options, recipes_dir=recipes_dir)

        with st.expander("Input Parameters 📥", expanded=False):
            st.json(options)

        recipe = A.generate_recipe(
            options,
            generate=generate,
            recipes_dir=recipes_dir,
        )

        if recipe is not None:
            with st.expander("Download Recipe 👇", expanded=True):
                download_recipe = FileDownloader(
                        data=recipe, 
                        filename="meta", 
                        file_ext="yaml"
                    ).download(
                        header="**Download recipe as YAML**",
                        hyperlinktext=None,
                        iconshape='128x128'
                    )

                st.info('Filetype: **YAML**')

    # if IS_GITHUB:
    #     U.show_not_implemented_banner()


if __name__ == "__main__":
    main()