"""Public dataset discovery with explicit origin and rights."""

from datascout.discovery import filter_datasets, load_discovery
from datascout.ui_i18n import label, t
from datascout.ui_theme import card


def render_catalog(st, *, preview_only=False):

    lang = st.session_state.get("ui_language", "zh")
    items = load_discovery()
    previous_language = st.session_state.get("catalog_filter_language")
    if previous_language is not None and previous_language != lang:
        st.session_state["catalog_search"] = ""
    st.session_state["catalog_filter_language"] = lang
    st.caption(t(st, "发现 · 比较 · 选择", "DISCOVER · COMPARE · CHOOSE"))
    st.title(t(st, "找到适合你的下一份数据。", "Find the data for your next idea."))
    st.write(
        t(
            st,
            "浏览公开数据的用途、来源和许可。本站收录元数据；完整数据请从官方获取。",
            "Explore uses, sources and licenses. We host metadata; access full datasets through their publishers.",
        )
    )
    search = st.text_input(
        t(st, "搜索数据集", "Search datasets"),
        placeholder=t(st, "例如：共享单车、空气质量、驾驶", "Try: bike, air quality, driving"),
        key="catalog_search",
    )
    cols = st.columns(3)
    all_label = t(st, "全部", "All")

    def fmt(x):
        return all_label if x == "all" else label(x, lang)

    task = cols[0].selectbox(
        t(st, "用途", "Task"),
        ["all", "vision", "classification", "regression", "time_series"],
        format_func=fmt,
        key="catalog_task_" + lang,
    )
    typ = cols[1].selectbox(
        t(st, "数据类型", "Data type"),
        ["all", "tabular", "image", "multimodal"],
        format_func=fmt,
        key="catalog_type_" + lang,
    )
    access = cols[2].selectbox(
        t(st, "获取方式", "Access"),
        ["all", "free", "research"],
        format_func=fmt,
        key="catalog_access_" + lang,
    )
    matches = filter_datasets(items, query=search, task=task, data_type=typ, access=access)
    st.caption(
        t(
            st,
            f"显示 {len(matches)} / {len(items)} 个数据集",
            f"Showing {len(matches)} of {len(items)} datasets",
        )
    )
    if not matches:
        st.info(
            t(
                st,
                "未找到匹配项，请尝试其他关键词或筛选条件。",
                "No matches. Try another keyword or filter.",
            )
        )
    for start in range(0, len(matches), 3):
        columns = st.columns(3, gap="large")
        for column, item in zip(columns, matches[start : start + 3]):
            with column:
                card(
                    st,
                    item["name"] + (" · " + item["name_zh"] if lang == "zh" else ""),
                    item["description_" + lang],
                    symbol="search",
                    eyebrow=label(item["type"], lang) + " · " + label(item["access"], lang),
                )
                with st.expander(t(st, "来源、许可与获取", "Source, license and access")):
                    st.write(
                        t(st, "许可：", "License: ")
                        + (
                            item.get("license_en", item["license"])
                            if lang == "en"
                            else item["license"]
                        )
                    )
                    st.write(t(st, "规模：", "Scale: ") + item["scale_" + lang])
                    st.write(t(st, "文件格式：", "Formats: ") + item["formats_" + lang])
                    st.write(t(st, "发布版本：", "Edition: ") + item["source_version_" + lang])
                    st.write(
                        t(
                            st,
                            "注册要求：无需注册即可访问官方公开下载",
                            "Registration: public download without an account",
                        )
                        if item["registration"] == "not_required"
                        else t(
                            st,
                            "注册要求：请按发布方要求申请访问",
                            "Registration: follow the publisher's access requirements",
                        )
                    )
                    st.write(
                        t(
                            st,
                            "商业用途：按 CC BY 4.0 注明作者与来源，仍需遵守数据说明",
                            "Commercial use: credit authors and source under CC BY 4.0 and follow dataset-specific notes",
                        )
                        if item["commercial"] == "attribution_required"
                        else t(
                            st,
                            "商业用途：需要核验或联系发布方",
                            "Commercial use: verify terms or contact the publisher",
                        )
                    )
                    st.write(
                        t(st, "数据获取费用：免费", "Data access fee: free")
                        if item["acquisition_fee_cny"] == 0
                        else t(
                            st,
                            "数据获取费用：待确认或询价，不是 0 元",
                            "Data access fee: unconfirmed or by quotation, not zero",
                        )
                    )
                    st.write(
                        t(
                            st,
                            "商业许可费用：无单独许可费，需遵守署名等条件",
                            "Commercial license fee: no separate fee; attribution and other terms apply",
                        )
                        if item["commercial_license_fee_cny"] == 0
                        else t(
                            st,
                            "商业许可费用：待核验或询价",
                            "Commercial license fee: verify or request a quote",
                        )
                    )
                    if not preview_only and item["simulated_offer_cny"] is not None:
                        st.caption(
                            t(
                                st,
                                f"流程演示模拟报价：¥{item['simulated_offer_cny']:,.0f}（不代表实际费用）",
                                f"Simulated workflow offer: ¥{item['simulated_offer_cny']:,.0f} (not an actual price)",
                            )
                        )
                    st.write(item["conditions_" + lang])
                    st.caption(t(st, "来源核查：", "Source checked: ") + item["checked_on"])
                    st.link_button(
                        t(st, "访问官方数据 ↗", "Visit official dataset ↗"),
                        item["source"],
                        use_container_width=True,
                    )
                if not preview_only:
                    from datascout.ui_auth import current_account

                    if st.button(
                        t(st, "加入我的需求 →", "Use in my request →"),
                        key="select_dataset_" + item["id"],
                        use_container_width=True,
                    ):
                        st.session_state["selected_dataset"] = item["id"]
                        st.session_state["page"] = "buyer" if current_account(st) else "login"
                        st.rerun()
