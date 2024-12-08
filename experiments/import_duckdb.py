import duckdb
import time
import matplotlib.pyplot as plt
import os

# Define helper functions
def plot_histogram(data, title):
    plt.hist(data, bins=100, edgecolor='k')
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()

# Define datasets and queries
datasets = [
    "/Users/nahid/Documents/Duckdb_Project/b/Run2012B_SingleMu_1000.parquet",
    "/Users/nahid/Documents/Duckdb_Project/b/Run2012B_SingleMu_4000.parquet"
]

queries = {
    "Q1": "SELECT MET.pt AS Emiss_T FROM hep_data",
    "Q2": "SELECT UNNEST(Jet).pt AS Jet_pT FROM hep_data",
    "Q3": """
        SELECT jet.pt AS Jet_pT
        FROM (SELECT UNNEST(Jet) AS jet FROM hep_data) AS jet
        WHERE ABS(jet.eta) < 1
    """,
    "Q4": """
        SELECT MET.pt AS Emiss_T
        FROM hep_data
        WHERE (
            SELECT COUNT(*) 
            FROM (SELECT UNNEST(Jet) AS jet FROM hep_data) AS jet
            WHERE jet.pt > 40
        ) >= 2
    """,
    "Q5": """
        SELECT MET.pt AS Emiss_T
        FROM hep_data, (select UNNEST(Muon) as muon1 from hep_data) AS muon1, (select UNNEST(Muon) as muon2 from hep_data) AS muon2
        WHERE muon1.charge != muon2.charge
            AND ABS(muon1.pt + muon2.pt) BETWEEN 60 AND 120
        LIMIT 100000
    """,
    "Q6a": """
        WITH trijet_combinations AS (
            SELECT trijet.pt AS Trijet_pT
            FROM hep_data, (SELECT UNNEST(Jet) AS trijet FROM hep_data) AS trijet
            WHERE ABS(trijet.mass - 172.5) = (
                SELECT MIN(ABS(trijet.mass - 172.5))
                FROM (SELECT UNNEST(Jet) AS trijet FROM hep_data) AS trijet
            )
        )
        SELECT Trijet_pT FROM trijet_combinations
    """,
    "Q6b": """
        WITH trijet_combinations AS (
            SELECT trijet.pt AS Trijet_pT, MAX(trijet.btag) AS Max_b_tagging
            FROM (SELECT UNNEST(Jet) AS trijet FROM hep_data) AS trijet
            WHERE ABS(trijet.mass - 172.5) = (
                SELECT MIN(ABS(trijet.mass - 172.5))
                FROM (SELECT UNNEST(Jet) AS trijet FROM hep_data) AS trijet
            )
            GROUP BY trijet.pt
        )
        SELECT Max_b_tagging FROM trijet_combinations
    """,
    "Q7": """
        SELECT SUM(jet1.pt) AS Scalar_sum_pT
        FROM hep_data, (SELECT UNNEST(Jet) AS jet1 FROM hep_data) AS jet1
        WHERE jet1.pt > 30
          AND NOT EXISTS (
              SELECT 1
              FROM (SELECT UNNEST(Muon) AS lepton FROM hep_data) AS lepton
              WHERE ABS(jet1.eta - lepton.eta) < 0.4 
                AND ABS(jet1.phi - lepton.phi) < 0.4
          )
        GROUP BY event
    """,
    "Q8": """
        WITH lepton_pair AS (
            SELECT lepton1.pt AS pt1, lepton2.pt AS pt2, 
                   (lepton1.pt + lepton2.pt) AS transverse_mass
            FROM hep_data, 
                 (SELECT UNNEST(Muon) AS lepton1 FROM hep_data) AS lepton1,
                 (SELECT UNNEST(Muon) AS lepton2 FROM hep_data) AS lepton2
            WHERE ABS(lepton1.pt - lepton2.pt) BETWEEN 60 AND 120
        )
        SELECT transverse_mass
        FROM lepton_pair
        WHERE transverse_mass IS NOT NULL
        LIMIT 200000
    """
}

# Initialize DuckDB connection
con = duckdb.connect(database=':memory:')

# Run benchmarks
results = []

for dataset in datasets:
    if not os.path.exists(dataset):
        print(f"Dataset {dataset} not found, skipping.")
        continue

    print(f"\nProcessing dataset: {dataset}")
    
    # Drop the existing table if it exists
    con.execute("DROP TABLE IF EXISTS hep_data")
    
    # Create the new table
    con.execute(f"CREATE TABLE hep_data AS SELECT * FROM read_parquet('{dataset}')")

    for query_id, query in queries.items():
        print(f"Running {query_id}...")
        try:
            # Measure execution time
            start_time = time.time()
            result = con.execute(query).fetchall()
            end_time = time.time()

            # Log execution time
            elapsed_time = end_time - start_time
            print(f"{query_id} executed in {elapsed_time:.4f} seconds")

            # Optional: Visualize results
            if query_id.startswith("Q"):
                plot_histogram([row[0] for row in result if row[0] is not None], title=query_id)

            # Record result
            results.append({
                "query_id": query_id,
                "dataset": dataset,
                "running_time": elapsed_time,
                "result_count": len(result)
            })

        except Exception as e:
            print(f"Error running {query_id}: {e}")


# Print summary of results
print("\nSummary of Results:")
for res in results:
    print(res)
