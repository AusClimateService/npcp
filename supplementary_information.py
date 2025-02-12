"""Command line program to generate supplementary information documents"""

import argparse
import os

from fpdf import FPDF


var_names = {
    'pr': 'precipitation',
    'tasmax': 'daily maximum temperature',
    'tasmin': 'daily minimum temperature',
}

metric_names = {
    'mean-bias': 'annual mean',
    'seasonal-cycle': 'seasonal cycle of',
    'interannual-variaiblity': 'interannual variability',
}

gcm_names = {
    'CSIRO-ACCESS-ESM1-5': 'ACCESS-ESM1-5',
    'EC-Earth-Consortium-EC-Earth3': 'EC-Earth3',
    'NCAR-CESM2': 'CESM2',
}

rcm_names = {
    'BOM-BARPA-R': 'BARPA-R',
    'CSIRO-CCAM-2203': 'CCAM-v2203-SN',
    'UQ-DES-CCAM-2105': 'CCAM-v2105',
}

valid_vars = list(var_names.keys())
valid_metrics = list(metric_names.keys())
gcms = list(gcm_names.keys())
rcms = list(rcm_names.keys())


def main(args):
    """Run the program."""

    var_name = var_names[args.var]
    metric_name = metric_names[args.metric]

    pdf = FPDF()

    # Title page
    pdf.add_page()
    pdf.ln()
    pdf.ln()
    pdf.set_font('Times', size=14, style='B')
    pdf.multi_cell(
        text='Supplementary Information',
        w=pdf.epw,
        align='L',
        new_x='LEFT'
    )
    pdf.ln()
    pdf.set_font('Times', size=11)
    pdf.multi_cell(
        text=f'This document presents supplementary figures showing the bias in {metric_name} {var_name}.',
        w=pdf.epw,
        align='L',
        new_x='LEFT'
    )

    fignum = 0

    # Calibration task
    pdf.add_page()
    pdf.set_font("Times", size=12, style='B')
    pdf.multi_cell(
        text="Calibration task",
        w=pdf.epw,
        align='L',
        new_x='LEFT'
    )
    pdf.ln()
    pdf.ln()
    pdf.set_font("Times", size=11)
    for gcm in gcms:
        gcm_name = gcm_names[gcm]
        for rcm in rcms:
            rcm_name = rcm_names[rcm]
            infile = f'/g/data/ia39/npcp/code/results/figures/{args.var}_{args.metric}_task-historical_{gcm}_{rcm}.png'
            if os.path.isfile(infile):
                pdf.image(infile, w=0.70 * pdf.epw)
                pdf.ln()
                fignum += 1
                abbrev_text = ' ' if args.metric == 'seasonal-cycle' else ' (MAE = mean absolute error.)'
                if args.var == 'pr':
                    extra_text = f' Land areas where the AGCD data are unreliable due to weather station sparsity have been masked in white.{abbrev_text}'
                else:
                    extra_text = abbrev_text 
                if (gcm_name == 'CESM2') and 'tas' in args.var:
                    caption = f"Figure S{fignum}: Bias in {metric_name} {var_name} (relative to the AGCD dataset) for the calibration assessment task. Results are shown for the {rcm_name} RCM forced by the {gcm_name} GCM (panel a) and various bias correction methods applied to those RCM data (panels b-e) data. Unlike the other GCMs, no raw CESM2 data were available.{extra_text}"
                else:
                    caption = f"Figure S{fignum}: Bias in {metric_name} {var_name} (relative to the AGCD dataset) for the calibration assessment task. Results are shown for the {gcm_name} GCM (panel a), the {rcm_name} RCM forced by that GCM (panel c), and various bias correction methods applied to those GCM (panel b) and RCM (panels d-g) data.{extra_text}"
                pdf.multi_cell(text=caption, w=pdf.epw, new_x='LEFT')
                if fignum in [2, 4, 6]:
                    pdf.add_page()
                    pdf.ln()
                    pdf.ln()
                    pdf.ln()
                else:
                    pdf.ln()
                    pdf.ln()
                    pdf.ln()
            else:
                print(f"{infile} does not exist")

    # Cross validation task
    pdf.add_page()
    pdf.set_font("Times", size=12, style='B')
    pdf.multi_cell(
        text="Cross validation task",
        w=pdf.epw,
        align='L',
        new_x='LEFT'
    )
    pdf.ln()
    pdf.ln()
    pdf.set_font("Times", size=11)
    for gcm in gcms:
        gcm_name = gcm_names[gcm]
        for rcm in rcms:
            rcm_name = rcm_names[rcm]
            infile = f'/g/data/ia39/npcp/code/results/figures/{args.var}_{args.metric}_task-xvalidation_{gcm}_{rcm}.png'
            if os.path.isfile(infile):
                pdf.image(infile, w=1.0 * pdf.epw)
                pdf.ln()
                fignum += 1
                abbrev_text = ' ' if args.metric == 'seasonal-cycle' else ' (MAE = mean absolute error.)'
                if args.var == 'pr':
                    extra_text = f' Land areas where the AGCD data are unreliable due to weather station sparsity have been masked in white.{abbrev_text}'
                else:
                    extra_text = abbrev_text
                if (gcm_name == 'CESM2') and 'tas' in args.var:
                    caption = f"Figure S{fignum}: Bias in {metric_name} {var_name} (relative to the AGCD dataset) for the cross validation assessment task. Results are shown for the {rcm_name} RCM forced by the {gcm_name} GCM (panel a) and various bias correction methods applied to those RCM data (panels b, c, d, f and g). A reference case where the AGCD training data (1960-1989) was simply duplicated for the assessment period (1990-2019) is also shown (panel e). Unlike the other GCMs, no raw CESM2 data were available.{extra_text}"
                else:
                    caption = f"Figure S{fignum}: Bias in {metric_name} {var_name} (relative to the AGCD dataset) for the cross validation assessment task. Results are shown for the {gcm_name} GCM (panel a), the {rcm_name} RCM forced by that GCM (panel d), and various bias correction methods applied to those GCM (panels b and c) and RCM (panels e, f, g, i and j) data. A reference case where the AGCD training data (1960-1989) was simply duplicated for the assessment period (1990-2019) is also shown (panel h).{extra_text}"
                pdf.multi_cell(text=caption, w=pdf.epw, new_x='LEFT')
                if fignum in [9, 11, 13]:
                    pdf.add_page()
                    pdf.ln()
                    pdf.ln()
                    pdf.ln()
                else:
                    pdf.ln()
                    pdf.ln()
                    pdf.ln()
            else:
                print(f"{infile} does not exist")

    pdf.output(f"/g/data/ia39/npcp/code/reports/phase1/supplementary/{args.var}_{args.metric}_supplementary_information.pdf")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("var", choices=valid_vars, type=str, help="variable")
    parser.add_argument("metric", choices=valid_metrics, type=str, help="metric")
    args = parser.parse_args()
    main(args)
