from flask import Flask, request

app = Flask(__name__)

@app.route('/wpbot', methods=['POST'])
def bot():
    try:
        user_message = request.values.get('Body', '').lower()
        print(user_message)
    except:
        print('Não foi possível receber a mensagem')

if __name__ == '__main__':
    app.run()