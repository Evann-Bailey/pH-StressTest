import numpy as np
from biopandas.pdb import PandasPdb

def peel_protein_shell(input_pdb, output_pdb, strip_percent):
    """
    Calculates center of mass, measures residue-level distances,
    and deletes the outermost X% of residues (and strips waters).
    """
    ppdb = PandasPdb().read_pdb(input_pdb)
    df_atom = ppdb.df['ATOM']
    if df_atom.empty:
        return False
        
    center_x = df_atom['x_coord'].mean()
    center_y = df_atom['y_coord'].mean()
    center_z = df_atom['z_coord'].mean()
    
    df_atom = df_atom.copy()
    df_atom['distance_to_center'] = np.sqrt(
        (df_atom['x_coord'] - center_x)**2 + 
        (df_atom['y_coord'] - center_y)**2 + 
        (df_atom['z_coord'] - center_z)**2
    )
    
    res_keys = ['chain_id', 'residue_number', 'insertion']
    res_distances = df_atom.groupby(res_keys)['distance_to_center'].mean().reset_index()
    
    keep_percent = (100.0 - strip_percent) / 100.0
    if keep_percent <= 0:
        return False
    cutoff_distance = np.percentile(res_distances['distance_to_center'], keep_percent * 100)
    
    kept_res = res_distances[res_distances['distance_to_center'] <= cutoff_distance]
    ppdb.df['ATOM'] = df_atom.merge(kept_res[res_keys], on=res_keys, how='inner').drop(columns=['distance_to_center'])
    
    if not ppdb.df['HETATM'].empty:
        df_het = ppdb.df['HETATM']
        df_het_clean = df_het[df_het['residue_name'] != 'HOH'].copy()
        if not df_het_clean.empty:
            df_het_clean['distance_to_center'] = np.sqrt(
                (df_het_clean['x_coord'] - center_x)**2 + 
                (df_het_clean['y_coord'] - center_y)**2 + 
                (df_het_clean['z_coord'] - center_z)**2
            )
            ppdb.df['HETATM'] = df_het_clean[df_het_clean['distance_to_center'] <= cutoff_distance].drop(columns=['distance_to_center'])
        else:
            ppdb.df['HETATM'] = df_het_clean

    ppdb.to_pdb(path=output_pdb, records=['ATOM', 'HETATM'])
    return True
