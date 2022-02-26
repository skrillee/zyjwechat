import qrcode
from io import BytesIO
img = qrcode.make("123")
buf = BytesIO()
img.save(buf)
buf.getvalue()
print(buf)
