# LLM Exam Grader

Sistem penilaian ujian otomatis menggunakan Google Gemini AI untuk menilai jawaban mahasiswa pada soal-soal Web Development.

## 📋 Deskripsi

Proyek ini adalah aplikasi Python yang menggunakan Google Gemini AI (model `gemini-2.5-flash`) untuk secara otomatis menilai jawaban ujian mahasiswa. Sistem ini dirancang khusus untuk menilai soal-soal yang berisi analisis tentang masalah, penyebab, dan solusi dalam konteks Web Development.

### Fitur Utama

- ✅ Penilaian otomatis menggunakan AI
- ✅ Evaluasi komprehensif berdasarkan 3 aspek: Validasi Masalah, Evaluasi Penyebab, dan Evaluasi Solusi
- ✅ Validasi penggunaan keyword/istilah teknis
- ✅ Skor breakdown per aspek
- ✅ Feedback detail untuk setiap jawaban
- ✅ Export hasil penilaian ke file JSON

## 🎯 Kriteria Penilaian

Sistem menilai jawaban mahasiswa berdasarkan:

1. **Validasi Masalah (0-3.33 poin)**: Apakah masalah yang disebutkan realistis dan masuk akal dalam konteks frontend?
2. **Evaluasi Penyebab (0-3.33 poin)**: Apakah penyebab yang disebutkan secara logika dan teknis sesuai dengan konteks frontend rendering/behavior?
3. **Evaluasi Solusi (0-3.34 poin)**: Apakah solusi menyelesaikan akar masalah, bukan sekadar menghilangkan gejala?

**Total skor maksimal: 10 poin**

### Penilaian Keyword Khusus

- ❌ Menggunakan keyword dengan **definisi SALAH** → Kesalahan fatal, pengurangan skor signifikan
- ✅ Menggunakan keyword dengan **benar** → Nilai sesuai kualitas analisis
- ⭐ Menggunakan konsep/istilah **alternatif yang logis** → Apresiasi dengan skor lebih tinggi

## 📁 Struktur File

```
LLM-exam-grader/
├── main.py              # Script utama untuk grading
├── questions.json       # Database soal ujian
├── answers.json         # Database jawaban mahasiswa
├── output.json          # Hasil penilaian (generated)
├── .env                 # Konfigurasi API key
└── .env-copy            # Template file .env
```

## 🚀 Cara Menggunakan

### 1. Instalasi Dependencies

```bash
pip install google-generativeai python-dotenv
```

### 2. Setup API Key

1. Buat file `.env` di root directory
2. Tambahkan API key Gemini Anda:

```
GEMINI_API_KEY=your_api_key_here
```

> Dapatkan API key dari [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Persiapan Data

#### Format `questions.json`:

```json
{
  "questions": [
    {
      "question_id": "Q1",
      "masalah": "Deskripsi masalah",
      "penyebab": "Deskripsi penyebab",
      "solusi": "Deskripsi solusi",
      "keywords": [
        {
          "istilah": "Nama istilah",
          "definisi": "Definisi istilah"
        }
      ]
    }
  ]
}
```

#### Format `answers.json`:

```json
{
  "question_answer": [
    {
      "student_id": "221524053",
      "name": "Nama Mahasiswa",
      "answers": [
        {
          "question_id": "Q1",
          "verdict": "Sahih",
          "answer": "Reasoning mahasiswa..."
        }
      ]
    }
  ]
}
```

### 4. Menjalankan Program

```bash
python main.py
```

Program akan:
1. Membaca soal dari `questions.json`
2. Membaca jawaban dari `answers.json`
3. Menilai setiap jawaban menggunakan Gemini AI
4. Menampilkan hasil di terminal
5. Menyimpan hasil detail ke `output.json`

## 📊 Output

### Output Terminal

```
Grading Najib Alimudin Fajri - Q1...
Grading Najib Alimudin Fajri - Q2...
...

==================================================
HASIL PENILAIAN
==================================================

Najib Alimudin Fajri (221524053)
Total Score: 8.5
----------------------------------------
  Q1: 9/10
  Masalah: ...
  Penyebab: ...
  Solusi: ...
  Verdict Mahasiswa: Sahih
  Verdict Benar: Sahih
  Breakdown:
    - validasi_masalah: 3.0
    - evaluasi_penyebab: 3.2
    - evaluasi_solusi: 3.3
  Penggunaan Keyword: ...
  Feedback: ...
```

### Output `output.json`

File JSON berisi detail lengkap setiap penilaian termasuk:
- Score total dan breakdown per aspek
- Verdict yang benar
- Analisis penggunaan keyword
- Feedback detail

## 🛠️ Teknologi

- **Python 3.x**
- **Google Generative AI (Gemini 2.5 Flash)** - Model AI untuk penilaian
- **python-dotenv** - Manajemen environment variables

## ⚙️ Fungsi Utama

### `grade(payload: dict) -> dict`

Menilai satu jawaban mahasiswa berdasarkan payload yang berisi:
- Masalah, penyebab, solusi
- Keywords dan definisi
- Verdict dan reasoning mahasiswa

**Return:** Dictionary berisi score, breakdown, correct_verdict, keyword_usage, dan feedback.

### `grade_all_students() -> list`

Menilai semua jawaban dari semua mahasiswa secara otomatis.

**Return:** List berisi hasil penilaian semua mahasiswa.

## 📝 Catatan

- Model AI yang digunakan: `gemini-2.5-flash`
- Response format: JSON structured output
- Encoding file: UTF-8 untuk mendukung karakter Indonesia
- Sistem mendukung dua format key untuk jawaban: `"answer"` atau `"student_answer"`

## 🔒 Keamanan

- **Jangan commit file `.env`** ke repository
- API key bersifat rahasia dan personal
- Gunakan `.env-copy` sebagai template tanpa API key asli