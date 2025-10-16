from flask import Flask, jsonify, request
import sqlite3

# Configuração
app = Flask(__name__)

# --- Funções do Banco de Dados ---

# Função para conectar ao banco
def conectar():
    """Conecta e retorna a conexão com o banco de dados 'banco.db'."""
    return sqlite3.connect('banco.db') # [cite: 38, 39]

# Função para criar a tabela de alunos
def criar_tabela():
    """Cria a tabela 'alunos' se ela não existir."""
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER
        )
    ''') # [cite: 41, 44, 45, 46, 47, 48, 49]
    con.commit() # [cite: 51]
    con.close() # [cite: 52]

# Cria a tabela ao iniciar o aplicativo
criar_tabela() # [cite: 53]

# --- Rotas da API (CRUD) ---

# Rota de teste/home
@app.route('/') # [cite: 54]
def home():
    """Retorna uma mensagem simples para confirmar que a API está rodando."""
    return 'API de Alunos funcionando!' # [cite: 55, 56]

# Rota para LISTAR todos os alunos (GET)
@app.route('/alunos', methods=['GET']) # [cite: 57, 58]
def listar():
    """Consulta e retorna a lista de todos os alunos."""
    con = conectar()
    cur = con.cursor()
    cur.execute('SELECT * FROM alunos') # [cite: 64]
    dados = cur.fetchall() # [cite: 65]
    con.close() # [cite: 66]
    
    # Formata os dados para JSON
    alunos = [{"id": a[0], "nome": a[1], "idade": a[2]} for a in dados]
    return jsonify(alunos) # [cite: 67]

# Rota para ADICIONAR um novo aluno (POST)
@app.route('/alunos', methods=['POST']) # [cite: 68, 69]
def adicionar():
    """Adiciona um novo aluno ao banco de dados."""
    novo = request.get_json() # Pega o JSON enviado no corpo da requisição [cite: 71]
    
    # Garante que 'nome' e 'idade' estão presentes no JSON
    nome = novo.get('nome') # [cite: 72]
    idade = novo.get('idade') # [cite: 73]
    
    if not nome or not idade:
        return jsonify({"erro": "Nome e idade são obrigatórios"}), 400

    con = conectar() # [cite: 74]
    cur = con.cursor() # [cite: 75]
    cur.execute('INSERT INTO alunos (nome, idade) VALUES (?, ?)', (nome, idade)) # [cite: 76]
    con.commit() # [cite: 77]
    con.close() # [cite: 78]

    return jsonify({"mensagem": "Aluno adicionado com sucesso!"}), 201 # [cite: 79]

# Rota para EXCLUIR um aluno por ID (DELETE) - Desafio Extra
@app.route('/alunos/<int:id>', methods=['DELETE']) # [cite: 104, 107]
def deletar(id):
    """Exclui um aluno com o ID fornecido."""
    con = conectar() # [cite: 109]
    cur = con.cursor() # [cite: 110]
    
    # O comando SQL correto seria: DELETE FROM alunos WHERE id=?
    cur.execute('DELETE FROM alunos WHERE id=?', (id,)) # [cite: 111]
    
    # Verifica se alguma linha foi afetada (se o aluno existia)
    if cur.rowcount == 0:
        con.close()
        return jsonify({"erro": f"Aluno com ID {id} não encontrado"}), 404
        
    con.commit() # [cite: 112]
    con.close() # [cite: 113]
    return jsonify({"mensagem": f"Aluno {id} removido com sucesso!"}) # [cite: 116]

# Rota para ATUALIZAR um aluno por ID (PUT) - Desafio Extra
@app.route('/alunos/<int:id>', methods=['PUT']) # [cite: 118, 125]
def atualizar(id):
    """Atualiza o nome e/ou idade de um aluno com o ID fornecido."""
    dados = request.get_json() # [cite: 127]
    
    # Garante que 'nome' e 'idade' estão presentes no JSON
    nome = dados.get('nome')
    idade = dados.get('idade')
    
    if not nome and not idade:
         return jsonify({"erro": "Pelo menos um campo (nome ou idade) deve ser fornecido para atualização"}), 400

    con = conectar() # [cite: 128]
    cur = con.cursor() # [cite: 129]
    
    # Monta a query de forma dinâmica
    sets = []
    params = []
    if nome:
        sets.append('nome=?')
        params.append(nome)
    if idade:
        sets.append('idade=?')
        params.append(idade)
        
    params.append(id) # O último parâmetro é sempre o ID para a cláusula WHERE
    
    query = f"UPDATE alunos SET {', '.join(sets)} WHERE id=?"
    
    cur.execute(query, tuple(params)) # [cite: 130, 131]
    
    # Verifica se alguma linha foi afetada (se o aluno existia)
    if cur.rowcount == 0:
        con.close()
        return jsonify({"erro": f"Aluno com ID {id} não encontrado"}), 404
        
    con.commit() # [cite: 132]
    con.close() # [cite: 133]
    return jsonify({"mensagem": "Aluno atualizado com sucesso!"}) # [cite: 134]


if __name__ == '__main__':
    # Roda a aplicação em modo debug, acessível em http://127.0.0.1:5000/
    app.run(debug=True) # [cite: 80, 81]