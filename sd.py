# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 19:02:44 2018

@author: diana
"""

from nn import infos
from nn import excel
import random
import xlsxwriter as exe


ler=infos()
ex=excel()

if __name__=='__main__':
    
    gg_1=ler.get_random()

    see_ori=[]
    for kl in gg_1:
        gwe=open('files'+kl+'.txt','r').read()
        see_ori.append((kl,gwe))


    percent=(50,40,30,20,10)    
    
    lista=[] #(id original seq, percentagem, seq)
     
    for elemnt in gg_1: # split in random percentage
         result=ler.gerar_random(percent,elemnt)
         try:
             lista.append((elemnt,result[0], result[1][0]))
             lista.append((elemnt,result[0], result[1][1]))
         except BaseException: pass

    b=random.sample(lista,len(lista)) #suffle list
    
    aj=100 # new id
    
    print ('blast split seq')
    see=[] #(nr, seq) split
    for el in b:
        nome=el[0]+'_'+el[1]
        ex.blast_1x(str(aj),nome,el[2])
        see.append((str(aj),el[2]))
        aj+=1


    
    print('procura de pares')
    po=ler.b_pares() # find pair
    ppo, ppo_inv=po[0],po[1] #ppo->(pt_1, pt_2) ppo_inv->(pt_2,pt_1)
    
    

#    see, s --> [(nr,seq),(nr,seq),(nr,seq)]
#    ppo,ml->[(pt_1, pt_2),(pt_1, pt_2) ,(pt_1, pt_2)]
#    see_ori ->[(nome, seq), (nome,seq)] original
#    tto ->[(nome,seq)]


# =============================================================================
# Find pairs
# =============================================================================
    tto=[] 
    for ml in ppo:  #join two sequences
        seq_1=''
        seq_2=''        
        for s in see:
            if ml[0]==s[0]: seq_1=s[1]
            if ml[1]==s[0]: seq_2=s[1]
        
        seqq=seq_1+seq_2
        tto.append((ml,seqq))
    
  
    df=exe.Workbook('pares_90.xlsx') #write pairs
    sh=df.add_worksheet('ppo')
    row=0
    
    for ee in see_ori:
        for t in tto:
            if t[1]==ee[1]:
                cee=(str(t[0])+'-->'+str(ee[0]))
                sh.write(row,0,cee)
                for oo in b:
                    if ee[0]==oo[0]:
                        sh.write(row, 3, oo[1])
                        break
                row+=1
    
    tto_inv=[] 
    for ml in ppo_inv:
        seq_1=''
        seq_2=''        
        for s in see:
            if ml[0]==s[0]: seq_1=s[1]
            if ml[1]==s[0]: seq_2=s[1]
        
        seqq=seq_1+seq_2
        tto_inv.append((ml,seqq))

    
    for ee in see_ori:
        for t in tto_inv:
            if t[1]==ee[1]:
                cee=(str(t[0])+'-->'+str(ee[0]))
                sh.write(row,0,cee)
                for oo in b:
                    if ee[0]==oo[0]:
                        sh.write(row, 3, oo[1])
                        break
                row+=1

    
    df.close()
                
    

# =============================================================================
# Blast to confirm the results        
# =============================================================================
    print('final blast')
    for ee in see_ori:
        for t in tto:
            if t[1]==ee[1]:
                ex.blast_f(ee,t)
    
    for ee in see_ori:
        for t in tto_inv:
            if t[1]==ee[1]:
                ex.blast_f(ee,t)
    
        
        
        
        
        
    
    
        
        
    



    
    
    
