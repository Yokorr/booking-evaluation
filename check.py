#!/usr/bin/env python
"""Run a selected assessment test group from the repository root."""
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Booking evaluation checks')
group = parser.add_mutually_exclusive_group()
group.add_argument('--todo0', action='store_true', help='M4 Django template tests')
group.add_argument('--todo1', action='store_true', help='Serializer tests')
group.add_argument('--todo2', action='store_true', help='REST endpoint tests')
group.add_argument('--todo3', action='store_true', help='JSON report tests')
args = parser.parse_args()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_eval.settings')
from django.core.management import execute_from_command_line
label = 'rooms.tests'
if args.todo0: label += '.TemplateEvaluationTests'
if args.todo1: label += '.SerializerEvaluationTests'
if args.todo2: label += '.ApiEvaluationTests'
if args.todo3: label += '.ReportEvaluationTests'
execute_from_command_line([sys.argv[0], 'test', label, '--verbosity', '2'])
