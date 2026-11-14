import numpy as np, pandas as pd
rng=np.random.default_rng(2026)
periodos=["2023-1","2023-2","2024-1","2024-2","2025-1","2025-2","2026-1"]
fechas=["2023-02-06","2023-08-08","2024-02-05","2024-08-05","2025-02-03","2025-08-04","2026-02-02"]
base=[1620,1540,1710,1630,1780,1690,1820]
progs={"Tec. en Desarrollo de Software":(.24,.25),"Tec. en Gestión Empresarial":(.20,0),"Tec. en Logística":(.14,.10),
"Tec. en Contabilidad y Finanzas":(.16,-.05),"Tec. en Mercadeo Digital":(.14,.15),"Téc. en Sistemas y Redes":(.12,.30)}
sedes={"Chapinero":(.38,-.15),"Kennedy":(.34,.20),"Suba":(.28,.05)}
rows=[];n=0
for i,(p,f,b) in enumerate(zip(periodos,fechas,base)):
    for _ in range(b):
        n+=1
        prog=rng.choice(list(progs),p=[v[0] for v in progs.values()])
        sede=rng.choice(list(sedes),p=[v[0] for v in sedes.values()])
        mod=rng.choice(["Presencial","Virtual"],p=[.68,.32])
        jor=rng.choice(["Diurna","Nocturna"],p=[.55,.45])
        sem=int(rng.choice([1,2,3,4,5,6],p=[.27,.21,.17,.14,.11,.10]))
        trab=rng.choice(["Sí","No"],p=[.62,.38] if jor=="Nocturna" else [.35,.65])
        fin=rng.choice(["Contado","Crédito ICETEX","Crédito directo","Beca"],p=[.38,.22,.30,.10])
        pm=.12+.012*i+(.10 if fin=="Crédito directo" else 0)
        mora="Sí" if rng.random()<pm else "No"
        asis=float(np.clip(rng.normal(84-(4 if trab=="Sí" else 0)-(3 if mod=="Virtual" else 0)-0.5*i,9),35,100))
        prom=float(np.clip(rng.normal(3.55+ (asis-82)*0.025,0.45),1.0,5.0))
        lms=float(np.clip(rng.normal(5.5+(asis-82)*0.08+(1.5 if mod=="Virtual" else 0),2),0,15))
        z=-3.15+.075*i+progs[prog][1]+sedes[sede][1]+(.55 if sem==1 else .30 if sem==2 else 0)+(.25 if mod=="Virtual" else 0)\
          +(.15 if jor=="Nocturna" else 0)+(.95 if mora=="Sí" else 0)-(asis-82)*.055-(prom-3.5)*.9
        des=rng.random()<1/(1+np.exp(-z))
        cred=int(rng.choice([14,16,18]))
        apro=int(round(cred*np.clip((prom-1.8)/1.9,0,1))) if not des else int(round(cred*np.clip((prom-2.4)/2.2,0,1)))
        rows.append(dict(id_matricula=f"M{n:06d}",periodo=p,fecha_inicio=f,sede=sede,programa=prog,modalidad=mod,jornada=jor,
          semestre=sem,trabaja=trab,financiacion=fin,en_mora=mora,asistencia_pct=round(asis,1),promedio=round(prom,2),
          accesos_lms_semana=round(lms,1),creditos_inscritos=cred,creditos_aprobados=apro,estado="Desertor" if des else "Activo",
          desertor=int(des)))
df=pd.DataFrame(rows)
df["riesgo_alto"]=((df.promedio<3.0)&(df.asistencia_pct<75)).astype(int)
df.to_csv("matriculas_ita.csv",index=False,encoding="utf-8-sig")
pd.set_option("display.width",200)
print(len(df), df.desertor.mean())
g=df.groupby("periodo").agg(mat=("desertor","size"),des=("desertor","sum"),tasa=("desertor","mean"),prom=("promedio","mean"),asis=("asistencia_pct","mean"),mora=("en_mora",lambda s:(s=="Sí").mean()),riesgo=("riesgo_alto","sum"))
print(g.round(4))
u=df[df.periodo=="2026-1"]
for c in ["programa","sede","semestre","modalidad","jornada","en_mora","financiacion","trabaja"]:
    print(u.groupby(c).desertor.agg(["size","sum","mean"]).round(3))
u=u.assign(banda=pd.cut(u.asistencia_pct,[0,70,80,90,101],right=False,labels=["<70","70-79","80-89","90+"]))
print(u.groupby("banda").desertor.agg(["size","sum","mean"]).round(3))
print(u.groupby("riesgo_alto").desertor.agg(["size","sum","mean"]).round(3))
print(u.groupby("estado")[["promedio","asistencia_pct","accesos_lms_semana"]].mean().round(2))
print((u.creditos_aprobados.sum()/u.creditos_inscritos.sum()).round(4))
s12=u[u.semestre<=2]; print(len(s12),s12.desertor.sum(),u.desertor.sum())
