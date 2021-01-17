import penguins as pg
from penguins.private import nmrd
from penguins.private import Andrographolide as Andro
import numpy as np

p = nmrd() / "201115-7a-c13-sehsqc-full"

standalone_clipc = pg.read(p, 4)

read_noah = lambda expno: [pg.read(p, e) for e in (expno * 1000 + 1,
                                                   expno * 1000 + 2)]
[s, ed_s, crk4, ed_crk4,
 spv14, ed_spv14, spv24, ed_spv24,
 crk8, ed_crk8, spv18, ed_spv18, spv28, ed_spv28] = [read_noah(x)
                                                     for x in range(11, 25)]

def hsqc_rel(ds, ref_ds, edited):
    df = Andro.hsqc.rel_ints_df(dataset=ds, ref_dataset=ref_ds, edited=edited)
    m = df.groupby("mult").mean()
    return m["int"].tolist()
def cosy_rel(ds):
    df = Andro.cosy.rel_ints_df(dataset=ds, ref_dataset=standalone_clipc)
    m = df.mean()
    return m["int"].tolist()
def p_hsqc_cosy_rel(dss, ref_dss, edited):
    hsqcr = hsqc_rel(dss[0], ref_dss[0], edited=edited)
    cosyr = cosy_rel(dss[1])
    allr = [*hsqcr, cosyr]
    fs = lambda f: f"{f:.2f}"
    print(" & ".join(map(fs, allr)) + " \\\\")

p_hsqc_cosy_rel(s    , s, False)
p_hsqc_cosy_rel(crk8 , s, False)
p_hsqc_cosy_rel(spv18, s, False)
p_hsqc_cosy_rel(spv28, s, False)
p_hsqc_cosy_rel(crk4 , s, False)
p_hsqc_cosy_rel(spv14, s, False)
p_hsqc_cosy_rel(spv24, s, False)

p_hsqc_cosy_rel(ed_s    , ed_s, True)
p_hsqc_cosy_rel(ed_crk8 , ed_s, True)
p_hsqc_cosy_rel(ed_spv18, ed_s, True)
p_hsqc_cosy_rel(ed_spv28, ed_s, True)
p_hsqc_cosy_rel(ed_crk4 , ed_s, True)
p_hsqc_cosy_rel(ed_spv14, ed_s, True)
p_hsqc_cosy_rel(ed_spv24, ed_s, True)
