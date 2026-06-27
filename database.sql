-- Active: 1782467939925@@gateway01.ap-southeast-1.prod.aws.tidbcloud.com@4000
USE test;

CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS profil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    judul_profesi VARCHAR(100),
    deskripsi TEXT,
    foto_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_skill VARCHAR(50) NOT NULL,
    tingkat_keahlian VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS experience (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perusahaan VARCHAR(100) NOT NULL,
    posisi VARCHAR(100) NOT NULL,
    tahun VARCHAR(50),
    deskripsi TEXT
);

CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_proyek VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    link_proyek VARCHAR(255),
    gambar_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pengirim VARCHAR(100) NOT NULL,
    email_pengirim VARCHAR(100) NOT NULL,
    isi_pesan TEXT NOT NULL,
    tanggal_kirim TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);