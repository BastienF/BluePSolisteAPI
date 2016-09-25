import boto3
from flask import Flask
from zipfile import ZipFile

app = Flask(__name__)
session = boto3.Session(
    region_name="eu-central-1"
)
s3_client = session.client('s3')

from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter


@app.route('/install/<regex("[0-9]+"):gameid>')
def hello_world(gameid):
    s3_client.download_file('bluepolo-games', gameid + '.zip', 'Z:\\' + gameid + '.zip')
    with ZipFile('Z:\\' + gameid + '.zip', 'r') as zip_ref:
        zip_ref.extractall('Z:\\' + gameid)
    return gameid


if __name__ == '__main__':
    app.run(host='0.0.0.0')

