# -*- coding: utf-8 -*-
"""
Created on Thu May 31 17:24:22 2018

@author: diana
"""

from nn import ncbi
from nn import infos
from nn import excel



blast=ncbi()
ler=infos()
excel=excel()


   
# =============================================================================
#    Look for patterns
# =============================================================================
    
perc=[50,40,30,20,10]
file=[] # name files
    
excel.blast_2x(file,perc)



