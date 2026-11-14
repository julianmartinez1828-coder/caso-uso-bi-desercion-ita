import pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams["font.family"]="DejaVu Sans"
df=pd.read_csv("matriculas_ita.csv"); u=df[df.periodo=="2026-1"]
AZ="#1F4E79"; GR="#5B6770"; CL="#DCE6F1"
# Fig flujo
fig,ax=plt.subplots(figsize=(11,4.2)); ax.set_xlim(0,11); ax.set_ylim(0,4.2); ax.axis("off")
cols=[("Fuentes de datos",["Sistema académico (SIA)","Moodle (LMS)","Cartera y pagos","Encuesta de Bienestar","Tickets PQRS"]),
("ETL",["Extracción de fuentes","Limpieza y validación","Integración por matrícula","Carga por periodo"]),
("Data Warehouse",["Hecho: matrícula","Dim. tiempo","Dim. programa","Dim. sede","Dim. estudiante"]),
("Modelo analítico",["Cálculo de KPI","Bandas de asistencia","Regla de riesgo alto"]),
("Dashboard",["Tarjetas KPI","Gráficos y tabla","Filtros y periodo"]),
("Decisiones",["Alertas tempranas","Tutorías y acuerdos","Seguimiento por sede"])]
w=1.5; gap=0.33
for i,(t,items) in enumerate(cols):
    x=0.1+i*(w+gap)
    ax.add_patch(FancyBboxPatch((x,0.25),w,3.7,boxstyle="round,pad=0.02,rounding_size=0.08",fc="white",ec=AZ,lw=1.4))
    ax.add_patch(FancyBboxPatch((x,3.35),w,0.6,boxstyle="round,pad=0.02,rounding_size=0.08",fc=AZ,ec=AZ))
    ax.text(x+w/2,3.65,t,ha="center",va="center",color="white",fontsize=8.2,fontweight="bold")
    for j,it in enumerate(items):
        ax.text(x+w/2,2.95-j*0.52,it,ha="center",va="center",fontsize=6.4,color="#222",
                bbox=dict(boxstyle="round,pad=0.3",fc=CL,ec="none"))
    if i<5: ax.annotate("",xy=(x+w+gap-0.03,2.0),xytext=(x+w+0.04,2.0),arrowprops=dict(arrowstyle="-|>",color=GR,lw=1.6))
fig.savefig("fig_flujo.png",dpi=200,bbox_inches="tight"); plt.close()

# Dashboard
fig=plt.figure(figsize=(11,7.6)); fig.patch.set_facecolor("#F4F6F8")
fig.text(0.03,0.955,"Tablero de permanencia estudiantil — Instituto Tecnológico Andino",fontsize=14,fontweight="bold",color=AZ)
for k,t in enumerate(["Periodo: 2026-1 ▾","Sede: Todas ▾","Programa: Todos ▾","Modalidad: Todas ▾","Semestre: Todos ▾"]):
    fig.text(0.03+k*0.19,0.905,t,fontsize=8.5,color="#222",bbox=dict(boxstyle="round,pad=0.45",fc="white",ec="#B8C2CC"))
kp=[("Tasa de deserción",f"{u.desertor.mean()*100:.1f} %".replace(".",","),"+1,5 pp vs. 2025-2"),
("Aprobación de créditos",f"{u.creditos_aprobados.sum()/u.creditos_inscritos.sum()*100:.1f} %".replace(".",","),"créditos aprobados / inscritos"),
("Asistencia promedio",f"{u.asistencia_pct.mean():.1f} %".replace(".",","),"meta: 85 %"),
("Estudiantes en mora",f"{(u.en_mora=='Sí').mean()*100:.1f} %".replace(".",","),"393 de 1.820"),
("Riesgo alto",f"{u.riesgo_alto.sum()}","promedio < 3,0 y asistencia < 75 %")]
for k,(a,b,c) in enumerate(kp):
    ax=fig.add_axes([0.03+k*0.19,0.735,0.175,0.125]); ax.set_facecolor("white"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color("#D0D7DE")
    ax.text(0.06,0.78,a,fontsize=8.5,color=GR,transform=ax.transAxes)
    ax.text(0.06,0.38,b,fontsize=17,fontweight="bold",color=AZ,transform=ax.transAxes)
    ax.text(0.06,0.10,c,fontsize=7,color=GR,transform=ax.transAxes)
def sty(ax,t):
    ax.set_title(t,fontsize=9.5,loc="left",fontweight="bold",color="#222"); ax.set_facecolor("white")
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7.5)
g=df.groupby("periodo").desertor.mean()*100
ax=fig.add_axes([0.06,0.40,0.40,0.26]); sty(ax,"Tasa de deserción por periodo (%)")
ax.plot(g.index,g.values,color=AZ,marker="o",lw=2); ax.set_ylim(0,22)
for x,y in zip(g.index,g.values): ax.text(x,y+1,f"{y:.1f}".replace(".",","),ha="center",fontsize=7.5)
p=(u.groupby("programa").desertor.mean()*100).sort_values()
ax=fig.add_axes([0.66,0.40,0.31,0.26]); sty(ax,"Deserción por programa, 2026-1 (%)")
ax.barh(p.index,p.values,color=AZ); ax.set_xlim(0,27)
for y,v in enumerate(p.values): ax.text(v+0.4,y,f"{v:.1f}".replace(".",","),va="center",fontsize=7.5)
u2=u.assign(banda=pd.cut(u.asistencia_pct,[0,70,80,90,101],right=False,labels=["Menos de 70 %","70–79 %","80–89 %","90 % o más"]))
b=u2.groupby("banda",observed=True).desertor.mean()*100
ax=fig.add_axes([0.06,0.06,0.40,0.25]); sty(ax,"Deserción según asistencia, 2026-1 (%)")
ax.bar(b.index.astype(str),b.values,color=AZ,width=0.6); ax.set_ylim(0,38)
for x,v in enumerate(b.values): ax.text(x,v+0.8,f"{v:.1f}".replace(".",","),ha="center",fontsize=7.5)
s=u.groupby("sede").agg(m=("desertor","size"),d=("desertor","sum"),t=("desertor","mean"),mo=("en_mora",lambda z:(z=="Sí").mean()),a=("asistencia_pct","mean"))
ax=fig.add_axes([0.52,0.06,0.45,0.25]); ax.axis("off"); ax.set_title("Detalle por sede, 2026-1",fontsize=9.5,loc="left",fontweight="bold")
cell=[[i,f"{r.m:,.0f}".replace(",","."),int(r.d),f"{r.t*100:.1f} %".replace(".",","),f"{r.mo*100:.1f} %".replace(".",","),f"{r.a:.1f} %".replace(".",",")] for i,r in s.iterrows()]
tb=ax.table(cellText=cell,colLabels=["Sede","Matriculados","Desertores","Deserción","En mora","Asistencia"],loc="center",cellLoc="center")
tb.auto_set_font_size(False); tb.set_fontsize(8); tb.scale(1,1.7)
for (r,c),ce in tb.get_celld().items():
    ce.set_edgecolor("#D0D7DE")
    if r==0: ce.set_facecolor(AZ); ce.set_text_props(color="white",fontweight="bold")
fig.savefig("fig_dashboard.png",dpi=200,facecolor=fig.get_facecolor()); plt.close()
print(s.round(3)); print(g.round(2))
