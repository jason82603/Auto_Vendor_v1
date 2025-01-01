
def count_numbers(words):
    words = words.upper().replace(" ", "")  # 將words全部轉大寫並且將空格移除
    sorted_words = sorted(words) #將words重新排序

    numbers_dic = {}
    for i in sorted_words:
        numbers_dic[i] = numbers_dic.get(i, 0) + 1 #如果dict裡找不到i這個key,預設他的value為0
    print("輸出:")
    for key, value in numbers_dic.items():
        print(f"{key} {value}")


words = "Hello welcome to Cathay 60th year anniversary"
count_numbers(words)
