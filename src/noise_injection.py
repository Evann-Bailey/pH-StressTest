import numpy as np
from biopandas.pdb import PandasPdb

def apply_isotropic_noise(input_pdb, output_pdb, sigma):
    """Applies Gaussian noise N(0, sigma) independently to X, Y, Z coordinates."""
    ppdb = PandasPdb().read_pdb(input_pdb)
    for record in ['ATOM', 'HETATM']:
        if not ppdb.df[record].empty:
            num_atoms = len(ppdb.df[record])
            ppdb.df[record]['x_coord'] += np.random.normal(0, sigma, num_atoms)
            ppdb.df[record]['y_coord'] += np.random.normal(0, sigma, num_atoms)
            ppdb.df[record]['z_coord'] += np.random.normal(0, sigma, num_atoms)
    ppdb.to_pdb(path=output_pdb)

def apply_anisotropic_noise(input_pdb, output_pdb, sigma, axis='x'):
    """Applies Gaussian noise along a single structural axis (x, y, or z)."""
    ppdb = PandasPdb().read_pdb(input_pdb)
    axis_col = f"{axis.lower()}_coord"
    for record in ['ATOM', 'HETATM']:
        if not ppdb.df[record].empty:
            num_atoms = len(ppdb.df[record])
            ppdb.df[record][axis_col] += np.random.normal(0, sigma, num_atoms)
    ppdb.to_pdb(path=output_pdb)
