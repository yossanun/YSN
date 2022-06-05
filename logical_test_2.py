"""
Convert Arabic Number to Roman Number.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลขอราบิก เป็นตัวเลขโรมัน
โดยที่ค่าที่รับต้องมีค่ามากกว่า 0 จนถึง 1000

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""
output = ""
roman_text = [['M', 1000], ['D', 500], ['C', 100], ['L', 50], ['X', 10], ['V', 5], ['I', 1]]

try:
    while True:

        num = int(input("โปรดใส่ค่าที่ต้องการที่นี่: "))
        if 0 < num <= 1000:
            lt = []
            for i in range(len(roman_text)):
                a = num//roman_text[i][1]
                if a == 4:
                    lt.append(roman_text[i][0] + roman_text[i-1][0])
                else:
                    [lt.append(roman_text[i][0]) for ch in range(a)]
                if a != 0:
                    num &= roman_text[i][1]

            print("\n")
            print(''.join(lt))
            print("\n")

        else:
            print("\n")
            print("ค่าที่ใส่ไม่อยู่ในช่วงที่กำหนด")
            print("\n")

except ValueError:
    print("\n")
    print("ใส่ตัวเลขเท่านั้นน้ะจ้ะ")
    print("\n")