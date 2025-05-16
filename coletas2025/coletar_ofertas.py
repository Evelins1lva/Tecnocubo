import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class TecnocuboSpider:
    def __init__(self):
        # Criar a pasta de prints se não existir
        os.makedirs("prints", exist_ok=True)

        # Configura o log
        logging.basicConfig(
            filename='tecnocubo_coleta.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Spider inicializada")

        # Configura o navegador
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        self.dados = []

    def scrape(self, url="https://www.tecnocubo.com.br/ofertas"):
        logging.info(f"Acessando URL: {url}")
        self.driver.get(url)

        try:
            wait = WebDriverWait(self.driver, 10)
            produtos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product")))

            logging.info(f"{len(produtos)} produtos encontrados.")

            for i, produto in enumerate(produtos, start=1):
                try:
                    nome = produto.find_element(By.CLASS_NAME, "product-name").text.strip()
                except NoSuchElementException:
                    nome = "Nome não encontrado"
                except Exception as e:
                    logging.error(f"Erro inesperado ao capturar nome: {e}")
                    raise

                try:
                    preco = produto.find_element(By.CLASS_NAME, "current-price").text.strip()
                except NoSuchElementException:
                    preco = "Preço não encontrado"
                except Exception as e:
                    logging.error(f"Erro inesperado ao capturar preço: {e}")
                    raise

                try:
                    # Usando um seletor mais confiável para pegar a URL do produto
                    url_produto = produto.find_element(By.TAG_NAME, "a").get_attribute("href")
                except NoSuchElementException:
                    url_produto = "URL não encontrada"
                except Exception as e:
                    logging.error(f"Erro inesperado ao capturar URL: {e}")
                    raise

                nome_arquivo = f"prints/{i}.jpeg"
                produto.screenshot(nome_arquivo)

                logging.info(f"Produto {i}: {nome} | {preco} | {url_produto}")
                logging.info(f"Print salvo em {nome_arquivo}")

                self.dados.append({
                    "nome": nome,
                    "preco": preco,
                    "url": url_produto,  # Aqui estamos adicionando a URL do produto
                    "print": nome_arquivo
                })

            # Print geral da página
            self.driver.save_screenshot("pagina_ofertas.png")
            logging.info("Print geral salvo: pagina_ofertas.png")

        except Exception as e:
            logging.error(f"Erro ao processar a página: {e}")

    def salvar_dados(self):
        with open("produtos_tecnocubo.json", "w", encoding="utf-8") as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=4)
            logging.info("Dados salvos em produtos_tecnocubo.json")

    def fechar(self):
        self.driver.quit()
        logging.info("Navegador fechado")

# Execução
if __name__ == "__main__":
    spider = TecnocuboSpider()
    spider.scrape()
    spider.salvar_dados()
    spider.fechar()



