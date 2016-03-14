i=0
with open('toutt.xml', 'r') as f:
   for line in f:
      if '<Project>' in line:
         i+=1
   print i      
