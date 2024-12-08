# 🦆 Evaluating High-Energy Physics Data Queries Using DuckDB

![High-Energy Physics Banner](https://via.placeholder.com/1200x400?text=High-Energy+Physics+Benchmarks+with+DuckDB)

Welcome to the repository for **"Evaluating High-Energy Physics Data Queries Using DuckDB"**. This project benchmarks DuckDB's performance for high-energy physics queries inspired by the VLDB paper, [*"Evaluating Query Languages and Systems for High-Energy Physics Data"*](https://www.vldb.org/pvldb/vol15/p154-muller.pdf). Explore the power of DuckDB for local analytical workloads and learn how it compares to distributed systems.

---

## 📜 About This Project

DuckDB is a lightweight, in-process analytical database management system optimized for Online Analytical Processing (OLAP) workloads. This repository replicates and extends the high-energy physics benchmarks outlined in the VLDB paper, demonstrating DuckDB’s capabilities on smaller datasets.

### Key Highlights
- **💡 Lightweight Setup**: Benchmarks run on a local environment (MacBook Air with M2 chip).
- **📊 Performance Analysis**: Execution times for multiple queries on datasets of different sizes.
- **🌌 High-Energy Physics Focus**: Evaluates realistic queries from high-energy physics datasets.

---

## 📄 Related Papers and Resources

- 📘 **VLDB Paper**: [Evaluating Query Languages and Systems for High-Energy Physics Data](https://www.vldb.org/pvldb/vol15/p154-muller.pdf)  
  The original paper that inspired this benchmarking project.

- 📂 **Benchmark Scripts**: [Zenodo Benchmark Scripts Repository](https://zenodo.org/records/6505492)  
  Official scripts and resources for the benchmarks evaluated in the paper.

---

## 🚀 Getting Started

Follow these steps to reproduce the benchmarks and explore the results:

### Prerequisites
1. Install [DuckDB](https://duckdb.org/).
2. Ensure you have Python or your preferred programming language environment set up.
3. Download the required datasets:
   - [Run2012B_SingleMu_1000.parquet](https://zenodo.org/record/6505492/files/Run2012B_SingleMu_1000.parquet)
   - [Run2012B_SingleMu_4000.parquet](https://zenodo.org/record/6505492/files/Run2012B_SingleMu_4000.parquet)

---

## 📊 Results Overview

DuckDB demonstrated excellent performance for smaller datasets, handling high-energy physics queries efficiently. For larger datasets, distributed systems like Presto or BigQuery may offer scalability advantages. Full details are available in the report included in this repository.

---

## 🛠️ Repository Contents

- **`experiment/`**: Scripts for running DuckDB benchmarks.
- **`datasets/`**: Smaller versions of the high-energy physics datasets.
- **`report/`**: The LaTeX report and PDF file detailing the results.
- **`results/`**: Output from the benchmarks, including execution times and query results.

