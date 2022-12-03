#  T2T_Assembly
##  Data preparation  
Pacbio Hifi data: 001.ccs.bam, 001.ccs.bam.pbi
###  Step1 Extraction hifi.fastq.gz data  
```
conda install -c hcc smrtlink-tools  
or
wget https://www.pacb.com/support/software-downloads/  
```  
Using:   
```
bam2fastq -o hifiasm.fq.gz 001.ccs.bam  
```  
### Step2 Hifiasm haplotype typing  
Hifiasm offical website and usage: https://hifiasm.readthedocs.io/en/latest/hic-assembly.html
Githup download ZIP: https://github.com/chhylp123/hifiasm , suggested latest version 0.16.1-r375.  
```  
hifiasm -o hifiasm.asm --primary -t 32 hifiasm.fq.g  
```  
Generate files：hifiasm.asm.p_ctg.gfa  hifiasm.asm.a_ctg, next, replace the .gfa file with a .fa file  
```
awk '/^S/{print ">"$2;print $3}' < hifiasm.asm.p_ctg.gfa> > hifiasm.fa  
```  
###  Step3 Using mummer, according to reference correct contigs, adjust order and orientation
Install  
```  
./configure --prefix=/path/to/installation  
make  
make install  
```
Using: https://github.com/mummer4/mummer 
```  
nucmer --mum -t 10 -p output hifiasm.fa reference.fa  
delta-filter -i 95 -l 10000 -q output.delta > output.delta-filter  
mummerplot -t png -s large -p output output.delta-filter  
show-coords -T -q -H output.delta-filter > coord.txt  
```  
Assemble scaffold by manually adjusting according to the coord.txt. scaffold.fa
###  Step4 Using Minimap2 for comparison and verification  
Using:https://github.com/lh3/minimap2  
Install  
```  
git clone https://github.com/lh3/minimap2
cd minimap2 && make  
```    
PacBio HiFi/CCS genomic reads (v2.19 or later)  
```  
./minimap2 -ax map-hifi scaffold.fa pacbio-ccs.fq.gz > aln.sam  
```  
###  Step5 After comparison, the .sam file is obtained, and subsequent analysis needs to convert .sam to .bam  
Install and using 
```  
conda install samtools  
samtools view -@10 -b aln.sam > aln.bam  
samtools sort -O bam -o aln.sorted.bam aln.bam  
samtools index aln.sorted.bam  
```  
