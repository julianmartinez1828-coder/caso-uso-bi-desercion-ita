import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
df=pd.read_csv("matriculas_ita.csv"); df["fecha_inicio"]=pd.to_datetime(df["fecha_inicio"])
cols=[("id_matricula","ID matrícula",14,"Identificador único de la matrícula (un registro por estudiante y periodo)"),
("periodo","Periodo",10,"Periodo académico, de 2023-1 a 2026-1"),
("fecha_inicio","Fecha de inicio",15,"Fecha de inicio del periodo; sirve para la segmentación temporal del tablero"),
("sede","Sede",13,"Chapinero, Kennedy o Suba"),
("programa","Programa",33,"Programa académico en el que está matriculado"),
("modalidad","Modalidad",13,"Presencial o Virtual"),
("jornada","Jornada",12,"Diurna o Nocturna"),
("semestre","Semestre",11,"Semestre que cursa (1 a 6)"),
("trabaja","Trabaja",10,"Sí / No: si el estudiante trabaja mientras estudia"),
("financiacion","Financiación",17,"Contado, Crédito ICETEX, Crédito directo o Beca"),
("en_mora","En mora",10,"Sí / No: si tiene cuotas vencidas en el periodo"),
("asistencia_pct","Asistencia (%)",15,"Porcentaje de asistencia a clases en el periodo (0 a 100)"),
("promedio","Promedio",11,"Promedio académico del periodo (escala 0,0 a 5,0)"),
("accesos_lms_semana","Accesos LMS por semana",17,"Promedio de ingresos semanales a Moodle"),
("creditos_inscritos","Créditos inscritos",14,"Créditos matriculados en el periodo"),
("creditos_aprobados","Créditos aprobados",14,"Créditos aprobados en el periodo"),
("estado","Estado",12,"Activo o Desertor (no renovó matrícula)"),
("desertor","Desertor (1/0)",13,"1 si desertó, 0 si continuó; facilita sumar y promediar"),
("riesgo_alto","Riesgo alto (1/0)",14,"1 si promedio < 3,0 y asistencia < 75 %; 0 en caso contrario")]
F="Arial"; AZ="1F4E79"
hf=Font(name=F,bold=True,color="FFFFFF",size=10); hfill=PatternFill("solid",fgColor=AZ)
thin=Side(style="thin",color="D0D7DE"); bd=Border(left=thin,right=thin,top=thin,bottom=thin)
band=PatternFill("solid",fgColor="F2F6FA")
wb=Workbook(); ws=wb.active; ws.title="Matriculas"
ws.append([c[1] for c in cols]); ws.row_dimensions[1].height=32
for r in df[[c[0] for c in cols]].itertuples(index=False): ws.append([v.to_pydatetime() if hasattr(v,"to_pydatetime") else v for v in r])
n=len(df)+1
for j,c in enumerate(cols,1):
    ws.column_dimensions[L(j)].width=c[2]
    h=ws.cell(1,j); h.font=hf; h.fill=hfill; h.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True); h.border=bd
left={"programa","sede","modalidad","jornada","financiacion","estado","id_matricula"}
fmt={"fecha_inicio":"dd/mm/yyyy","asistencia_pct":"0.0","promedio":"0.00","accesos_lms_semana":"0.0"}
bf=Font(name=F,size=10)
for row in ws.iter_rows(min_row=2,max_row=n):
    z=row[0].row%2==0
    for j,cell in enumerate(row):
        k=cols[j][0]; cell.font=bf; cell.border=bd
        cell.alignment=Alignment(horizontal="left" if k in left else "center")
        if k in fmt: cell.number_format=fmt[k]
        if z: cell.fill=band
ws.freeze_panes="B2"; ws.auto_filter.ref=f"A1:{L(len(cols))}{n}"

# Resumen con fórmulas
rs=wb.create_sheet("Resumen")
rs["A1"]="Resumen por periodo (calculado con fórmulas sobre la hoja Matriculas)"; rs["A1"].font=Font(name=F,bold=True,size=12,color=AZ)
heads=["Periodo","Matriculados","Desertores","Tasa de deserción","Asistencia promedio (%)","Promedio académico","Estudiantes en mora","% en mora","Riesgo alto","Aprobación de créditos"]
for j,h in enumerate(heads,1):
    c=rs.cell(3,j,h); c.font=hf; c.fill=hfill; c.border=bd; c.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
    rs.column_dimensions[L(j)].width=17
rs.row_dimensions[3].height=32
M=lambda col:f"Matriculas!${col}$2:${col}${n}"
ci={c[0]:L(i) for i,c in enumerate(cols,1)}
pers=sorted(df.periodo.unique())
for i,p in enumerate(pers):
    r=4+i; P=M(ci["periodo"])
    vals=[p,f'=COUNTIF({P},A{r})',f'=SUMIFS({M(ci["desertor"])},{P},A{r})',f'=C{r}/B{r}',
     f'=AVERAGEIFS({M(ci["asistencia_pct"])},{P},A{r})',f'=AVERAGEIFS({M(ci["promedio"])},{P},A{r})',
     f'=COUNTIFS({P},A{r},{M(ci["en_mora"])},"Sí")',f'=G{r}/B{r}',f'=SUMIFS({M(ci["riesgo_alto"])},{P},A{r})',
     f'=SUMIFS({M(ci["creditos_aprobados"])},{P},A{r})/SUMIFS({M(ci["creditos_inscritos"])},{P},A{r})']
    nf=[None,"#,##0","#,##0","0.0%","0.0","0.00","#,##0","0.0%","#,##0","0.0%"]
    for j,v in enumerate(vals,1):
        c=rs.cell(r,j,v); c.font=bf; c.border=bd; c.alignment=Alignment(horizontal="center")
        if nf[j-1]: c.number_format=nf[j-1]
r=4+len(pers)
tot=["Total",f"=SUM(B4:B{r-1})",f"=SUM(C4:C{r-1})",f"=C{r}/B{r}",f'=AVERAGE({M(ci["asistencia_pct"])})',f'=AVERAGE({M(ci["promedio"])})',f"=SUM(G4:G{r-1})",f"=G{r}/B{r}",f"=SUM(I4:I{r-1})",f'=SUM({M(ci["creditos_aprobados"])})/SUM({M(ci["creditos_inscritos"])})']
for j,v in enumerate(tot,1):
    c=rs.cell(r,j,v); c.font=Font(name=F,bold=True,size=10); c.border=bd; c.alignment=Alignment(horizontal="center"); c.fill=band
    if nf[j-1]: c.number_format=nf[j-1]
rs.freeze_panes="B4"

# Diccionario
d=wb.create_sheet("Diccionario")
d["A1"]="Diccionario de datos — Instituto Tecnológico Andino (caso ficticio)"; d["A1"].font=Font(name=F,bold=True,size=12,color=AZ)
d["A2"]="Datos simulados en Python para la Guía 11 (Casos de uso de BI). No corresponden a una institución real."; d["A2"].font=Font(name=F,italic=True,size=10)
for j,h in enumerate(["Columna","Nombre técnico","Descripción"],1):
    c=d.cell(4,j,h); c.font=hf; c.fill=hfill; c.border=bd; c.alignment=Alignment(horizontal="center")
for i,c in enumerate(cols):
    for j,v in enumerate([c[1],c[0],c[3]],1):
        x=d.cell(5+i,j,v); x.font=bf; x.border=bd; x.alignment=Alignment(wrap_text=True,vertical="top")
d.column_dimensions["A"].width=24; d.column_dimensions["B"].width=22; d.column_dimensions["C"].width=80
wb.save("Base_de_datos_ITA_matriculas.xlsx")
