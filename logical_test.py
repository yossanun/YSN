"""
Convert Number to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""


# Start 07/06/2022 20:43 - Finish 07/06/2022 22:09

def num_to_words(n):
    units = [
        "ศูนย์",
        "หนึ่ง",
        "สอง",
        "สาม",
        "สี่",
        "ห้า",
        "หก",
        "เจ็ด",
        "แปด",
        "เก้า",
    ]

    teens = ["สิบ", "สิบเอ็ด", "สิบสอง", "สิบสาม", "สิบสี่", "สิบห้า", "สิบหก", "สิบเจ็ด", "สิบแปด",
             "สิบเก้า"]

    tens = ["ยี่สิบ", "สามสิบ", "สี่สิบ", "ห้าสิบ", "หกสิบ", "เจ็ดสิบ", "แปดสิบ", "เก้าสิบ"]

    suffix = ["ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
    if n <= 9:
        return units[n]

    elif 10 <= n <= 19:
        return teens[n - 10]

    elif 20 <= n <= 99:
        return tens[(n // 10) - 2] + ((units[n % 10] if n % 10 != 1 else "เอ็ด") if n % 10 != 0 else "")

    elif 100 <= n <= 999:
        return num_to_words(n // 100) + suffix[0] + (
            (num_to_words(n % 100) if n % 100 != 1 else "เอ็ด") if n % 100 != 0 else "")

    elif 1000 <= n <= 9999:
        return num_to_words(n // 1000) + suffix[1] + (
            (num_to_words(n % 1000) if n % 1000 != 1 else "เอ็ด") if n % 1000 != 0 else "")

    elif 10000 <= n <= 99999:
        return num_to_words(n // 10000) + suffix[2] + (
            (num_to_words(n % 10000) if n % 10000 != 1 else "เอ็ด") if n % 10000 != 0 else "")

    elif 100000 <= n <= 999999:
        return num_to_words(n // 100000) + suffix[3] + (
            (num_to_words(n % 100000) if n % 100000 != 1 else "เอ็ด") if n % 100000 != 0 else "")

    elif 1000000 <= n < 10000000:
        return num_to_words(n // 1000000) + suffix[4] + (
            (num_to_words(n % 1000000) if n % 1000000 != 1 else "เอ็ด") if n % 1000000 != 0 else "")


while True:
    try:
        num = int(input("โปรดใส่ค่าที่ต้องการที่นี่: "))
        if 0 <= num < 10000000:
            print(num_to_words(num))
        else:
            print('\n')
            print('ค่าที่ใส่ไม่อยู่ในช่วง!')
            print('\n')

    except ValueError:
        print('\n')
        print('ใส่เลขเท่านั้นนะจ้ะ!')
        print('\n')
