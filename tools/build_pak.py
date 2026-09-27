#!/usr/bin/env python3
"""Gera um PAK Unreal V11 (índice criptografado, entradas sem compressão) a partir de uma pasta — equivalente a
`repak --aes-key K pack <pasta> <saida.pak> --version V11 --path-hash-seed 3911529124`, sem precisar do repak.exe.

  python tools/build_pak.py --input <pasta raiz com ProjectTT/...> --output <arquivo.pak> --key-file <arquivo com 64 hex>
      [--mount-point ../../../] [--path-hash-seed 3911529124] [--verify]

Formato reproduzido do código-fonte do repak 0.2.3 (pak.rs/entry.rs/data.rs/footer.rs). Só para PAKs pequenos de dados
(tabelas CSV); não implementa compressão.
"""
import argparse, hashlib, os, struct, sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
MAGIC=0x5A6F12E1; VERSION=11
def fstr(s):
    if s=='' or s.isascii(): b=s.encode(); return struct.pack('<I',len(b)+1)+b+b'\0'
    u=s.encode('utf-16-le'); return struct.pack('<i',-(len(u)//2+1))+u+b'\0\0'
def fnv64_path(path,seed):
    h=(0xcbf29ce484222325+seed)&0xFFFFFFFFFFFFFFFF
    for b in path.lower().encode('utf-16-le'):
        h^=b; h=(h*0x00000100000001b3)&0xFFFFFFFFFFFFFFFF
    return h
def pad16(b): return b+b'\0'*((-len(b))%16)
def aes_ecb(key,b):
    e=Cipher(algorithms.AES(key),modes.ECB()).encryptor(); return e.update(b)+e.finalize()
def sha1(b): return hashlib.sha1(b).digest()
def split_child(p):
    if p in('/',''): return None
    q=p[:-1] if p.endswith('/') else p
    i=q.rfind('/')
    return (q[:i+1],q[i+1:]) if i>=0 else ('/',q)
def build(input_dir,output,key,mount_point,seed):
    files=[]
    for root,_,names in os.walk(input_dir):
        for n in names: files.append(os.path.join(root,n))
    rel=sorted(os.path.relpath(f,input_dir).replace(os.sep,'/') for f in files)
    out=bytearray(); entries=[]  # (path, offset, size, hash)
    for r in rel:
        data=open(os.path.join(input_dir,r),'rb').read()
        off=len(out); h=sha1(data)
        out+=struct.pack('<QQQI',0,len(data),len(data),0)+h+b'\0'+struct.pack('<I',0)  # header 53 bytes
        out+=data; entries.append((r,off,len(data),h))
    index_offset=len(out)
    encoded=bytearray(); offsets=[]
    for r,off,size,h in entries:
        offsets.append(len(encoded))
        assert off<=0xFFFFFFFF and size<=0xFFFFFFFF
        encoded+=struct.pack('<III',(1<<29)|(1<<30)|(1<<31),off,size)
    mp=fstr(mount_point)
    before=len(mp)+8+4+4+(8+8+20)+4+(8+8+20)+4+len(encoded)+4
    before=(before+15)&~15
    phi_off=index_offset+before
    phi=struct.pack('<I',len(entries))+b''.join(struct.pack('<QI',fnv64_path(r,seed),o) for (r,_,_,_),o in zip(entries,offsets))+struct.pack('<I',0)
    phi=pad16(phi); phi_hash=sha1(phi); phi_enc=aes_ecb(key,phi)
    fdi_off=phi_off+len(phi_enc)
    dirs={}
    for (r,_,_,_),o in zip(entries,offsets):
        p=r
        while (sc:=split_child(p)) is not None:
            p=sc[0]; dirs.setdefault(p,{})
        d,f=split_child(r); dirs.setdefault(d,{})[f]=o
    fdi=struct.pack('<I',len(dirs))
    for d in sorted(dirs):
        fdi+=fstr(d)+struct.pack('<I',len(dirs[d]))
        for f in sorted(dirs[d]): fdi+=fstr(f)+struct.pack('<I',dirs[d][f])
    fdi=pad16(fdi); fdi_hash=sha1(fdi); fdi_enc=aes_ecb(key,fdi)
    idx=mp+struct.pack('<IQ',len(entries),seed)+struct.pack('<IQQ',1,phi_off,len(phi_enc))+phi_hash+struct.pack('<IQQ',1,fdi_off,len(fdi_enc))+fdi_hash+struct.pack('<I',len(encoded))+encoded+struct.pack('<I',0)
    idx=pad16(idx); assert len(idx)==before, (len(idx),before)
    idx_hash=sha1(idx); idx_enc=aes_ecb(key,idx)
    out+=idx_enc+phi_enc+fdi_enc
    footer=b'\0'*16+b'\x01'+struct.pack('<IIQQ',MAGIC,VERSION,index_offset,len(idx_enc))+idx_hash+b'\0'*160
    assert len(footer)==221
    out+=footer
    open(output,'wb').write(out)
    return len(entries),len(out)
def main():
    a=argparse.ArgumentParser(); a.add_argument('--input',required=True); a.add_argument('--output',required=True); a.add_argument('--key-file',required=True)
    a.add_argument('--mount-point',default='../../../'); a.add_argument('--path-hash-seed',type=int,default=3911529124)
    o=a.parse_args()
    key=bytes.fromhex(open(o.key_file,encoding='utf-8').read().strip().removeprefix('0x'))
    assert len(key)==32,'chave deve ter 64 hex'
    n,size=build(o.input,o.output,key,o.mount_point,o.path_hash_seed)
    print(f'{o.output}: {n} entradas, {size} bytes, sha256 {hashlib.sha256(open(o.output,"rb").read()).hexdigest()}')
if __name__=='__main__': main()
