#!/usr/bin/python3

# Copyright (c) 2019, Denis Mingulov
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of vcfstr2111 nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import getopt
import gzip
import builtins

def show_help():
    print ('vcfstr2111.py --regions <STR info .bed file> --str-vcf <VCF with STRs>')

def read_bed(filename):
    out = {}
    with open(filename, 'rt') as f:
        for line in f:
            info = line.strip().split("\t")
            baselen = int(info[3])
            reflen = float(info[4])
            names = info[5]
            for name in names.split('/'):
                out[name] = (baselen, reflen)
    return out

def read_vcf(filename):
    out = {}
    m = builtins
    if filename.endswith('.gz'):
        m = gzip
    with m.open(filename, 'rt') as f:
        for line in f:
            if not line.startswith('#'):
                info = line.strip().split("\t")
                ref = info[3]
                gen = info[4]
                strs = info[2]
                for str in strs.split('/'):
                    out[str] = (ref, gen)
    return out

def str_size(str, bed, vcf):
    if str not in bed:
        raise ValueError("STR %s is missing in BED file" % (str,))
    if str not in vcf:
        return None
    (baselen, reflen) = bed[str]
    (ref, gen) = vcf[str]
    if gen == '.':
        gen = ''

    val = len(gen) / baselen
    out = int(val)
    print("Len %d, baselen %d, val %f (reflen %f), out %d" % (len(gen), baselen, val, reflen, out))

    return out

def generate_y12(bed, vcf):
    val = ('DYS460', 'DYS393', 'DYS390', 'DYS19', 'DYS391', '!DYS385', 'DYS426', 'DYS388', 'DYS439.1', 'DYS439.2', 'DYS389I', 'DYS392', 'DYS389II')
    val = ('DYS390',)
    for str in val:
        if not str.startswith('!'):
            size = str_size(str, bed, vcf)
            if size is None:
                size = -1
            print("Str %s, size %d" % (str, size))

def show_y111(bed, vcf):
    generate_y12(bed, vcf)

def main(argv):
    bedfile = ''
    vcffile = ''
    try:
        opts, args = getopt.getopt(argv,"hr:s:",["regions=","str-vcf="])
    except getopt.GetoptError:
        show_help()
        sys.exit(0)
    for opt, arg in opts:
        if opt == '-h':
             show_help()
             sys.exit()
        elif opt in ("-r", "--regions"):
             bedfile = arg
        elif opt in ("-s", "--str-vcf"):
             vcffile = arg
    print('BED file is "%s", VCF file is "%s"' % (bedfile, vcffile))
    bed = read_bed(bedfile)
    vcf = read_vcf(vcffile)
    show_y111(bed, vcf)

if __name__ == "__main__":
    main(sys.argv[1:])
