# DataScout AI · Public Preview

This repository contains the **read-only public preview** of DataScout AI. It shows the product homepage and a catalog of 15 publicly described datasets, with links to their original publishers. It does not provide accounts, private uploads, procurement submissions, GPT evaluation, orders, or payments. Catalog descriptions are metadata; check source pages and licenses before using a dataset.

## Run locally

```bash
pip install -r preview/requirements.txt
streamlit run preview/streamlit_app.py
```

## Deploy on Streamlit Community Cloud

Connect this GitHub repository to Streamlit Community Cloud and select `preview/streamlit_app.py` as the entrypoint. Dependencies are listed beside the entrypoint in `preview/requirements.txt`. Streamlit will assign a `*.streamlit.app` URL. This repository contains no private account or runtime data.

The buyer/seller prototype is separate and currently runs locally. A public multiuser version needs persistent storage, production authentication, and per-user model authorization before deployment.

## Latest public preview · 2026-10-15

[Open the deployed preview](https://datascout-ai-preview.streamlit.app/).
This release syncs the current shared theme and preserves the original dataset
cards, hover lift, border highlight and shadow. Search, filters, bilingual labels,
official source links and all 15 catalog records remain available.

The public build is based on local source revision `65d7221`. The private buyer
workspace, model evaluation runner, accounts and runtime data are not part of this
repository or this deployment.
