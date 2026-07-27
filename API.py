from flask import Flask, jsonify

app = Flask(__name__)

# Essa é a sua rota da API
@app.route('/api/mensagem', methods=['GET'])
def mensagem():
    return jsonify({
        "mensagem": "Olá! Agora sim, API rodando em Python sem mentira!",
        "status": "online"
    })

if __name__ == '__main__':
    # Roda o servidor na porta 3000
    app.run(host='0.0.0.0', port=3000)
    