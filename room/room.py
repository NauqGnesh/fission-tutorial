import requests
from flask import request

def main():
    digi = str(request.args.get('digi'))
    return f'Toggling all {digi}'
