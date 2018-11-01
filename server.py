import json

import pandas as pd
from datetime import datetime
from flask import Flask, Response, make_response, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.contrib.cache import SimpleCache

from dora.demo.json_data.chart_helpers import ChartHelpers
from dora.demo.json_data.company_helper import CompanyHelper
from dora.demo.json_data.data_transform import DataTransform
from dora.demo.json_data.document_helper import DocumentHelper
from dora.demo.json_data.elastic_helper import ElasticHelper
from dora.demo.json_data.sector_helper import SectorHelper
from dora.demo.json_data.signal_helper import SignalHelper
from dora.demo.json_data.scoring_helper import ScoringHelper
from dora.demo.json_data.training_helper import TrainingHelper
from dora.demo.json_data.lda_helper import LDAHelperDora
from models.lda.lda_helpers import LDAHelper

server = Flask(__name__)
auth = HTTPBasicAuth()
cache = SimpleCache()


@auth.get_password
@server.route("/")
@server.route("/company")
def company():
    region = request.cookies.get('region')
    if region is None:
        region = 'all'

    company_id = request.args.get('c')

    if company_id is None:
        if region == 'eur':
            company_id = 3404
        else:
            company_id = 184

    signals = SignalHelper().signal_map
    sectors = SectorHelper().get_sectors()
    ch = CompanyHelper()
    company_dropdown = ch.get_company_dropdown(region)
    company_info = ch.get_profile(company_id)
    sector_id = company_info[0]['sector_id']
    if sector_id is None:
        sector_id = 0

    resp = make_response(render_template('company.html', signals=signals, sectors=sectors,
                                         company_id=company_id, sector_id=sector_id, company_dropdown=company_dropdown))
    return resp


@server.route("/top_bottom", methods=['GET'])
def top_bottom_page():
    signals = SignalHelper().signal_map
    signal = request.args.get('s')
    toggle = request.args.get('t')
    sectors = SectorHelper().get_sectors()
    if not toggle:
        toggle = 'top'
    else:
        toggle = toggle.lower()

    if not signal:
        signal = signals[0]['column']
    resp = make_response(render_template('top_bottom.html',sectors=sectors, signals=signals, signal=signal, toggle=toggle))
    return resp
