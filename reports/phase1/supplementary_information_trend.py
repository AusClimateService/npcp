"""Command line program to generate supplementary information documents for trends"""

import argparse
import os

from fpdf import FPDF


var_names = {
    'pr': 'precipitation',
    'tasmax': 'daily maximum temperature',
    'tasmin': 'daily minimum temperature',
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

file_numbers = {
    'tasmin': '23',
    'tasmax': '24',
    'pr': '25',
}

valid_vars = list(var_names.keys())
gcms = list(gcm_names.keys())
rcms = list(rcm_names.keys())


def main(args):
    """Run the program."""

    var_name = var_names[args.var]

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
        text=f'This document presents supplementary figures showing the trend in {var_name}.',
        w=pdf.epw,
        align='L',
        new_x='LEFT'
    )

    fignum = 0

    # Calibration task
    pdf.add_page()
    pdf.set_font("Times", size=12, style='B')
    pdf.multi_cell(
        text="Projection task",
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
            infile = f'/g/data/ia39/npcp/code/results/figures/{args.var}_trend_task-projection_{gcm}_{rcm}.png'
            if os.path.isfile(infile):
                pdf.image(infile, w=1.0 * pdf.epw)
                pdf.ln()
                fignum += 1
                if (gcm_name == 'CESM2') and 'tas' in args.var:
                    caption = f"Figure S{fignum}: Change in annual mean {var_name} between 1980-2019 and 2060-2099 for the projection assessment task. Results are shown for the {rcm_name} RCM forced by the {gcm_name} GCM (panel a) and for various bias correction methods applied to those RCM data (panels b-f). Unlike the other GCMs, no raw CESM2 data were available."
                else:
                    caption = f"Figure S{fignum}: Change in annual mean {var_name} between 1980-2019 and 2060-2099 for the projection assessment task. Results are shown for the {gcm_name} GCM (panel a), the {rcm_name} RCM forced by that GCM (panel b), and for various bias correction methods applied to those RCM data (panels c-g)."
                if args.var == 'pr':
                    caption = f'{caption} Land areas where the AGCD data are unreliable due to weather station sparsity have been masked in white.'
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

    file_number = file_numbers[args.var]
    pdf.output(f"/g/data/ia39/npcp/code/reports/phase1/supplementary/supplementary-file{file_number}_{args.var}_trend.pdf")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("var", choices=valid_vars, type=str, help="variable")
    args = parser.parse_args()
    main(args)
