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
SUPPORT_EMAIL = "voltec366+lockbar@gmail.com"  # one line to change everywhere
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
                                "ru": "Находит чувствительные фото на iPhone и прячет их в зашифрованный сейф."})]

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
    home()
    (ROOT / ".nojekyll").write_text("")
    print("built")
