def jugador_mas_cercano(jugadores, balon):
    return min(jugadores, key=lambda j: j.distancia_a(balon))
