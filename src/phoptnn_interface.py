import os
import subprocess
import pandas as pd

def run_phoptnn_inference(pdb_file, custom_env, pred_csv_path):
    """Executes pHoptNN inference via subprocess and returns predicted optimum pH."""
    cmd = ["python", "phoptnn_interface.py", pdb_file]
    result = subprocess.run(cmd, capture_output=True, text=True, env=custom_env)
    
    if os.path.exists(pred_csv_path) and (result.returncode == 0):
        try:
            df_pred = pd.read_csv(pred_csv_path)
            return float(df_pred.iloc[0]['ph_optimum_pred'])
        except Exception:
            return None
    return None
