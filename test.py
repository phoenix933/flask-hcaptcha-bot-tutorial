import asyncio
from pyppeteer import launch
from capsolver_api import HCaptchaTask
from proxy import proxy
import random
import json
import os
import sys


async def main():
    capsolver = HCaptchaTask("CAP-6BF20141323EA1AEB3AF105272AE089A")

    task_id = capsolver.create_task(
        task_type="HCaptchaTaskProxyLess",  # HCaptchaTask
        website_url="https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp",
        website_key="af4fc5a3-1ac5-4e6d-819d-324d412a5e9d",
        is_invisible=True,
        cookies=[
            {"name": c.split("=")[0], "value": c.split("=")[1]}
            for c in "".split("; ")
        ],
        # proxy= proxy_chosen
    )
    captcha_key = None
    while True:
        solution = capsolver.get_solution(task_id)
        if solution:
            captcha_key = solution["gRecaptchaResponse"]
            print(captcha_key)
            break
        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    # asyncio.get_event_loop().run_until_complete(save_text_as_txt(f'{token}.json',"HERE"))
