import os
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
os.makedirs("prints", exist_ok=True)

# Configuração do logging
logging.basicConfig(
    filename='tecnocubo_coleta.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info('Iniciando scraping da Tecnocubo')

# Configura o Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Acessa a página
    url = "https://www.tecnocubo.com.br/ofertas"
    driver.get(url)
    logging.info(f"Acessou a URL: {url}")

    # carregamento
    wait = WebDriverWait(driver, 10)
    produtos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product")))

    logging.info(f"Encontrados {len(produtos)} produtos")

    dados = []

    for i, produto in enumerate(produtos, start=1):
        try:
            nome = produto.find_element(By.CLASS_NAME, "product-name").text.strip()
        except:
            nome = "Nome não encontrado"

        try:
            preco = produto.find_element(By.CLASS_NAME, "current-price").text.strip()
        except:
            preco = "Preço não encontrado"

        # Salva print individual do produto
        nome_arquivo = f"prints/{i}.jpeg"
        produto.screenshot(nome_arquivo)
        logging.info(f"Print salvo: {nome_arquivo}")

        dados.append({
            "nome": nome,
            "preco": preco,
            "print": nome_arquivo
        })
        logging.info(f"Produto: {nome} - Preço: {preco}")

    # Salva um print da tela
    driver.save_screenshot("pagina_ofertas.png")
    logging.info("Print salvo: pagina_ofertas.png")

    # Salva os dados em JSON
    with open("produtos_tecnocubo.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
        logging.info("Dados salvos em produtos_tecnocubo.json")

except Exception as e:
    logging.error(f"Erro durante scraping: {e}")

finally:
    driver.quit()
    logging.info("Navegador fechado")


