import os
import streamlit as st
from textwrap import dedent

from components import utils as U
from components import appfactory as A

Defaults = U.Defaults

def main():
    options = dict()

    os.environ["RECIPES_DIR"] = os.path.join(
        Defaults.APP_DIR, Defaults.DEFAULT_RECIPES_DIR)

    recipes_dir = U.create_recipes_dir(recipes_dir=None, app_dir=Defaults.APP_DIR)


    st.header("Conda Forger App :zap:")

    st.write(dedent("""
        This app helps you in creating **conda-forge** recipes.

        > *Powered by* [**`grayskull`**](https://github.com/conda-incubator/grayskull) ❤️
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

    st.info(dedent(f"""### Tip 💡
        If the recipe generation fails, you may want to try with 
        a higher timeout (`>{options.get("timeout")},<={A.MAX_TIME_OUT}` seconds).
        """))

    IS_PYPI = U.source_pypi(options)
    IS_GITHUB = U.source_github(options)
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

    # if IS_GITHUB:
    #     U.show_not_implemented_banner()


if __name__ == "__main__":
    main()