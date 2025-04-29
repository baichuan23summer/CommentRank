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


def auth(pack):
    session, url = pack
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headers = {
        'User-Agent': 'Mozilla/5.0',
        # Add cookies if needed
    }

    def get_value(name):
        tag = soup.find("input", {"name": name})
        return tag["value"] if tag else ""

    pwd = input("password: ")
    payload = {
        "email": get_value("email"),
        "password": pwd,  # <-- Replace this securely
        "appActionToken": get_value("appActionToken"),
        "appAction": get_value("appAction"),
        "workflowState": get_value("workflowState"),
        "openid.return_to": get_value("openid.return_to"),
        "prevRID": get_value("prevRID"),
        "metadata1": get_value("metadata1"),
        "aaToken": get_value("aaToken"),
    }

    session.post("https://www.amazon.com/ap/signin", data=payload, headers=headers)
    print("Status Code:", response.status_code)
    print("Final URL:", response.url)


def submitCaptcha(session, pack):
    html, text = pack
    # session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0',
        # Add cookies if needed
    }

    soup = BeautifulSoup(html, "html.parser")
    amzn = soup.find('input', {'name': 'amzn'})['value']
    amzn_r = soup.find('input', {'name': 'amzn-r'})['value']

    payload = {
        'amzn': amzn,
        'amzn-r': amzn_r,
        'field-keywords': text
    }

    response = session.get('https://www.amazon.com/errors/validateCaptcha', params=payload, headers=headers)
    
    # Step 6: Check result
    print("Final URL:", response.url)
    print("Status:", response.status_code)
    return response.url


def fetchRecaptcha(response):
    html = response.content.decode('utf-8')
    match = re.search(r'< img src="(https://images-na\.ssl-images-amazon\.com/captcha/[^"]+)"', html)

    if match:
        captcha_url = match.group(1)
        print("CAPTCHA URL:", captcha_url)
        return html, captcha_url
    else:
        print("CAPTCHA not found")
        return html, None
    
def recaptchaHandler(pack):
    html, url = pack
    resp = requests.get(url)
    img = Image.open(BytesIO(resp.content)).convert('RGB')
    img_np = np.array(img)

    reader = easyocr.Reader(['en'])
    results = reader.readtext(img_np)
    
    for (bbox, text, prob) in results:
        print(f'Text: {text}, Confidence: {prob}')
    return html, text


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

def fetch_reviews(asin, cookies, page=1):
    url = f"https://www.amazon.com/product-reviews/{asin}/?pageNumber={page}"
    
    session = requests.Session()
    session.cookies.update(cookies)
    # session.cookies.update({
    #     "ad-id":            "A7iT1bGYIkVju8MA20oXv7I",
    #     "ad-privacy":       "0",
    #     # "am-token":         "",
    #     "at-main":          "Atza|IwEBIP_KA6ngHTT4KYT0SALMjBvUCtkOmD5qgJcnWqL4j-cOzo-vb4GTAFK381Wq-gqGLUzsN79qfXhGJdxf2UNeonoYJdDvYfeH6tmGkS3WEBx1GywrMuPPphjD5zlKQqG0ySYzQIsAA7b7vy9uaAYcl3do137lqJep8PJoeVw36bNpGcwxijPRYp79QP4aOe23jU74Hby5oXZEAs2t7AWGdFdEgrsQJRfq31k7aFH-XY2-yM5DbWim4ef0zbxjfy4eSEk",
    #     # "csd-key":          "",
    #     "csm-hit":          "tb:YKYVDEHPDCH7XA3KFJ44+s-9P57JXC2HRVG73EY36ZA|1743368196325&t:1743368196325&adb:adblk_no",
    #     # "csm-sid":          "",
    #     "i18n-prefs":       "USD",
    #     "lc-main":          "en_US",
    #     "sess-at-main":     "\"b2w8C64QXi0802QdBXiL5DTAsl3dfBs7bqOETE4PCBA=\"",
    #     "session-id":       "133-7155148-5289116",
    #     "session-id-time":  "2082787201l",
    #     "session-token":    "oxzfMdkwSGCLfH9nCyxCg2GJJl7DgxtO3eCr8RtB++7nrfoXBHA5pwk40IarKco6J95kWV9XZ72nWhhHuNMr1kgUnXokiWJnwmYz2IPGZda8q31k3Dqtq+t8mjbI3klYHWdpuaK2w+aqBpc4W6WMk/RjnmrdLsPR7HXlzHGG9Z6H3emB1OJ+91X+/qSjiQM4oUU36HZsAa03ECagBClLogdyIIdXf0CGWU3dSA247SfLyt7RGR3mg0f3T91W67zSrAJ//LVIXPqjJoiuBc4f1aPDMNuZvVh7GWCGEjzLFmi0knoEOJB70kHPH+ERJy6bhnn3Fpt7YD4MZx+VG51nx57EclsZ3llWb5vE3cDF1Vmiv9jpBu8pBsqrtIMTsxRJ",
    #     "skin":             "noskin",  
    #     "sst-main":         "Sst1|PQHVwDUuAIJqYLjamVXMRa-zCcJD9_9e_1Zn6pfFIT-8LDmG_PwJPHxJRaL_6L02M3aa2zEJmXvq5NCLPMe4pqsEtHlDJgtKNmo78PVOIFvrIyyWEZxWnWTPbbjQv8v70P2Q7S5fAQ-_MSAe1YtMRRV5F_czsDpEyuvwxq_ebs_wRoCEA74mcH9G7sqkpTdzag48FA5mNE43ZIxhW_-R4Ry4szdVgdKgD23rAlQ9Gd_VJyCcPa1BUio1s2azxKlEE2yjukAWZlS-gYpZBo9nPfZRRoSmtmuYoIUo_XsuBjbgSPI",
    #     "ubid-main":        "132-8679684-1200428",
    #     "x-amz-captcha-1":  "1741325986593754",
    #     "x-amz-captcha-2":  "nI6b/6S9DPqGnM+Su9DUjg==",
    #     "x-main":           "\"kqRY3uh8@5DEEhsvDMDUS418XOghXTP@duR55CtZS9gvK88zNOeKBr7B6Gb3?wTy\"",
    # })

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
    if "captcha" in response.text.lower():
        print("[Info] CAPTCHA detected, trying to solve...")

        # Step 3: Solve CAPTCHA
        # Assume fetchRecaptcha, recaptchaHandler, submitCaptcha are implemented
        recaptcha_image = fetchRecaptcha(response)
        ocr_result = recaptchaHandler(recaptcha_image)
        authUrl = submitCaptcha(session, ocr_result)

        # Step 4: Visit the auth URL (with same session)
        print("final url:", authUrl)
        response = session.get(authUrl)
    
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
    asin = "B0D326XTTP"  # 替换为目标产品的 ASIN

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
        df.to_excel("amazon_reviews.xlsx", index=False)
        print("评论已保存到 amazon_reviews.xlsx")
    else:
        print("未抓取到任何评论数据。")


if __name__ == "__main__":
    main()