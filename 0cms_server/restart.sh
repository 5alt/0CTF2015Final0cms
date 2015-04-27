#!/bin/bash
find . -name "*.pyc"  | xargs rm -f
python app.py
