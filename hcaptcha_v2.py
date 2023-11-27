import asyncio
from pyppeteer import launch
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import HcaptchaRequest, HcaptchaProxylessRequest
from proxy import proxy
import random
import json
import os
import sys

token = sys.argv[1]
cnpj = sys.argv[2]
file_path = f"data/{token}.json"

current_directory = os.getcwd()

EXTENSION_ID = "lfpfbgeoodeejmjdlfjbfjkemjlblijg"
EXTENSION_PATH = f"{current_directory}/LFPFBGEOODEEJMJDLFJBFJKEMJLBLIJG_1_3_1_0"


async def save_text_as_txt(content):
    # os.makedirs(os.path.dirname("save_datas"), exist_ok=True)
    try:
        with open(file_path, "w") as f:
            json.dump(content, f)
        # with open(file_path, "w", encoding="utf-8") as file:
        #     file.write(content)
    except:
        pass


async def main():
    limit_count = 5
    count = 0
    browser = None
    while True:
        try:
            proxy_chosen = proxy[random.randint(0, len(proxy))]
            url = "https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp"
            browser = await launch(
                options={
                    "headless": False,#True
                    "ignoreDefaultArgs": "--disable extensions",
                    "args": [
                        # "--no-sandbox",
                        # "--disable-setuid-sandbox",
                        # f"--proxy-server=http://{proxy_chosen}",
                        f"--disable-extensions-except={EXTENSION_ID}",
                        f"--load-extension={EXTENSION_PATH}",
                    ],
                }
            )
            page = await browser.newPage()
            await page.goto(url)
            element = await page.querySelector(".h-captcha[data-sitekey]")
            website_key = await page.evaluate(
                '(element) => element.getAttribute("data-sitekey")', element
            )
            
            
            
            
            
            
            capMonsterOptions = ClientOptions(
                api_key="3e79c97ba8afa9fb6bd60335e0e2b852"
            )

            task_id = HcaptchaProxylessRequest( # ! HcaptchaRequest
                websiteUrl=url,
                websiteKey=website_key,
                # proxyType="http",
                # proxyAddress="8.8.8.8",
                # proxyPort=8080,
            )

            cap_monster_client = CapMonsterClient(options=capMonsterOptions)
            
            solution = await cap_monster_client.solve_captcha(task_id)
            # print(solution)
            if solution:
                captcha_key = solution["gRecaptchaResponse"]
            
            
            
            
            
            txt_cnpj_element = await page.querySelector("input#cnpj")
            if txt_cnpj_element:
                await txt_cnpj_element.type(cnpj)
            else:
                print("txt_cnpj element not found!")

            await page.waitForSelector("iframe")
            await page.evaluate(
                "(element, captchaKey) => element.value = captchaKey",
                await page.querySelector('textarea[name="h-captcha-response"]'),
                captcha_key,
            )
            await page.waitFor(2000)
            btn = await page.querySelector('button.btn-primary[type="submit"]')
            await btn.click()
            await page.waitFor(5000)
            # titleSelector = "h1[class='documentFirstHeading']"
            # titleSelector = "h1"
            # title = await page.evaluate(
            #     "(selector) => document.querySelector(selector).textContent", titleSelector
            # )
            # # print(await page.evaluate('(btn) => btn.getAttribute("class")', await page.querySelector('h1')))
            # print(title)
            selector = "#app"  # div[id='main']
            text = await page.evaluate(
                "(selector) => document.querySelector(selector).innerHTML", selector
            )
            savedTxt = text
            await save_text_as_txt({"type": "content", "data": savedTxt})
            print(text)
            return
        except Exception as e:
            count = count + 1
            if count < limit_count:
                await save_text_as_txt(
                    {"type": "error", "data": f"{str(e)} Try again {count} time(s)."}
                )
            else:
                await save_text_as_txt({"type": "error", "data": f"{str(e)}, Failed!"})
                return
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    # asyncio.get_event_loop().run_until_complete(save_text_as_txt(f'{token}.json',"HERE"))
