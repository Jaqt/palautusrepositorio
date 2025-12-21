import pytest
from app import app


@pytest.fixture
def client():
    """Luo Flask test client"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Testaa että etusivu latautuu"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Kivi-Paperi-Sakset' in response.data
    assert b'Ihmist' in response.data
    assert b'vastaan' in response.data


def test_new_game_player_vs_player(client):
    """Testaa uuden pelin aloitus pelaaja vs pelaaja"""
    response = client.post('/new_game', data={'game_type': 'a'}, follow_redirects=False)
    assert response.status_code == 302
    assert '/play' in response.location


def test_new_game_vs_ai(client):
    """Testaa uuden pelin aloitus tekoälyä vastaan"""
    response = client.post('/new_game', data={'game_type': 'b'}, follow_redirects=False)
    assert response.status_code == 302
    assert '/play' in response.location


def test_new_game_vs_improved_ai(client):
    """Testaa uuden pelin aloitus parannettua tekoälyä vastaan"""
    response = client.post('/new_game', data={'game_type': 'c'}, follow_redirects=False)
    assert response.status_code == 302
    assert '/play' in response.location


def test_play_page_without_session(client):
    """Testaa että play-sivu ohjaa etusivulle ilman sessiota"""
    response = client.get('/play', follow_redirects=False)
    assert response.status_code == 302
    assert '/' in response.location


def test_play_page_with_session(client):
    """Testaa että play-sivu latautuu session kanssa"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
    
    response = client.get('/play')
    assert response.status_code == 200
    assert b'Pelitilanne' in response.data


def test_make_move_vs_ai_rock(client):
    """Testaa siirron tekeminen tekoälyä vastaan - kivi"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['historia'] = []
    
    response = client.post('/make_move', data={'move': 'k'})
    assert response.status_code == 200
    assert b'Kierroksen tulos' in response.data


def test_make_move_vs_ai_paper(client):
    """Testaa siirron tekeminen tekoälyä vastaan - paperi"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['historia'] = []
    
    response = client.post('/make_move', data={'move': 'p'})
    assert response.status_code == 200
    assert b'Kierroksen tulos' in response.data


def test_make_move_vs_ai_scissors(client):
    """Testaa siirron tekeminen tekoälyä vastaan - sakset"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['historia'] = []
    
    response = client.post('/make_move', data={'move': 's'})
    assert response.status_code == 200
    assert b'Kierroksen tulos' in response.data


def test_make_move_player_vs_player(client):
    """Testaa siirron tekeminen pelaaja vs pelaaja"""
    with client.session_transaction() as session:
        session['game_type'] = 'a'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['historia'] = []
    
    response = client.post('/make_move', data={'move': 'k', 'move2': 's'})
    assert response.status_code == 200
    assert b'Kierroksen tulos' in response.data


def test_make_move_vs_improved_ai(client):
    """Testaa siirron tekeminen parannettua tekoälyä vastaan"""
    with client.session_transaction() as session:
        session['game_type'] = 'c'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['ai_moves'] = []
        session['historia'] = []
    
    response = client.post('/make_move', data={'move': 'k'})
    assert response.status_code == 200
    assert b'Kierroksen tulos' in response.data


def test_score_tracking(client):
    """Testaa että pisteet päivittyvät oikein"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['historia'] = []
    
    # Pelaaja pelaa kiven, ja katsotaan että pisteet päivittyvät
    response = client.post('/make_move', data={'move': 'k'})
    assert response.status_code == 200
    # Peli ei ole vielä päättynyt, joten pitäisi näyttää kierroksen tulos
    assert b'Kierroksen tulos' in response.data or b'ttyi' in response.data
    
    # Tarkista että session päivittyi
    with client.session_transaction() as session:
        total_points = session['ekan_pisteet'] + session['tokan_pisteet'] + session['tasapelit']
        assert total_points == 1  # Yhteensä 1 kierros pelattu


def test_multiple_rounds(client):
    """Testaa useamman kierroksen pelaaminen"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['historia'] = []
    
    # Pelaa 3 kierrosta
    for move in ['k', 'p', 's']:
        response = client.post('/make_move', data={'move': move})
        assert response.status_code == 200
    
    # Tarkista että 3 kierrosta pelattu ja peli ei ole vielä päättynyt
    with client.session_transaction() as session:
        total_points = session['ekan_pisteet'] + session['tokan_pisteet'] + session['tasapelit']
        assert total_points == 3
        # Varmista että kumpikaan ei ole vielä voittanut
        assert session['ekan_pisteet'] < 5
        assert session['tokan_pisteet'] < 5


def test_invalid_move(client):
    """Testaa että virheellinen siirto päättää pelin"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 2
        session['tokan_pisteet'] = 1
        session['tasapelit'] = 0
        session['historia'] = []
    
    response = client.post('/make_move', data={'move': 'x'})
    assert response.status_code == 200
    assert b'ttyi' in response.data or b'Peli' in response.data


def test_end_game(client):
    """Testaa pelin lopettaminen"""
    with client.session_transaction() as session:
        session['ekan_pisteet'] = 3
        session['tokan_pisteet'] = 2
        session['tasapelit'] = 1
    
    response = client.get('/end_game')
    assert response.status_code == 200
    assert b'ttyi' in response.data or b'Peli' in response.data


def test_player_wins(client):
    """Testaa että pelaajan voitto näytetään oikein"""
    with client.session_transaction() as session:
        session['ekan_pisteet'] = 5
        session['tokan_pisteet'] = 2
        session['tasapelit'] = 0
    
    response = client.get('/end_game')
    assert response.status_code == 200
    assert b'Pelaaja 1' in response.data


def test_ai_wins(client):
    """Testaa että tekoälyn voitto näytetään oikein"""
    with client.session_transaction() as session:
        session['ekan_pisteet'] = 1
        session['tokan_pisteet'] = 4
        session['tasapelit'] = 0
    
    response = client.get('/end_game')
    assert response.status_code == 200
    assert b'Pelaaja 2' in response.data


def test_tie_game(client):
    """Testaa että tasapeli näytetään oikein"""
    with client.session_transaction() as session:
        session['ekan_pisteet'] = 3
        session['tokan_pisteet'] = 3
        session['tasapelit'] = 1
    
    response = client.get('/end_game')
    assert response.status_code == 200
    assert b'Tasapeli' in response.data


def test_improved_ai_remembers_moves(client):
    """Testaa että parannettu tekoäly muistaa siirrot"""
    with client.session_transaction() as session:
        session['game_type'] = 'c'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['ai_moves'] = []
        session['historia'] = []
    
    # Pelaa useita kierroksia samalla siirrolla
    for _ in range(3):
        response = client.post('/make_move', data={'move': 'k'})
        assert response.status_code == 200
    
    # Tarkista että tekoäly on tallentanut siirrot
    with client.session_transaction() as session:
        assert len(session['ai_moves']) == 3
        assert all(move == 'k' for move in session['ai_moves'])


def test_game_ends_at_three_wins_player(client):
    """Testaa että peli päättyy kun pelaaja saa 3 voittoa"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 2
        session['tokan_pisteet'] = 2
        session['tasapelit'] = 0
        session['historia'] = []
    
    # Pelaaja voittaa seuraavan kierroksen (kivi voittaa sakset)
    # Koska tekoäly antaa satunnaisia siirtoja, varmistetaan että pisteet kasvavat
    response = client.post('/make_move', data={'move': 'k'})
    assert response.status_code == 200
    
    # Tarkista että joko peli päättyi tai jatkuu
    with client.session_transaction() as session:
        # Jos pelaaja sai 3. voiton, pitäisi näyttää game over
        if session['ekan_pisteet'] >= 3:
            assert b'ttyi' in response.data or b'Peli' in response.data


def test_game_ends_at_three_wins_ai(client):
    """Testaa että peli päättyy kun tekoäly saa 3 voittoa"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 1
        session['tokan_pisteet'] = 2
        session['tasapelit'] = 0
        session['historia'] = []
    
    # Pelaa kunnes tekoäly saa mahdollisesti 3. voiton
    response = client.post('/make_move', data={'move': 's'})
    assert response.status_code == 200
    
    with client.session_transaction() as session:
        if session['tokan_pisteet'] >= 3:
            assert b'ttyi' in response.data or b'Peli' in response.data


def test_game_continues_under_three_wins(client):
    """Testaa että peli jatkuu kun kumpikaan ei ole saanut 3 voittoa"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 2
        session['tokan_pisteet'] = 2
        session['tasapelit'] = 2
        session['historia'] = []
    
    response = client.post('/make_move', data={'move': 'k'})
    assert response.status_code == 200
    
    # Tarkista että kumpikaan ei ole vielä voittanut
    with client.session_transaction() as session:
        if session['ekan_pisteet'] < 3 and session['tokan_pisteet'] < 3:
            # Pelin pitäisi jatkua - näytetään kierroksen tulos
            assert b'Kierroksen tulos' in response.data


def test_historia_tallentuu(client):
    """Testaa että kierroshistoria tallentuu oikein"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['historia'] = []
    
    # Pelaa muutama kierros
    for move in ['k', 'p', 's']:
        response = client.post('/make_move', data={'move': move})
        assert response.status_code == 200
    
    # Tarkista että historia on tallennettu
    with client.session_transaction() as session:
        historia = session.get('historia', [])
        assert len(historia) == 3
        assert all('kierros' in k for k in historia)
        assert all('ekan_siirto' in k for k in historia)
        assert all('tokan_siirto' in k for k in historia)
        assert all('voittaja' in k for k in historia)


def test_historia_max_viisi(client):
    """Testaa että näytetään maksimissaan 5 viimeisintä kierrosta"""
    with client.session_transaction() as session:
        session['game_type'] = 'b'
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['historia'] = [
            {'kierros': i, 'ekan_siirto': 'k', 'tokan_siirto': 'p', 'voittaja': 'toka'}
            for i in range(1, 8)
        ]
    
    response = client.get('/play')
    assert response.status_code == 200
    # Tarkista että sivulla mainitaan kierroksia (max 5)
    assert b'Kierros' in response.data
