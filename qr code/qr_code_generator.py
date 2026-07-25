import qrcode

github_url = "https://github.com/Omrawat11"

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(github_url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("github_qr.png")

print("QR Code generated successfully!")
print("File saved as: github_qr.png")
