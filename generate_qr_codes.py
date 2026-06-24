import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# Classic 6-stripe pride flag colors (one per task QR)
PRIDE_FLAG_COLORS = [
    {"name": "Red", "hex": "#E40303", "qr_fill": "#E40303"},
    {"name": "Orange", "hex": "#FF8C00", "qr_fill": "#FF8C00"},
    {"name": "Yellow", "hex": "#FFED00", "qr_fill": "#C9A600"},  # darker for scan contrast
    {"name": "Green", "hex": "#00811F", "qr_fill": "#00811F"},
    {"name": "Blue", "hex": "#24408E", "qr_fill": "#24408E"},
    {"name": "Violet", "hex": "#732982", "qr_fill": "#732982"},
]


def create_qr_code_with_label(url, label, filename, pride_color):
    """Create a QR code with URL, label, and pride-flag styling."""

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color=pride_color["qr_fill"],
        back_color="white",
    )

    img_width = 400
    img_height = 500
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Pride stripe accent at top
    stripe_height = 8
    stripe_width = img_width // len(PRIDE_FLAG_COLORS)
    for i, color in enumerate(PRIDE_FLAG_COLORS):
        draw.rectangle(
            [i * stripe_width, 0, (i + 1) * stripe_width - 1, stripe_height],
            fill=color["hex"],
        )

    qr_size = 300
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    qr_x = (img_width - qr_size) // 2
    qr_y = 48
    img.paste(qr_img, (qr_x, qr_y))

    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        url_font = ImageFont.truetype("arial.ttf", 14)
        instruction_font = ImageFont.truetype("arial.ttf", 12)
        badge_font = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        title_font = ImageFont.load_default()
        url_font = ImageFont.load_default()
        instruction_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()

    title_text = label
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (img_width - title_width) // 2
    draw.text((title_x, 18), title_text, fill=pride_color["hex"], font=title_font)

    badge_text = f"Pride {pride_color['name']}"
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_width = badge_bbox[2] - badge_bbox[0]
    badge_x = (img_width - badge_width) // 2
    draw.text((badge_x, 368), badge_text, fill=pride_color["hex"], font=badge_font)

    url_text = url
    url_bbox = draw.textbbox((0, 0), url_text, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (img_width - url_width) // 2
    draw.text((url_x, 388), url_text, fill="#666666", font=url_font)

    instruction_text = "Enter your Team ID when prompted"
    instruction_bbox = draw.textbbox((0, 0), instruction_text, font=instruction_font)
    instruction_width = instruction_bbox[2] - instruction_bbox[0]
    instruction_x = (img_width - instruction_width) // 2
    draw.text((instruction_x, 418), instruction_text, fill="#444444", font=instruction_font)

    step_label = label.split(" - ")[1] if " - " in label else label
    step_text = f"Scan this QR code to access {step_label}"
    step_bbox = draw.textbbox((0, 0), step_text, font=instruction_font)
    step_width = step_bbox[2] - step_bbox[0]
    step_x = (img_width - step_width) // 2
    draw.text((step_x, 438), step_text, fill="#444444", font=instruction_font)

    draw.rectangle(
        [0, 0, img_width - 1, img_height - 1],
        outline=pride_color["hex"],
        width=4,
    )

    img.save(filename, "PNG", quality=95)
    print(f"✅ Created: {filename} ({pride_color['name']} — {pride_color['hex']})")


def main():
    base_url = "https://tusharzinnia07.github.io/treasure-hunt-deploy"

    print("🎯 Generating Pride-Flag QR Codes for Treasure Hunt Game")
    print("=" * 50)
    print(f"🌐 Your GitHub Pages URL: {base_url}")
    print()

    os.makedirs("qr_codes", exist_ok=True)

    tasks = [
        {
            "url": f"{base_url}/task1.html",
            "label": "Task 1 - Start Your Hunt!",
            "filename": "qr_codes/task1_qr.png",
        },
        {
            "url": f"{base_url}/task2.html",
            "label": "Task 2 - Second Clue",
            "filename": "qr_codes/task2_qr.png",
        },
        {
            "url": f"{base_url}/task3.html",
            "label": "Task 3 - Third Clue",
            "filename": "qr_codes/task3_qr.png",
        },
        {
            "url": f"{base_url}/task4.html",
            "label": "Task 4 - Fourth Challenge",
            "filename": "qr_codes/task4_qr.png",
        },
        {
            "url": f"{base_url}/task5.html",
            "label": "Task 5 - Fifth Challenge",
            "filename": "qr_codes/task5_qr.png",
        },
        {
            "url": f"{base_url}/task6.html",
            "label": "Task 6 - Final Challenge",
            "filename": "qr_codes/task6_qr.png",
        },
    ]

    print("🏳️‍🌈 Creating QR codes in pride flag colors:")
    print("-" * 40)

    for i, task in enumerate(tasks):
        create_qr_code_with_label(
            task["url"],
            task["label"],
            task["filename"],
            PRIDE_FLAG_COLORS[i],
        )

    print("\n🎉 All QR codes generated successfully!")
    print("📁 Check the 'qr_codes' folder for your QR code images")
    print()
    print("🌈 COLOR KEY:")
    print("-" * 30)
    for i, color in enumerate(PRIDE_FLAG_COLORS):
        print(f"• QR {i + 1}: {color['name']} ({color['hex']})")
    print()
    print("📋 GAME INSTRUCTIONS:")
    print("=" * 50)
    print("1. 🖨️  Print the 6 QR codes")
    print("2. 📍 Place QR codes at different locations in your office")
    print("3. 👥 Teams scan QR codes in sequence (Task 1 → 2 → 3 → 4 → 5 → 6)")
    print("4. 📝 Teams enter their Team ID when prompted (e.g., ALPHA, BRAVO)")
    print("5. 🎮 Teams enter previous task codes to proceed")
    print("6. 📊 Monitor all teams in real-time at: " + base_url + "/admin.html")
    print()
    print("🎯 GAME FLOW:")
    print("-" * 30)
    print("• Task 1: Teams enter their Team ID → Get TC441")
    print("• Task 2: Teams enter Team ID + TC441 → Get TC242")
    print("• Task 3: Teams enter Team ID + TC242 → Get TC803")
    print("• Task 4: Teams enter Team ID + TC803 → Get TC200")
    print("• Task 5: Teams enter Team ID + TC200 → Get TC505")
    print("• Task 6: Teams enter Team ID + TC505 → 🏆 WINNER! 🏆")
    print()
    print("🚀 Ready for your treasure hunt!")


if __name__ == "__main__":
    main()
