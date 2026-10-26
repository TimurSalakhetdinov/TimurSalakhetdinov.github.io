# Timur Salakhetdinov - Portfolio Website

Personal portfolio site live at [timursalakhetdinov.com](https://timursalakhetdinov.com).

## About

Data Scientist & Data Analyst specialising in LLM agent systems for analytics workflows. Currently a Working Student in Analytics at InnoGames in Hamburg, testing Microsoft Fabric for analytics workflows, plus funnel and A/B-test analysis. In parallel, the company project is also my M.Sc. thesis at Leuphana University: daily net revenue over a 90-day horizon, with agent-compiled planning-text covariates tested against a shuffled-text placebo. The held-out evaluation is pending. I bring ten years of experience across telecommunications, finance, insurance, and gaming.

M.Sc. Management & Data Science at Leuphana Universität Lüneburg, Oct 2024 to Mar 2027 (expected), GPA 1.9 (German scale, 1.0 = best), Deutschlandstipendium scholar. Available full time in Germany from April 2027.

## Featured Projects

| Project | Description |
|---|---|
| One-off multi-agent LLM toolkit | Built a one-off multi-agent LLM toolkit (MCP) to speed up reporting work |
| [ChefTreff AI Hackathon 2025](https://github.com/TimurSalakhetdinov/Hackathon-2025) | Computer vision app to identify broken objects |
| [Pareto/NBD Model](https://github.com/TimurSalakhetdinov/Abe_2009_model_implementation) | Hierarchical Bayesian Pareto/NBD model (Abe 2009) on CDNOW dataset |
| [Applied Statistical Analysis](https://github.com/TimurSalakhetdinov/Applied-Statistical-Analysis) | Bayesian inference & time series modeling with PyMC |
| [Neo4j Graph Project](https://github.com/TimurSalakhetdinov/Networks-Project) | Artist influence network analysis using Neo4j & Cypher |
| [Knowledge Graph QA System](https://github.com/lucagem29/KGQA_Project) | Team project: SPARQL-based question answering over RDF knowledge graphs |
| [KVG ML Route Modelling](https://github.com/freiraum-bq/KVG_Ulf) | Team project: ML-based transportation route prediction |

## Tech Stack

**Languages:** Python (NumPy, Pandas, Scikit-Learn) · SQL (MS SQL Server, Hive, StarRocks)

**LLM & Agents:** LangGraph · MCP · tool calling · RAG · coding agents

**ML & Forecasting:** TabPFN · Chronos · TimesFM · LightGBM · PyMC · PyTorch

**Methods:** time-series forecasting · A/B testing · cohort and churn analysis · customer segmentation

**Tools & Platforms:** Microsoft Fabric / Power BI · Apache Superset · Docker · Git

## Contact

- Email: [timsalakhetdinov@gmail.com](mailto:timsalakhetdinov@gmail.com)
- LinkedIn: [linkedin.com/in/timursalakhetdinov](https://www.linkedin.com/in/timursalakhetdinov)
- GitHub: [github.com/TimurSalakhetdinov](https://github.com/TimurSalakhetdinov)

## Built With

Hand-written HTML / CSS / vanilla JS. Visitor counts use GoatCounter, a privacy-friendly, cookie-free counter that stores no personal data. No framework.

## Writing / articles

Articles are Markdown files in `content/writing/`. Add `content/writing/<slug>.md` with YAML front matter (`title`, `date` as `YYYY-MM-DD`, `description`, `slug`, `tags`, and optional `og_image`, `substack_url`, `updated`, and `related_projects`). Put images in `content/writing/<slug>/`. Files whose names start with `_` are drafts and are not published; `content/writing/_example.md` shows the format.

```bash
python3 -m pip install -r scripts/requirements-writing.txt
python3 scripts/build_writing.py
```

The script writes `writing/index.html`, each `writing/<slug>.html`, and `writing/feed.xml`, and updates the `/writing/` entries in `sitemap.xml`. It also refreshes the homepage Writing block in `index.html` and `de.html` (between the `writing:latest` markers) and the `data-writing-nav` link on every page that shares the nav. With no published articles that block stays hidden and the nav link points at `/writing/`. The first article shows the three newest cards (`HOME_LATEST_COUNT` in `scripts/build_writing.py`) and points the nav at the block. The format is documented in `content/writing/README.md`. Run the script again after edits; a second run with the same sources does not change the output.
