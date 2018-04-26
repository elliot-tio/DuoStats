from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, current_app
from wtforms import Form, StringField, SelectField, validators
import regex
import requests
import sys

app = Flask(__name__)
apikey = 'RGAPI-95a436c5-4aae-4486-a5ec-8956be25d875'


class SummonerForm(Form):   # SummonerForm class
    expression = regex.compile('^[0-9\p{L} _\.]+$')
    summoner_1 = StringField('Summoner 1', validators=[validators.Regexp(expression, message="Summoner names can only contain any visible Unicode letter characters, digits (0-9), spaces, underscores, and periods."),
                                                       validators.InputRequired()])
    summoner_2 = StringField('Summoner 2', validators=[validators.Regexp(
        expression, message="Summoner names can only contain any visible Unicode letter characters, digits (0-9), spaces, underscores, and periods."),
        validators.InputRequired()])
    region_1 = SelectField(u'Region', choices=[('na1', 'NA'), ('euw1', 'EUW'), ('eun1', 'EUNE'), ('br1', 'BR'), (
        'jp1', 'JP'), ('kr', 'KR'), ('la1', 'LAN'), ('la2', 'LAS'), ('oc1', 'OCE'), ('tr1', 'TR'), ('ru', 'RU')])
    region_2 = SelectField(u'Region', choices=[('na1', 'NA'), ('euw1', 'EUW'), ('eun1', 'EUNE'), ('br1', 'BR'), (
        'jp1', 'JP'), ('kr', 'KR'), ('la1', 'LAN'), ('la2', 'LAS'), ('oc1', 'OCE'), ('tr1', 'TR'), ('ru', 'RU')])


def requestSummonerInfo(region, summonerName):
    URL = 'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + \
        summonerName + '?api_key=' + apikey

    response = requests.get(URL)
    return response.json()


def requestRecentGames(region, summonerId):
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v3/matchlists/by-account/' + \
        summonerId + '/recent?api_key=' + apikey

    print('Hello world!', file=sys.stderr)

    response = requests.get(URL)
    return response.json()


@app.route('/', methods=['GET', 'POST'])    # Home
def index():
    form = SummonerForm(request.form)
    if request.method == 'POST' and form.validate():
        name1 = form.summoner_1.data
        name2 = form.summoner_2.data
        region_1 = form.region_1.data
        region_2 = form.region_2.data
        results = []
        endIndex = 10

        # Grab JSON objects here
        try:
            summ1ID = requestSummonerInfo(region_1, name1)['accountId']
            recentGames = requestRecentGames(region_1, summ1ID)
            results.append(recentGames)
            for key in recentGames.items():
                results.append(key)
        except Exception as e:
            summ1ID = "Could not find ID of " + name1 + " in " + region_1

        try:
            summ2ID = requestSummonerInfo(region_2, name2)['accountId']
        except Exception as e:
            summ2ID = "Could not find ID of " + name2 + " in " + region_2

        return render_template('results.html', form=form, name1=name1, name2=name2, results=results)
    return render_template('index.html', form=form)


@app.route('/results')  # Results
def about():
    return render_template('results.html')


# Main function - remove debug to remove dynamic update
if __name__ == '__main__':
    app.secret_key = 'duoSecret123'
    app.run(debug=True)
