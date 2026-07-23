![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-In%20Development-orange)
![Version](https://img.shields.io/badge/version-v0.3-blue)

# 🇮🇩 Indo Programming Language

Bahasa pemrograman sederhana dengan sintaks bergaya Bahasa Indonesia.

Proyek ini dibuat sebagai sarana belajar membangun **lexer**, **parser**, dan **interpreter** dari nol menggunakan Python.

> 🇬🇧 This project is primarily documented in Indonesian because the language itself is designed around Indonesian syntax.

> 🚧 **Masih dalam tahap pengembangan.**  
> Sintaks dan fitur dapat berubah sewaktu-waktu.

---

## 📝 Contoh

```python
>> 25 + 6 * 15 : 2 - 3
((INT:25, PLUS, ((INT:6, MUL, INT:15), DIV, INT:2)), MINUS, INT:3)

>> 20 : (-5 - (-10))
(INT:20, DIV, ((MINUS INT:5), MINUS, (MINUS INT:10)))
```

---

## 📸 Screenshot

### v0.1

<p align="center">
  <img src="assets/interpreter_v0.1.jpg" width="400">
</p>

### v0.2

<p align="center">
  <img src="assets/interpreter_v0.2.jpg">
</p>

---

## 📋 Persyaratan

- Python 3.11 atau lebih baru

---

## ⚙️ Instalasi

```bash
git clone https://github.com/Idhmoneys/IDlang.git
cd IDlang
python main.py
```

---

## ✨ Fitur

Saat ini Indo sudah memiliki:

- REPL interaktif
- Lexer
- Parser
- Operasi aritmatika
- Unary operator
- Prioritas operator
- Tanda kurung
- Runtime Error
- Context

---

## 📈 Progress

> ℹ️ v0.3 merupakan hasil penulisan ulang (rewrite) dari proyek sebelumnya.
> Beberapa fitur yang ada di v0.2 kebawah sedang dibangun ulang dengan implementasi yang lebih rapi dan tanpa bergantung pada tutorial.

### v0.1

- Lexer
- Parser
- Unary operator
- Operasi aritmatika dasar

### v0.2

- Refactor lexer
- Refactor parser
- Runtime Error
- Context
- Operator perpangkatan (^)

### v0.3 (sedang dikerjakan)

- AST
- Interpreter

---

## 🛣️ Roadmap

- [x] Lexer
- [x] Parser
- [ ] AST
- [ ] Interpreter
- [ ] Variables
- [ ] String
- [ ] Boolean
- [ ] If Statement
- [ ] Loop
- [ ] Function
- [ ] Lists
- [ ] Dictionary
- [ ] Module
- [ ] Standard Library
- [ ] Error Traceback

---

## 🤷 Kenapa membuat Indo?

Awalnya proyek ini dibuat sebagai media belajar membuat bahasa pemrograman.

Namun seiring berjalannya waktu, proyek ini berkembang menjadi eksperimen untuk membuat bahasa pemrograman yang terasa lebih natural bagi penutur Bahasa Indonesia.

---

## 📦 Project Info

**Nama**
IDlang (Indo Programming Language)

**Dibuat oleh**
[Idhm](https://github.com/Idhmoneys)

**Dibuat menggunakan**
Python

**Dimulai pada**
19 Juli 2026

---

## License

MIT