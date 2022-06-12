"""
Convert Arabic Number to Roman Number.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลขอราบิก เป็นตัวเลขโรมัน
โดยที่ค่าที่รับต้องมีค่ามากกว่า 0 จนถึง 1000

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""


# Start 07/06/2022 15:39 - Finish 07/06/2022 16:52
def solve(num):
    if 0 < num <= 1000:
        result = ""
        table = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]
        for cap, roman in table:
            d, m = divmod(num, cap)
            result += roman * d
            num = m

        return result

    else:
        print("\n")
        print("ค่าที่ใส่ไม่อยู่ในช่วงที่กำหนด")
        print("\n")


try:
    while True:
        num = int(input("โปรดใส่ค่าที่ต้องการที่นี่: "))
        print("\n")
        print(solve(num))
        print("\n")

except ValueError:
    print("\n")
    print("ใส่ตัวเลขเท่านั้นน้ะจ้ะ")
    print("\n")
