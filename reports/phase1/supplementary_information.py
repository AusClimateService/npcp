"""Command line program to generate supplementary information documents"""

import argparse
import os

from fpdf import FPDF


var_names = {
    'pr': 'precipitation',
    'tasmax': 'daily maximum temperature',
    'tasmin': 'daily minimum temperature',
}

gcm_names = {
    'ECMWF-ERA5': 'ERA5',
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
    ('mean-bias', 'tasmin'): '01',
    ('mean-bias', 'tasmax'): '02',
    ('mean-bias', 'pr'): '03',
    ('seasonal-cycle', 'tasmin'): '04',
    ('seasonal-cycle', 'tasmax'): '05',
    ('seasonal-cycle', 'pr'): '06',
    ('interannual-variability-bias', 'tasmin'): '07',
    ('interannual-variability-bias', 'tasmax'): '08',
    ('interannual-variability-bias', 'pr'): '09',
    ('CSDI-bias', 'tasmin'): '10',
    ('WSDI-bias', 'tasmax'): '11',
    ('wet-day-freq', 'pr'): '12',
    ('R10mm-bias', 'pr'): '13',
    ('R20mm-bias', 'pr'): '14',
    ('R95pTOT-bias', 'pr'): '15',
    ('R99pTOT-bias', 'pr'): '16',
    ('pct01-bias', 'tasmin'): '17',
    ('pct99-bias', 'tasmax'): '18',
    ('pct99-bias', 'pr'): '19',
    ('1-in-10yr-bias', 'tasmin'): '20',
    ('1-in-10yr-bias', 'tasmax'): '21',
    ('1-in-10yr-bias', 'pr'): '22',
}

valid_vars = list(var_names.keys())
gcms = list(gcm_names.keys())
rcms = list(rcm_names.keys())


def main(args):
    """Run the program."""

    var_name = var_names[args.var]
    if args.metric in ['pct99-bias', '1-in-10yr-bias'] and args.var == 'pr':
        var_name = 'daily precipitation'
    metric_names = {
        'mean-bias': f'annual mean {var_name}',
        'seasonal-cycle': f'the seasonal cycle of {var_name}',
        'interannual-variability-bias': f'the interannual variability of annual mean {var_name}',
        'CSDI-bias': 'the Cold Spell Duration Index (CSDI)',
        'WSDI-bias': 'the Warm Spell Duration Index (WSDI)',
        'wet-day-freq': 'wet day frequency',
        'R10mm-bias': 'the annual number of heavy precipitation days (>10mm)',
        'R20mm-bias': 'the annual number of very heavy precipitation days (>20mm)',
        'pct99-bias': f'the 99th percentile of {var_name}',
        'pct01-bias': f'the 1st percentile of {var_name}',
        '1-in-10yr-bias': f'the 1-in-10 year {var_name}',
        'R95pTOT-bias': 'the fraction of annual precipitation that falls on very wet days (>95th percentile; R95pTOT)',
        'R99pTOT-bias': 'the fraction of annual precipitation that falls on extremely wet days (>99th percentile; R99pTOT)',
    }
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
        text=f'This document presents supplementary figures showing bias in {metric_name}.',
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
                    caption = f"Figure S{fignum}: Bias in {metric_name} (relative to the AGCD dataset) for the calibration assessment task. Results are shown for the {rcm_name} RCM forced by the {gcm_name} GCM (panel a) and various bias correction methods applied to those RCM data (panels b-e) data. Unlike the other GCMs, no raw CESM2 data were available.{extra_text}"
                else:
                    caption = f"Figure S{fignum}: Bias in {metric_name} (relative to the AGCD dataset) for the calibration assessment task. Results are shown for the {gcm_name} GCM (panel a), the {rcm_name} RCM forced by that GCM (panel c), and various bias correction methods applied to those GCM (panel b) and RCM (panels d-g) data.{extra_text}"
                pdf.multi_cell(text=caption, w=pdf.epw, new_x='LEFT')
                if fignum in [2, 4, 6, 8]:
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
                    caption = f"Figure S{fignum}: Bias in {metric_name} (relative to the AGCD dataset) for the cross validation assessment task. Results are shown for the {rcm_name} RCM forced by the {gcm_name} GCM (panel a) and various bias correction methods applied to those RCM data (panels b, c, d, f and g). A reference case where the AGCD training data (1960-1989) was simply duplicated for the assessment period (1990-2019) is also shown (panel e). Unlike the other GCMs, no raw CESM2 data were available.{extra_text}"
                else:
                    caption = f"Figure S{fignum}: Bias in {metric_name} (relative to the AGCD dataset) for the cross validation assessment task. Results are shown for the {gcm_name} GCM (panel a), the {rcm_name} RCM forced by that GCM (panel d), and various bias correction methods applied to those GCM (panels b and c) and RCM (panels e, f, g, i and j) data. A reference case where the AGCD training data (1960-1989) was simply duplicated for the assessment period (1990-2019) is also shown (panel h).{extra_text}"
                pdf.multi_cell(text=caption, w=pdf.epw, new_x='LEFT')
                if fignum in [12, 14, 16, 18]:
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

    file_number = file_numbers[(args.metric, args.var)]
    if not 'bias' in args.metric:
        file_metric = f'{args.metric}-bias'
    else:
        file_metric = args.metric

    pdf.output(f"/g/data/ia39/npcp/code/reports/phase1/supplementary/supplementary-file{file_number}_{args.var}_{file_metric}.pdf")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("var", choices=valid_vars, type=str, help="variable")
    valid_metrics = [
        'mean-bias',
        'seasonal-cycle',
        'interannual-variability-bias',
        'CSDI-bias',
        'WSDI-bias',
        'wet-day-freq',
        'R10mm-bias',
        'R20mm-bias',
        'pct99-bias',
        'pct01-bias',
        '1-in-10yr-bias',
        'R95pTOT-bias',
        'R99pTOT-bias',
    ]
    parser.add_argument("metric", choices=valid_metrics, type=str, help="metric")
    args = parser.parse_args()
    main(args)
