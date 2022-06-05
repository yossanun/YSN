
"""
Convert Number to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""

# Start 29/5/2022 10:30 - Finish 29/5/2022

# thai_text = {
#     '0': "ศูนย์",
#     '1': "หนึ่ง",
#     '2': "สอง",
#     '3': "สาม",
#     '4': "สี่",
#     '5': "ห้า",
#     '6': "หก",
#     '7': "เจ็ด",
#     '8': "แปด",
#     '9': "เก้า",
# }

thai_text = [
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

# unit_text = ["", "หน่วย", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
unit_text = ["สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
unit_numb = [10, 100, 1000, 10000, 100000, 1000000]

try:
    while True:

        input_user = int(input("Please insert your integer here:"))

        text = ""

        if 0 <= input_user < 10000000:
            # input_user = str(input_user)

            if len(str(input_user)) == 1:  # หลักหน่วย
                print("\n")
                print(thai_text[input_user])
                print("\n")

            elif len(str(input_user)) > 1:  # สองหลักขึ้นไป
                for index, numb in enumerate(unit_numb):
                    if input_user < numb:
                        x = numb - input_user
                        if x == 0:
                            print(unit_text[index])


            # elif len(input_user) > 1:  # สองหลักขึ้นไป
            #
            #     if len(input_user) == 2:
            #         if input_user[-1] == '0':
            #             if input_user[0] == '1':
            #                 print("\n")
            #                 print(unit_text[0])
            #                 print("\n")
            #
            #             elif input_user[0] == '2':
            #                 print("\n")
            #                 print("ยี่" + unit_text[0])
            #                 print("\n")
            #
            #             else:
            #                 print("\n")
            #                 print(thai_text[input_user[0]] + unit_text[0])
            #                 print("\n")
            #
            #         elif input_user[-1] == '1':
            #
            #             if input_user[0] == '1':
            #                 print("\n")
            #                 print(unit_text[0] + 'เอ็ด')
            #                 print("\n")
            #
            #             elif input_user[0] == '2':
            #                 print("\n")
            #                 print("ยี่" + unit_text[0] + 'เอ็ด')
            #                 print("\n")
            #
            #             else:
            #                 print("\n")
            #                 print(thai_text[input_user[0]] + unit_text[0] + 'เอ็ด')
            #                 print("\n")
            #
            #         elif input_user[0] == '1':
            #             print("\n")
            #             print(unit_text[0] + thai_text[input_user[-1]])
            #             print("\n")
            #
            #         elif input_user[0] == '2':
            #             print("\n")
            #             print("ยี่" + unit_text[0] + thai_text[input_user[-1]])
            #             print("\n")
            #
            #         else:
            #             print("\n")
            #             print(thai_text[input_user[0]] + unit_text[0] + thai_text[input_user[-1]])
            #             print("\n")
            #
            #     elif len(input_user) == 3:
            #         pass
            #
            #     elif len(input_user) == 4:
            #         pass
            #
            #     elif len(input_user) == 5:
            #         pass
            #
            #     elif len(input_user) == 6:
            #         pass
            #
            #     elif len(input_user) == 7:
            #         pass

        else:
            print("\n")
            print("Your input is not range zero to ten million.")

except ValueError:
    print("\n")
    print("Your input's type is not integer.")
