import requests
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

def get_bypass_code(eurl, platform):
    # Tạo số ngẫu nhiên làm uuid
    uuid = str(random.randint(100000, 999999))

    # Chuẩn hóa url: bỏ http, https, www, / và khoảng trắng
    eurl = eurl.lower().replace("http://", "").replace("https://", "").replace("www.", "").replace("/", "").strip()
    platform = platform.lower()
    if platform in ['facebook', 'fb', 'meta']:
        platform = 'facebook'
    elif platform in ['google', 'gg', 'g']:
        platform = 'google'

    # Mapping url sang hurl và code
    if eurl == 'bamivapharma.com':
        hurl = 'https://bamivapharma.com/'
        code = 'e9VJokISt'
    elif eurl == 'suamatzenmilk.com':
        hurl = 'https://suamatzenmilk.com/'
        code = 'viyjUHvaj'
    elif eurl == 'china-airline.net':
        hurl = 'https://enzymevietnam.com/'
        code = 'oTedsZr2m'
    elif eurl == 'scarmagic-gm.com':
        hurl = 'https://bamivapharma.com/'
        code = 'e9VJokISt'
    else:
        return None, "❌ URL không hợp lệ hoặc chưa được hỗ trợ!"

    try:
        # Request tới layma.net
        headers = {
            'Host': 'layma.net',
            'Accept-Language': 'en-GB,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Referer': hurl,
            'Connection': 'keep-alive',
        }
        response = requests.get(f'https://layma.net/Traffic/Index/{code}', headers=headers, timeout=10)
        if response.status_code == 200:
            sheaders = {
                'Host': 'api.layma.net',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
                'Accept': '*/*',
                'Origin': hurl,
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': hurl,
                'Priority': 'u=1, i',
            }
            sparams = {
                'keytoken': code,
                'flatform': platform,
            }
            sresponse = requests.get('https://api.layma.net/api/admin/campain', params=sparams, headers=sheaders, timeout=10)
            if sresponse.status_code != 200:
                return None, '❌ Lỗi khi lấy data, vui lòng báo cáo admin'
            try:
                html = sresponse.json()
            except Exception:
                return None, '❌ Data trả về không phải dạng JSON!'
            theaders = sheaders
            tjson_data = {
                'uuid': uuid,
                'browser': 'Chrome',
                'browserVersion': '100',
                'browserMajorVersion': 100,
                'cookies': True,
                'mobile': False,
                'os': 'OS',
                'osVersion': '5',
                'screen': '1000 x 1000',
                'referrer': hurl,
                'trafficid': html.get('id', ''),
                'solution': '1',
            }
            tresponse = requests.post('https://api.layma.net/api/admin/codemanager/getcode', headers=theaders, json=tjson_data, timeout=10)
            if tresponse.status_code == 200:
                try:
                    th = tresponse.json()
                    return th.get('html', 'Không có mã'), None
                except Exception:
                    return None, '❌ Kết quả trả về không phải JSON!'
            else:
                return None, '❌ Lỗi khi lấy mã, vui lòng báo cáo admin'
        else:
            return None, '❌ Lỗi khi lấy data, vui lòng báo cáo admin'
    except requests.exceptions.RequestException as ex:
        return None, f'❌ Lỗi kết nối: {ex}'

async def layma_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        # Trả về hướng dẫn sử dụng + domain/platform hỗ trợ
        await update.message.reply_text(
            "❗ Cách dùng: /layma <quest_url> <platform>\n"
            "Ví dụ: /layma bamivapharma.com facebook\n\n"
            "Các domain hỗ trợ:\n"
            "- bamivapharma.com\n"
            "- suamatzenmilk.com\n"
            "- china-airline.net\n"
            "- scarmagic-gm.com\n\n"
            "Platform: facebook, google"
        )
        return
    quest_url = context.args[0]
    platform = context.args[1]
    code, err = get_bypass_code(quest_url, platform)
    if err:
        await update.message.reply_text(err)
    else:
        await update.message.reply_text(
            f"🌐 Domain: {quest_url}\n"
            f"🔰 Nền tảng: {platform.capitalize()}\n"
            f"✅ Mã bypass: <code>{code}</code>",
            parse_mode="HTML"
        )

def main():
    # Nhớ thay token bằng token bot của bạn!
    application = Application.builder().token("7905621710:AAEGFz44YBSzkUevXKDoEM73VLJl12ilnes").build()
    application.add_handler(CommandHandler("layma", layma_command))
    application.run_polling()

if __name__ == "__main__":
    main()