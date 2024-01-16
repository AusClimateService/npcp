#!/bin/bash
#PBS -P e53
#PBS -q normal
#PBS -l walltime=2:00:00
#PBS -l mem=96GB
#PBS -l storage=scratch/xv83+gdata/xv83+gdata/wp00+gdata/hh5+gdata/ia39+gdata/e53
#PBS -l wd
#PBS -l ncpus=5

module use /g/data3/hh5/public/modules
module load conda/analysis3

###### bias-corrected models
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
declare -a rcms=("GCM" "BOM-BARPA-R" "CSIRO-CCAM-2203" "UQ-DES-CCAM-2105")
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
				out_dir="/g/data/ia39/npcp/data/icclim/${metric}"
                if [ ! -d "$out_dir" ]; then
                    mkdir -p "$out_dir"
                else
					echo "Directory '$out_dir' already exists."
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



###### RCMs BC QME
# declare -a metrics=("R95pTOT" "R99pTOT" "WSDI" "CSDI" "R20mm" "R10mm" "FD")
# declare -A var_metrics
# var_metrics["R95pTOT"]="pr"
# var_metrics["R99pTOT"]="pr"
# var_metrics["WSDI"]="tasmax"
# var_metrics["CSDI"]="tasmin"
# var_metrics["R20mm"]="pr"
# var_metrics["R10mm"]="pr"
# var_metrics["FD"]="tasmin"
# declare -a rcms=("BOM-BARPA-R" "CSIRO-CCAM-2203" "UQ-DES-CCAM-2105")
# declare -a tasks=("historical" "xvalidation" "projection")
# for metric in "${metrics[@]}"; do
	# for rcm in "${rcms[@]}"; do
		# for task in "${tasks[@]}"; do
			# data_dir="/g/data/ia39/npcp/data/${var_metrics[$metric]}/CSIRO-ACCESS-ESM1-5/${rcm}/qme/task-${task}"
			# case ${task} in
				# "historical")
					# start_date=1980-01-01
					# end_date=2019-12-31
					# start_date_train=19800101
					# end_date_train=20191231
					# ;;
				# "xvalidation")
					# start_date=1990-01-01
					# end_date=2019-12-31
					# start_date_train=19600101
					# end_date_train=19891231
					# ;;
				# "projection")
					# start_date=2060-01-01
					# end_date=2099-12-31
					# start_date_train=19800101
					# end_date_train=20191231
					# ;;
				# *)
					# echo "Unknown task: ${task}"
					# exit 1
					# ;;
			# esac
			# out_dir="/g/data/ia39/npcp/data/icclim/${metric}"	
			# outfile="${out_dir}/${metric}_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_${rcm}_v1_day_${start_date//-/}-${end_date//-/}_qme-AGCD-${start_date_train}-${end_date_train}.nc"
			
			# echo "Processing $metric for ${var_metrics[$metric]}, $task, $start_date_command, $end_date_command"
			# echo "Input file: $infile"
			# echo "Output file: $outfile"
			
			# python /g/data/xv83/users/at2708/bias_adjustment/evaluation/indices/run_icclim.py --input_files /g/data/ia39/npcp/data/${var_metrics[$metric]}/CSIRO-ACCESS-ESM1-5/${rcm}/qme/task-${task}/${var_metrics[$metric]}*.nc --variable "${var_metrics[$metric]}" --start_date "$start_date" --end_date "$end_date" --verbose "$metric" "$outfile"
		# done
	# done
# done





###### RCMs raw
# declare -a metrics=("R95pTOT" "R99pTOT" "WSDI" "CSDI" "R20mm" "R10mm" "FD")
# declare -A var_metrics
# var_metrics["R95pTOT"]="pr"
# var_metrics["R99pTOT"]="pr"
# var_metrics["WSDI"]="tasmax"
# var_metrics["CSDI"]="tasmin"
# var_metrics["R20mm"]="pr"
# var_metrics["R10mm"]="pr"
# var_metrics["FD"]="tasmin"
# declare -a rcms=("BOM-BARPA-R" "CSIRO-CCAM-2203" "UQ-DES-CCAM-2105")
# declare -a tasks=("historical" "xvalidation" "projection")
# for metric in "${metrics[@]}"; do
	# for rcm in "${rcms[@]}"; do
		# data_dir="/g/data/ia39/npcp/data/${var_metrics[$metric]}/CSIRO-ACCESS-ESM1-5/${rcm}/raw/task-reference"
		# for task in "${tasks[@]}"; do
			# case ${task} in
				# "historical")
					# start_date_command=1980-01-01
					# end_date_command=2019-12-31
					# mode="ssp370"
					# ;;
				# "xvalidation")
					# start_date_command=1990-01-01
					# end_date_command=2019-12-31
					# mode="ssp370"
					# ;;
				# "projection")
					# start_date_command=2060-01-01
					# end_date_command=2099-12-31
					# mode="ssp370"
					# ;;
				# *)
					# echo "Unknown task: ${task}"
					# exit 1
					# ;;
			# esac
			# out_dir="/g/data/ia39/npcp/data/icclim/${metric}"			
			# outfile="${out_dir}/${metric}_NPCP-20i_CSIRO-ACCESS-ESM1-5_${mode}_r6i1p1f1_${rcm}_v1_day_${start_date_command//-/}-${end_date_command//-/}.nc"

			# echo "Processing $metric for ${var_metrics[$metric]}, $task, $start_date_command, $end_date_command"
			# echo "Input file: $infile"
			# echo "Output file: $outfile"
			
			# python /g/data/xv83/users/at2708/bias_adjustment/evaluation/indices/run_icclim.py --input_files /g/data/ia39/npcp/data/${var_metrics[$metric]}/CSIRO-ACCESS-ESM1-5/${rcm}/raw/task-reference/${var_metrics[$metric]}_NPCP-20i_CSIRO-ACCESS-ESM1-5_*_r6i1p1f1_${rcm}_v1_day_*.nc --variable "${var_metrics[$metric]}" --start_date "$start_date_command" --end_date "$end_date_command" --verbose "$metric" "$outfile"
		# done
	# done
# done



###### AGCD raw
# declare -a metrics=("R95pTOT" "R99pTOT" "WSDI" "CSDI" "R20mm" "R10mm" "FD")
# declare -A var_metrics
# var_metrics["R95pTOT"]="pr"
# var_metrics["R99pTOT"]="pr"
# var_metrics["WSDI"]="tasmax"
# var_metrics["CSDI"]="tasmin"
# var_metrics["R20mm"]="pr"
# var_metrics["R10mm"]="pr"
# var_metrics["FD"]="tasmin"
# declare -a tasks=("historical" "xvalidation" "training")
# for metric in "${metrics[@]}"; do
	# data_dir="/g/data/ia39/npcp/data/${var_metrics[$metric]}/observations/AGCD/raw/task-reference"
	# for task in "${tasks[@]}"; do
		# case ${task} in
			# "historical")
				# start_date_command=1980-01-01
				# end_date_command=2019-12-31
				# ;;
			# "xvalidation")
				# start_date_command=1990-01-01
				# end_date_command=2019-12-31
				# ;;
			# "training")
				# start_date_command=1960-01-01
				# end_date_command=1989-12-31
				# ;;
			# *)
				# echo "Unknown task: ${task}"
				# exit 1
				# ;;
		# esac
		# out_dir="/g/data/ia39/npcp/data/icclim/${metric}"
		
		# infile=${data_dir}/${var_metrics[$metric]}_NPCP-20i_AGCD_v1-0-1_day_*.nc
		# outfile="${out_dir}/${metric}_NPCP-20i_AGCD_v1-0-1_day_${start_date_command//-/}-${end_date_command//-/}.nc"
		
		# echo "Processing $metric for ${var_metrics[$metric]}, $task, $start_date_command, $end_date_command"
		# echo "Input file: $infile"
		# echo "Output file: $outfile"
		
		# python /g/data/xv83/users/at2708/bias_adjustment/evaluation/indices/run_icclim.py --input_files /g/data/ia39/npcp/data/${var_metrics[$metric]}/observations/AGCD/raw/task-reference/${var_metrics[$metric]}_NPCP-20i_AGCD_v1-0-1_day_*.nc --variable "${var_metrics[$metric]}" --start_date "$start_date_command" --end_date "$end_date_command" --verbose "$metric" "$outfile"
	# done
# done




###### GCM raw
# declare -a metrics=("R95pTOT" "R99pTOT" "WSDI" "CSDI" "R20mm" "R10mm" "FD")
# declare -A var_metrics
# var_metrics["R95pTOT"]="pr"
# var_metrics["R99pTOT"]="pr"
# var_metrics["WSDI"]="tasmax"
# var_metrics["CSDI"]="tasmin"
# var_metrics["R20mm"]="pr"
# var_metrics["R10mm"]="pr"
# var_metrics["FD"]="tasmin"
# declare -a tasks=("historical" "xvalidation" "projection")
# for metric in "${metrics[@]}"; do
	# for task in "${tasks[@]}"; do
		# case ${task} in
			# "historical")
				# start_date=19600101
				# end_date=20191231
				# start_date_command=1980-01-01
				# end_date_command=2019-12-31
				# ;;
			# "xvalidation")
				# start_date=19600101 #changed date because of the input file structure
				# end_date=20191231
				# start_date_command=1990-01-01
				# end_date_command=2019-12-31
				# ;;
			# "projection")
				# start_date=20600101
				# end_date=20991231	
				# start_date_command=2060-01-01
				# end_date_command=2099-12-31
				# ;;
			# *)
				# echo "Unknown task: ${task}"
				# exit 1
				# ;;
		# esac
		# out_dir="/g/data/ia39/npcp/data/icclim/${metric}"

		# infile="/g/data/ia39/npcp/data/${var_metrics[$metric]}/CSIRO-ACCESS-ESM1-5/GCM/raw/task-reference/${var_metrics[$metric]}_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_GCM_latest_day_${start_date}-${end_date}.nc"
		# outfile="${out_dir}/${metric}_NPCP-20i_CSIRO-ACCESS-ESM1-5_ssp370_r6i1p1f1_GCM_latest_day_${start_date_command//-/}-${end_date_command//-/}.nc"
						
		# echo "Processing $metric for ${var_metrics[$metric]}, $task, $start_date_command, $end_date_command"
		# echo "Input file: $infile"
		# echo "Output file: $outfile"
		
		# python /g/data/xv83/users/at2708/bias_adjustment/evaluation/indices/run_icclim.py --input_files "$infile" --variable "${var_metrics[$metric]}" --start_date "$start_date_command" --end_date "$end_date_command" --verbose "$metric" "$outfile"
	# done
# done
