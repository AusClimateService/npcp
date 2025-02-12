"""Command line program to generate supplementary information document"""

import argparse
import os

from fpdf import FPDF
import xarray as xr


var_names = {
    'pr': 'precipitation',
    'tasmax': 'daily maximum temperature',
    'tasmin': 'daily minimum temperature',
}

metric_names = {
    'mean-bias': 'annual mean',
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
    pdf.set_font('Times', size=14, style='B')
    pdf.multi_cell(
        txt='Supplementary Information',
        w=pdf.epw,
        align='L',
        new_x='LEFT'
    )
    pdf.ln()
    pdf.set_font('Times', size=11)
    pdf.multi_cell(
        txt=f'This document presents supplementary figures showing the bias in {metric_name} {var_name}.',
        w=pdf.epw,
        align='L',
        new_x='LEFT'
    )

    fignum = 0

    # Calibration task
    pdf.add_page()
    pdf.set_font("Times", size=12, style='B')
    pdf.multi_cell(
        txt="Calibration task",
        w=pdf.epw,
        align='L',
        new_x='LEFT'
    )
    pdf.ln()
    pdf.set_font("Times", size=11)
    for gcm in gcms:
        gcm_name = gcm_names[gcm]
        for rcm in rcms:
            rcm_name = rcm_names[rcm]
            infile = f'/g/data/ia39/npcp/code/results/figures/{var}_{metric}_task-historical_{gcm}_{rcm}.png'
            if os.path.isfile(infile):
                pdf.image(infile, w=0.65 * pdf.epw)
                pdf.ln()
                fignum += 1
                caption = f"Figure S{fignum}: Bias in {metric_name} {var_name} (relative to the AGCD dataset) for the calibration assessment task. Results are shown for the {gcm_name} GCM (top left), the {rcm_name} RCM forced by that GCM (bottom left), and various bias correction methods applied to those GCM (top row, columns to the right) and RCM (middle and bottom rows, columns to the right) data. (MAE = mean absolute error.)"
                pdf.multi_cell(txt=caption, w=pdf.epw, new_x='LEFT')
                pdf.ln()
                pdf.ln()
                pdf.ln()
            else:
                print(f"{infile} does not exist")

    pdf.output(f"supplementary_information_{var}_{metric}.pdf")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("var", choices=valid_vars, type=str, help="variable")
    parser.add_argument("metric", choices=valid_metrics, type=str, help="metric")
    args = parser.parse_args()
    main(args)
