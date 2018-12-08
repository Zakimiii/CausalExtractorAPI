# coding: utf-8

import django_filters
from rest_framework import viewsets, filters
import re
import sys
import json
import uuid
from collections import OrderedDict
from django.http import HttpResponse
import causal
from causal.models import Pattern, Relation, Causal, Goal, Step, Smart, PrunedUser
from causal.extractor import extractor
from causal.repository import causal_repository
from causal.cross_bootstrap import cross_bootstrap
from data.scraping import googleScraping
from Util.FileUtilities import FileUtilities
import urllib.request, urllib.error
from urllib.error import HTTPError
import pandas as pd

repository = causal_repository()
extracter = extractor()

def render_json_response(request, data, status=None):
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    callback = request.GET.get('callback')
    if not callback:
        callback = request.POST.get('callback')  # POSTでJSONPの場合
    if callback:
        json_str = "%s(%s)" % (callback, json_str)
        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=status)
    else:
        response = HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
    return response


def render_goal_causal(text, causal):
    goals = []
    if text in causal.basis:
        goals.append(causal.result)
    return goals

def run_crawle(request, init_keyword, limit, per_limit):
    repository = causal_repository()
    repository.routineCrawle(init_keyword, limit=limit, per_limit=per_limit)
    return None

def causal_extraction_no_user(request, text):
    crawlers = repository.syncCrawle(text, limit=20)
    causals, crawlers = extracter.extract(crawlers, Relation.cause)
    repository.setCausalData(causals, crawlers)
    return render_json_response(request, OrderedDict([ ('causals', [causal.toJson() for causal in causals])]))

def causal_extraction(request, user_id, text):
    crawlers = repository.syncCrawle(text, limit=20)
    causals, crawlers = extracter.extract(crawlers, Relation.cause)
    repository.setCausalData(causals, crawlers)
    return render_json_response(request, OrderedDict([('causals', [causal.toJson() for causal in causals])]))

def causal_extraction_from_crawle(request, user_id, text):
    crawlers = repository.syncCrawle(text, limit=20)
    causals, crawlers = extracter.extract(crawlers, Relation.cause)
    repository.setCausalData(causals, crawlers)
    return render_json_response(request, OrderedDict([('causals', [causal.toJson() for causal in causals])]))

def goal_extraction_no_user(request, text):
    crawlers = repository.syncCrawle(text, limit=20)
    causals, crawlers = extracter.extract(crawlers, Relation.goal)
    repository.setCausalData(causals, crawlers)
    return render_json_response(request, OrderedDict([('causals', [causal.toJson() for causal in causals])]))

def goal_extraction(request, user_id, text):
    crawlers = repository.syncCrawle(text, limit=20)
    causals, crawlers = extracter.extract(crawlers, Relation.goal)
    repository.setCausalData(causals, crawlers)
    return render_json_response(request, OrderedDict([('causals', [causal.toJson() for causal in causals])]))

def equal_extraction_no_user(request, text):
    crawlers = repository.syncCrawle(text, limit=20)
    causals, crawlers = extracter.extract(crawlers, Relation.equal)
    repository.setCausalData(causals, crawlers)
    return render_json_response(request, OrderedDict([('causals', [causal.toJson() for causal in causals])]))

def equal_extraction(request, user_id, text):
    crawlers = repository.syncCrawle(text, limit=20)
    causals, crawlers = extracter.extract(crawlers, Relation.equal)
    repository.setCausalData(causals, crawlers)
    return render_json_response(request, OrderedDict([('causals', [causal.toJson() for causal in causals])]))