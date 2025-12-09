import time
from giaodien import (
    img_dua_hau, img_bi_ngo,
    img_plus, img_thanhtoan,
    click_if_found
)

def mua_popup(template):

    if not click_if_found(template, 0.72):
        return False

    time.sleep(0.2)

    for _ in range(5):
        click_if_found(img_plus, 0.7, 0.05)

    time.sleep(0.5)

    click_if_found(img_thanhtoan, 0.7, 0.1)
    return True


def vong_lap_mua():
    print("🔁 Bắt đầu AUTO mua hạt...")

    while True:

        if mua_popup(img_dua_hau):
            print("✔ Mua dưa hấu xong")
            time.sleep(0.8)
            continue


        if mua_popup(img_bi_ngo):
            print("✔ Mua bí ngô xong")
            time.sleep(0.8)
            continue

        print("⏳ Chờ popup mua...")
        time.sleep(0.5)

