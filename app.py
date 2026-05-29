import streamlit as st
import google.generativeai as genai
from PIL import Image

# =====================================================================
# 1. KONFIGURASI AI (API KEY SUDAH DIMASUKKAN)
# =====================================================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Mengatur konfigurasi halaman utama aplikasi (Tampilan HP & Desktop)
st.set_page_config(page_title="AgriCheck & Konsultasi AI", page_icon="🌱", layout="centered")

# =====================================================================
# 2. MENU NAVIGASI SIDEBAR
# =====================================================================
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/sprout.png", width=100)
    st.title("Menu Utama")
    pilihan_menu = st.radio(
        "Pilih Layanan AI:",
        ["📸 Deteksi Penyakit Tanaman", "💬 Konsultasi Budidaya & Perawatan"]
    )
    st.markdown("---")
    st.caption("AgriCheck AI v2.0 - Asisten Digital Petani Cerdas")

# =====================================================================
# FITUR 1: DETEKSI PENYAKIT TANAMAN
# =====================================================================
if pilihan_menu == "📸 Deteksi Penyakit Tanaman":
    st.title("🌱 AgriCheck AI: Dokter Tanaman")
    st.write("Ambil foto daun atau bagian tanaman yang sakit menggunakan kamera HP Anda untuk mendeteksi penyakit secara instan.")

    tab1, tab2 = st.tabs(["📸 Ambil Foto Kamera", "📁 Unggah dari Galeri"])
    foto_daun = None

    with tab1:
        foto_kamera = st.camera_input("Arahkan kamera ke daun yang sakit")
        if foto_kamera:
            foto_daun = foto_kamera

    with tab2:
        foto_galeri = st.file_uploader("Pilih foto tanaman dari galeri HP", type=["jpg", "jpeg", "png"])
        if foto_galeri:
            foto_daun = foto_galeri

    if foto_daun is not None:
        img = Image.open(foto_daun)
        st.image(img, caption="Foto Tanaman Berhasil Dimuat", use_container_width=True)
        
        if st.button("🔍 Analisis Penyakit Sekarang"):
            with st.spinner("Dokter AI sedang menganalisis gejala pada daun... Mohon tunggu..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt_instruksi = """
                    Bertindaklah sebagai Ahli Agronomi dan Patologi Tanaman berpengalaman. 
                    Analisis gambar tanaman yang sakit ini dengan sangat teliti dan berikan laporan dalam Bahasa Indonesia dengan format berikut:
                    
                    ### 📊 Hasil Identifikasi
                    * **Nama Tanaman:** (Sebutkan jenis tanamannya)
                    * **Kemungkinan Penyakit/Hama:** (Sebutkan nama penyakitnya)
                    * **Tingkat Keparahan:** (Perkiraan Ringan/Sedang/Parah)
                    
                    ### 🔬 Gejala yang Terlihat
                    (Jelaskan bercak, warna, atau pola apa yang terlihat pada gambar)
                    
                    ### 🛠️ Langkah Penanganan Ringkas
                    1. **Tindakan Darurat:** (Potong bagian sakit, isolasi, dll)
                    2. **Solusi Organik/Alami:** (Cara ramah lingkungan)
                    3. **Solusi Kimia (Jika terpaksa):** (Kandungan fungisida/pestisida yang tepat)
                    """
                    respon = model.generate_content([prompt_instruksi, img])
                    st.success("✅ Analisis Selesai!")
                    st.markdown("---")
                    st.markdown(respon.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}. Pastikan API Key Anda valid.")

# =====================================================================
# FITUR 2: KONSULTASI BUDIDAYA
# =====================================================================
elif pilihan_menu == "💬 Konsultasi Budidaya & Perawatan":
    st.title("💬 Konsultan Pertanian AI")
    st.write("Dapatkan panduan lengkap mulai dari pengolahan tanah, pemupukan, obat-obatan, hingga penanganan hasil panen.")

    st.subheader("📋 Informasi Tanaman Anda")
    
    jenis_tanaman = st.text_input("Nama Tanaman (contoh: Cabai Rawit, Tomat, Padi, Jagung):", placeholder="Ketik nama tanaman di sini...")
    
    topik_konsultasi = st.selectbox(
        "Tahapan apa yang ingin Anda tanyakan?",
        [
            "Semua Tahapan (Panduan Lengkap)",
            "🏗️ Proses Awal & Pengolahan Tanah",
            "🧪 Pola Pemupukan (Fase Vegetatif & Generatif)",
            "💊 Rekomendasi Obat-Obatan & Pencegahan Hama",
            "🌾 Manajemen Hasil Panen & Pascapanen"
        ]
    )
    
    pertanyaan_spesifik = st.text_area(
        "Pertanyaan spesifik atau kendala Anda (Opsional):",
        placeholder="Contoh: Tanah saya agak asam, atau bagaimana cara menyimpan hasil panen agar tidak cepat busuk?"
    )

    if st.button("🚀 Mulai Konsultasi AI"):
        if not jenis_tanaman:
            st.warning("⚠️ Silakan isi nama tanaman terlebih dahulu agar AI bisa memberikan jawaban yang spesifik!")
        else:
            with st.spinner(f"Mengumpulkan data panduan terbaik untuk budidaya {jenis_tanaman}..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt_konsultasi = f"""
                    Anda adalah Konsultan Pertanian Ahli dan Penyuluh Lapangan Kementerian Pertanian terkemuka.
                    Berikan panduan profesional, praktis, dan mudah dipahami oleh petani lokal di Indonesia mengenai tanaman: **{jenis_tanaman}**.
                    
                    Fokus pembahasan yang diminta pengguna adalah: **{topik_konsultasi}**.
                    Pertanyaan atau kendala tambahan dari petani: "{pertanyaan_spesifik if pertanyaan_spesifik else 'Tidak ada'}"
                    
                    Jika pengguna memilih 'Semua Tahapan', struktur jawaban Anda WAJIB memuat 4 poin utama di bawah ini. Jika pengguna memilih poin spesifik, perdalam poin tersebut namun tetap singgung poin lainnya secara ringkas:
                    
                    1. 🏗️ **PROSES AWAL & PENGOLAHAN TANAH:**
                       * Cara penggemburan, kebutuhan bajak/cangkul.
                       * Pengaturan pH tanah yang ideal untuk tanaman ini dan pemberian kapur dolomit jika diperlukan.
                       * Pembuatan bedengan dan penggunaan mulsa (jika relevan).
                    
                    2. 🧪 **POLA PEMUPUKAN:**
                       * Pupuk dasar saat olah tanah (organik/kandang).
                       * Pupuk susulan fase Vegetatif (pertumbuhan daun/batang) beserta dosis atau jenisnya (misal: NPK, Urea).
                       * Pupuk susulan fase Generatif (pembungaan/pembuahan) beserta jenisnya (misal: KCl, Gandasil B).
                    
                    3. 💊 **OBAT-OBATAN & PENCEGAHAN HAMA:**
                       * Hama dan penyakit utama yang sering menyerang tanaman ini.
                       * Cara pencegahan dini.
                       * Rekomendasi obat pestisida/fungisida organik (alami) maupun kimia beserta waktu penyemprotan yang tepat.
                    
                    4. 🌾 **MANAJEMEN HASIL PANEN & PASCAPANEN:**
                       * Ciri-ciri fisik tanaman siap panen (usia panen dan penampakan buah/daun).
                       * Waktu dan cara pemetikan/pemanenan yang benar agar tanaman tidak rusak.
                       * Tips penanganan pascapanen agar hasil panen tahan lama, segar, dan punya nilai jual tinggi di pasar.
                    
                    Gunakan gaya bahasa yang ramah, menyemangati, edukatif, dan gunakan format Markdown (bullet points, bold text) agar nyaman dibaca di layar HP petani.
                    """
                    
                    respon = model.generate_content(prompt_konsultasi)
                    
                    st.success("✅ Dokumen Panduan Konsultasi Berhasil Dibuat!")
                    st.markdown("---")
                    st.markdown(respon.text)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}. Periksa koneksi atau API Key Anda.")
