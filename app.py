from flask import Flask, request, jsonify, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__)

# File untuk menyimpan data paket
DATA_FILE = 'list.json'

# Fungsi untuk memuat data dari file JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        # Buat file dengan data default jika belum ada
        default_data = [
            {
                "id": 1,
                "nama": "Internet Harian",
                "harga": 10000,
                "kuota": "1GB",
                "masa_aktif": "1 Hari",
                "kecepatan": "4G",
                "zona": "Nasional",
                "bonus": "",
                "note": "",  # <-- tambahkan field note
                "whatsapp_text": "Saya ingin memesan paket Internet Harian Rp 10.000"
            },
            {
                "id": 2,
                "nama": "Internet Mingguan",
                "harga": 25000,
                "kuota": "5GB",
                "masa_aktif": "7 Hari",
                "kecepatan": "4G",
                "zona": "Nasional",
                "bonus": "1GB Musik",
                "note": "",
                "whatsapp_text": "Saya ingin memesan paket Internet Mingguan Rp 25.000"
            },
            {
                "id": 3,
                "nama": "Internet Bulanan",
                "harga": 75000,
                "kuota": "20GB",
                "masa_aktif": "30 Hari",
                "kecepatan": "4G",
                "zona": "Nasional",
                "bonus": "5GB Musik & Video, 2GB Games",
                "note": "",
                "whatsapp_text": "Saya ingin memesan paket Internet Bulanan Rp 75.000"
            },
            {
                "id": 4,
                "nama": "Internet Unlimited",
                "harga": 150000,
                "kuota": "Unlimited (FAIR USE 30GB)",
                "masa_aktif": "30 Hari",
                "kecepatan": "4G/5G",
                "zona": "Nasional",
                "bonus": "Streaming: Unlimited, Gaming: Low Latency",
                "note": "",
                "whatsapp_text": "Saya ingin memesan paket Internet Unlimited Rp 150.000"
            },
            {
                "id": 5,
                "nama": "Internet Malam",
                "harga": 5000,
                "kuota": "5GB",
                "masa_aktif": "1 Malam (00:00-06:00)",
                "kecepatan": "4G",
                "zona": "Nasional",
                "bonus": "",
                "note": "",
                "whatsapp_text": "Saya ingin memesan paket Internet Malam Rp 5.000"
            },
            {
                "id": 6,
                "nama": "Internet Sosmed",
                "harga": 8000,
                "kuota": "3GB (Khusus Sosmed)",
                "masa_aktif": "3 Hari",
                "kecepatan": "4G",
                "zona": "Nasional",
                "bonus": "Include: Facebook, Instagram, Twitter, WhatsApp",
                "note": "",
                "whatsapp_text": "Saya ingin memesan paket Internet Sosmed Rp 8.000"
            }
        ]
        save_data(default_data)
        return default_data
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

# Fungsi untuk menyimpan data ke file JSON
def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

# Endpoint untuk mendapatkan semua paket
@app.route('/api/paket', methods=['GET'])
def get_paket():
    data = load_data()
    return jsonify(data)

# Endpoint untuk mendapatkan paket berdasarkan ID
@app.route('/api/paket/<int:paket_id>', methods=['GET'])
def get_paket_by_id(paket_id):
    data = load_data()
    paket = next((p for p in data if p['id'] == paket_id), None)
    if paket:
        return jsonify(paket)
    else:
        return jsonify({'error': 'Paket tidak ditemukan'}), 404

# Endpoint untuk menambahkan paket baru
@app.route('/api/paket', methods=['POST'])
def add_paket():
    try:
        data = load_data()
        new_paket = request.get_json()
        
        # Validasi hanya field yang benar-benar wajib
        required_fields = ['nama', 'harga', 'kuota', 'masa_aktif', 'whatsapp_text']
        for field in required_fields:
            if field not in new_paket or not new_paket[field]:
                return jsonify({'error': f'Field {field} wajib diisi'}), 400
        
        # Generate ID baru
        if len(data) > 0:
            new_id = max(p['id'] for p in data) + 1
        else:
            new_id = 1
        
        # Tambahkan nilai default jika kecepatan/zona/note tidak dikirim
        new_paket['id'] = new_id
        new_paket.setdefault('kecepatan', '-')      # <-- default jika tidak ada
        new_paket.setdefault('zona', '-')           # <-- default jika tidak ada
        new_paket.setdefault('note', '')            # <-- default note kosong
        new_paket.setdefault('bonus', '')           # <-- aman jika tidak dikirim
        
        data.append(new_paket)
        
        if save_data(data):
            return jsonify(new_paket), 201
        else:
            return jsonify({'error': 'Gagal menyimpan data'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

# Endpoint untuk memperbarui paket
@app.route('/api/paket/<int:paket_id>', methods=['PUT'])
def update_paket(paket_id):
    try:
        data = load_data()
        updated_paket = request.get_json()
        
        # Validasi hanya field yang benar-benar wajib
        required_fields = ['nama', 'harga', 'kuota', 'masa_aktif', 'whatsapp_text']
        for field in required_fields:
            if field not in updated_paket or not updated_paket[field]:
                return jsonify({'error': f'Field {field} wajib diisi'}), 400
        
        # Cari paket berdasarkan ID
        paket_index = None
        for i, paket in enumerate(data):
            if paket['id'] == paket_id:
                paket_index = i
                break
        
        if paket_index is not None:
            # Update paket dengan ID yang sama
            updated_paket['id'] = paket_id
            
            # Tambahkan nilai default jika kecepatan/zona/note tidak dikirim
            updated_paket.setdefault('kecepatan', '-')
            updated_paket.setdefault('zona', '-')
            updated_paket.setdefault('note', '')
            updated_paket.setdefault('bonus', '')
            
            data[paket_index] = updated_paket
            
            if save_data(data):
                return jsonify(updated_paket)
            else:
                return jsonify({'error': 'Gagal menyimpan data'}), 500
        else:
            return jsonify({'error': 'Paket tidak ditemukan'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

# Endpoint untuk menghapus paket
@app.route('/api/paket/<int:paket_id>', methods=['DELETE'])
def delete_paket(paket_id):
    try:
        data = load_data()
        original_length = len(data)
        data = [p for p in data if p['id'] != paket_id]
        
        if len(data) < original_length:
            if save_data(data):
                return jsonify({'message': 'Paket berhasil dihapus'}), 200
            else:
                return jsonify({'error': 'Gagal menyimpan data'}), 500
        else:
            return jsonify({'error': 'Paket tidak ditemukan'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

# Serve file static (HTML, CSS, JS, JSON)
@app.route('/')
def serve_index():
    return send_from_directory('.', 'katalog.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory('.', 'admin.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("Server starting...")
    print("Katalog: http://localhost:5000/")
    print("Admin: http://localhost:5000/admin")
    print("API: http://localhost:5000/api/paket")
    
    # Jalankan server di host 0.0.0.0 agar bisa diakses dari luar
    app.run(host='0.0.0.0', port=3000, debug=True)
