n = 23

print("о" if n%10==1 and n//10%10!=1 else "а" if n%10<5 and n%10>1 and n//10%10!=1 else "")
