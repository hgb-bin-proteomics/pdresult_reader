#!/usr/bin/env python3

# 2024 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

## REQUIREMENTS
# pip install pandas
# pip install openpyxl

# set study folder path here
PDRESULT_FOLDER = "study_folder"

################################################################################

import glob
import sqlite3
import pandas as pd

def read_results(folder_name: str = PDRESULT_FOLDER) -> pd.DataFrame:
    result = {"file": [],
              "#PSM": [], "#PSM@5%FDR": [], "#PSM@1%FDR": [],
              "#CSM": [], "#CSM@5%FDR": [], "#CSM@1%FDR": [],
              "#CSM_target": [], "#CSM@5%FDR_target": [], "#CSM@1%FDR_target": [],
              "#XL": [], "#XL@5%FDR": [], "#XL@1%FDR": [],
              "#XL_target": [], "#XL@5%FDR_target": [], "#XL@1%FDR_target": []}
    for f in glob.glob(f"{folder_name}/*.pdResult"):
        conn = sqlite3.connect(f)
        psms = pd.read_sql_query("SELECT * FROM TargetPsms", conn)
        csms = pd.read_sql_query("SELECT * FROM CSMs", conn)
        crosslinks = pd.read_sql_query("SELECT * FROM Crosslinks", conn)
        result["file"].append(f.split("\\")[-1].strip())
        result["#PSM"].append(psms.shape[0])
        result["#PSM@5%FDR"].append(psms[psms["MatchConfidence"] > 1].shape[0])
        result["#PSM@1%FDR"].append(psms[psms["MatchConfidence"] > 2].shape[0])
        result["#CSM"].append(csms.shape[0])
        result["#CSM_target"].append(csms[(csms["AlphaTD"] == "T") & (csms["BetaTD"] == "T")].shape[0])
        result["#CSM@5%FDR"].append(csms[csms["MatchConfidence"] > 1].shape[0])
        result["#CSM@5%FDR_target"].append(csms[(csms["MatchConfidence"] > 1) & (csms["AlphaTD"] == "T") & (csms["BetaTD"] == "T")].shape[0])
        result["#CSM@1%FDR"].append(csms[csms["MatchConfidence"] > 2].shape[0])
        result["#CSM@1%FDR_target"].append(csms[(csms["MatchConfidence"] > 2) & (csms["AlphaTD"] == "T") & (csms["BetaTD"] == "T")].shape[0])
        result["#XL"].append(crosslinks.shape[0])
        result["#XL_target"].append(crosslinks[crosslinks["Decoy"] == False].shape[0])
        result["#XL@5%FDR"].append(crosslinks[crosslinks["Confidence"] > 1].shape[0])
        result["#XL@5%FDR_target"].append(crosslinks[(crosslinks["Confidence"] > 1) & (crosslinks["Decoy"] == False)].shape[0])
        result["#XL@1%FDR"].append(crosslinks[crosslinks["Confidence"] > 2].shape[0])
        result["#XL@1%FDR_target"].append(crosslinks[(crosslinks["Confidence"] > 2) & (crosslinks["Decoy"] == False)].shape[0])
    result_df = pd.DataFrame(result)
    result_df.to_csv(folder_name + ".csv", index = False)
    result_df.to_excel(folder_name + ".xlsx", index = False)
    return result_df

if __name__ == "__main__":
    read_results()
