from flask import Flask, render_template, request, url_for
import rsa
import des
# bulma template: https://bulmatemplates.github.io/bulma-templates/templates/contact.html
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        key_size = int(request.form.get("keySize"))
        user_message = request.form.get("msg")

        # Perform RSA Algorithm for key agreement
        rsa_obj = rsa.RSA()
        rsa_obj.key_generation(key_size)
        rsa_obj.encrypt()
        rsa_obj.decrypt()

        print(f"Public Key: {rsa_obj.public_key}")
        print(f"Private Key: {rsa_obj.private_key}")
        print(f"Ciphertext: {rsa_obj.ciphertext}")
        print(f"Plaintext: {rsa_obj.plaintext}")

        # Perform DES algorithm for user message
        des_obj = des.DES(user_message, rsa_obj.plaintext)
        des_obj.encrypt()
        des_obj.decrypt()

        print(f"Original Message: {des_obj.user_message}")
        print(f"Master Key: {des_obj.master_key}")
        print(f"Ciphertext: {des_obj.ciphertext_text}")
        print(f"Decrypted Message: {des_obj.plaintext_text}")
        
        return render_template("index.html", 
                               rsa_public_key = rsa_obj.public_key, 
                               rsa_private_key = rsa_obj.private_key, 
                               rsa_ciphertext = rsa_obj.ciphertext, 
                               rsa_plaintext = rsa_obj.plaintext,
                               des_original_message = des_obj.user_message,
                               des_master_key = des_obj.master_key,
                               des_ciphertext = des_obj.ciphertext_text,
                               des_plaintext = des_obj.plaintext_text)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    # "python app.py" to run app
    app.run(host="0.0.0.0", port=5000, debug=True)