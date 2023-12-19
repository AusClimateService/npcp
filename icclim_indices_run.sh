#!/bin/bash
#PBS -P xv83
#PBS -q normal
#PBS -l walltime=2:00:00
#PBS -l mem=96GB
#PBS -l storage=scratch/xv83+gdata/xv83+gdata/wp00+gdata/hh5+gdata/ia39
#PBS -l wd
#PBS -l ncpus=5

module use /g/data3/hh5/public/modules
module load conda/analysis3


declare -a metrics=("R95pTOT" "R99pTOT" "WSDI" "CSDI" "R20mm" "R10mm" "FD")
declare -A var_metrics
var_metrics["R95pTOT"]="pr"
var_metrics["R99pTOT"]="pr"
var_metrics["WSDI"]="tasmax"
var_metrics["CSDI"]="tasmin"
var_metrics["R20mm"]="pr"
var_metrics["R10mm"]="pr"
var_metrics["FD"]="tasmin"

declare -a methods=("ecdfm" "qdm")
declare -a rcms=("BOM-BARPA-R" "CSIRO-CCAM-2203" "UQ-DES-CCAM-2105")

for metric in "${metrics[@]}"; do
    for rcm in "${rcms[@]}"; do
        for method in "${methods[@]}"; do
            declare -a tasks=()  

            case ${method} in
                "qdm")
                    tasks=("xvalidation" "projection")
                    ;;
                "ecdfm")
                    tasks=("historical" "xvalidation" "projection")
                    ;;
                *)
                    echo "Unknown method: ${method}"
                    exit 1
                    ;;
            esac

            for task in "${tasks[@]}"; do
                data_dir="/g/data/ia39/npcp/data/${var_metrics[$metric]}/CSIRO-ACCESS-ESM1-5/${rcm}/${method}/task-${task}"
                ### out_dir="${data_dir}/${metric}"
				out_dir="/g/data/ia39/npcp/data/icclim/${metric}"
                if [ ! -d "$out_dir" ]; then
					# echo "Directory is missing"
                    mkdir -p "$out_dir"
                else
					echo "Directory '$out_dir' already exists."
					### rm -rf "$out_dir"  
                fi

				if [[ ${var_metrics[$metric]} == "pr" ]]; then
					method_amend="multiplicative-monthly"
					interp="linear"
					q="q100"
					case ${method} in
						"qdm")
							q="q1000"
							method_amend="multiplicative"
							interp="nearest"
							;;
						"ecdfm")
							;;
						*)
							echo "Unknown method: ${method}"
							exit 1
							;;
					esac
				else
					method_amend="additive-monthly"
					interp="nearest"
					q="q100"
				fi

				case ${task} in
					"historical")
						start_date=19800101
						end_date=20191231
						start_date_train=19800101
						end_date_train=20191231
						;;
					"xvalidation")
						start_date=19900101
						end_date=20191231
						start_date_train=19600101
						end_date_train=19891231
						;;
					"projection")
						start_date=20600101
						end_date=20991231
						start_date_train=19800101
						end_date_train=20191231
						;;
					*)
						echo "Unknown task: ${task}"
						exit 1
						;;
				esac

				infile="${data_dir}/${var_metrics[$metric]}_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_${rcm}_v1_day_${start_date}-${end_date}_${method}-${method_amend}-${q}-${interp}-AGCD-${start_date_train}-${end_date_train}.nc"
				outfile="${out_dir}/${metric}_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_${rcm}_v1_day_${start_date}-${end_date}_${method}-${method_amend}-${q}-${interp}-AGCD-${start_date_train}-${end_date_train}.nc"

				echo "Processing $metric for ${var_metrics[$metric]}, $rcm, $method, $task"
				echo "Input file: $infile"
				echo "Output file: $outfile"
				
				if [ ! -f "$outfile" ]; then
					python /g/data/xv83/users/at2708/bias_adjustment/evaluation/indices/run_icclim.py --input_files "$infile" --variable "${var_metrics[$metric]}" --verbose "$metric" "$outfile"
				else
					echo "File '$outfile' already exists."
				fi
            done
        done
    done
done




