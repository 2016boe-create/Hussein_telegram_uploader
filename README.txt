Hussein Telegram Uploader
=========================

محتويات الحزمة:
- bot.php        -> نسخة PHP من البوت (تعامل عبر webhook على /bot.php)
- bot.py         -> نسخة Python (Flask) من البوت (تعامل عبر webhook على /bot)
- uploads/       -> مجلد لحفظ الملفات وملف seen_users.txt لتخزين المستخدمين الذين استقبلوا الترحيب
- README.txt     -> هذا الملف

ملاحظات أمنية مهمة:
- لا تُدخل توكن البوت داخل الملفات. ضع التوكن كمتغير بيئي على Render (اسم المتغير: BOT_TOKEN).
- أي شخص يعرف رابط webhook يمكنه إرسال تحديثات، لذلك احرص على إبقاء التوكن سريًا.

تشغيل على Render (Python):
1. ارفع المشروع إلى GitHub (مجلد المشروع).
2. أنشئ Web Service على Render وربطه بالمستودع.
3. Environment: Python 3
4. Build Command: leave empty
5. Start Command:
   gunicorn bot:app --bind 0.0.0.0:$PORT
6. في إعدادات الخدمة على Render، أضف Environment Variable:
   BOT_TOKEN = <توكن_البوت_الخاصة_بك>
7. بعد النشر، خذ عنوان الخدمة (مثال: https://your-service.onrender.com)
8. ربط الـWebhook:
   افتح المتصفح:
   https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://your-service.onrender.com/bot
   استبدل <YOUR_TOKEN> واسم الخدمة.
9. الآن البوت سيعمل 24/7 ويخزن الملفات في مجلد uploads/

تشغيل على Render (PHP):
1. ارفع المشروع إلى GitHub.
2. أنشئ Web Service على Render.
3. Environment: PHP
4. Start Command:
   php -S 0.0.0.0:10000 -t .
5. أضف Environment Variable:
   BOT_TOKEN = <توكن_البوت_الخاصة_بك>
6. بعد النشر، رابط الخدمة مثل: https://your-php-service.onrender.com
7. ربط الـWebhook:
   https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://your-php-service.onrender.com/bot.php

ملاحظات نهائية:
- الملفات المرفوعة ستظهر داخل مجلد uploads.
- ستتلقى رسالة ترحيب مرة واحدة عند أول تفاعل لكل مستخدم.
- لو احتجت أعدت تكوين لتفريغ الملفات بشكل دوري أو إرسالها لحساب Google Drive أو Dropbox، أخبرني وسأضيف ذلك.

بالتوفيق، حسين!