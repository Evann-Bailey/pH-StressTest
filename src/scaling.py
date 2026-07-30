import numpy as np
from biopandas.pdb import PandasPdb

def scale_coordinate_matrix(input_pdb, output_pdb, scale_percent):
    """Uniformly expands or contracts atomic coordinates by scale_percent."""
    ppdb = PandasPdb().read_pdb(input_pdb)
    factor = 1.0 + (scale_percent / 100.0)
    
    df_atom = ppdb.df['ATOM']
    if df_atom.empty:
        return False
        
    cx, cy, cz = df_atom['x_coord'].mean(), df_atom['y_coord'].mean(), df_atom['z_coord'].mean()
    
    for record in ['ATOM', 'HETATM']:
        if not ppdb.df[record].empty:
            ppdb.df[record]['x_coord'] = cx + (ppdb.df[record]['x_coord'] - cx) * factor
            ppdb.df[record]['y_coord'] = cy + (ppdb.df[record]['y_coord'] - cy) * factor
            ppdb.df[record]['z_coord'] = cz + (ppdb.df[record]['z_coord'] - cz) * factor
            
    ppdb.to_pdb(path=output_pdb)
    return True
