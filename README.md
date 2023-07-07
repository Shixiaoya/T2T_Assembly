#  Methods for assembling high-quality genomes
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
Generate files：`hifiasm.asm.p_ctg.gfa` `hifiasm.asm.a_ctg`, next, replace the `.gfa` file with a `.fa` file  
```
awk '/^S/{print ">"$2;print $3}' hifiasm.asm.p_ctg.gfa > hifiasm.fa  
```  
###  Step3 Using mummer, according to reference correct contigs, adjust order and orientation
Install  
```  
wget https://gigenet.dl.sourceforge.net/project/mummer/mummer/3.23/MUMmer3.23.tar.gz
tar -xf MUMmer3.23.tar.gz
cd  MUMmer3.23
make install  
```
Using: https://github.com/mummer4/mummer 
```  
nucmer --mum -t 10 -p output hifiasm.fa reference.fa  
delta-filter -i 95 -l 10000 -q output.delta > output.delta-filter  
mummerplot -t png -s large -p output output.delta-filter  
show-coords -T -q -H output.delta-filter > coord.txt  
```  
Assemble scaffold by manually adjusting according to the `coord.txt`. `scaffold.fa`
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
###  Step5 After comparison, the SAM file is obtained, and subsequent analysis needs to convert SAM to BAM  
Install and using:  
Convert SAM to BAM  
Sort sorts the BAM files  
The sorted sequence is indexed and output as a `.bai` file  
```  
conda install samtools  
samtools view -@10 -b aln.sam > aln.bam  
samtools sort -O bam -o aln.sorted.bam aln.bam  
samtools index aln.sorted.bam  
```  
Import the bam file to IGV and see if reads is supported  
###  Step6 The gaps were filled using the sequencing read  
Statistics GAP and its location  
```  
python getgaps.py scaffols.fa > gaps.txt  
```  
Extract the corresponding position and 50kb before and after according to the chromosome location of the `gap.txt`, after obtaining the sequence file, the operation is the same as Step 5.  

Extract the sequence  
```  
samtools view -b sorted.bam chrID:start-end > gap01.sorted.bam  
samtools index gap01.sorted.bam  
```
Import IGV software, find and extract the sequence of gap region, create `gap.fa` file. Extract the `chrX.fa` file according to chromosome ID, each line is 200bp everywhere, and fill the gap sequence found in the gap area of each chromosome. After filling, convert `chrX_fill.fa` to a chromosome line
```
seqkit split -i -w 200 chrX.fa
vim chrX.fa   #filling
seqkit seq -w 0 chr_fill.fa > chrX_fill0.fa
```
Then use minimap to verify whether the filling is correct, as shown in Step4 and Step5
```
cat chr1_fill0.fa chr2_fill0.fa ...... chrX_fill0.fa > gap_free.fa
```
Merge all chromosomes to get the final `gap-free.fa` genome file



#  Citation  

