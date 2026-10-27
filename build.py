#!/usr/bin/env python3
"""Builds the static site: one folder per app (/lockbar/privacy, /lockbar/support, en + ru).

Usage: python3 build.py            # writes the pages next to this file
       python3 build.py --publish  # same, but refuses to run while SUPPORT_EMAIL is empty
New app: add an entry to APPS, a content module like lockbar below, and run the script again.
"""
import html
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
DEVELOPER = "Mikhail Mukminov"
SUPPORT_EMAIL = "voltec.apps@gmail.com"  # one line to change everywhere
EFFECTIVE = {"en": "October 22, 2026", "ru": "22 октября 2026"}
SITE = "https://voltec.github.io"

CSS = """
:root{color-scheme:light dark;--bg:#fff;--fg:#14171a;--mut:#5b6670;--acc:#0a7f4a;--line:#e3e7ea}
@media (prefers-color-scheme:dark){:root{--bg:#0b0d0e;--fg:#e8ecef;--mut:#98a3ab;--acc:#3ddc84;--line:#23282c}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Roboto,sans-serif}
main{max-width:720px;margin:0 auto;padding:32px 20px 64px}
h1{font-size:2rem;line-height:1.2;margin:.2em 0 .3em}h2{font-size:1.25rem;margin:2em 0 .4em;padding-top:.6em;border-top:1px solid var(--line)}
p,li{margin:.5em 0}ul,ol{padding-left:1.3em}a{color:var(--acc)}small,.mut{color:var(--mut)}
nav{display:flex;gap:16px;flex-wrap:wrap;font-size:.95rem;margin-bottom:8px}nav a{text-decoration:none}nav .on{font-weight:600;text-decoration:underline}
code{background:var(--line);padding:1px 5px;border-radius:5px;font-size:.92em}
footer{margin-top:3em;color:var(--mut);font-size:.9rem}
"""

APPS = [("lockbar", "Lockbar", {"en": "Find sensitive photos on your iPhone and lock them in an encrypted vault.",
                                "ru": "Находит чувствительные фото на iPhone и прячет их в зашифрованный сейф."}),
        ("couchdial", "Couchdial", {"en": "A player for your own IPTV playlists on iPhone, iPad and Apple TV.",
                                    "ru": "Плеер для ваших IPTV-плейлистов на iPhone, iPad и Apple TV."})]

T = {  # UI strings
    "en": {"privacy": "Privacy Policy", "support": "Support", "home": "Home", "lang": "Русский", "eff": "Effective"},
    "ru": {"privacy": "Политика конфиденциальности", "support": "Поддержка", "home": "Главная", "lang": "English", "eff": "Действует с"},
}


def e(s):
    return html.escape(s, quote=False)


def mail():
    return f'<a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>'


def page(path, lang, title, body, app=None, kind=None):
    """path: folder relative to ROOT; writes index.html."""
    base = f"/{app}" if app else ""
    other = "ru" if lang == "en" else "en"
    prefix = lambda l: base + ("/ru" if l == "ru" else "")
    if app:
        nav = (f'<a href="{prefix(lang)}/privacy/"{" class=on" if kind == "privacy" else ""}>{T[lang]["privacy"]}</a>'
               f'<a href="{prefix(lang)}/support/"{" class=on" if kind == "support" else ""}>{T[lang]["support"]}</a>'
               f'<a href="{prefix(other)}/{kind}/">{T[lang]["lang"]}</a>')
    else:
        nav = ""
    out = ROOT / path
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><style>{CSS}</style></head><body><main><nav>{nav}</nav>
{body}
<footer>© {DEVELOPER}</footer></main></body></html>
""")


def lockbar():
    A = "Lockbar"
    privacy_en = f"""<h1>{A} Privacy Policy</h1><p class="mut">Effective {EFFECTIVE['en']}</p>
<p>{A} is made by {DEVELOPER} ("we"). This policy explains what happens to your information when you use the {A} app for iPhone and its Share extension.</p>
<h2>The short version</h2><ul>
<li>We <b>do not collect any personal data</b>. We have no servers, no accounts and no analytics, and we show no ads.</li>
<li>Your photos, the text recognized in them, the scan results and your vault never leave your device unless <b>you</b> export them or save a backup file somewhere.</li>
<li>Purchases are handled entirely by Apple.</li></ul>
<h2>What the app does on your device</h2>
<p><b>Photo scanning.</b> With your permission, the app reads your photo library to find photos that look like identity documents, driver's licenses, payment cards, passwords and recovery codes, crypto wallet recovery phrases and other documents. It uses Apple's on-device frameworks (Vision text recognition). Recognized text is processed in memory and is never saved, logged or sent anywhere.</p>
<p><b>Intimate photos (optional).</b> If you have turned on Sensitive Content Warning (or Communication Safety) in iOS Settings, the app uses Apple's on-device SensitiveContentAnalysis framework to flag photos that may contain nudity. The analysis runs on your device. Neither we nor Apple receive the photos or the results. If the setting is off, this check does not run.</p>
<p><b>Scan results.</b> For each photo checked, the app keeps a small encrypted record on your device: the photo's local identifier, the category and confidence of any finding, the detector version, and whether you hid or dismissed it. The record is encrypted with a key that never leaves the device and is excluded from device backups. You can erase it in Settings.</p>
<p><b>Your vault.</b> Photos and files you move into the vault are encrypted on your device with AES-256-GCM. The key is protected by your PIN and, if you turn it on, by Face ID through the iOS Keychain. Face ID data itself is handled by iOS and is never available to the app. The vault is stored only on this device and is <b>not included in iCloud or iPhone backups</b>.</p>
<p><b>Deleting originals.</b> After a photo is copied into the vault and the copy is verified, iOS asks you to confirm deleting the original. Deleted originals stay in Recently Deleted in the Photos app for about 30 days.</p>
<p><b>Share extension.</b> When you share items to {A} from another app, they are encrypted immediately and kept in the app's private storage on your device until you next unlock the vault.</p>
<p><b>Backup files.</b> You can create an encrypted backup file (<code>.vaultbackup</code>). It is saved wherever you choose (for example Files, a computer or a drive) and can be opened only with your recovery key, which only you hold. We never receive your backups or your recovery key.</p>
<p><b>Preferences.</b> Settings such as auto-lock delay are stored on your device.</p>
<h2>Purchases</h2>
<p>{A} Pro is sold through Apple's App Store using In-App Purchase. Apple processes the payment and your Apple Account information under <a href="https://www.apple.com/legal/privacy/">Apple's Privacy Policy</a>. The app checks your Pro status on your device using Apple's StoreKit. We do not receive your name, email address, payment details or a purchase history linked to you. We see only aggregated sales reports that Apple provides to all developers.</p>
<h2>Network connections</h2>
<p>The app does not connect to any server operated by us or by third parties. iOS may connect to Apple's services when you buy or restore a purchase, or when you choose to download originals of photos stored only in iCloud Photos.</p>
<h2>Crash reports</h2>
<p>If you have chosen in iOS Settings to share analytics with app developers, Apple may provide us with anonymous crash reports and performance data. They do not contain your photos, text or vault contents. You can turn this off in Settings → Privacy &amp; Security → Analytics &amp; Improvements.</p>
<h2>What we don't do</h2><ul>
<li>We do not sell, rent or share any data, because we collect none.</li>
<li>We do not track you across apps or websites and do not use advertising identifiers.</li>
<li>We do not use your photos or scan results to train any model.</li></ul>
<h2>Children</h2><p>The app is not directed at children and collects no data from anyone, including children.</p>
<h2>Your choices and rights</h2>
<p>All data the app handles is on your device and under your control. You can change or revoke Photos access in iOS Settings, delete scan results in the app, export or delete vault items, and delete everything by deleting the app. Because we hold no personal data about you, there is nothing for us to access, correct, port or erase on your behalf. If you are in the EU/EEA, the UK or another region with data-protection laws, you can still contact us with any question.</p>
<p>If you forget your PIN, we cannot recover your vault: no one else has the key. A backup file can be restored with its recovery key.</p>
<h2>Contact</h2><p>{DEVELOPER} · {mail()}</p>
<p>If you email us, we use your message and address only to answer you and delete the conversation when it is no longer needed.</p>
<h2>Changes</h2><p>If this policy changes, we will update the date above and the in-app text. We will never start collecting personal data without saying so clearly in the app and in this policy first.</p>"""

    privacy_ru = f"""<h1>Политика конфиденциальности {A}</h1><p class="mut">Действует с {EFFECTIVE['ru']}</p>
<p>{A} разрабатывает {DEVELOPER} («мы»). Эта политика объясняет, что происходит с вашей информацией, когда вы пользуетесь приложением {A} для iPhone и его расширением «Поделиться».</p>
<h2>Коротко</h2><ul>
<li>Мы <b>не собираем персональные данные</b>. У нас нет серверов, аккаунтов и аналитики, мы не показываем рекламу.</li>
<li>Ваши фото, распознанный в них текст, результаты проверки и сейф никогда не покидают устройство, пока <b>вы сами</b> не экспортируете их или не сохраните файл резервной копии.</li>
<li>Покупками полностью занимается Apple.</li></ul>
<h2>Что приложение делает на вашем устройстве</h2>
<p><b>Проверка фото.</b> С вашего разрешения приложение читает фотобиблиотеку, чтобы найти фото, похожие на удостоверения личности, водительские права, платёжные карты, пароли и коды восстановления, seed-фразы криптокошельков и другие документы. Для этого используются системные средства Apple на устройстве (распознавание текста Vision). Распознанный текст обрабатывается только в памяти и нигде не сохраняется, не записывается в журналы и не отправляется.</p>
<p><b>Интимные фото (по желанию).</b> Если в Настройках iOS включено «Предупреждение о конфиденциальном контенте» (или Communication Safety), приложение использует системную функцию Apple SensitiveContentAnalysis на устройстве, чтобы отметить фото, где может быть обнажённое тело. Анализ идёт на вашем устройстве. Ни мы, ни Apple не получаем ни фото, ни результаты. Если настройка выключена, эта проверка не выполняется.</p>
<p><b>Результаты проверки.</b> Для каждого проверенного фото приложение хранит на устройстве небольшую зашифрованную запись: локальный идентификатор фото, категорию и уверенность находки, версию детектора и ваше решение (спрятали или отклонили). Запись шифруется ключом, который не покидает устройство, и не попадает в резервные копии устройства. Её можно стереть в Настройках приложения.</p>
<p><b>Ваш сейф.</b> Фото и файлы, перенесённые в сейф, шифруются на вашем устройстве по AES-256-GCM. Ключ защищён вашим PIN-кодом и, если вы включили, Face ID через связку ключей iOS. Данные Face ID обрабатывает сама iOS, приложению они недоступны. Сейф хранится только на этом устройстве и <b>не входит в резервные копии iCloud и iPhone</b>.</p>
<p><b>Удаление оригиналов.</b> Когда фото скопировано в сейф и копия проверена, iOS просит подтвердить удаление оригинала. Удалённые оригиналы около 30 дней лежат в «Недавно удалённых» в приложении «Фото».</p>
<p><b>Расширение «Поделиться».</b> Когда вы отправляете файлы в {A} из другого приложения, они сразу шифруются и до следующей разблокировки сейфа хранятся в закрытом хранилище приложения на вашем устройстве.</p>
<p><b>Файлы резервной копии.</b> Вы можете создать зашифрованный файл резервной копии (<code>.vaultbackup</code>). Он сохраняется там, где вы выберете (например, в «Файлах», на компьютере или на диске), и открывается только ключом восстановления, который есть только у вас. Мы никогда не получаем ваши копии и ключ.</p>
<p><b>Настройки.</b> Параметры вроде задержки автоблокировки хранятся на вашем устройстве.</p>
<h2>Покупки</h2>
<p>{A} Pro продаётся через App Store с помощью встроенных покупок Apple. Платёж и данные вашей учётной записи Apple обрабатывает Apple в соответствии со своей <a href="https://www.apple.com/legal/privacy/">политикой конфиденциальности</a>. Приложение проверяет статус Pro на устройстве через StoreKit. Мы не получаем ваше имя, адрес почты, платёжные данные и историю покупок, связанную с вами. Мы видим только сводные отчёты о продажах, которые Apple даёт всем разработчикам.</p>
<h2>Сетевые подключения</h2>
<p>Приложение не подключается ни к каким серверам, ни нашим, ни сторонним. iOS может обращаться к сервисам Apple, когда вы покупаете или восстанавливаете покупку, а также когда вы сами решили загрузить оригиналы фото, которые хранятся только в iCloud Фото.</p>
<h2>Отчёты о сбоях</h2>
<p>Если в Настройках iOS вы разрешили делиться аналитикой с разработчиками, Apple может передавать нам анонимные отчёты о сбоях и производительности. В них нет ваших фото, текста и содержимого сейфа. Отключить это можно в Настройки → Конфиденциальность и безопасность → Аналитика и улучшения.</p>
<h2>Чего мы не делаем</h2><ul>
<li>Мы не продаём, не сдаём в аренду и не передаём никакие данные, потому что ничего не собираем.</li>
<li>Мы не отслеживаем вас между приложениями и сайтами и не используем рекламные идентификаторы.</li>
<li>Мы не используем ваши фото и результаты проверки для обучения каких-либо моделей.</li></ul>
<h2>Дети</h2><p>Приложение не предназначено для детей и не собирает данные ни у кого, включая детей.</p>
<h2>Ваш выбор и права</h2>
<p>Все данные, с которыми работает приложение, находятся на вашем устройстве и под вашим контролем. Вы можете изменить или отозвать доступ к Фото в Настройках iOS, удалить результаты проверки в приложении, экспортировать или удалить элементы сейфа и удалить всё, удалив приложение. Поскольку у нас нет персональных данных о вас, нам нечего показывать, исправлять, переносить или стирать. Если вы находитесь в ЕС/ЕЭЗ, Великобритании или другом регионе с законами о защите данных, вы всё равно можете написать нам с любым вопросом.</p>
<p>Если вы забудете PIN-код, мы не сможем восстановить сейф: ключа нет ни у кого, кроме вас. Файл резервной копии можно восстановить его ключом восстановления.</p>
<h2>Связь</h2><p>{DEVELOPER} · {mail()}</p>
<p>Если вы напишете нам, мы используем ваше письмо и адрес только чтобы ответить и удаляем переписку, когда она больше не нужна.</p>
<h2>Изменения</h2><p>Если политика изменится, мы обновим дату выше и текст в приложении. Мы никогда не начнём собирать персональные данные, не сказав об этом ясно в приложении и в этой политике заранее.</p>"""

    support_en = f"""<h1>{A} Support</h1>
<p>{A} finds photos of passports and IDs, driver's licenses, bank cards, passwords and recovery codes, seed phrases and other documents in your photo library, and locks them in an encrypted vault on your iPhone. Everything runs on the device: no account, no servers.</p>
<p><b>Contact:</b> {mail()}. We usually reply within 2 business days. Please never send us photos of your documents, your PIN or your recovery key.</p>
<h2>Getting started</h2><ol>
<li>Open the app and tap <b>Allow access to Photos</b>. Full access lets the app check your whole library; with limited access it checks only the photos you selected.</li>
<li>The check runs on your iPhone and shows what it found by category.</li>
<li>Open a category and review the photos (everything found is preselected; uncheck false alarms, or switch to <b>Cards</b> to go one by one), then tap <b>Hide</b>.</li>
<li>The first time you hide something you create a 6-digit PIN and can turn on Face ID.</li>
<li>The app encrypts each photo and checks the copy, then iOS asks you to confirm deleting the originals. They stay in <b>Recently Deleted</b> in Photos for about 30 days.</li></ol>
<h2>Frequently asked questions</h2>
<p><b>Is anything uploaded?</b><br>No. Photos, recognized text, results and the vault stay on your device. The app has no servers and no analytics. Purchases go through Apple.</p>
<p><b>Why didn't it find a photo?</b><br>Detection is not perfect. Printed documents and screenshots are found best. Handwritten notes (for example a seed phrase on paper) are often missed by the normal check. Turn on the deep scan in Settings for a slower, more thorough check that runs while your iPhone charges. Always review the results yourself.</p>
<p><b>Why is "Intimate photos" unavailable?</b><br>This category uses Apple's on-device Sensitive Content Analysis, which only works when you turn on <b>Sensitive Content Warning</b> in iOS <b>Settings → Privacy &amp; Security</b>. The app cannot turn it on for you.</p>
<p><b>The scan stopped when I left the app.</b><br>iOS may pause long checks. The app shows "Scan · stopped" with <b>Continue</b>, and nothing already checked is lost.</p>
<p><b>What is free and what is Pro?</b><br>The scan of your whole library is free. Findings in photos from the last 30 days are free to review and hide, as many as you like. Copies of the same photo are cleaned up for free. Findings in older photos show up as a count and open with Pro. You can also add your own photos and files: free for photos from the last 30 days and up to 10 files, with Pro any age and any number. Export is always free. Pro is a one-time purchase or a yearly subscription that also checks new photos automatically (prices are shown in the app).</p>
<p><b>How do I cancel or manage my subscription?</b><br>Open iOS <b>Settings → [your name] → Subscriptions</b>, or the App Store → your profile → Subscriptions. Deleting the app does not cancel a subscription.</p>
<p><b>I bought Pro but the app shows Free.</b><br>Open <b>Settings → Restore Purchases</b> in the app, signed in with the same Apple Account you used to buy.</p>
<p><b>Refunds</b><br>Refunds are handled by Apple: <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</p>
<h2>Your vault and backups (please read)</h2><ul>
<li><b>The vault lives only on this iPhone.</b> It is <b>not included in iCloud backups, iPhone backups or Quick Start transfers to a new iPhone</b>. To move it or keep it safe, create a backup file in Settings and store it in Files, on a computer or on a drive.</li>
<li><b>Keep your recovery key.</b> Backups open only with it. Write it down or store it in a password manager, not in Photos.</li>
<li><b>Restore on a new iPhone:</b> install the app, tap <b>I have a backup</b> (or Settings → Restore from file), choose the file and enter the recovery key.</li>
<li><b>Forgot your PIN?</b> No one, including us, can open the vault without it. If you have a backup file and your recovery key, delete and reinstall the app, then restore from the backup.</li>
<li><b>Deleting the app deletes the vault.</b> Make a backup file first.</li></ul>
<h2>Adding items yourself</h2>
<p>In the <b>Vault</b> tab tap <b>Add → From Photos</b> or <b>From Files</b>. From any app, use <b>Share → {A}</b>: shared items are encrypted right away and move into the vault the next time you unlock it.</p>
<h2>Security at a glance</h2><ul>
<li>AES-256-GCM encryption on the device</li>
<li>6-digit PIN with optional Face ID; repeated wrong PINs add a growing delay</li>
<li>The vault locks when you leave the app (adjustable in Settings) and is covered in the app switcher</li></ul>
<h2>Privacy</h2><p>Read the <a href="{SITE}/lockbar/privacy/">full policy</a>. Short version: we collect no data.</p>
<h2>Reporting a problem</h2>
<p>Email {mail()} with your iPhone model, iOS version and app version (Settings → Version in the app), and what you did before the problem. Screenshots of the app screens are welcome; please don't include screenshots of your documents.</p>"""

    support_ru = f"""<h1>Поддержка {A}</h1>
<p>{A} находит в фотобиблиотеке фото паспортов и удостоверений, водительских прав, банковских карт, паролей и кодов восстановления, seed-фраз и других документов и прячет их в зашифрованный сейф на вашем iPhone. Всё работает на устройстве: без аккаунта и серверов.</p>
<p><b>Связь:</b> {mail()}. Обычно отвечаем в течение 2 рабочих дней. Пожалуйста, никогда не присылайте нам фото документов, PIN-код или ключ восстановления.</p>
<h2>Как начать</h2><ol>
<li>Откройте приложение и нажмите <b>«Разрешить доступ к Фото»</b>. Полный доступ позволяет проверить всю библиотеку; при ограниченном проверяются только выбранные фото.</li>
<li>Проверка идёт на вашем iPhone и показывает найденное по категориям.</li>
<li>Откройте категорию и разберите фото (всё найденное уже выбрано; снимите лишнее или переключитесь на <b>карточки</b>, чтобы идти по одному), затем нажмите <b>«Спрятать»</b>.</li>
<li>При первом переносе вы создаёте 6-значный PIN-код и можете включить Face ID.</li>
<li>Приложение шифрует каждое фото и проверяет копию, после чего iOS просит подтвердить удаление оригиналов. Они около 30 дней лежат в <b>«Недавно удалённых»</b> в «Фото».</li></ol>
<h2>Частые вопросы</h2>
<p><b>Что-нибудь загружается в сеть?</b><br>Нет. Фото, распознанный текст, результаты и сейф остаются на вашем устройстве. У приложения нет серверов и аналитики. Покупки идут через Apple.</p>
<p><b>Почему оно не нашло фото?</b><br>Распознавание не идеально. Лучше всего находятся печатные документы и скриншоты. Рукописные записи (например, seed-фраза на бумаге) обычная проверка часто пропускает. Включите глубокую проверку в Настройках: она медленнее и тщательнее и работает, пока iPhone заряжается. Результаты всегда просматривайте сами.</p>
<p><b>Почему «Интимные фото» недоступны?</b><br>Эта категория использует системный анализ Apple на устройстве, который работает, только если в iOS включено <b>«Предупреждение о конфиденциальном контенте»</b> (<b>Настройки → Конфиденциальность и безопасность</b>). Приложение не может включить его за вас.</p>
<p><b>Проверка остановилась, когда я вышел из приложения.</b><br>iOS может приостанавливать долгие проверки. Приложение показывает «Scan · stopped» с кнопкой <b>«Продолжить»</b>, уже проверенное не теряется.</p>
<p><b>Что бесплатно, а что в Pro?</b><br>Проверка всей библиотеки бесплатна. Находки в фото за последние 30 дней можно просматривать и прятать бесплатно, сколько угодно. Копии одного фото чистятся бесплатно. Находки в старых фото видны числом и открываются с Pro. Свои фото и файлы тоже можно добавлять: бесплатно фото за последние 30 дней и до 10 файлов, с Pro любой давности и в любом количестве. Экспорт всегда бесплатен. Pro — разовая покупка или годовая подписка, которая ещё и сама проверяет новые фото (цены показаны в приложении).</p>
<p><b>Как отменить подписку или управлять ею?</b><br>Откройте <b>Настройки iOS → [ваше имя] → Подписки</b> или App Store → профиль → Подписки. Удаление приложения подписку не отменяет.</p>
<p><b>Я купил Pro, а приложение показывает бесплатную версию.</b><br>Откройте <b>Настройки → Восстановить покупки</b> в приложении, войдя с той же учётной записью Apple, с которой покупали.</p>
<p><b>Возврат денег</b><br>Возвратами занимается Apple: <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</p>
<h2>Ваш сейф и резервные копии (важно)</h2><ul>
<li><b>Сейф хранится только на этом iPhone.</b> Он <b>не входит в резервные копии iCloud и iPhone и не переносится при быстром начале на новый iPhone</b>. Чтобы перенести его или сохранить, создайте файл резервной копии в Настройках и храните в «Файлах», на компьютере или на диске.</li>
<li><b>Сохраните ключ восстановления.</b> Копии открываются только им. Запишите его или храните в менеджере паролей, но не в «Фото».</li>
<li><b>Восстановление на новом iPhone:</b> установите приложение, нажмите <b>«У меня есть копия»</b> (или Настройки → Восстановить из файла), выберите файл и введите ключ восстановления.</li>
<li><b>Забыли PIN-код?</b> Никто, включая нас, не может открыть сейф без него. Если есть файл копии и ключ восстановления, удалите и заново установите приложение и восстановите из копии.</li>
<li><b>Удаление приложения удаляет сейф.</b> Сначала сделайте файл резервной копии.</li></ul>
<h2>Добавление своих файлов</h2>
<p>На вкладке <b>«Сейф»</b> нажмите <b>«Добавить → Из Фото»</b> или <b>«Из Файлов»</b>. Из любого приложения используйте <b>«Поделиться → {A}»</b>: файлы сразу шифруются и переносятся в сейф при следующей разблокировке.</p>
<h2>Безопасность в двух словах</h2><ul>
<li>Шифрование AES-256-GCM на устройстве</li>
<li>6-значный PIN-код, Face ID по желанию; неверные попытки увеличивают задержку</li>
<li>Сейф блокируется при выходе из приложения (настраивается) и закрыт в переключателе приложений</li></ul>
<h2>Конфиденциальность</h2><p>Прочитайте <a href="{SITE}/lockbar/ru/privacy/">полную политику</a>. Коротко: мы не собираем данные.</p>
<h2>Сообщить о проблеме</h2>
<p>Напишите на {mail()} модель iPhone, версию iOS и версию приложения (Настройки → Версия в приложении) и что вы делали перед проблемой. Скриншоты экранов приложения приветствуются, но не присылайте скриншоты своих документов.</p>"""

    page("lockbar/privacy", "en", f"{A} Privacy Policy", privacy_en, "lockbar", "privacy")
    page("lockbar/ru/privacy", "ru", f"Политика конфиденциальности {A}", privacy_ru, "lockbar", "privacy")
    page("lockbar/support", "en", f"{A} Support", support_en, "lockbar", "support")
    page("lockbar/ru/support", "ru", f"Поддержка {A}", support_ru, "lockbar", "support")


def couchdial():
    A = "Couchdial"
    eff = {"en": "October 27, 2026", "ru": "27 октября 2026"}
    eula = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
    cancel = "https://support.apple.com/118428"
    privacy_en = f"""<h1>{A} Privacy Policy</h1><p class="mut">Effective {eff['en']}</p>
<h2>The short version</h2><ul>
<li>{A} has no accounts and no servers of its own. Your playlists, logins and viewing history never reach us.</li>
<li>If you use iCloud, your sources move between your devices through your private iCloud. Everything the app stores there is end-to-end encrypted.</li>
<li>No ads, no tracking, no analytics and no crash-reporting services.</li>
<li>The app connects only to the servers in the sources you add, and to Apple.</li></ul>
<h2>Who is responsible</h2>
<p>{A} is made by {DEVELOPER}, an individual developer ("we"). For the purposes of the GDPR and the UK GDPR, we are the controller for the {A} apps. Contact: {mail()}.</p>
<p>This policy covers {A} for iPhone, iPad, Apple TV and Mac, and this website. The website uses no cookies, scripts or third-party resources.</p>
<h2>How {A} works</h2>
<p>{A} is a player for your own M3U playlists and Xtream accounts. It contains no channels. What you add is stored on your devices and, if you're signed in to iCloud, in your private iCloud storage, which Apple runs for you. We don't run any server that your data passes through, and we can't see what you store in your iCloud.</p>
<h2>What the app stores and where</h2>
<p><b>Source details.</b> The name you give the source, its type (M3U link, M3U file or Xtream), the server address (host and port only), the Xtream user name, your settings for the source (for example "Show on Apple TV"), and the expiry date and connection limit if your provider reports them. Stored on your device and, if you use iCloud, in your private iCloud database, end-to-end encrypted. Apple sees only technical metadata, such as the record type and dates. Used to show your sources and move them between your devices.</p>
<p><b>Links, logins and playlist files.</b> The full playlist link (it may contain a token), the Xtream server, user name and password, and the contents of an M3U file you import. Stored in the Keychain on each device. In your private iCloud only end-to-end encrypted: links and logins in encrypted fields, playlist files encrypted with their own key before upload. The keys are kept in your iCloud Keychain, so neither Apple nor we can read them.</p>
<p><b>Your devices.</b> For each device where {A} runs: its name, its type and when the app was last open on it. When you send a source to a specific device, a record of which source went where, the name of the sending device and when it arrived. Stored in your private iCloud database, end-to-end encrypted, to show "Apple TV nearby", send a source to that device and confirm that it arrived.</p>
<p><b>Favorites, recent channels, Order changes, player settings, parental PIN.</b> Only on this device.</p>
<p><b>Channel lists and programme guide.</b> Downloaded from your sources and kept in a cache on your device.</p>
<p><b>Purchases.</b> Apple handles payment. The app asks Apple's StoreKit on your device whether you have {A} Pro. We never see your name, Apple Account or payment details. Apple gives us sales reports that don't identify you.</p>
<h2>Sending a source to Apple TV with a QR code</h2>
<p>The Apple TV shows a QR code with a one-time code and an encryption key. Your iPhone scans it, encrypts the source with that key (AES-GCM, 256-bit) and leaves the encrypted package in the app's public iCloud database under the one-time code. The Apple TV downloads the package, decrypts it and confirms, and your iPhone then deletes the package. The key exists only in the QR code: without it nobody, including Apple and us, can read the package. Each code works once and only for 10 minutes. If the Apple TV never confirms, the encrypted package can stay in the public database, still unreadable without the key.</p>
<h2>Who the app connects to</h2><ul>
<li><b>The servers in your sources</b>: playlists, Xtream servers, streams, and logo and guide addresses listed in your playlist. Like any website, they see your IP address and what the app requests. Their own privacy policies apply, and we get nothing from them. Addresses that start with http:// are not encrypted.</li>
<li><b>Apple</b>: iCloud (syncing and QR transfer) and the App Store (purchases).</li></ul>
<p>Nothing else. We have no servers and keep no logs.</p>
<h2>What we don't do</h2><ul>
<li>No ads, no tracking, and no analytics or crash-reporting services in the app. The app never asks for permission to track you.</li>
<li>We don't sell or share personal information, and we don't build profiles.</li>
<li>Sorting your playlist ("Order") happens on your device.</li></ul>
<p>If you turned on "Share with App Developers" in your device's privacy settings, Apple may share crash reports and aggregated usage statistics with us. That is Apple's feature, under Apple's privacy policy, and the reports don't identify you.</p>
<h2>When you email us</h2>
<p>We receive your email address and what you write, use it only to answer you, and keep it only as long as we need to help you, unless the law requires longer. Please don't send passwords or full playlist links.</p>
<h2>Legal bases (GDPR and UK GDPR)</h2><ul>
<li>Storing and syncing your sources, playing streams and checking your purchase are needed to provide the app you chose to use (Art. 6(1)(b)).</li>
<li>Answering your emails: our legitimate interest in helping you (Art. 6(1)(f)), or performance of a contract when it's about your purchase.</li></ul>
<h2>How long data is kept</h2><ul>
<li>On your device: until you delete the source, clear recent channels or delete the app.</li>
<li>In your iCloud: until you delete the source on an iPhone, iPad or Mac, which removes it from all your devices. Deleting a source on Apple TV only hides it there.</li>
<li>With us: nothing from the app, because nothing from the app reaches us.</li></ul>
<h2>Your rights</h2>
<p>Under the GDPR and the UK GDPR you can access, correct, delete, restrict or object to processing of your data, receive it in a portable format and withdraw consent. You can also complain to a data protection authority. The app's data is on your devices and in your iCloud, so you control it directly: edit or delete sources in the app, or delete {A}'s iCloud data (see <a href="/couchdial/support/">Support</a>). Apple lets you request a copy of your iCloud data at <a href="https://privacy.apple.com">privacy.apple.com</a>. For anything else, email {mail()}. We reply within one month.</p>
<p>California and other US states: we don't sell or share personal information, don't use it for targeted advertising and don't use sensitive personal information.</p>
<h2>Children</h2><p>{A} is not made for children. We don't knowingly collect personal data from anyone, including children.</p>
<h2>Security</h2><p>Logins are kept in the Keychain. Everything the app stores in your iCloud is end-to-end encrypted, and the QR transfer is encrypted with a one-time key. Keep your devices up to date, use two-factor authentication for your Apple Account, and prefer sources with https:// addresses.</p>
<h2>Changes</h2><p>When we change this policy, we update this page and the date above. If the app starts handling your data in a new way, we'll describe it here before that update is released and ask for your consent in the app where it's required.</p>
"""

    privacy_ru = f"""<h1>Политика конфиденциальности {A}</h1><p class="mut">Действует с {eff['ru']}</p>
<h2>Коротко</h2><ul>
<li>В {A} нет аккаунтов и нет наших серверов. Ваши плейлисты, логины и история просмотров к нам не попадают.</li>
<li>Если вы пользуетесь iCloud, источники переходят между вашими устройствами через ваш личный iCloud. Всё, что приложение там хранит, защищено сквозным шифрованием.</li>
<li>Нет рекламы, слежки, аналитики и сервисов отчётов о сбоях.</li>
<li>Приложение подключается только к серверам из ваших источников и к Apple.</li></ul>
<h2>Кто отвечает за данные</h2>
<p>{A} разрабатывает {DEVELOPER}, индивидуальный разработчик («мы»). По GDPR и UK GDPR мы — контролёр данных для приложений {A}. Связь: {mail()}.</p>
<p>Политика относится к {A} для iPhone, iPad, Apple TV и Mac и к этому сайту. Сайт не использует cookie, скрипты и сторонние ресурсы.</p>
<h2>Как устроен {A}</h2>
<p>{A} — плеер для ваших собственных плейлистов M3U и аккаунтов Xtream. Каналов в нём нет. То, что вы добавляете, хранится на ваших устройствах и, если вы вошли в iCloud, в вашем личном хранилище iCloud, которое для вас ведёт Apple. Через наши серверы ваши данные не проходят, и мы не видим, что лежит в вашем iCloud.</p>
<h2>Что хранит приложение и где</h2>
<p><b>Сведения об источнике.</b> Название, тип (ссылка M3U, файл M3U или Xtream), адрес сервера (только хост и порт), логин Xtream, ваши настройки источника (например, «Показывать на Apple TV»), срок действия и лимит подключений, если их сообщает провайдер. Хранятся на устройстве и, если вы пользуетесь iCloud, в вашей личной базе iCloud со сквозным шифрованием. Apple видит только служебные метаданные: тип записи и даты. Нужны, чтобы показывать источники и переносить их между устройствами.</p>
<p><b>Ссылки, логины и файлы плейлистов.</b> Полная ссылка на плейлист (в ней может быть токен), сервер, логин и пароль Xtream, содержимое импортированного файла M3U. Хранятся в связке ключей на каждом устройстве. В вашем личном iCloud — только со сквозным шифрованием: ссылки и логины в зашифрованных полях, файлы плейлистов шифруются собственным ключом до загрузки. Ключи лежат в вашей связке ключей iCloud, поэтому ни Apple, ни мы прочитать их не можем.</p>
<p><b>Ваши устройства.</b> Для каждого устройства с {A}: название, тип и когда приложение было на нём открыто последний раз. Когда вы отправляете источник на конкретное устройство — какой источник куда ушёл, название отправившего устройства и время получения. Хранится в вашей личной базе iCloud со сквозным шифрованием, чтобы показать «Apple TV рядом», отправить на него источник и подтвердить получение.</p>
<p><b>Избранное, недавние каналы, изменения «Порядка», настройки плеера, родительский PIN.</b> Только на этом устройстве.</p>
<p><b>Списки каналов и телепрограмма.</b> Загружаются из ваших источников и хранятся в кэше на устройстве.</p>
<p><b>Покупки.</b> Оплату проводит Apple. Приложение через StoreKit на устройстве проверяет, есть ли у вас {A} Pro. Ваше имя, Apple Account и платёжные данные мы не видим. Apple присылает нам отчёты о продажах, по которым вас нельзя опознать.</p>
<h2>Передача источника на Apple TV по QR-коду</h2>
<p>Apple TV показывает QR-код с одноразовым кодом и ключом шифрования. iPhone сканирует его, шифрует источник этим ключом (AES-GCM, 256 бит) и кладёт зашифрованный пакет в публичную базу iCloud приложения под одноразовым кодом. Apple TV скачивает пакет, расшифровывает и подтверждает получение, после чего iPhone удаляет пакет. Ключ есть только в QR-коде: без него пакет не прочитает никто, включая Apple и нас. Каждый код срабатывает один раз и только 10 минут. Если Apple TV не подтвердит получение, зашифрованный пакет может остаться в публичной базе, но без ключа он нечитаем.</p>
<h2>К кому подключается приложение</h2><ul>
<li><b>К серверам ваших источников</b>: плейлисты, серверы Xtream, потоки, адреса логотипов и телепрограммы из вашего плейлиста. Как любой сайт, они видят ваш IP-адрес и что запрашивает приложение. У них свои правила конфиденциальности, мы от них ничего не получаем. Адреса на http:// не шифруются.</li>
<li><b>К Apple</b>: iCloud (синхронизация и передача по QR) и App Store (покупки).</li></ul>
<p>Больше ни к кому. Своих серверов у нас нет, логов мы не ведём.</p>
<h2>Чего мы не делаем</h2><ul>
<li>Нет рекламы, слежки, сервисов аналитики и отчётов о сбоях. Приложение никогда не просит разрешения на отслеживание.</li>
<li>Мы не продаём и не передаём персональные данные и не составляем профили.</li>
<li>Упорядочивание плейлиста («Порядок») происходит на вашем устройстве.</li></ul>
<p>Если в настройках устройства включено «Делиться с разработчиками», Apple может передавать нам отчёты о сбоях и обобщённую статистику. Это функция Apple по правилам Apple, и по этим отчётам вас нельзя опознать.</p>
<h2>Когда вы пишете нам</h2>
<p>Мы получаем ваш email и текст письма, используем их только для ответа и храним, пока это нужно, чтобы помочь, если закон не требует дольше. Не присылайте пароли и полные ссылки на плейлисты.</p>
<h2>Правовые основания (GDPR и UK GDPR)</h2><ul>
<li>Хранение и синхронизация источников, воспроизведение потоков и проверка покупки нужны, чтобы предоставить приложение, которым вы решили пользоваться (ст. 6(1)(b)).</li>
<li>Ответы на письма: наш законный интерес помочь вам (ст. 6(1)(f)) или исполнение договора, если вопрос о покупке.</li></ul>
<h2>Сколько хранятся данные</h2><ul>
<li>На устройстве: пока вы не удалите источник, не очистите недавние каналы или не удалите приложение.</li>
<li>В iCloud: пока вы не удалите источник на iPhone, iPad или Mac — тогда он исчезнет со всех устройств. Удаление на Apple TV только скрывает источник там.</li>
<li>У нас: ничего из приложения, потому что из приложения к нам ничего не приходит.</li></ul>
<h2>Ваши права</h2>
<p>По GDPR и UK GDPR вы вправе получить доступ к данным, исправить, удалить их, ограничить обработку или возразить против неё, получить данные в переносимом формате и отозвать согласие, а также пожаловаться в надзорный орган. Данные приложения лежат на ваших устройствах и в вашем iCloud, поэтому вы управляете ими сами: меняйте или удаляйте источники в приложении или удалите данные {A} из iCloud (см. <a href="/couchdial/ru/support/">Поддержку</a>). Копию данных iCloud можно запросить у Apple на <a href="https://privacy.apple.com">privacy.apple.com</a>. По остальным вопросам пишите на {mail()}. Мы отвечаем в течение месяца.</p>
<h2>Дети</h2><p>{A} не предназначен для детей. Мы сознательно не собираем персональные данные ни у кого, в том числе у детей.</p>
<h2>Безопасность</h2><p>Логины хранятся в связке ключей. Всё, что приложение хранит в вашем iCloud, защищено сквозным шифрованием, передача по QR шифруется одноразовым ключом. Обновляйте устройства, включите двухфакторную аутентификацию Apple Account и по возможности используйте источники с адресами https://.</p>
<h2>Изменения</h2><p>Когда мы меняем политику, мы обновляем эту страницу и дату выше. Если приложение начнёт обращаться с данными по-новому, мы опишем это здесь до выхода обновления и спросим согласие в приложении, где это нужно.</p>
"""

    support_en = f"""<h1>{A} Support</h1>
<p>{A} is a player for your own IPTV playlists on iPhone, iPad, Apple TV and Mac. It doesn't include, sell or recommend channels, playlists or providers.</p>
<p><b>Contact:</b> {mail()}. Please tell us your device and system version, the app version (Settings → About) and what you did and saw; a screenshot helps. Never send passwords or full playlist links.</p>
<h2>Frequently asked questions</h2>
<p><b>How do I add a playlist?</b><br>On iPhone, iPad or Mac tap <b>Add source</b> and choose <b>Link</b> (an M3U playlist link), <b>Xtream</b> (server, login and password) or <b>File</b> (an M3U file). The app checks the source, imports it and sorts the channels into categories. On Apple TV choose <b>Add from iPhone</b>, <b>Scan a code</b> or <b>Type on this Apple TV</b>.</p>
<p><b>Why won't a channel play?</b><br>{A} plays what your source sends and shows the reason when a channel fails. On the error screen tap <b>What to tell the provider</b> to copy a ready-made message.</p><ul>
<li>Access denied (401, 403): the login is wrong, the subscription doesn't include this channel, or the provider blocks your network or region.</li>
<li>Not found (404): the channel moved or was removed. Refresh the source; if it's still broken, the provider needs to fix the link.</li>
<li>Server error or no response: the provider's server is down or overloaded. Try later or another mirror of the channel.</li>
<li>Subscription expired, or connection limit reached: reported by your provider.</li>
<li>A web page instead of a stream: ask the provider for a direct stream or M3U link.</li>
<li>Unsupported format: turn on <b>Compatible player for other formats</b> in Settings → Player.</li></ul>
<p><b>How do I move my sources to Apple TV?</b><br>With the same Apple Account, sign in to iCloud on both devices and sources with <b>Show on Apple TV</b> appear by themselves. With any Apple Account, choose <b>Scan a code</b> on Apple TV and scan it with your iPhone camera. When {A} is open on your Apple TV, your iPhone also offers <b>Send to Apple TV</b>.</p>
<p><b>How do I cancel my subscription?</b><br>Subscriptions are managed by Apple: on iPhone or iPad open <b>Settings → [your name] → Subscriptions</b>; on Apple TV <b>Settings → Users and Accounts → your account → Subscriptions</b>. Cancel at least 24 hours before the period or free trial ends. Deleting the app doesn't cancel a subscription. See <a href="{cancel}">Apple's guide</a>. Refunds: <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</p>
<p><b>How do I restore my purchase?</b><br>Sign in with the Apple Account you used to buy Pro and open <b>Settings → Purchases → Restore purchase</b>. Pro works on every device with that Apple Account and for family members through Family Sharing.</p>
<p><b>How do I delete my data?</b><br>Delete a source on iPhone, iPad or Mac to remove it from all devices and iCloud. Delete the app to remove its local data and Keychain logins. To remove everything from iCloud, open <b>Settings → [your name] → iCloud → Manage Storage</b>, choose {A} and delete its data. We keep none of your data.</p>
<h2>Privacy and terms</h2>
<p><a href="/couchdial/privacy/">Privacy Policy</a>. Short version: we collect no data. Terms of Use: <a href="{eula}">Apple's Standard License Agreement (EULA)</a>.</p>
"""

    support_ru = f"""<h1>Поддержка {A}</h1>
<p>{A} — плеер для ваших собственных IPTV-плейлистов на iPhone, iPad, Apple TV и Mac. Мы не включаем в него, не продаём и не советуем каналы, плейлисты или провайдеров.</p>
<p><b>Связь:</b> {mail()}. Напишите устройство и версию системы, версию приложения (Настройки → О приложении), что вы делали и что увидели; скриншот помогает. Никогда не присылайте пароли и полные ссылки на плейлисты.</p>
<h2>Частые вопросы</h2>
<p><b>Как добавить плейлист?</b><br>На iPhone, iPad или Mac нажмите <b>«Добавить источник»</b> и выберите <b>«Ссылка»</b> (ссылка на плейлист M3U), <b>Xtream</b> (сервер, логин и пароль) или <b>«Файл»</b> (файл M3U). Приложение проверит источник, импортирует его и разложит каналы по категориям. На Apple TV выберите <b>«Добавить с iPhone»</b>, <b>«Сканировать код»</b> или <b>«Ввести на этом Apple TV»</b>.</p>
<p><b>Почему не играет канал?</b><br>{A} воспроизводит то, что отдаёт источник, и показывает причину ошибки. На экране ошибки нажмите <b>«Что сказать провайдеру»</b>, чтобы скопировать готовое сообщение.</p><ul>
<li>Доступ запрещён (401, 403): неверный логин, канал не входит в подписку или провайдер блокирует вашу сеть или регион.</li>
<li>Не найдено (404): канал переехал или удалён. Обновите источник; если не помогло, ссылку должен исправить провайдер.</li>
<li>Ошибка сервера или нет ответа: сервер провайдера не работает или перегружен. Попробуйте позже или другое зеркало канала.</li>
<li>Подписка истекла или достигнут лимит подключений: это сообщает провайдер.</li>
<li>Веб-страница вместо потока: попросите у провайдера прямую ссылку на поток или M3U.</li>
<li>Формат не поддерживается: включите <b>«Совместимый плеер для других форматов»</b> в Настройки → Плеер.</li></ul>
<p><b>Как перенести источники на Apple TV?</b><br>С одним Apple Account войдите в iCloud на обоих устройствах — источники с включённым <b>«Показывать на Apple TV»</b> появятся сами. С любым Apple Account выберите на Apple TV <b>«Сканировать код»</b> и отсканируйте его камерой iPhone. Когда {A} открыт на Apple TV, iPhone также предлагает <b>«Отправить на Apple TV»</b>.</p>
<p><b>Как отменить подписку?</b><br>Подписками управляет Apple: на iPhone или iPad — <b>Настройки → ваше имя → Подписки</b>; на Apple TV — <b>Настройки → Пользователи и учётные записи → ваша учётная запись → Подписки</b>. Отмените не позже чем за 24 часа до конца периода или пробного периода. Удаление приложения подписку не отменяет. Подробнее — в <a href="{cancel}">инструкции Apple</a>. Возврат денег: <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</p>
<p><b>Как восстановить покупку?</b><br>Войдите в Apple Account, с которого покупали Pro, и откройте <b>Настройки → Покупки → Восстановить покупку</b>. Pro работает на всех устройствах с этим Apple Account и у членов семьи через «Семейный доступ».</p>
<p><b>Как удалить мои данные?</b><br>Удалите источник на iPhone, iPad или Mac — он исчезнет со всех устройств и из iCloud. Удалите приложение — исчезнут локальные данные и логины в связке ключей. Чтобы стереть всё из iCloud, откройте <b>Настройки → ваше имя → iCloud → Управление хранилищем</b>, выберите {A} и удалите данные. У нас ваших данных нет.</p>
<h2>Конфиденциальность и условия</h2>
<p><a href="/couchdial/ru/privacy/">Политика конфиденциальности</a>. Коротко: мы не собираем данные. Условия использования: <a href="{eula}">стандартное лицензионное соглашение Apple (EULA)</a>.</p>
"""

    page("couchdial/privacy", "en", f"{A} Privacy Policy", privacy_en, "couchdial", "privacy")
    page("couchdial/ru/privacy", "ru", f"Политика конфиденциальности {A}", privacy_ru, "couchdial", "privacy")
    page("couchdial/support", "en", f"{A} Support", support_en, "couchdial", "support")
    page("couchdial/ru/support", "ru", f"Поддержка {A}", support_ru, "couchdial", "support")


def home():
    items = "".join(f'<li><a href="/{slug}/support/">{e(name)}</a> <span class="mut">— {e(desc["en"])}</span></li>'
                    for slug, name, desc in APPS)
    page("", "en", DEVELOPER, f"<h1>{DEVELOPER}</h1><p class=\"mut\">iPhone apps</p><ul>{items}</ul>")


if __name__ == "__main__":
    if "--publish" in sys.argv and not SUPPORT_EMAIL:
        sys.exit("SUPPORT_EMAIL is empty: set it in build.py before publishing")
    if not SUPPORT_EMAIL:
        SUPPORT_EMAIL = "support-email-not-set@example.invalid"
    lockbar()
    couchdial()
    home()
    (ROOT / ".nojekyll").write_text("")
    print("built")
