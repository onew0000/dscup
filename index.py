from flask import Flask, request, jsonify, render_template, send_from_directory
import csv
import os

app = Flask(__name__)
votes_db = {}
players_db = {}

def load_players():
    with open('static/player.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            player_number = row['number']
            players_db[player_number] = {
                'name': row['name'],
                'leader': row['leader'],
                'height': row['height'],
                'weight': row['weight'],
                'position': row['position'],
                'main_foot': row['main_foot'],
                'votes': int(row['votes']) if 'votes' in row else 0
            }

def save_players():
    with open('static/player.csv', mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['number', 'name', 'leader', 'height', 'weight', 'position', 'main_foot', 'votes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for player_number, player_info in players_db.items():
            writer.writerow({
                'number': player_number,
                'name': player_info['name'],
                'leader': player_info['leader'],
                'height': player_info['height'],
                'weight': player_info['weight'],
                'position': player_info['position'],
                'main_foot': player_info['main_foot'],
                'votes': player_info['votes']
            })

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/annoincement')
def announcement():
    return render_template('announcementindex.html')

@app.route('/timerecord')
def timerecord():
    return render_template('timerecord_mainpage.html')

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/player')
def player():
    return render_template('player.html')

@app.route('/index')
def index():
    return render_template('mvp.html')

@app.route('/no51')
def no51():
    return render_template('tornement_popup51.html')

@app.route('/no52')
def no52():
    return render_template('tornement_popup52.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    player_number = data.get('player_number')
    device_id = data.get('device_id')

    if not device_id:
        return jsonify({'error': '기기 식별자가 필요합니다'}), 400
    if player_number not in players_db:
        return jsonify({'error': '유효하지 않은 선수 번호입니다'}), 400
    if device_id in votes_db:
        return jsonify({'error': '이미 투표하셨습니다'}), 403

    votes_db[device_id] = player_number
    players_db[player_number]['votes'] += 1
    save_players()
    return jsonify({'message': '투표가 성공적으로 기록되었습니다'})

@app.route('/players', methods=['GET'])
def players():
    return jsonify(players_db)

if __name__ == '__main__':
    load_players()
    app.run(port=8000, debug=True)
