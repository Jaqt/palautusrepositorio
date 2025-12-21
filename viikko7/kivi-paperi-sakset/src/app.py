from flask import Flask, render_template, request, session, redirect, url_for
from kps_tehdas import luo_peli
from tuomari import Tuomari

app = Flask(__name__)
app.secret_key = 'dev-secret-key-kivi-paperi-sakset-2025'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False


@app.route('/')
def index():
    # Nollaa peli uudella vierailulla
    session.clear()
    return render_template('index.html')


@app.route('/new_game', methods=['POST'])
def new_game():
    game_type = request.form.get('game_type')
    print(f"DEBUG: Uusi peli aloitettu, game_type={game_type}")
    session['game_type'] = game_type
    session['round'] = 0
    session['ekan_pisteet'] = 0
    session['tokan_pisteet'] = 0
    session['tasapelit'] = 0
    session['ai_moves'] = []  # Parannetulle tekoälylle
    session['historia'] = []  # Kierroshistoria
    print(f"DEBUG: Session asetettu: {dict(session)}")
    return redirect(url_for('play'))


@app.route('/play')
def play():
    print(f"DEBUG: /play kutsuttu, session={dict(session)}")
    if 'game_type' not in session:
        print("DEBUG: game_type ei sessionissa, ohjataan index-sivulle")
        return redirect(url_for('index'))
    
    game_type = session['game_type']
    historia = session.get('historia', [])
    print(f"DEBUG: Renderöidään play.html, game_type={game_type}")
    return render_template('play.html',
                         game_type=game_type,
                         ekan_pisteet=session.get('ekan_pisteet', 0),
                         tokan_pisteet=session.get('tokan_pisteet', 0),
                         tasapelit=session.get('tasapelit', 0),
                         historia=historia[-5:])


@app.route('/make_move', methods=['POST'])
def make_move():
    if 'game_type' not in session:
        return redirect(url_for('index'))
    
    ekan_siirto = request.form.get('move')
    game_type = session['game_type']
    
    # Tarkista onko siirto validi
    if ekan_siirto not in ['k', 'p', 's']:
        return render_template('game_over.html',
                             ekan_pisteet=session.get('ekan_pisteet', 0),
                             tokan_pisteet=session.get('tokan_pisteet', 0),
                             tasapelit=session.get('tasapelit', 0))
    
    # Tee vastustajan siirto
    peli = luo_peli(game_type)
    
    if game_type == 'a':
        # Pelaaja vs pelaaja - toisen pelaajan siirto
        tokan_siirto = request.form.get('move2')
        if tokan_siirto not in ['k', 'p', 's']:
            return render_template('game_over.html',
                                 ekan_pisteet=session.get('ekan_pisteet', 0),
                                 tokan_pisteet=session.get('tokan_pisteet', 0),
                                 tasapelit=session.get('tasapelit', 0))
    elif game_type == 'b':
        # Tavallinen tekoäly
        from tekoaly import Tekoaly
        ai = Tekoaly()
        tokan_siirto = ai.anna_siirto()
    else:  # game_type == 'c'
        # Parannettu tekoäly
        from tekoaly_parannettu import TekoalyParannettu
        ai = TekoalyParannettu(10)
        # Lataa aiemmat pelaajan siirrot muistiin
        for move in session.get('ai_moves', []):
            ai.aseta_siirto(move)
        # Nyt aseta nykyinen pelaajan siirto
        ai.aseta_siirto(ekan_siirto)
        # Pyydä tekoälyn siirto (se ennustaa pelaajan seuraavaa siirtoa)
        tokan_siirto = ai.anna_siirto()
        # Tallenna pelaajan siirto sessioon seuraavaa kierrosta varten
        session['ai_moves'] = session.get('ai_moves', []) + [ekan_siirto]
    
    # Päivitä pisteet
    tuomari = Tuomari()
    tuomari.ekan_pisteet = session.get('ekan_pisteet', 0)
    tuomari.tokan_pisteet = session.get('tokan_pisteet', 0)
    tuomari.tasapelit = session.get('tasapelit', 0)
    
    tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
    
    session['ekan_pisteet'] = tuomari.ekan_pisteet
    session['tokan_pisteet'] = tuomari.tokan_pisteet
    session['tasapelit'] = tuomari.tasapelit
    session['round'] = session.get('round', 0) + 1
    
    # Tallenna kierros historiaan
    historia = session.get('historia', [])
    
    # Määritä voittaja
    if ekan_siirto == tokan_siirto:
        voittaja = 'tasapeli'
    elif (ekan_siirto == 'k' and tokan_siirto == 's') or \
         (ekan_siirto == 's' and tokan_siirto == 'p') or \
         (ekan_siirto == 'p' and tokan_siirto == 'k'):
        voittaja = 'eka'
    else:
        voittaja = 'toka'
    
    kierros_tulos = {
        'kierros': session['round'],
        'ekan_siirto': ekan_siirto,
        'tokan_siirto': tokan_siirto,
        'voittaja': voittaja
    }
    historia.append(kierros_tulos)
    session['historia'] = historia
    
    # Tarkista onko jompikumpi saavuttanut 5 voittoa
    if tuomari.ekan_pisteet >= 3 or tuomari.tokan_pisteet >= 3:
        return render_template('game_over.html',
                             ekan_pisteet=tuomari.ekan_pisteet,
                             tokan_pisteet=tuomari.tokan_pisteet,
                             tasapelit=tuomari.tasapelit)
    
    # Näytä kierroksen tulos
    return render_template('round_result.html',
                         ekan_siirto=ekan_siirto,
                         tokan_siirto=tokan_siirto,
                         ekan_pisteet=tuomari.ekan_pisteet,
                         tokan_pisteet=tuomari.tokan_pisteet,
                         tasapelit=tuomari.tasapelit,
                         game_type=game_type,
                         historia=historia[-5:])


@app.route('/end_game')
def end_game():
    return render_template('game_over.html',
                         ekan_pisteet=session.get('ekan_pisteet', 0),
                         tokan_pisteet=session.get('tokan_pisteet', 0),
                         tasapelit=session.get('tasapelit', 0))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
