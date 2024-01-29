package require autopsf
package require mutator

set filelist [glob *fep.pdb]
set sortedfilelist [lsort -dictionary $filelist]
foreach file $sortedfilelist {
set filewhext [file rootname $file]
mol new $file
mol addfile ${filewhext}.psf type psf
set strmolid [molinfo top]
#autopsf -mol $strmolid -protein -top top_all22_prot.inp
package require solvate
solvate ${filewhext}.psf ${filewhext}.pdb -t 10 -o ${filewhext}_wb
package require autoionize
autoionize -psf ${filewhext}_wb.psf -pdb ${filewhext}_wb.pdb -o ${filewhext}_wb_ionized -seg ION -sc 0.15 -cation POT -anion CLA -from 5 -between 5
#mutator -psf ${filewhext}_autopsf_wb_ionized.psf -pdb ${filewhext}_autopsf_wb_ionized.pdb -o mutout -ressegname AP1 -resid 330 -mut THR -FEP ${filewhext}_autopsf_wb_ionized_fep
resetpsf
mol delete all
}

#mutator -psf <psffile> -pdb <pdbfile> -o <prefix>  -ressegname <targetresiduesegname> -resid <targetresid> -mut <resname> -FEP <prefix2>
