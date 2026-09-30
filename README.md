# Autosalon

Konsolda ishlaydigan, MySQL bazasiga ulanuvchi oddiy avtosalon (avtomobil savdosi) ilovasi. Foydalanuvchi terminal orqali mijoz sifatida ro'yxatdan o'tishi, mavjud avtomobillar ro'yxatini ko'rishi, model bo'yicha qidirishi, bitta avtomobilni id bo'yicha ko'rishi va uni "sotib olishi" mumkin.

## Xususiyatlar

- Interaktiv konsol menyusi (1–6 tanlovlar)
- Mijozni `customers` jadvaliga ro'yxatdan o'tkazish
- `cars` jadvalidagi barcha avtomobillarni jadval ko'rinishida chiqarish
- Model nomi bo'yicha qidirish (`LIKE` so'rovi)
- Avtomobilni id bo'yicha to'liq ma'lumotlari bilan ko'rish
- Avtomobil sotib olish: to'lov summasini narx bilan solishtirish, yetarli bo'lsa yozuvni bazadan o'chirish va qaytim (agar ortiqcha to'langan bo'lsa) hisoblash

## Texnologiyalar

- Python
- `mysql-connector-python` — MySQL bilan ishlash uchun
- MySQL (yoki mos relyatsion baza)

## O'rnatish va ishga tushirish

Repoda `requirements.txt`/`Pipfile` mavjud emas — kod faqat `mysql-connector-python` kutubxonasidan foydalanadi:

```bash
git clone https://github.com/ozodbekxoldarov/autosalon.git
cd autosalon
pip install mysql-connector-python
```

Kodda ulanish parametrlari (`host`, `user`, `password`, `database`) `Database` klassiga argument sifatida uzatiladi — ularni `app.py` faylini ochib, o'zingizning MySQL ma'lumotlaringizga moslab kiriting.

MySQL bazasida quyidagi jadvallar oldindan yaratilgan bo'lishi kerak (kod ularga so'rov yuboradi, lekin repoda tayyor SQL/schema fayli yo'q):

- **customers**: `first_name`, `last_name`, `phone`, `email`, `passport`
- **cars**: `id`, `brand`, `model`, `year`, `price`, `color` (va boshqa mos ustunlar)

Keyin ilovani ishga tushiring:

```bash
python app.py
```

## Menyu bandlari

| Tanlov | Amal |
|--------|------|
| 1 | Ro'yxatdan o'tish (mijoz qo'shish) |
| 2 | Avtomobillar jadvalini ko'rish |
| 3 | Model bo'yicha qidirish |
| 4 | Avtomobilni id bo'yicha ko'rish |
| 5 | Avtomobil sotib olish |
| 6 | Dasturdan chiqish |

## Papka tuzilmasi

```
autosalon/
└── app.py    # Database klassi (MySQL ulanishi) va App klassi (konsol menyusi)
```

## Muallif

**Ozodbek** — [github.com/ozodbekxoldarov](https://github.com/ozodbekxoldarov)
