import ast
import os
import argparse
import yaml
import json
import re
import math
from collections import Counter

# --- KURAL TANIMLARI ---

class BaseRule:
    def check(self, node):
        return None

class SubprocessShellTrueRule(BaseRule):
    def check(self, node):
        if not isinstance(node, ast.Call):
            return None
        
        is_subprocess_call = False
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == 'subprocess' and node.func.attr in ['run', 'call', 'check_output', 'Popen']:
                is_subprocess_call = True

        if is_subprocess_call:
            for keyword in node.keywords:
                if keyword.arg == 'shell' and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    return {
                        "line": node.lineno,
                        "type": "KOMUT ENJEKSİYONU RİSKİ",
                        "code": ast.unparse(node).strip(),
                        "message": "'subprocess' modülü 'shell=True' ile kullanılmış. Bu parametre, kullanıcıdan gelen girdilerle birleştiğinde ciddi güvenlik zafiyetlerine yol açabilir."
                    }
        return None

class PickleLoadRule(BaseRule):
    def check(self, node):
        if not isinstance(node, ast.Call):
            return None

        is_pickle_load = False
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == 'pickle' and node.func.attr in ['load', 'loads']:
                is_pickle_load = True
        
        if is_pickle_load:
            return {
                "line": node.lineno,
                "type": "GÜVENSİZ DESERIALIZATION",
                "code": ast.unparse(node).strip(),
                "message": "'pickle.load' veya 'pickle.loads' kullanımı tehlikelidir. Güvenilmeyen bir kaynaktan gelen veri, rastgele kod çalıştırılmasına neden olabilir."
            }
        return None

class HardcodedSecretRule(BaseRule):
    def _shannon_entropy(self, data):
        if not data:
            return 0
        entropy = 0
        for char in set(data):
            p_x = float(data.count(char)) / len(data)
            entropy += - p_x * math.log2(p_x)
        return entropy

    def check(self, node):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Constant) or not isinstance(node.value.value, str):
            return None

        secret_regex = re.compile(r'(key|secret|password|token|auth)', re.IGNORECASE)
        target_variable = ""

        for target in node.targets:
            if isinstance(target, ast.Name):
                target_variable = target.id

        if secret_regex.search(target_variable):
            string_value = node.value.value
            entropy = self._shannon_entropy(string_value)
            
            # Yüksek entropili (rastgele görünen) veya yeterince uzun string'ler şüphelidir.
            if entropy > 3.5 or len(string_value) > 12:
                return {
                    "line": node.lineno,
                    "type": "HARD-CODED SIR (GİZLİ BİLGİ)",
                    "code": ast.unparse(node).strip(),
                    "message": f"'{target_variable}' değişkenine atanmış, potansiyel olarak hassas bir bilgi bulundu. Entropi: {entropy:.2f}"
                }
        return None


# --- TARAYICI MOTORU ---

class SecurityScanner:
    def __init__(self, rules):
        self.rules = rules
        self.vulnerabilities = []
        self.current_file = ""

    def check_file(self, path):
        self.current_file = path
        file_vulnerabilities = []
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            try:
                tree = ast.parse(content, filename=path)
                for node in ast.walk(tree):
                    for rule in self.rules:
                        result = rule.check(node)
                        if result:
                            result['file'] = self.current_file
                            file_vulnerabilities.append(result)
            except SyntaxError as e:
                print(f"[HATA] Syntax hatası: {path}: {e}")
        return file_vulnerabilities


# --- ANA ÇALIŞTIRMA MANTIĞI ---

def get_active_rules_from_config(config_path=".kodgozu.yml"):
    if not os.path.exists(config_path):
        return [SubprocessShellTrueRule(), PickleLoadRule(), HardcodedSecretRule()]

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    active_rules = []
    rule_definitions = {
        "SubprocessShellTrueRule": SubprocessShellTrueRule,
        "PickleLoadRule": PickleLoadRule,
        "HardcodedSecretRule": HardcodedSecretRule
    }

    for rule_name, settings in config.get('rules', {}).items():
        if settings.get('enabled', False) and rule_name in rule_definitions:
            active_rules.append(rule_definitions[rule_name]())
    
    return active_rules

def main():
    parser = argparse.ArgumentParser(description="KodGözü - Python için Güvenlik Odaklı Statik Kod Analizcisi.")
    parser.add_argument("target_path", help="Taranacak dosya veya dizin yolu.")
    parser.add_argument("-o", "--output", help="Çıktı formatı (text, json).", default="text")
    args = parser.parse_args()
    
    active_rules = get_active_rules_from_config()
    if not active_rules:
        print("[BİLGİ] Konfigürasyon dosyasında aktif kural bulunamadı. Çıkılıyor.")
        return
        
    scanner = SecurityScanner(active_rules)
    all_vulnerabilities = []
    files_to_scan = []

    target_path = args.target_path
    if not os.path.exists(target_path):
        print(f"[HATA] Belirtilen yol bulunamadı: {target_path}")
        return

    if os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(".py"):
                    files_to_scan.append(os.path.join(root, file))
    elif os.path.isfile(target_path):
        if target_path.endswith(".py"):
            files_to_scan.append(target_path)
    
    print(f"--- KodGözü SAST Tarayıcı V1.0 ---")
    print(f"Aktif Kurallar: {[rule.__class__.__name__ for rule in active_rules]}")
    print(f"{len(files_to_scan)} dosya taranacak...\n")

    for filepath in files_to_scan:
        vulnerabilities = scanner.check_file(filepath)
        if vulnerabilities:
            all_vulnerabilities.extend(vulnerabilities)

    if args.output == 'json':
        print(json.dumps(all_vulnerabilities, indent=2))
    else: # text formatı
        if not all_vulnerabilities:
            print("\n[BİLGİ] Tarama tamamlandı. Yüksek riskli bir kalıp bulunamadı.")
        else:
            print(f"\n[UYARI] Tarama tamamlandı. Toplam {len(all_vulnerabilities)} potansiyel sorun tespit edildi:")
            for vuln in all_vulnerabilities:
                print("-" * 50)
                print(f"  Tip   : {vuln['type']}")
                print(f"  Dosya : {vuln['file']}")
                print(f"  Satır : {vuln['line']}")
                print(f"  Kod   : {vuln['code']}")
                print(f"  Not   : {vuln['message']}")
            print("-" * 50)

if __name__ == "__main__":
    main()