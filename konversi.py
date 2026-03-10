import cv2
import numpy as np
import sys

# 1. LOAD IMAGE
img = cv2.imread('face.jpg')

def nothing(x):
    # Fungsi callback kosong untuk trackbar
    pass

def main():
    if img is None:
        print("❌ File gooo.jpg tidak ditemukan!")
        return

    # Inisialisasi Jendela
    title_window = "PCD INTERACTIVE - RENDI"
    cv2.namedWindow(title_window, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    
    # 2. MEMBUAT TRACKBAR
    # Parameter: Nama, Nama Jendela, Nilai Awal, Nilai Maks, Fungsi Callback
    cv2.createTrackbar('Threshold Value', title_window, 127, 255, nothing)

    print("🚀 Sistem Aktif!")
    print("👉 Geser Slider untuk mengubah Binarisasi.")
    print("👉 Tekan 'q' untuk keluar.")

    while True:
        # Ambil nilai terbaru dari trackbar
        thresh_val = cv2.getTrackbarPos('Threshold Value', title_window)

        # A. PROSES KONVERSI
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # B. BINARISASI DENGAN NILAI DARI SLIDER
        _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)

        # C. PENGGABUNGAN OUTPUT (LAYOUTING)
        # Kita perkecil sedikit agar bisa ditampilkan dalam satu jendela besar
        h, w = img.shape[:2]
        r = 400.0 / w
        dim = (400, int(h * r))

        res_bgr = cv2.resize(img, dim)
        res_gray = cv2.resize(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), dim)
        res_hsv = cv2.resize(hsv, dim)
        res_binary = cv2.resize(cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR), dim)

        # Gabungkan gambar (Top: BGR & Gray, Bottom: HSV & Binary)
        top_row = np.hstack((res_bgr, res_gray))
        bottom_row = np.hstack((res_hsv, res_binary))
        combined = np.vstack((top_row, bottom_row))

        # Tambahkan teks panduan pada layar
        cv2.putText(combined, f"Threshold: {thresh_val}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow(title_window, combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()