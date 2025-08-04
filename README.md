# 👁️ KodGozu - Python SAST Aracı

Python ile geliştirilmiş, AST (Abstract Syntax Tree) tabanlı, yapılandırılabilir ve genişletilebilir bir Güvenlik Odaklı Statik Kod Analiz Aracı.

![KodGozu Terminal Arayüzü](https://github.com/user-attachments/assets/19e34279-3382-4f32-849c-a87f55c82662)

---

### 🇹🇷 Türkçe

KodGozu, Python kaynak kodlarını analiz ederek yaygın güvenlik zafiyetlerini ve riskli kod kalıplarını tespit etmek için tasarlanmıştır. Yalnızca metin taraması yapmak yerine, kodun anlamsal yapısını (AST) analiz ederek daha doğru ve bağlama duyarlı sonuçlar üretir.

### 🚀 Özellikler

* **AST Tabanlı Analiz:** Kodun anlamsal ve yapısal bütünlüğünü anlayarak analiz yapar, bu da yanlış pozitif (false positive) oranını düşürür ve daha isabetli sonuçlar sağlar.
* **Modüler Kural Motoru:** Her bir güvenlik kuralı kendi bağımsız sınıfı olarak tasarlanmıştır. Bu sayede yeni zafiyet kuralları eklemek veya mevcutları değiştirmek son derece kolaydır.
* **Dışarıdan Yapılandırma:** Hangi kuralların aktif olacağı, proje kök dizinindeki `.kodgozu.yml` dosyası üzerinden kolayca yönetilebilir. Bu, her proje için farklı tarama profilleri oluşturmaya olanak tanır.
* **Gelişmiş Kural Seti:** `shell=True` gibi tehlikeli fonksiyon kullanımlarından, güvensiz deserialization'a ve hard-coded (sabit kodlanmış) gizli bilgilere kadar çeşitli zafiyetleri tespit edebilir.
* **Esnek Çıktı Formatları:** Tarama sonuçlarını hem insan tarafından okunabilir standart metin formatında hem de otomasyon sistemleri için ideal olan JSON formatında sunar.

### 🛠️ Kullanılan Teknolojiler

* **Backend:** Python 3.8+
* **Kod Analizi:** `ast` (Python Standard Library)
* **Konfigürasyon:** PyYAML (`.yml` dosyaları için)
* **CLI Arayüzü:** `argparse` (Python Standard Library)
* **Paketleme:** PyInstaller

### ⚙️ Kurulum ve Çalıştırma

**Gereksinimler**
1.  **Python 3.8+**: [Python'un resmi sitesinden](https://www.python.org/downloads/) indirip kurun ve `PATH`'e eklediğinizden emin olun.

**Adımlar**
1.  Bu depoyu klonlayın veya dosyaları ZIP olarak indirin.
    ```bash
    git clone [https://github.com/senin-kullanici-adin/KodGozu-SAST-Tool.git](https://github.com/senin-kullanici-adin/KodGozu-SAST-Tool.git)
    ```
2.  Terminali açıp projenin ana klasörüne gidin ve gerekli Python kütüphanesini yükleyin.
    ```bash
    pip install PyYAML
    ```
3.  Uygulamayı çalıştırmak için aşağıdaki komutları kullanın:
    ```bash
    # Belirli bir dizini taramak için
    python sast.py /path/to/your/project

    # Sonuçları JSON formatında almak için
    python sast.py /path/to/your/project -o json
    ```
    Windows kullanıcıları, `scan.bat` dosyasını argümanlarla birlikte de kullanabilir:
    ```bash
    scan.bat C:\Users\Kullanici\Desktop\projem
    ```

### 📦 .EXE Haline Getirme

Projenin kaynak kodunu, Python veya kütüphaneleri kurulu olmayan herhangi bir Windows bilgisayarında çalışacak tek bir `.exe` dosyasına dönüştürmek için:

1.  **PyInstaller'ı yükleyin:**
    ```bash
    pip install pyinstaller
    ```
2.  Proje ana klasöründe bir terminal açın ve aşağıdaki komutu çalıştırın:
    ```bash
    pyinstaller --noconfirm --onefile --console sast.py
    ```
    * `--onefile`: Tüm bağımlılıkları tek bir çalıştırılabilir dosyada birleştirir.
    * `--console`: Bu bir komut satırı aracı olduğu için bu gereklidir.
3.  Oluşturulan `.exe` dosyası `dist` klasörünün içinde yer alacaktır.

### ⚠️ Etik Kullanım Uyarısı

Bu araç, yazılım güvenliği eğitimi ve geliştiricilerin kendi kodlarını denetlemesi amacıyla oluşturulmuştur. Bu aracın ürettiği bulgular, potansiyel riskleri işaret eder ve her zaman bir uzman tarafından doğrulanmalıdır. Bu araç, size ait olmayan veya analiz etme izninizin bulunmadığı kodlar üzerinde kullanılmamalıdır.

---

### 🇬🇧 English

KodGozu is designed to analyze Python source code to detect common security vulnerabilities and risky code patterns. Instead of just performing text-based searches, it analyzes the code's semantic structure (AST) to produce more accurate and context-aware results.

### 🚀 Features

* **AST-Based Analysis:** Analyzes the semantic and structural integrity of the code, which reduces the false-positive rate and provides more precise findings.
* **Modular Rule Engine:** Each security rule is designed as an independent class, making it extremely easy to add new vulnerability rules or modify existing ones.
* **External Configuration:** Users can easily manage which rules are active through the `.kodgozu.yml` file in the project's root directory, allowing for different scanning profiles for each project.
* **Advanced Rule Set:** Capable of detecting a variety of vulnerabilities, from dangerous function usage like `shell=True` to insecure deserialization and hard-coded secrets.
* **Flexible Output Formats:** Presents scan results in both human-readable standard text format and machine-readable JSON format, ideal for automation systems.

### 🛠️ Tech Stack

* **Backend:** Python 3.8+
* **Code Analysis:** `ast` (Python Standard Library)
* **Configuration:** PyYAML (for `.yml` files)
* **CLI Interface:** `argparse` (Python Standard Library)
* **Packaging:** PyInstaller

### ⚙️ Setup and Run

**Prerequisites**
1.  **Python 3.8+**: Download and install from the [official Python website](https://www.python.org/downloads/), ensuring it's added to your `PATH`.

**Steps**
1.  Clone this repository or download the files as a ZIP.
    ```bash
    git clone [https://github.com/your-username/KodGozu-SAST-Tool.git](https://github.com/your-username/KodGozu-SAST-Tool.git)
    ```
2.  Open a terminal, navigate to the project's root directory, and install the required Python library:
    ```bash
    pip install PyYAML
    ```
3.  Use the following commands to run the application:
    ```bash
    # To scan a specific directory
    python sast.py /path/to/your/project

    # To get the results in JSON format
    python sast.py /path/to/your/project -o json
    ```
    Windows users can also utilize the `scan.bat` helper script with arguments:
    ```bash
    scan.bat C:\Users\User\Desktop\myproject
    ```

### 📦 Packaging into .EXE

To convert the source code into a single `.exe` file that runs on any Windows machine without requiring Python or libraries to be installed:

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  Open a terminal in the project's root directory and run the following command:
    ```bash
    pyinstaller --noconfirm --onefile --console sast.py
    ```
    * `--onefile`: Bundles all dependencies into a single executable.
    * `--console`: This is necessary as it's a command-line interface tool.
3.  The generated `.exe` file will be located in the `dist` folder.

### ⚠️ Ethical Use Disclaimer

This tool was created for software security education and for developers to audit their own code. The findings produced by this tool indicate potential risks and should always be verified by an expert. This tool should not be used on code that you do not own or have permission to analyze.
