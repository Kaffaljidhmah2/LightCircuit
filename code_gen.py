import os 


url = 'FA.dgn'
x = 0
y = 0
s=open(url,'r').read()

#Parsing

u = s.split('\n')
for i in range(len(u)):
    if u[i]=='' or u[i][0]=='/':
        continue
    else:
        ilist = u[i].strip().split(' ')
        if ilist[0]!='a':
            raise BaseException("ERROR")
        ilist[1]=str(int(ilist[1])+x)
        ilist[2]=str(int(ilist[2])+y)
        u[i] = ' '.join(ilist)
res = "\n".join(u)
