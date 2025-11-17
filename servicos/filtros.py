# adicionar filtros por data, número, etc.
def filtrar_por_data(loteria, data_inicio=None, data_fim=None):
    if not data_inicio and not data_fim:
        return loteria.sorteios
    filtrados = []
    for sorteio in loteria.sorteios:
        if data_inicio and sorteio.data < data_inicio:
            continue
        if data_fim and sorteio.data > data_fim:
            continue
        filtrados.append(sorteio)
    return filtrados

# Exemplo futuro
# def filtrar_por_numero(loteria, numero):
#     return [s for s in loteria.sorteios if numero in s.numeros_sorteados]

