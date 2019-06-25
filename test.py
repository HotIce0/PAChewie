print(b'\xf0\xff\xaa\x01\x08\x00\r\n')
print(b'\xff\xaa\x01\x08\x00\r\n')
print(b'\xff\xaa\x01\x08\x00')  # 角度参考
print(b'\xff\xaa\x01\x03\x00')  # 高度
#  \xff\xaa'\x01\x00进入设置模式
# ffaa010800

# class sao:
#     def __init__(self):
#         self.val = [1,2]
#         print(id(self.val))
#
#     def get(self):
#         return self.val
#
#     def print_val(self):
#         print(self.val)
#
#
# a = sao()
# val = a.get()
# val[0] = 100
# print(id(val))
# a.print_val()