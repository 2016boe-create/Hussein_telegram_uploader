<?php
// Hussein Telegram Uploader - PHP version
// Usage: set environment variable BOT_TOKEN (do NOT put token here)
// On Render: add environment variable BOT_TOKEN with your bot token

$botToken = getenv('6140362743:AAEDXyA37n0gNnxwnertVcf3ZKe_9mAPVgE');
$apiUrl = "https://api.telegram.org/bot$botToken/";

// Simple storage for known users to send welcome message once
$seenFile = __DIR__ . '/uploads/seen_users.txt';

// ensure uploads directory exists
$targetDir = __DIR__ . '/uploads/';
if (!file_exists($targetDir)) {
    mkdir($targetDir, 0777, true);
    // create seen file
    file_put_contents($seenFile, "");
}

// Read incoming update
$update = json_decode(file_get_contents("php://input"), true);
if (!$update) {
    echo "Bot (PHP) alive";
    exit;
}

$chat_id = $update["message"]["chat"]["id"];
$from_id = $update["message"]["from"]["id"];
$text = $update["message"]["text"] ?? '';
$file = $update["message"]["document"] ?? null;

// send message helper
function sendMessage($apiUrl, $chat_id, $text) {
    $text = urlencode($text);
    file_get_contents($apiUrl . "sendMessage?chat_id=$chat_id&text=$text");
}

// welcome message once per user
$seen = file($seenFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
if (!in_array($from_id, $seen)) {
    file_put_contents($seenFile, $from_id . PHP_EOL, FILE_APPEND | LOCK_EX);
    sendMessage($apiUrl, $chat_id, "مرحبًا! أرسل لي أي ملف وسأرفعه لك 🔼");
}

if ($file) {
    $file_id = $file["file_id"];
    $getFile = json_decode(file_get_contents($apiUrl . "getFile?file_id=$file_id"), true);
    if (isset($getFile["result"]["file_path"])) {
        $file_path = $getFile["result"]["file_path"];
        $download_url = "https://api.telegram.org/file/bot$botToken/$file_path";
        $localFile = $targetDir . basename($file_path);
        // Download file
        $data = file_get_contents($download_url);
        if ($data === false) {
            sendMessage($apiUrl, $chat_id, "❌ فشل تحميل الملف من Telegram.");
            exit;
        }
        file_put_contents($localFile, $data);
        sendMessage($apiUrl, $chat_id, "✅ تم حفظ الملف في السيرفر: " . basename($localFile));
    } else {
        sendMessage($apiUrl, $chat_id, "❌ حدث خطأ عند الحصول على معلومات الملف.");
    }
} else {
    sendMessage($apiUrl, $chat_id, "أرسل لي ملفًا وسأحفظه لك 📥");
}
?>