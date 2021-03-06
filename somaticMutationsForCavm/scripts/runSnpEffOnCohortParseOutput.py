#!/usr/bin/env python

import argparse
import os
import re
import subprocess
import string

os.sys.path.insert(0, os.path.dirname(__file__) )

def findSampleID (vcfFile): # this isRADIA specific
    fin =open(vcfFile,'r')
    while 1:
        line = fin.readline()
        if line[0]!="#":
            return ""
        if string.find(line,"##SAMPLE=<")!=-1 and string.find (line,"TUMOR")!=-1:# this isRADIA specific
            if string.find(line,"SampleName=")!=-1:
                id =string.split(string.split (line,"SampleName=")[1],",")[0]
                return id
        else:
            continue
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputVcfDir", type=str,
                        help="Directory of input VCFs, with wildcards")
    parser.add_argument("-id", type=str, default="",
                        help="CAVM ID")
    args = parser.parse_args()

    for vcfFile in os.listdir(args.inputVcfDir):
        if re.search("\.vcf$", vcfFile):
            if args.id != "":
                cavmId = vcfFile.split("/")[-1]
            else:
                #tumorBarcode = re.split("[_\.]", vcfFile)[1]
                #cavmId = "-".join(tumorBarcode.split("-")[0:4])[:-1]
                cavmId= findSampleID (args.inputVcfDir+"/"+vcfFile)

            vcfPathname = args.inputVcfDir + "/" + vcfFile
            cmd = "export PATH="+ os.path.dirname(__file__)+"/:$PATH; runSnpEffAgainstRefSeq.bash "+vcfPathname +" | "+ os.path.dirname(__file__)+ "/parseSnpEffVcf.py "+cavmId
            subprocess.call(cmd, shell=True)
        

if __name__ == '__main__':
        main()
    

