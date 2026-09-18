import pandas as pd
import sqlite3

def get_anomalies():
    conn = sqlite3.connect("support_tickets.db")
    df = pd.read_csv("support_tickets.csv")
    conn.close()

    anomalies = []

    # 1. Statistical Outliers: Resolution time > (Mean + 3 * StdDev)
    resolved = df[df["status"] == "Resolved"].copy()
    mean_resol = resolved["resolution_time_hrs"].mean()
    std_resol = resolved["resolution_time_hrs"].std()
    threshold = mean_resol + (2.5 * std_resol)

    outliers = resolved[resolved["resolution_time_hrs"] > threshold]
    for _, row in outliers.iterrows():
        anomalies.append({
            "ticket_id": row["ticket_id"],
            "type": "Extreme Resolution Delay (Statistical)",
            "priority": row["priority"],
            "status": row["status"],
            "details": f"Resolution took {row['resolution_time_hrs']} hrs (Benchmark threshold: {threshold:.1f} hrs)"
        })

    # 2. Heuristic: Critical or High priority tickets still Unresolved
    stalled = df[(df["priority"].isin(["Critical", "High"])) & (df["status"].isin(["Open", "Escalated"]))]
    for _, row in stalled.iterrows():
        anomalies.append({
            "ticket_id": row["ticket_id"],
            "type": "Unresolved High/Critical Priority Bottleneck",
            "priority": row["priority"],
            "status": row["status"],
            "details": f"Issue: '{row['issue_summary']}' is currently {row['status']} assigned to {row['agent_id']}"
        })

    return {
        "total_anomalies": len(anomalies),
        "statistical_threshold_hrs": round(threshold, 2),
        "anomalies": anomalies
    }