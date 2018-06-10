# -*- coding: utf-8 -*-
"""
Created on Sat May  5 21:49:51 2018

@author: diana
"""

from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import random
from Bio import Entrez
import xlsxwriter as ex
import pandas as pd


class ncbi:
        
    def nuc(self,sequencia,n):  #Blast
        nome='blast'+str(n)
        print (nome)
        file_name=open(nome+'.xml','w')
        f_blast=NCBIWWW.qblast('blastn','nr',sequencia)
        file_name.write(f_blast.read())
        file_name.close()
        return
 
    
    def get_fasta(self,gene_id): # get the fasta files   
        handle = Entrez.efetch(db="nucleotide", id=gene_id ,rettype="fasta")
        record = handle.read()
        out_handle = open(gene_id+'.xml', 'w') #to create a file with gene name
        out_handle.write(record)
        out_handle.close
        return

    
    
class infos:
    
    def ler_file(self, nome,formato): #Parse of FASTA files
        file=SeqIO.read(nome,formato)
        return (file.seq) #return the sequence
    
    
    def percn(self, seq, valor): # Separates the sequence in 2 according to given percentage
        sequencias=[]
        valor=valor/100
        val=len(seq)*valor
        seq1, seq2=seq[:int(val)], seq[int(val):]# smaller, biggest
        sequencias.append(seq1)
        sequencias.append(seq2)
        return sequencias #return a list of seqs
    
    
    def info_nuc(self,file): # Parse XML obtained from BLAST
        
        blast=open(file,'r')
        records=NCBIXML.parse(blast)
        item=next(records)
        
        acession=[]
        defn=[]
        evalue=[]
        
        for align in item.alignments: 
            acession.append(align.hit_id)  #acession number
            defn.append(align.hit_def)   # name of the organism
            for hsp in align.hsps:
                evalue.append(hsp.expect) # e-value
               
        blast.close()
        return acession, defn, evalue # return lists, acession, def and e-value
    
    
    def get_id(self,nome): # Get the gene id's from a genbank file
    
        gene_id=[]
        for record in SeqIO.parse(nome, "genbank"):
            for feat in record.features:
                if feat.type=='CDS':
                    g = feat.qualifiers.get("db_xref")
                    for gg in g:
                        gene=[x for x in gg.split(':')]
                        gene_id.append(gene[1])
                    
        return gene_id # return a list of ID
    
    def id_random(self, amostra, tam):  # pick random numbers
        return random.sample(amostra,tam)
    
    def get_random(self): # return random id
        gb=self.get_id('phila.gb')
        id_gen=self.id_random(gb,100)
        print(id_gen)
    
    def gerar_random(self,lst_perc,elemnt): #split in a random percentage
        try:
            valor_p=str(self.id_random(lst_perc,1))
            valor_p=valor_p.strip('[]')
            
            file=open('files'+elemnt+'.txt','r').read()
            seqs=self.percn(file,int(valor_p))
        except BaseException: pass
        
        return valor_p,seqs
    
    def b_pares(self): # get pairs
        pares=[]
        pares_inv=[]
        for i in range(100,299):
            try:
                pt_1=pd.read_excel(str(i)+'.xlsx', sheet_name=str(i))
                for ii in range(i+1,300):
                    pt_2=pd.read_excel(str(ii)+'.xlsx', sheet_name=str(ii))
                    
                    ig=0
                    for elem in pt_1['Unnamed: 1']:
                        for ele in pt_2['Unnamed: 1']:
                            if elem==ele:
                                ig+=1 
                            
                    vl_90=ig/50
                    if vl_90>=0.7:
                        pares.append((str(i),str(ii)))
                        print((str(i),str(ii)))
                        pares_inv.append((str(ii),str(i)))
                                
            except BaseException: pass
        return pares, pares_inv
    
    
class excel (ncbi, infos): # creates excel files from blast results
    
    def blast_2x(self,file,perc): #compares results from two sequence fragments
    
        for f in range(len(file)):
            book=ex.Workbook(str(file[f])+'.xlsx')
            print(file[f])
            sheet=book.add_worksheet(file[f])
            sheet.set_column(6,6,65)
            sheet.set_column(10,10,65)
            a=self.ler_file(file[f]+'.fasta','fasta') # used to get the size of the original sequence
            tam=len(a)
            
            linha_ini=book.add_format({'bg_color':' yellow'}) 
            linha_seq=book.add_format({'bg_color':'#66bb6a'}) 
            bold=book.add_format({'bold':True})
            red=book.add_format({'color':'#d84315'})
            sheet.set_row(0, cell_format=linha_ini)
            sheet.write(0,1,'len='+str(tam))  # fisrt line, size of the original sequence
            
            row=1
            
            for p in perc: #perc: list of percentages used to split the sequences
                sheet.set_row(row,cell_format=linha_seq)
                sheet.write(row,3,str(p)+'/'+str(100-p)) 
                row+=1
        
                seqs=self.percn(a,p) #split a sequence
                 
                for i in range(len(seqs)):
                    try:
                        self.nuc(seqs[i],i) # performs the blast
                    except BaseException: pass
         
                try:
                    acession_1, defn_1, evalue_1=self.info_nuc('blast0.xml') #parse of xml file from seq_1
                    acession_2, defn_2, evalue_2=self.info_nuc('blast1.xml') #parse of xml file from seq_2
            
                
                    for i1 in range(len(defn_1)):
                        if defn_1[i1]==defn_2[i1]: #same result in the same position, write in bold
                            
                            sheet.write(row,5,acession_1[i1])
                            sheet.write(row,6,defn_1[i1],bold)
                            sheet.write(row,7,evalue_1[i1])
                            
                            sheet.write(row,9,acession_2[i1])
                            sheet.write(row,10,defn_2[i1],bold)
                            sheet.write(row,11,evalue_2[i1])
                            
                            row+=1
                        
                        elif defn_1[i1]!=defn_2[i1]: #same result in different position, write in red, else write in black
                            if defn_1[i1] in defn_2: 
                                sheet.write(row,5,acession_1[i1])
                                sheet.write(row,6,defn_1[i1],red)
                                sheet.write(row,7,evalue_1[i1])
                            
                            if defn_2[i1] in defn_1: 
                                sheet.write(row,9,acession_2[i1])
                                sheet.write(row,10,defn_2[i1],red)
                                sheet.write(row,11,evalue_2[i1])
                            
                            if defn_1[i1] not in defn_2: 
                                sheet.write(row,5,acession_1[i1])
                                sheet.write(row,6,defn_1[i1])
                                sheet.write(row,7,evalue_1[i1])
                                
                            if defn_2[i1] not in defn_1: 
                                sheet.write(row,9,acession_2[i1])
                                sheet.write(row,10,defn_2[i1])
                                sheet.write(row,11,evalue_2[i1])
                            
                            row+=1
                            
                except BaseException: pass
                            
            print('book created')    
            book.close()


    def blast_uni(self,file): # blast to a single sequence
        
        ls_seq=[]
        for f in range(len(file)):
            seq=''
            try:
                book=ex.Workbook(str(file[f])+'.xlsx')
                print(file[f])
                sheet=book.add_worksheet(file[f])
                sheet.set_column(2,2,65)
                sheet.set_column(3,3,65)
                seq=open('files'+file[f]+'.txt','r').read()
          
                linha_ini=book.add_format({'bg_color':'#4B8A08'})
                sheet.set_row(0, cell_format=linha_ini)

                row=1
            
            except FileNotFoundError: pass
            
            ls_seq.append((file, seq))
            
            try:
                self.nuc(seq,file[f])
            except BaseException: pass

            
            try:
                acession_1, defn_1, evalue_1=self.info_nuc('blast'+str(file[f])+'.xml')
                
                for i1 in range(len(defn_1)):                        
                    sheet.write(row,2,acession_1[i1])
                    sheet.write(row,3,defn_1[i1])
                    sheet.write(row,4,evalue_1[i1])
                                            
                    row+=1
                    
            except BaseException: pass
                            
            print('book created')    
            book.close()
        return ls_seq #retunr a list with the number of the sequence a the sequence



    def blast_1x(self,aj,nome,seq): # blast to a split sequence without comparing

        book=ex.Workbook(aj+'.xlsx')
        print(aj)
        sheet=book.add_worksheet(aj)
        sheet.set_column(2,2,65)
        sheet.set_column(3,3,65)
        
        linha_ini=book.add_format({'bg_color':'#4B8A08'}) 
        sheet.set_row(0, cell_format=linha_ini)
        sheet.write(0,1,nome)  #write the id from the original sequence
        
        row=1
        
        try:
            self.nuc(seq,nome)
        except BaseException: pass
            
        try:
            acession_1, defn_1, evalue_1=self.info_nuc('blast'+str(nome)+'.xml')
            
            for i1 in range(len(defn_1)):                        
                sheet.write(row,2,acession_1[i1])
                sheet.write(row,3,defn_1[i1])
                sheet.write(row,4,evalue_1[i1])
                                        
                row+=1
                
        except BaseException: pass
                            
        print('book created')    
        book.close()
    
    def blast_f(self,ori,fin): #compare two sequence without splited them
        
        book=ex.Workbook(str(ori[0]+'_f.xlsx'))
        print(str(ori[0]))
        sheet=book.add_worksheet()
        linha_ini=book.add_format({'bg_color':'#4B8A08'})
        bold=book.add_format({'bold':True})
        red=book.add_format({'color':'red'}) 
        sheet.set_row(0, cell_format=linha_ini)
        sheet.write(0,1,str(ori[0])+'-'+str(fin[0]))  # write the id from the original sequence and the two fragemnts id's
            
        row=1
            
        
        self.nuc(ori[1],0) # blast-> original sequence
        self.nuc(fin[1],1) # blast -> sequence from fragmnets

         
        try:
            acession_1, defn_1, evalue_1=self.info_nuc('blast0.xml')
            acession_2, defn_2, evalue_2=self.info_nuc('blast1.xml')
            
                
            for i1 in range(len(defn_1)):
                if defn_1[i1]==defn_2[i1]:
                            
                    sheet.write(row,2,acession_1[i1])
                    sheet.write(row,3,defn_1[i1],bold)
                    sheet.write(row,4,evalue_1[i1])
                            
                    sheet.write(row,6,acession_2[i1])
                    sheet.write(row,7,defn_2[i1],bold)
                    sheet.write(row,8,evalue_2[i1])
                            
                    row+=1
                        
                elif defn_1[i1]!=defn_2[i1]: 
                    if defn_1[i1] in defn_2:
                        sheet.write(row,2,acession_1[i1])
                        sheet.write(row,3,defn_1[i1],red)
                        sheet.write(row,4,evalue_1[i1])
                            
                    if defn_2[i1] in defn_1:
                        sheet.write(row,6,acession_2[i1])
                        sheet.write(row,7,defn_2[i1],red)
                        sheet.write(row,8,evalue_2[i1])
                            
                    if defn_1[i1] not in defn_2: 
                        sheet.write(row,2,acession_1[i1])
                        sheet.write(row,3,defn_1[i1])
                        sheet.write(row,4,evalue_1[i1])
                                
                    if defn_2[i1] not in defn_1: 
                        sheet.write(row,6,acession_2[i1])
                        sheet.write(row,7,defn_2[i1])
                        sheet.write(row,8,evalue_2[i1])
                            
                    row+=1
                            
        except BaseException: pass
                            
        print('book created')    
        book.close()


        

  






