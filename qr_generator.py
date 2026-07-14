import os
import sys

try:
    import qrcode
except ImportError:
    print("Missing dependency: qrcode. Install it with `pip install qrcode[pil]`.")
    sys.exit(1)


def main():
    print("QR Code Generator")
    url = input("Enter the URL or text to encode: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        return

    output_filename = input("Output filename [qrcode.png]: ").strip() or "qrcode.png"
    output_path = os.path.abspath(output_filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)

    print(f"QR code saved to: {output_path}")


if __name__ == "__main__":
    main()
