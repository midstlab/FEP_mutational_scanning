# FEP_mutational_scanning

Mutational scanning of proteins using Free Energy Perturbation (FEP) simulations. In this pipeline, any amino acid position can be mutated to all possible single mutations, excluding GLY and PRO amino acids.
This pipeline consists of 7 steps:
- 1mutation_script.tcl: Mutates each residue to every other residue and generates psf and fep files.
- 2autopsf_batch_fep_after.tcl: Performs solvation and ionization processes.
- 3fep_file_correct_ion_anni_wt_res_neg.ipynb, 3fep_file_correct_ion_anni_wt_res_neu.ipynb, and 3fep_file_correct_ion_anni_wt_res_pos.ipynb: These scripts edit the ions (K and Cl atoms) to preserve the neutral charge of the system. Since the charge of the system changes between the mutations, such as negative to positive or neutral to positive, the variables of the code (annihilation of K or Cl) vary.
- 4fep_min_config_gen.py: Generates a configuration file for the minimization process.
- 5fep_forw_config_gen.py: Generates a configuration file for the forward FEP simulation.
- 6fep_back_config_gen.py: Generates a configuration file for the backward FEP simulation.
- 7config_file_jobgen.py: Generates a 'SLURM' submission script to perform serial and parallel FEP simulations on an HPC.
