# XOR Akış Şifreleme Web Uygulaması

Bu proje, metinleri XOR akış şifreleme (XOR stream cipher) yöntemiyle şifrelemek ve şifresini çözmek için geliştirilmiş basit bir web uygulamasıdır. Kullanıcı dostu bir arayüze sahiptir ve şifreleme sürecinin adımlarını görsel olarak gösterir.

## Ekran Görüntüleri

![Uygulama Ana Ekranı](static/img/image1.png)
*Uygulamanın ana arayüzü ve karanlık tema.*

![Şifreleme Adımları](static/img/image2.png)
*Encrypt butonuna basıldığında işlemin adım adım gösterilmesi.*

## Projenin Mantığı

XOR akış şifreleme, en basit ve hızlı simetrik şifreleme algoritmalarından biridir. Simetrik olması, aynı anahtarın hem şifreleme hem de şifre çözme için kullanıldığı anlamına gelir.

Uygulama şu adımları izler:

1.  **Anahtar Akışı Üretimi:** Kullanıcının girdiği sayısal bir **"seed" (tohum)** değeri, bir sözde rastgele sayı üretecini başlatmak için kullanılır. Bu üreteç, şifrelenecek metinle aynı uzunlukta olan ve "anahtar akışı" olarak adlandırılan bir byte dizisi oluşturur.
    > **Neden Seed?** Aynı "seed" değeri her zaman birebir aynı rastgele sayı dizisini üretir. Bu özellik, şifreli metni çözmek isteyen kişinin de aynı anahtar akışını üretebilmesini sağlar. Bu yüzden "seed", iki taraf arasında paylaşılan gizli anahtar görevi görür.

2.  **Byte'a Dönüştürme:** Şifrelenecek metin, standart bir format olan UTF-8 kullanılarak byte dizisine dönüştürülür.

3.  **XOR İşlemi:** Metnin her bir byte'ı, anahtar akışındaki karşılık gelen byte ile **XOR (özel veya)** mantıksal işlemine tabi tutulur.
    > XOR işleminin en önemli özelliği, tersine çevrilebilir olmasıdır: `(Metin XOR Anahtar) XOR Anahtar = Metin`. Bu sayede, şifreli metne aynı anahtarla tekrar XOR uygulandığında orijinal metin elde edilir.

4.  **Base64 Kodlama:** XOR işlemi sonucunda ortaya çıkan şifreli veri, her zaman yazdırılabilir karakterlerden oluşmayabilir. Bu yüzden sonuç, internet üzerinden güvenle aktarılabilen bir metin formatı olan **Base64**'e dönüştürülür. Şifre çözme işleminde bu süreç tersten işler.

## Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler

*   [Python 3.6+](https://www.python.org/downloads/)
*   pip (Python paket yöneticisi)

### Adımlar

1.  **Projeyi Klonlayın (veya ZIP olarak indirin):**
    ```bash
    git clone https://github.com/mertucan/XOR-Stream-Cipher.git
    cd XOR-Stream-Cipher
    ```

2.  **Sanal Ortam Oluşturun (Önerilir):**
    Projeye özel bir sanal ortam oluşturmak, bağımlılıkların sisteminizdeki diğer projelerle karışmasını engeller.
    ```bash
    python -m venv venv
    ```

3.  **Sanal Ortamı Aktif Edin:**
    *   **Windows:**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    *   **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Gerekli Kütüphaneleri Yükleyin:**
    Projenin tek bağımlılığı olan Flask'i yükleyin.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Web Sunucusunu Başlatın:**
    Aşağıdaki komut ile Flask geliştirme sunucusunu başlatın.
    ```bash
    python app.py
    ```

6.  **Uygulamayı Açın:**
    Terminalde `* Running on http://127.0.0.1:5000` gibi bir çıktı göreceksiniz. Bu adresi kopyalayıp web tarayıcınıza yapıştırarak uygulamayı açabilirsiniz.

Artık uygulamayı kullanmaya hazırsınız!
