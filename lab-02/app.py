from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)

# router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

# router routes for caesar cypher
@app.route("/caesar")
def caesar():
    return render_template('caesar.html') # Trang ban dau chua co ket qua

@app.route("/caesar/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    try:
        key = int(request.form['inputKeyPlain'])
    except ValueError:
        # Nếu có lỗi, trả về trang với thông báo lỗi
        return render_template('caesar.html', 
                               error_message="Loi: Key phai la mot so nguyen.",
                               original_text=text, 
                               key_used=request.form['inputKeyPlain'])

    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    # Tra ve template voi ket qua
    return render_template('caesar.html', 
                           original_text=text, 
                           key_used=key, 
                           result_text=encrypted_text, 
                           operation_type="ma hoa")

@app.route("/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    try:
        key = int(request.form['inputKeyCipher'])
    except ValueError:
        # Nếu có lỗi, trả về trang với thông báo lỗi
        return render_template('caesar.html', 
                               error_message="Loi: Key phai la mot so nguyen.",
                               original_text=text, 
                               key_used=request.form['inputKeyCipher'])

    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    # Tra ve template voi ket qua
    return render_template('caesar.html', 
                           original_text=text, 
                           key_used=key, 
                           result_text=decrypted_text, 
                           operation_type="giai ma")

# router routes for vigenere
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']

    Vigenere = VigenereCipher()
    encrypted_text = Vigenere.vigenere_encrypt(text, key) # <--- DOI TEN HAM O DAY
    return render_template('vigenere.html',
                           original_text=text,
                           key_used=key,
                           result_text=encrypted_text,
                           operation_type="ma hoa")

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']

    Vigenere = VigenereCipher()
    decrypted_text = Vigenere.vigenere_decrypt(text, key) # <--- DOI TEN HAM O DAY
    return render_template('vigenere.html',
                           original_text=text,
                           key_used=key,
                           result_text=decrypted_text,
                           operation_type="giai ma")

# router routes for railfence
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    try:
        key = int(request.form['inputKeyPlain'])
    except ValueError:
        return render_template('railfence.html', 
                               error_message="Loi: Key phai la mot so nguyen.",
                               original_text=text, 
                               key_used=request.form['inputKeyPlain'])

    Railfence = RailFenceCipher()
    encrypted_text = Railfence.rail_fence_encrypt(text, key)
    return render_template('railfence.html', 
                           original_text=text, 
                           key_used=key, 
                           result_text=encrypted_text, 
                           operation_type="ma hoa")

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    try:
        key = int(request.form['inputKeyCipher'])
    except ValueError:
        return render_template('railfence.html', 
                               error_message="Loi: Key phai la mot so nguyen.",
                               original_text=text, 
                               key_used=request.form['inputKeyCipher'])

    Railfence = RailFenceCipher()
    decrypted_text = Railfence.rail_fence_decrypt(text, key)
    return render_template('railfence.html', 
                           original_text=text, 
                           key_used=key, 
                           result_text=decrypted_text, 
                           operation_type="giai ma")

@app.route("/playfair")
def playfair_page():
    return render_template('playfair.html')

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']

    try:
        if not key.strip():
            raise ValueError("Key khong duoc de trong cho Playfair Cipher.")
            
        Playfair = PlayFairCipher() 
        playfair_matrix = Playfair.create_playfair_matrix(key) # TAO MATRIX O DAY
        
        # GỌI HÀM VỚI MATRIX
        encrypted_text = Playfair.playfair_encrypt(text, playfair_matrix) 
        
        return render_template('playfair.html', 
                               original_text=text, 
                               key_used=key, 
                               result_text=encrypted_text, 
                               operation_type="ma hoa",
                               playfair_matrix=playfair_matrix # TRUYEN MA TRAN VAO DAY
                               )
    except ValueError as e:
        return render_template('playfair.html', 
                               error_message=str(e),
                               original_text=text, 
                               key_used=key)
    except Exception as e:
        return render_template('playfair.html', 
                               error_message=f"Da co loi xay ra trong qua trinh ma hoa: {str(e)}",
                               original_text=text, 
                               key_used=key)

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']

    try:
        if not key.strip():
            raise ValueError("Key khong duoc de trong cho Playfair Cipher.")

        Playfair = PlayFairCipher() 
        playfair_matrix = Playfair.create_playfair_matrix(key) # TAO MATRIX O DAY
        
        # GỌI HÀM VỚI MATRIX
        decrypted_text = Playfair.playfair_decrypt(text, playfair_matrix) 
        
        return render_template('playfair.html', 
                               original_text=text, 
                               key_used=key, 
                               result_text=decrypted_text, 
                               operation_type="giai ma",
                               playfair_matrix=playfair_matrix # TRUYEN MA TRAN VAO DAY
                               )
    except ValueError as e:
        return render_template('playfair.html', 
                               error_message=str(e),
                               original_text=text, 
                               key_used=key)
    except Exception as e:
        return render_template('playfair.html', 
                               error_message=f"Da co loi xay ra trong qua trinh giai ma: {str(e)}",
                               original_text=text, 
                               key_used=key)
# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)