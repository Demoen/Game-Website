from flask import render_template,session,redirect,request,url_for,jsonify,flash
from game import app
from uuid import uuid4
from datetime import datetime
import os
import json
import random

avatars=os.listdir("game/static/avatars")

lang_file=open('game/lang.json','r')
lang_file_data=lang_file.read()
home_lang = json.loads(lang_file_data)['home']

games_file=open('game/games.json','r')
games_file_data=games_file.read()
games = json.loads(games_file_data)['games']

game_rooms={}
players={}
@app.route('/')
def home():
    if not 'lang' in session:
        session['lang']='english'
    return render_template('home.html',home=home_lang[session['lang']])

@app.route('/lang')
def lang():
    session['lang']=request.args.get('name')
    return redirect('/')

@app.route('/get-avatars')
def get_avatars():
    avatars=os.listdir("game/static/avatars")
    avatar_list=[]
    for i in avatars:
        avatar_list.append({
            "name": i,
            "path": "/static/avatars/"+i,
            "bg": i.split(".")[0].split("-")[1]
        })
    return jsonify({
        "success":True,
        "data":avatar_list
    })

@app.route("/chosen-avatar", methods=["POST"])
def chosen_avatar():
    player_id=session["player_id"]
    avatar=request.form["avatar"]
    room_code=request.form["room_code"]
    if room_code in game_rooms:
        pass
    else:
        return jsonify({
            "success":False,
            "message":"Room does not exists",
            "data":[]
        })
        
    if player_id in game_rooms[room_code]["players"]:
        game_rooms[room_code]['player_info'][player_id]['img']=avatar
    else:
        return jsonify({
            "success":False,
            "message":"Player is not in this game",
            "data":[]
        })
    
    return jsonify({
            "success":True,
            "message":"Avatar Added"
        })

@app.route('/create', methods=["POST"])
def create_game():
    player_name=request.form['player_name']
    room_code = str(uuid4())[:8]
    player_id = str(uuid4())[:15]
    session['player_id']=player_id
    players[player_id]=player_name
    game_rooms[room_code]={"players":[player_id]}
    game_rooms[room_code]["winner"]=None
    game_rooms[room_code]["creator"]={"id":player_id,"name":player_name,"time":datetime.now()}
    game_rooms[room_code]['player_info']={}
    game_rooms[room_code]["rounds"]=[]
    game_rooms[room_code]['player_info'][session['player_id']]={}
    game_rooms[room_code]['player_info'][session['player_id']]['time']=datetime.now()
    game_rooms[room_code]['player_info'][session['player_id']]['img']=random.choice(avatars)
    game_rooms[room_code]['player_info'][session['player_id']]['name']=player_name
    game_rooms[room_code]["player_info"][session['player_id']]["points"]=0
    return redirect('game/'+room_code)

@app.route('/game/<string:room_id>')
def game(room_id):
    if room_id in game_rooms:
        return render_template('game.html', room_id=room_id)
    else:
        return redirect("/")
    
@app.route('/check/<string:room_id>')
def check_players(room_id):
    if room_id in game_rooms:
        players=game_rooms[room_id]['players']
        game_rooms[room_id]['player_info'][session['player_id']]['time']=datetime.now()
        rlist=[]
        for pid in players:
            # Calculate the difference between datetime objects
            time_difference = datetime.now() - game_rooms[room_id]['player_info'][pid]['time']
            # Extract the difference in seconds
            seconds_difference = time_difference.total_seconds()
            if seconds_difference>10:
                rlist.append(pid)
        for pid in rlist:
            game_rooms[room_id]['players'].remove(pid)
        return jsonify(players)
    else:
        return jsonify([])

@app.route('/homeimg')
def homeimg():
    return render_template('home-img.html')

@app.route('/join',methods=["POST"])
def join():
    room_code = request.form["room_code"]
    if room_code in game_rooms:
        player_name=request.form['player_name']
        player_id = str(uuid4())[:15]
        session['player_id']=player_id
        players[player_id]=player_name
        game_rooms[room_code]["players"].append(player_id)
        game_rooms[room_code]['player_info'][session['player_id']]={}
        game_rooms[room_code]['player_info'][session['player_id']]['time']=datetime.now()
        game_rooms[room_code]['player_info'][session['player_id']]['img']=random.choice(avatars)
        game_rooms[room_code]['player_info'][session['player_id']]['name']=player_name
        game_rooms[room_code]["player_info"][session['player_id']]["points"]=0
        return redirect('game/'+room_code)
    flash('No such room')
    return redirect('/')

@app.route('/get-game-data')
def getgamedata():
  room_code=request.args.get("id")
  if room_code in game_rooms:
    a = {
      "room_data":game_rooms[room_code],
      "my_id":session['player_id'],
      "creator":game_rooms[room_code]["creator"]
    }
    return jsonify(a)
  else:
    return jsonify({"message":"No such room"})

@app.route('/get-round-data')
def getrounddata():
  room_code=request.args.get("id")
  if room_code in game_rooms:
    a = {
        "game":game_rooms[room_code],
        "success":True,
        "round_data":game_rooms[room_code]["rounds"],
        "player_info":game_rooms[room_code]["player_info"],
        "my_id":session['player_id'],
        "creator":game_rooms[room_code]["creator"]
    }
    if game_rooms[room_code]["rounds"]:
        if game_rooms[room_code]["rounds"][-1]["winner"]:
            a["player_name"]=players[game_rooms[room_code]["rounds"][-1]["winner"]]
    return jsonify(a)
  else:
    return jsonify({"success":False,"message":"No such room"})

@app.route("/choose-game")
def choose_game():
    temp_games=games.copy()
    choose_game_list=[]
    for _ in range(3):
        random_game =random.choice(list(temp_games.keys())) 
        data = {
            "name":random_game,
            "path":temp_games[random_game]["path"],
            "bg":temp_games[random_game]["bg"]
        }
        choose_game_list.append(data)
        del temp_games[random_game]
    return jsonify({
        "games":choose_game_list
    })
    
@app.route("/chosen-game", methods=["POST"])
def chosen_game():
    player_id=session["player_id"]
    game=request.form["game"]
    room_code=request.form["room_code"]
    if room_code in game_rooms:
        pass
    else:
        return jsonify({
            "success":False,
            "message":"Room does not exists",
            "data":[]
        })
        
    if player_id in game_rooms[room_code]["players"]:
        game_rooms[room_code]["rounds"].append({"round":1,"name":game,"winner":None, "creator":player_id})
    else:
        return jsonify({
            "success":False,
            "message":"Player is not in this game",
            "data":[]
        })
    return jsonify({
            "success":True,
            "message":"Game Added",
            "data":{
                "game":game,
                "my_id":session["player_id"],
                "rounds":game_rooms[room_code]["rounds"],
                "all":[request.referrer,game,session["player_id"],game_rooms[room_code]["rounds"]]
                }
        })

@app.route("/chosen-winner", methods=["POST"])
def chosen_winner():
    player_id=session["player_id"]
    winner_id=request.form["winner_id"]
    room_code=request.form["room_code"]
    if room_code in game_rooms:
        pass
    else:
        return jsonify({
            "success":False,
            "message":"Room does not exists",
            "data":[]
        })
        
    if player_id in game_rooms[room_code]["players"]:
        game_rooms[room_code]["rounds"][-1]["winner"]=winner_id
        game_rooms[room_code]["rounds"][-1]["winner_name"]=players[winner_id]
        game_rooms[room_code]["player_info"][winner_id]["points"]+=len(game_rooms[room_code]["rounds"])
    else:
        return jsonify({
            "success":False,
            "message":"Player is not in this game",
            "data":[]
        })
    player_ids=game_rooms[room_code]["player_info"].keys()
    for i in player_ids:
        if game_rooms[room_code]["player_info"][i]["points"]>50:
            game_rooms[room_code]["winner"]={"winner_id":i,"winner_name":players[i]}
        
    return jsonify({
            "success":True,
            "message":"Game Added",
            "data":{
                    "game":game_rooms[room_code],
                    "my_id":session["player_id"],
                    "player_name": players[winner_id],
                    "rounds":game_rooms[room_code]["rounds"],
                    "all":[request.referrer,game_rooms[room_code],session["player_id"],game_rooms[room_code]["rounds"]]
                }
        })



@app.route('/get-game-ui')
def getgameui():
    return jsonify({"style":"""
        body {
            font-family: 'Press Start 2P', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #212529;
            color: #dee2e6;
        }

        .container {
            margin: 50px;
            display: block;
            width: 400px;
            margin-left: auto;
            margin-right: auto;
            text-align: center;
        }

        .pixel,
        .pixel2 {
            font-size: 25px;
            color: white;
            height: auto;
            margin: 10px;
            font-family: 'VT323';

            position: relative;
            display: inline-block;
            vertical-align: top;
            text-transform: uppercase;

            cursor: pointer;

            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }

        .pixel:active,
        .pixel2:active {
            top: 2px;
        }

        .pixel {
            line-height: 0;

            image-rendering: optimizeSpeed;
            image-rendering: -moz-crisp-edges;
            /* Firefox */
            image-rendering: -o-crisp-edges;
            /* Opera */
            image-rendering: -webkit-optimize-contrast;
            /* Webkit (non-standard naming) */
            image-rendering: crisp-edges;
            -ms-interpolation-mode: nearest-neighbor;
            /* IE (non-standard property) */

            border-style: solid;
            border-width: 20px;
            -moz-border-image: url(https://i.imgur.com/sREM8Yn.png) 20 stretch;
            -webkit-border-image: url(https://i.imgur.com/sREM8Yn.png) 20 stretch;
            -o-border-image: url(https://i.imgur.com/sREM8Yn.png) 20 stretch;
            border-image: url(https://i.imgur.com/sREM8Yn.png) 20 stretch;
        }

        .pixel p {
            display: inline-block;
            vertical-align: top;
            position: relative;
            width: auto;
            text-align: center;
            margin: -20px -20px;
            line-height: 20px;
            padding: 10px 20px;

            background: #000000;
            background:
                linear-gradient(135deg, transparent 10px, #000000 0) top left,
                linear-gradient(225deg, transparent 10px, #000000 0) top right,
                linear-gradient(315deg, transparent 10px, #000000 0) bottom right,
                linear-gradient(45deg, transparent 10px, #000000 0) bottom left;
            background-size: 50% 50%;
            background-repeat: no-repeat;
            background-image:
                radial-gradient(circle at 0 0, rgba(204, 0, 0, 0) 14px, #000000 15px),
                radial-gradient(circle at 100% 0, rgba(204, 0, 0, 0) 14px, #000000 15px),
                radial-gradient(circle at 100% 100%, rgba(204, 0, 0, 0) 14px, #000000 15px),
                radial-gradient(circle at 0 100%, rgba(204, 0, 0, 0) 14px, #000000 15px);
        }

        .pixel2 {
            position: relative;
            display: block;
            width: 100%;
            margin: 10px;
            font-family: 'Press Start 2P';
            text-transform: uppercase;
            font-size: 25px;
            color: #ffffff;
        }

        .pixel2::before {
            content: "";
            display: block;
            position: absolute;
            top: 10px;
            bottom: 10px;
            left: -10px;
            right: -10px;
            background: #92CD41;
            z-index: -1;
        }

        .pixel2::before::before {
            content: "";
            display: block;
            position: absolute;
            top: 14px;
            bottom: 14px;
            left: -14px;
            right: -14px;
            background: #92CD41;
            z-index: -1;
        }

        .pixel2::after {
            content: "";
            display: block;
            position: absolute;
            top: 4px;
            bottom: 4px;
            left: -6px;
            right: -6px;
            background: #92CD41;
            z-index: -1;
            border: 2px black;
            outline: inset -2px white;
        }

        .pixel2 {
            padding: 10px 10px;
            position: relative;
            background: #92CD41;
            width: 100%;
            z-index: 2;
        }
 body {
            text-align: center;
            padding: 30px;
            font-family: 'Press Start 2P', cursive;
        }

        .eightbit-btn {
            background: #92CD41;
            display: inline-block;
            position: relative;
            text-align: center;
            font-size: 15px;
            padding: 10px;
            font-family: 'Press Start 2P', cursive;
            text-decoration: none;
            color: white;
            box-shadow: inset -2px -2px 0px 0px #4AA52E;
        }

        .eightbit-btn:hover,
        .eightbit-btn:focus {
            background: #76c442;
            box-shadow: inset -2px -2px 0px 0px #4AA52E;
        }

        .eightbit-btn:active {
            box-shadow: inset 2px 2px 0px 0px #4AA52E;
        }

        .eightbit-btn:before,
        .eightbit-btn:after {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            box-sizing: content-box;
        }

        .eightbit-btn:before {
            top: -4px;
            left: 0;
            border-top: 4px rgb(230, 230, 230) solid;
            border-bottom: 4px rgb(230, 230, 230) solid;
        }

        .eightbit-btn:after {
            left: -4px;
            top: 0;
            border-left: 4px rgb(230, 230, 230) solid;
            border-right: 4px rgb(230, 230, 230) solid;
        }

        .eightbit-btn--reset {
            background: #E76E55;
            box-shadow: inset -2px -2px 0px 0px #8C2022;
        }

        .eightbit-btn--reset:hover,
        .eightbit-btn--reset:focus {
            background: #CE372B;
            box-shadow: inset -4px -4px 0px 0px #8C2022;
        }

        .eightbit-btn--reset:active {
            box-shadow: inset 2px 2px 0px 0px #8C2022;
        }

        .eightbit-btn--proceed {
            background: #F7D51D;
            box-shadow: inset -2px -2px 0px 0px #E59400;
        }

        .eightbit-btn--proceed:hover,
        .eightbit-btn--proceed:focus {
            background: #F2C409;
            box-shadow: inset -4px -4px 0px 0px #E59400;
        }

        .eightbit-btn--proceed:active {
            box-shadow: inset 2px 2px 0px 0px #E59400;
        }

        *,
        *:before,
        *:after {
            box-sizing: border-box;
        }

        h1 {
            font-size: 2.8rem;
            line-height: 3.4rem;
        }

        h2 {
            font-size: 2rem;
        }

        h1,
        h2 {
            font-family: 'Press Start 2P', cursive;
        }

        p {
            font-size: 1.25rem;
            line-height: 1.75rem;
        }

        hr {
            margin: 40px auto;
            max-width: 100px;
            display: block;
            height: 1px;
            border: 0;
            border-top: 1px solid #ccc;
            padding: 0;
        }

        .pen-intro {
            text-align: center;
        }

        .game-choose {
            display: flex;
        }

        .game-img {
            width: 200px;
            height: 300px;
        }

        :root {
            --blue-rgb: 92 192 249;
            --green-rgb: 125 161 35;
            --brown-rgb: 127 46 23;
            --purple-rgb: 128 0 128;
            --red-rgb: 255 88 46;
            --grey-rgb: 143 143 143;
        }

        html,
        body {
            background-color: black;
        }

        body {
            min-height: 100vh;
            padding: 0;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 1000ms;
        }

        body:has(.card[data-color="blue"]:hover) {
            background-color: rgb(var(--blue-rgb) / 25%);
        }

        body:has(.card[data-color="purple"]:hover) {
            background-color: rgb(var(--purple-rgb) / 25%);
        }

        body:has(.card[data-color="green"]:hover) {
            background-color: rgb(var(--green-rgb) / 25%);
        }

        body:has(.card[data-color="brown"]:hover) {
            background-color: rgb(var(--brown-rgb) / 25%);
        }

        body:has(.card[data-color="grey"]:hover) {
            background-color: rgb(var(--grey-rgb) / 25%);
        }

        body:has(.card[data-color="red"]:hover) {
            background-color: rgb(var(--red-rgb) / 25%);
        }

        #cards {
            width: 100%;
            display: flex;
            justify-content: space-evenly;
        }

        .card {
            background-size: cover;
            background-position: center;
            position: relative;
            cursor: pointer;
            outline: none;
            transition: scale 100ms;
        }

        .card .card-front-image {
            position: relative;
            z-index: 2;
        }

        .card .card-image {
            width: clamp(150px, 20vw, 250px);
            aspect-ratio: 2 / 3;
            border-radius: clamp(0.5rem, 0.75vw, 2rem);
        }

        .card-faders {
            height: 100%;
            width: 100%;
            position: absolute;
            left: 0px;
            top: 0px;
            z-index: 1;
            opacity: 0;
            transition: opacity 1500ms;
            pointer-events: none;
        }

        .card:hover .card-faders {
            opacity: 1;
        }

        .card:active {
            scale: 0.98;
        }

        .card-fader {
            position: absolute;
            left: 0px;
            top: 0px;
        }

        .card-fader:nth-child(odd) {
            animation: fade-left 3s linear infinite;
        }

        .card-fader:nth-child(even) {
            animation: fade-right 3s linear infinite;
        }

        .card-fader:is(:nth-child(3), :nth-child(4)) {
            animation-delay: 750ms;
        }

        .card-fader:is(:nth-child(5), :nth-child(6)) {
            animation-delay: 1500ms;
        }

        .card-fader:is(:nth-child(7), :nth-child(8)) {
            animation-delay: 2250ms;
        }

        @media(max-width: 1200px) {
            body {
                justify-content: flex-start;
                align-items: flex-start;
            }

            #cards {
                flex-direction: column;
                align-items: center;
                gap: 4rem;
                padding: 4rem;
            }

            .card .card-image {
                width: 400px;
            }
        }

        @media(max-width: 1000px) {
            #cards {
                width: 500px;
                gap: 2rem;
                padding: 2rem;
            }

            .card {
                width: 80%;
            }

            .card .card-image {
                width: 100%;
            }
        }

        @media(max-width: 600px) {
            #cards {
                gap: 2rem;
                padding: 2rem;
            }

            .card {
                width: 80%;
            }

            .card .card-image {
                width: 100%;
            }
        }

        @keyframes fade-left {
            from {
                scale: 1;
                translate: 0%;
                opacity: 1;
            }

            to {
                scale: 0.8;
                translate: -30%;
                opacity: 0;
            }
        }

        @keyframes fade-right {
            from {
                scale: 1;
                translate: 0%;
                opacity: 1;
            }

            to {
                scale: 0.8;
                translate: 30%;
                opacity: 0;
            }
        }

        #exampleModal, #declareWinnerModal {
            z-index: 100000000000000000000000000;
        }

        .modal-body {
            background: transparent;
            width: 1200px;
        }

        .modal-content {
            background: transparent;
            width: 1200px;
        }

        .card {
            background-color: transparent;
        }

        body {
            font-family: 'Press Start 2P', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #212529;
            color: #dee2e6;
        }
        .pimg{
            border-radius: 50px;
        }
        .declare-winner {
            display: none;
        }
                    """,
      "body":"""<div class="center align-middle">
        <div class="round text-center h1 py-5" id="round">
            Round <span id="round_num">1</span>
        </div>
        
        <div>
            <div class="d-flex align-items-center justify-content-center">
                <div>
                    <div class="rounded-5 overflow-hidden">
                        <img class="img-fluid pimg" src="/static/avatars/4.jpg" alt="" width="300px" height="300px"
                            id="player_1_img">
                    </div>
                    <div class="h3 text-center py-2" id="player_1_name">Bhavin</div>
                    <div id="player_1_points">0</div> points
                </div>
                <div>
                    <img src="/static/images/vs.png" alt="VS" width="300px" height="300px">
                </div>
                <div>
                    <div class="rounded-5 overflow-hidden">
                        <img class="img-fluid pimg" src="/static/avatars/9.jpg" alt="" width="300px" height="300px"
                            id="player_2_img">
                    </div>
                    <div class="h3 text-center py-2" id="player_2_name">Vishal</div>
                    <div id="player_2_points">0</div> points
                </div>
            </div>
        </div>
        <link href='https://fonts.googleapis.com/css?family=VT323' rel='stylesheet' type='text/css'>

        <hr />
        <div class="d-flex justify-content-center">
            <div class="round text-center h5 px-5" id="wait-for-choose" style="display: none;">
                Waiting for other player to choose a game
            </div>
            <button type="button" class="eightbit-btn" data-toggle="modal" data-target="#exampleModal" id="choose-game">
                Choose
                Game</button>
        </div>
        <hr />
        <div class="d-flex justify-content-center">
            <button type="button" class="eightbit-btn declare-winner" data-toggle="modal" data-target="#declareWinnerModal" id="declare-winner">
                Declare Winner
            </button>
        </div>
        <hr class="declare-winner"/>
        <!-- <div class="container">

            <button type="button" class="pixel2" data-toggle="modal" data-target="#exampleModal">Choose Game</button>
        </div>
        <hr /> -->
    </div>
    """,
    "script":"""
    <script>
        const chooseGame = async () => {
            const response = await fetch("/choose-game");
            const data = await response.json();
            console.log(data.games);
            let imgs = data.games.map((game) => {
                console.log("game bg:- ", game.bg);
                return `
                <div class="card" data-color="${game.bg}">
                    <img class="card-front-image card-image" src="${game.path}" />
                <div class="card-faders">
                    <img class="card-fader card-image" src="${game.path}" />
                    <img class="card-fader card-image" src="${game.path}" />
                    <img class="card-fader card-image" src="${game.path}" />
                    <img class="card-fader card-image" src="${game.path}" />
                    <img class="card-fader card-image" src="${game.path}" />
                    <img class="card-fader card-image" src="${game.path}" />
                    <img class="card-fader card-image" src="${game.path}" />
                    <img class="card-fader card-image" src="${game.path}" />
                </div>
                </div>
            `})
            document.getElementById('cards').innerHTML = imgs;

        }
        $('#exampleModal').on('show.bs.modal', async function (event) {
            console.log("hi");
            chooseGame();
            var button = $(event.relatedTarget) // Button that triggered the modal
            var recipient = button.data('whatever') // Extract info from data-* attributes
            var modal = $(this)
        })
    </script>
</body>
    """})
