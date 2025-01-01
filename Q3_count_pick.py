
def count_pick(n,k = 3):
    if (n == 0):
        return 0
    elif (n == 1):
        return 1
    else:
        return (count_pick(n - 1, k) + k - 1) % n + 1


n = int(input("輸入：n值(0-100)"))
count_pick = count_pick(n)
print(f"輸出：第{count_pick}順位")
