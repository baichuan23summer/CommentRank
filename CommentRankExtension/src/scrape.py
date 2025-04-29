import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
import re
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import easyocr
import browser_cookie3


# def auth(pack):
#     session, url = pack
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")

#     headers = {
#         'User-Agent': 'Mozilla/5.0',
#         # Add cookies if needed
#     }

#     def get_value(name):
#         tag = soup.find("input", {"name": name})
#         return tag["value"] if tag else ""

#     pwd = input("password: ")
#     payload = {
#         "email": get_value("email"),
#         "password": pwd,  # <-- Replace this securely
#         "appActionToken": get_value("appActionToken"),
#         "appAction": get_value("appAction"),
#         "workflowState": get_value("workflowState"),
#         "openid.return_to": get_value("openid.return_to"),
#         "prevRID": get_value("prevRID"),
#         "metadata1": get_value("metadata1"),
#         "aaToken": get_value("aaToken"),
#     }

#     session.post("https://www.amazon.com/ap/signin", data=payload, headers=headers)
#     print("Status Code:", response.status_code)
#     print("Final URL:", response.url)


# def submitCaptcha(session, pack):
#     html, text = pack
#     # session = requests.Session()
#     headers = {
#         'User-Agent': 'Mozilla/5.0',
#         # Add cookies if needed
#     }

#     soup = BeautifulSoup(html, "html.parser")
#     amzn = soup.find('input', {'name': 'amzn'})['value']
#     amzn_r = soup.find('input', {'name': 'amzn-r'})['value']

#     payload = {
#         'amzn': amzn,
#         'amzn-r': amzn_r,
#         'field-keywords': text
#     }

#     response = session.get('https://www.amazon.com/errors/validateCaptcha', params=payload, headers=headers)
    
#     # Step 6: Check result
#     print("Final URL:", response.url)
#     print("Status:", response.status_code)
#     return response.url


# def fetchRecaptcha(response):
#     html = response.content.decode('utf-8')
#     match = re.search(r'< img src="(https://images-na\.ssl-images-amazon\.com/captcha/[^"]+)"', html)

#     if match:
#         captcha_url = match.group(1)
#         print("CAPTCHA URL:", captcha_url)
#         return html, captcha_url
#     else:
#         print("CAPTCHA not found")
#         return html, None
    
# def recaptchaHandler(pack):
#     html, url = pack
#     resp = requests.get(url)
#     img = Image.open(BytesIO(resp.content)).convert('RGB')
#     img_np = np.array(img)

#     reader = easyocr.Reader(['en'])
#     results = reader.readtext(img_np)
    
#     for (bbox, text, prob) in results:
#         print(f'Text: {text}, Confidence: {prob}')
#     return html, text


# def fetch_reviews(asin, page=1):
#     # 设置请求头，模拟浏览器访问s
#     headers = {
#         "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                        "AppleWebKit/537.36 (KHTML, like Gecko) "
#                        "Chrome/90.0.4430.93 Safari/537.36")
#     }
#     # 构造评论页面的URL（美国站示例，如需其它区域请调整URL）
#     url = f"https://www.amazon.com/product-reviews/{asin}/?pageNumber={page}"
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print(f"Error: Received status code {response.status_code}")
#         return []

#     session, authUrl = submitCaptcha(recaptchaHandler(fetchRecaptcha(response)))
#     print("final url:", authUrl)
#     headers = {
#         "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                        "AppleWebKit/537.36 (KHTML, like Gecko) "
#                        "Chrome/90.0.4430.93 Safari/537.36")
#     }

#     session.headers.update(headers)
#     # auth(authUrl)

#     # 解析页面内容
#     response = requests.get(authUrl, headers=headers)
#     soup = BeautifulSoup(response.text, "html.parser")
#     review_blocks = soup.find_all("li", {"data-hook": "review"})
#     reviews = []
#     for block in review_blocks:
#         title_tag = block.find("a", {"data-hook": "review-title"})
#         rating_tag = block.find("i", {"data-hook": "review-star-rating"})
#         body_tag = block.find("span", {"data-hook": "review-body"})
#         title = title_tag.get_text(strip=True) if title_tag else ""
#         rating = rating_tag.get_text(strip=True) if rating_tag else ""
#         body = body_tag.get_text(strip=True) if body_tag else ""
#         reviews.append({
#             "标题": title,
#             "评分": rating,
#             "评论内容": body
#         })
#     return reviews

def fetch_reviews(asin, page=1):
    url = f"https://www.amazon.com/product-reviews/{asin}/?pageNumber={page}"
    
    session = requests.Session()
    session.cookies.update({
        # "ad-id":            "A7iT1bGYIkVju8MA20oXv7I",
        # "ad-privacy":       "0",
        # "am-token":         "eyJkZXZpY2VJZCI6IjEzMzM5MjMyMTY2MTkwODMyIiwiaGFzQXV0aGVudGljYXRlZCI6dHJ1ZSwicHJvZmlsZUlkIjoiIiwiZ3Vlc3RUb2tlbiI6bnVsbCwiZ3Vlc3RVYmlkIjpudWxsLCJndWVzdENvbnRleHQiOm51bGwsImhhc0NvbXBsZXRlZERhdGFUcmFuc2ZlciI6ZmFsc2V9",
        "at-main":          "Atza|IwEBIMMIXpO6zyIHhGliLkKM6S4MKyTxtnB9HrpbI4N7gzzy1VkZGODId-zgLL6bVdykqz7bEWYCl7i-_cwOV5T-a8JeQW7-Xnf0MiKYJcWldIqDTIK-5qEJ7tuMc6Ew2zcTIEHDlQR7Jh3OTbMopl0JGM0YWCJ2FYTc6ua2X2TrIoMYVJCneqGYkWQamvnLg_fVVllJXQolrK8ZsO6p0TY1tJhCrftdVt_pSeeuma70LtNsFg",
        # "csd-key":          "eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiYWNhODY0Iiwia2V5IjoiTVF4QVFuK25KS25GV2JIc01zT2QrTU83bXRMS1ozb2hweVF3dnNPbDZTY2NGV3JJa1J5RUlhN3hIdzYzd0ZOaFR5OU01UWJXNDA0VW1TbU50SXhraVFrc20wb3JRVFpnT0Z1RXV0NkUrS0kxY1dGcmFNVnBVZGF0YUkyb2xDWUJxNWdTZTZlNHErYVBmanJ6NW9WcXBiZmhtTGdRRXNmcW5ncXBvWFFJcVVHS3YxZGZwVS9zQlhnQXVCMVlXSnBNTlZiQ3V2VjZEbUhWUkZLaUtvQWpHOStscmtKUldYSnZNY0FEbzlLSEF0ajFpS2ZLcHdjTXBMbGxsVFVodVdBNVo5dEoxWmlNVzd0T1pTRkNKUFh2TlN4S0ZHUnNndHJvb25wamE2dENtcDVkbW9tT1FabXJpbVRjM3c1TGxuUHF0Y0p6U2wwc202SkwwTnZUaDI0eEpBPT0ifQ==",
        "csm-hit":          "tb:KTRCEGXACW70GFX1Q79D+s-BF56MYDD7HKGCQ7BCVJP|1745794593730&t:1745794593730&adb:adblk_yes",
        # "csm-sid":          "",
        "i18n-prefs":       "USD",
        "id_pk":            "eyJuIjoiMSIsImFmIjoiMSJ9",
        "id_pkel":          "n1",
        "lc-main":          "en_US",
        "rxc": "AKcIs7DDgQpbOuBeOdI",
        "sess-at-main":     "\"OJwSjQFpjfw7oWpBhZIl9D5i1Vv+FjSvpfqETeQmsOQ=\"",
        "session-id":       "138-1032512-3474622",
        # "session-id-apay":  "134-6628320-8847659",
        "session-id-time":  "2082787201l",
        "session-token":    "\"S5LDXXj0Cfj0wGfNQNL+h27iJyRJ+J+9XAIg9bsQMGNh2rj2/x3m/hC80btgHWoEcgndc3WDMocOY9xAoLGBiaFcx3W2vCy2hwqmdszCU5qcnpCLStmdqQkp6Z1zgUnF4CyQJpzpoGq2NrZdWP6dHiQl/TRubcKoXKrUSf4XSmC5bbo9sId8fMe60uAku9UMQrkaHrgadrU0bwgT4z7SJRQFYJDHRwQeEaFjB07AgqpQ7a2yKOnDD8DspAKlJ+Tc+gvrNwseJier0ddTHlYvTy81m38CbF3Fenwmma+zgSpjkBX49YiMqNIp/ifB14eG/qirmgzfG7Mf7tRzd7BHJOc52bGRF714NR3jrlbByKsJukbtiKYc2Q==\"",
        "sst-main":         "Sst1|PQG_jhe1r5ZrYKtkke2zN2EUCS-QaJpVlHpiBQ0nilTuI884953XUaJKsi9vo71sx1YMdrPmkwPJjszlT6_9A6BImRPLnX3IB_my1tLJuh888N2mTQNSnOCzTdH09GRuPtPsao3Zq49R4FkxbuYLb2QDxjTdTq6lIChdvFl56WiSo66LhiKh_QIi8hAy4oVRPbakv-bF5WOP3DwjKhTE9yax3_4xzaPLR0Tqd8RaIfj6LuD8aAyIyEjSXJV6qPrPoQMjpsfmEfFI_OXjJs-3fV6M0cAAZclODHqVRmrQCnRh7TU",
        "ubid-main":        "132-8078235-1765222",
        "x-main":           "\"9eF@yR9sMtAK1CbSbMg3xAj?JjsJs8gohby1LNLN8Tb6chpOVJ@qXm2s@HTZJYPa\"",
        
    })
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.amazon.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }
    session.headers.update(headers)

    # Step 1: Load the initial reviews page (possibly hits CAPTCHA)
    response = session.get(url)

    if response.status_code != 200:
        print(f"[Error] Status code: {response.status_code}")
        return []

    # Step 2: Check if CAPTCHA page is shown
    # if "captcha" in response.text.lower():
    #     print("[Info] CAPTCHA detected, trying to solve...")

    #     # Step 3: Solve CAPTCHA
    #     # Assume fetchRecaptcha, recaptchaHandler, submitCaptcha are implemented
    #     recaptcha_image = fetchRecaptcha(response)
    #     ocr_result = recaptchaHandler(recaptcha_image)
    #     authUrl = submitCaptcha(session, ocr_result)

    #     # Step 4: Visit the auth URL (with same session)
    #     print("final url:", authUrl)
    #     response = session.get(authUrl)
    
    # Step 5: Parse reviews
    soup = BeautifulSoup(response.text, "html.parser")
    review_blocks = soup.find_all("li", {"data-hook": "review"})
    reviews = []

    for block in review_blocks:
        title_tag = block.find("a", {"data-hook": "review-title"})
        rating_tag = block.find("i", {"data-hook": "review-star-rating"})
        body_tag = block.find("span", {"data-hook": "review-body"})

        title = title_tag.get_text(strip=True) if title_tag else ""
        rating = rating_tag.get_text(strip=True) if rating_tag else ""
        body = body_tag.get_text(strip=True) if body_tag else ""

        reviews.append({
            "标题": title,
            "评分": rating,
            "评论内容": body
        })

    return reviews


def main():
    asin = "B00B42NQC2"  # 替换为目标产品的 ASIN

    all_reviews = []
    current_page = 1
    while True:
        print(f"正在抓取第 {current_page} 页评论...")
        reviews = fetch_reviews(asin, current_page)
        if not reviews:
            print("没有更多评论或发生错误。")
            break

        all_reviews.extend(reviews)
        current_page += 1
        # 随机延时 2~5 秒，防止请求过快
        time.sleep(random.uniform(2, 5))

    # 将抓取到的数据存储到 Excel 文件中
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        # 保存为 Excel 文件，需要安装 openpyxl 或 xlsxwriter（pip install openpyxl）
        df.to_csv("amazon_reviews.csv", index=False)
        print("评论已保存到 amazon_reviews.csv")
    else:
        print("未抓取到任何评论数据。")


if __name__ == "__main__":
    main()