import streamlit as st
import emoji
from typing import Union, Tuple

st.set_page_config(layout="wide")


class AppUISection(object):

    def __init__(self, num_cols: Union[int, Tuple[int]] = 1):
        self.num_cols = num_cols
        self.cols = st.beta_columns(num_cols)

title_text = "**Streamlit** Has an **Emoji Problem** :fire:: _**Here's a fix**_ :+1::zap:"
st.title(title_text)

st.write('> Author: Sugato Ray | Social: [github](https://github.com/sugatoray)')

green_circle = emoji.emojize(':green_circle:')

st.write(f"""
Streamlit works fine (mostly) with `markdown` text, and hence, also
seems to work well with anything that markdown allows. However, recently
I came across a **glitch** in Streamlit: I discovered that some
emojis, although supported by GitHub flavored markdown, **FAIL** to
render properly in Streamlit.

Take for instance `:fire:` :fire: and `:green_circle:` {green_circle} in
the following two examples. While `:fire:` renders successfully,
`:green_circle:` **fails to render**. :no_entry:
""")

st.success("The markdown syntax for 🔥 renders fine... `:fire:`\t :fire:")

sec1 = AppUISection(num_cols=(3,2))
sec1.cols[0].code('# run this code 🔥\nst.write("Let us write an emoji `:fire:`\\t :fire:")')
fire_pressed = sec1.cols[1].button('Run snippet?', key='run_fire')
if fire_pressed:
    sec1.cols[1].write("Let us write an emoji `: fire: `\t:fire: ")

st.error("The markdown syntax for 🟢 **FAILS** to render`:green_circle:`\t :green_circle:")

sec2 = AppUISection(num_cols=(3, 2))
sec2.cols[0].code('''# run this code 🟢
# import streamlit as st
st.write("Let us write an emoji `:fire:`\\t :green_circle:")
''')
green_circle_pressed = sec2.cols[1].button(
    'Run snippet?', key='run_green_circle')
if green_circle_pressed:
    sec2.cols[1].write("Let us write an emoji `:fire:`\t :green_circle:")


'''

### Any alternatives?

What if we use a `markdown` block directly instead of `st.write("your :emoji: here!")`?

- **Nope! it does not work!** :no_entry:

```python
# paste the following lines in the app.py file
use `markdown` block directly
  - :fire:
  - :green_circle:
```

---


## **So what is the fix?** :zap:

'''

st.warning('''
- use **`emoji`** library: https://github.com/carpedm20/emoji

  | Method of Installation |               Command                |
  |:----------------------:|:------------------------------------:|
  | **pip**                | `pip install emoji`                  |
  | **conda**              | `conda install -c conda-forge emoji` |
''')

st.write('''
  ```python
  import emoji

  # method-1: direct use of emoji.emojize()
  st.write(f'Try this out `:green_circle: -->` {emoji.emojize(":green_circle:")}')

  # Output: Try this out :green_circle: --> 🟢

  # method-2: indirect use of emoji.emojize() | with a variable
  green_circle = emoji.emojize(':green_circle:')
  st.write('Try this out `:green_circle: -->` {green_circle}')

  # Output: Try this out :green_circle: --> 🟢
  ```
''')

# sec3 = AppUISection(num_cols=(3, 2))
# sec2.cols[0].code('''# run this code 🟢
# # import streamlit as st
# st.write("Let us write an emoji `:fire:`\\t :green_circle:")
# ''')
fix_pressed = st.button('Run snippet?', key='run_fix')
if fix_pressed:
    st.write(f'> Try this out `:green_circle: -->` {green_circle}')

'''

---
Copyright: Sugato Ray, 2021

'''

with st.sidebar:

    st.write(f"""
    [{title_text}][#title]

    [#title]: #streamlit-has-an-emoji-problem-here-s-a-fix

    - [Any alternatives?](#any-alternatives)
    - [**So what is the fix?** :zap:](#so-what-is-the-fix)
    """)

