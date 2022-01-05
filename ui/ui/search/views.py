import json
import traceback
import sys
import csv
import os

from functools import reduce
from operator import and_

from django.shortcuts import render
from django import forms

import query
import heatmap
import stats


RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
    variable_1 = 'Variable 1',
    variable_2 = 'Variable 2'
)


def _load_column(filename, col=0):
    """Load single column from csv file."""
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)


def _load_res_column(filename, col=0):
    """Load column from resource directory."""
    return _load_column(os.path.join(RES_DIR, filename), col=col)


def _build_dropdown(options):
    """Convert a list to (value, caption) tuples."""
    return [(x, x) if x is not None else ('', '') for x in options]


VARIABLES = _build_dropdown([None] + _load_res_column('variables.csv'))
FITS = _build_dropdown([None] + _load_res_column('fits.csv'))


class SearchForm(forms.Form):
    variable_1 = forms.ChoiceField(label='Variable 1',
                                   choices=VARIABLES, required=True)
    variable_2 = forms.ChoiceField(label='Variable 2',
                                   choices=VARIABLES, required=True)
    fit_type = forms.ChoiceField(label='Fit Type', choices=FITS, required=True)

def home(request):
    context = {}
    res = None
    if request.method == 'GET':
        # Create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # Check whether it's valid:
        if form.is_valid():

            # Convert form data to an args list for query.py
            args = []
            variable_1 = form.cleaned_data['variable_1']
            if variable_1:
                args.append(variable_1)
            variable_2 = form.cleaned_data['variable_2']
            if variable_2:
                args.append(variable_2)
            fit = form.cleaned_data['fit_type']
            try:
                res = query.find_columns(args)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_columns:
                <pre>{}
{}</pre>
                """.format(e, '\n'.join(bt))

                res = None
    else:
        form = SearchForm()

    # Handle different responses of res
    if res is None:
        context['result'] = None
    else:
        data1 = stats.make_df(res[0], variable_1)
        data2 = stats.make_df(res[1], variable_2)
        data1_hm = stats.df_for_heatmap(res[0], variable_1)
        data2_hm = stats.df_for_heatmap(res[1], variable_2)
        heatmap.plot_heatmap(data1_hm, True)
        heatmap.plot_heatmap(data2_hm, False)
        stats.make_scatter(data1, data2)
        stats.make_fit(data1, data2, fit)
        context['columns'] = [COLUMN_NAMES.get(arg, arg) for arg in args]

    context['form'] = form
    return render(request, 'newsite.html', context)
