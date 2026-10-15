"""Shareable, read-only DataScout preview with no account or GPT route."""

import streamlit as st

from datascout.ui_catalog import render_catalog
from datascout.ui_home import render_home
from datascout.ui_i18n import t
from datascout.ui_theme import apply_theme, brand

PREVIEW_BUILD = "2026-10-15-65d7221"


def main():
    st.set_page_config(page_title="DataScout AI · Preview", page_icon="◈", layout="wide")
    apply_theme(st)
    page = st.session_state.get("page", "home")
    if page not in {"home", "catalog"}:
        page = "home"
        st.session_state["page"] = page
    with st.container(key="site_nav"):
        nav = st.columns([3.3, 1.7, 2.2, 1.4, 2])
        with nav[0]:
            brand(st)
        if nav[1].button(
            t(st, "产品首页", "Home"),
            key="nav_home",
            icon=":material/home:",
            use_container_width=True,
        ):
            st.session_state["page"] = "home"
            st.rerun()
        if nav[2].button(
            t(st, "数据集广场", "Dataset marketplace"),
            key="nav_catalog",
            icon=":material/dataset:",
            use_container_width=True,
        ):
            st.session_state["page"] = "catalog"
            st.rerun()
        nav[3].selectbox(
            "Language / 语言",
            ["zh", "en"],
            format_func=lambda value: "中文" if value == "zh" else "English",
            key="ui_language",
            label_visibility="collapsed",
        )
        nav[4].html(
            f'<div class="ds-preview-badge" data-build="{PREVIEW_BUILD}">'
            + t(st, "公开预览 · 只读", "Public preview · Read only")
            + "</div>"
        )
    if page == "home":
        render_home(st, preview_only=True)
    else:
        render_catalog(st, preview_only=True)


if __name__ == "__main__":
    main()
