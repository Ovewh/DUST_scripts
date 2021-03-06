# Shell script for doing initial processing of FLEXPART/FLEXDUST model output
# This might take a while to run...
# Dependencies, DUST python package, process_flexpart.py script
#
# Author: Ove Haugvaldstad
shopt -s extglob
shopt -s globstar

export PATH=$PATH:~/DUST_scripts/scripts/DUST

DATAPATH='/projects/NS2806K/ovewh/tracing_the_winds/flexpart/FLEXPART_spring/emission_sensitivities/'
OUTPATH='/projects/NS2806K/ovewh/tracing_the_winds/flexpart/FLEXPART_spring/source_contribution/'
PATHFLEXDUST='/projects/NS2806K/ovewh/tracing_the_winds/FLEXDUST_emission_flux/FLEXDUST1999_2019/'
SUBDIRS=('Conc' 'DryDep' 'WetDep')

#SUBDIRS=('Conc')

ps=('20micron' '2micron')

#liocations=('SACOL' 'BADOE' 'YINCHUAN' 'LINGTAI' 'LUOCHUAN' 'LANTIAN' 'SHAPOTOU')


proc_output () {
    echo "processing: $1"
    process_flexpart.py $1 $2 --op $3 --x0 73 --x1 115 --y0 30 --y1 50
}



for dir in "${SUBDIRS[@]}"; do
   mkdir ${OUTPATH}${dir} 
   for size in "${ps[@]}"; do
       mkdir ${OUTPATH}${dir}/${size}
       cd  ${DATAPATH}${dir}/${size}
       for year in {1999..2019}; do
           mkdir ${OUTPATH}${dir}/${size}/${year}
           if [[ -d ./surface_sensitivity/gridtime_${year}0306-00_${year}0331-21 ]]; then
                    
               cd surface_sensitivity/
               for ncf in ./gridtime_${year}*/*.nc; do
                    proc_output ${ncf} ${PATHFLEXDUST}${year}/ ${OUTPATH}${dir}/${size}/${year} 
                done
                cd ..
           else
                for ncf in ./${year}/**/output/*.nc; do
                    proc_output ${ncf} ${PATHFLEXDUST}${year}/ ${OUTPATH}${dir}/${size}/${year} 
                done
           fi
            
        done
    done
done



