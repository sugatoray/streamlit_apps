# cspell: disable
import base64
import os
import time

import pandas as pd
import streamlit as st

TIMESTR: str = time.strftime("%Y%m%d-%H%M%S")


def text_downloader(raw_text):
    b64 = base64.b64encode(raw_text.encode()).decode()
    new_filename = "new_text_file_{}_.txt".format(timestr)
    st.markdown("#### Download File ###")
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href, unsafe_allow_html=True)


def csv_downloader(data):
    csvfile = data.to_csv()
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "new_text_file_{}_.csv".format(timestr)
    st.markdown("#### Download File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href, unsafe_allow_html=True)


class FileDownloader(object):
    """FileDownloader class.

    Usage:
        >>> download = FileDownloader(data, filename, file_ext).download()
    """

    def __init__(self, data, filename='myfile', file_ext='txt', use_timestamp: bool=False):
        super(FileDownloader, self).__init__()
        self.data = data
        self.filename = filename
        self.file_ext = file_ext
        self.use_timestamp = use_timestamp

    def download(self, header='#### Download File', hyperlinktext='Click here!!', iconshape='64x64'):
        if hyperlinktext is None:
            icon_width, icon_height = iconshape.split('x')
            hyperlinktext = f'<img src="https://freeiconshop.com/wp-content/uploads/edd/download-flat.png" width="{icon_width}" height="{icon_height}">'
        b64 = base64.b64encode(self.data.encode()).decode()
        if self.use_timestamp:
            new_filename = f"{self.filename}_{TIMESTR}.{self.file_ext}"
        else:
            new_filename = f"{self.filename}.{self.file_ext}"
        if header:
            st.markdown(header)
        href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">{hyperlinktext}</a>'
        st.markdown(href, unsafe_allow_html=True)
