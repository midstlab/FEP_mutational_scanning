package require autopsf
package require mutator

set file wt_ap_100.pdb 
set filewhext [file rootname $file]
mol new $file

 

set sel1 [atomselect top "protein"]
set sel2 [atomselect top "(resname NDPH) or (resname D4PP)"]
$sel1 writepdb ${filewhext}_chainA.pdb
$sel2 writepdb ${filewhext}_chainB.pdb

resetpsf
mol delete all

for {set mutated_resid 69} {$mutated_resid < 70} {incr mutated_resid} {

set mutation_list {ALA ARG ASN ASP CYS GLU GLN HSD LEU LYS MET PHE SER THR TRP TYR VAL}
foreach mutation $mutation_list {

mol new ${filewhext}_chainA.pdb
set strmolid [molinfo top]

set wt_resname [[atomselect top "resid ${mutated_resid} and name CA"] get resname]

if {!($wt_resname == $mutation)} {


autopsf -mol $strmolid -top [list top_all36_prot.rtf top_all36_cgenff.rtf top_all36_na.rtf]
mutator -psf ${filewhext}_chainA_autopsf.psf -pdb ${filewhext}_chainA_autopsf.pdb -o mutout -resid $mutated_resid -mut $mutation -FEP ${filewhext}_chainA_${wt_resname}_${mutated_resid}_${mutation}_fep

resetpsf
mol delete all

mol new ${filewhext}_chainB.pdb
set strmolid [molinfo top]

autopsf -mol $strmolid -top [list top_all36_prot.rtf top_all36_cgenff.rtf top_all36_na.rtf TMPP.top D4TMPP.top]

resetpsf
mol delete all

readpsf ${filewhext}_chainA_${wt_resname}_${mutated_resid}_${mutation}_fep.fep.psf
readpsf ${filewhext}_chainB_autopsf.psf

coordpdb ${filewhext}_chainA_${wt_resname}_${mutated_resid}_${mutation}_fep.fep
coordpdb ${filewhext}_chainB_autopsf.pdb

writepsf ${filewhext}_${wt_resname}_${mutated_resid}_${mutation}_fep.psf
writepdb ${filewhext}_${wt_resname}_${mutated_resid}_${mutation}_fep.pdb

resetpsf
mol delete all


}
}
}
