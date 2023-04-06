from flask import Flask, render_template, request, url_for
import rsa
# bulma template: https://bulmatemplates.github.io/bulma-templates/templates/contact.html
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        key_size = int(request.form.get("keySize"))
        user_message = request.form.get("msg")

        # Perform RSA Algorithm
        results = rsa.RSA(user_message)
        results.key_generation(key_size)
        results.encrypt()
        results.decrypt()

        print(f"Message: {results.message}")
        print(f"Public Key: {results.public_key}")
        print(f"Private Key: {results.private_key}")
        print(f"Ciphertext: {results.ciphertext}")
        print(f"Plaintext: {results.plaintext}")
        
        return render_template("index.html",
                                message = results.message,
                                public_key = results.public_key,
                                private_key = results.private_key,
                                ciphertext = results.ciphertext,
                                plaintext = results.plaintext)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    # "python app.py" to run app
    app.run()