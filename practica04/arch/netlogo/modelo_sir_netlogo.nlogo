; ============================================================
; Practica 004 - Modelo SIR en NetLogo (Python vs NetLogo)
; NetLogo genera su propia simulacion (botones Preparar/Avanzar)
; y IMPORTA los resultados de Python desde resultados_python.csv
; ============================================================
extensions [csv]

globals [
  beta gamma poblacion pasos
  datos-python datos-netlogo
]
turtles-own [estado-sir]

; Ecuaciones diferenciales de la guia (referencia matematica)
to-report derivadas-sir [susceptibles infectados recuperados]
  let total susceptibles + infectados + recuperados
  if total <= 0 [ error "La poblacion debe ser positiva" ]
  let contagios beta * susceptibles * infectados / total
  let recuperaciones gamma * infectados
  report (list (0 - contagios) (contagios - recuperaciones) recuperaciones)
end

to-report numero-reproductivo-basico
  if gamma <= 0 [ error "Gamma debe ser positiva" ]
  report beta / gamma
end

to preparar
  clear-all
  set beta 0.30
  set gamma 0.10
  set poblacion 100
  set pasos 100
  random-seed 42
  create-turtles poblacion [
    setxy random-xcor random-ycor
    set estado-sir "S"
    set color blue
    set shape "circle"
    set size 1.2
  ]
  let infectados-iniciales 5
  ask n-of infectados-iniciales turtles [ set estado-sir "I" set color red ]
  set datos-python []
  set datos-netlogo []
  reset-ticks
  guardar-registro
  show (word "S inicial=" count turtles with [estado-sir = "S"]
    ", I inicial=" count turtles with [estado-sir = "I"]
    ", R0=" numero-reproductivo-basico)
  show (word "dS, dI, dR iniciales: "
    (derivadas-sir (poblacion - infectados-iniciales) infectados-iniciales 0))
end

to avanzar
  if ticks >= pasos [ stop ]
  let infectados-anteriores count turtles with [estado-sir = "I"]
  let probabilidad-contagio (1 - ((1 - beta / poblacion) ^ infectados-anteriores))
  ; Agentsets separados: los recien infectados no se recuperan hasta el proximo paso.
  let infectados-actuales turtles with [estado-sir = "I"]
  let susceptibles-actuales turtles with [estado-sir = "S"]
  ask susceptibles-actuales [
    if random-float 1 < probabilidad-contagio [ set estado-sir "I" set color red ]
  ]
  ask infectados-actuales [
    if random-float 1 < gamma [ set estado-sir "R" set color green ]
  ]
  tick
  guardar-registro
  actualizar-grafica-local
end

to ejecutar-todo
  preparar
  repeat pasos [ avanzar ]
  cargar-python
  exportar-netlogo
end

to guardar-registro
  set datos-netlogo lput (list ticks
    (count turtles with [estado-sir = "S"])
    (count turtles with [estado-sir = "I"])
    (count turtles with [estado-sir = "R"])) datos-netlogo
end

to exportar-netlogo
  csv:to-file "resultados_netlogo.csv"
    (fput (list "tiempo" "susceptibles" "infectados" "recuperados") datos-netlogo)
  user-message "Se guardo resultados_netlogo.csv"
end

to cargar-python
  set datos-python cargar-serie "resultados_python.csv"
  actualizar-graficas-importadas
end

to-report cargar-serie [nombre-archivo]
  if not file-exists? nombre-archivo [
    user-message (word "Archivo no encontrado: " nombre-archivo
      ". Guarda el modelo en la misma carpeta que el CSV.")
    report []
  ]
  let filas csv:from-file nombre-archivo
  if empty? filas [ report [] ]
  let encabezado first filas
  if encabezado != (list "tiempo" "susceptibles" "infectados" "recuperados") [
    user-message (word "Encabezado inesperado: " encabezado)
    report []
  ]
  report but-first filas
end

to actualizar-grafica-local
  set-current-plot "SIR NetLogo"
  clear-plot
  graficar-series datos-netlogo
end

to actualizar-graficas-importadas
  set-current-plot "SIR Python"
  clear-plot
  graficar-series datos-python
  set-current-plot "Comparacion infectados"
  clear-plot
  graficar-columna datos-python 2 "Python"
  graficar-columna datos-netlogo 2 "NetLogo"
  set-current-plot "Comparacion susceptibles"
  clear-plot
  graficar-columna datos-python 1 "Python"
  graficar-columna datos-netlogo 1 "NetLogo"
  set-current-plot "Comparacion recuperados"
  clear-plot
  graficar-columna datos-python 3 "Python"
  graficar-columna datos-netlogo 3 "NetLogo"
end

to graficar-series [datos]
  graficar-columna datos 1 "S"
  graficar-columna datos 2 "I"
  graficar-columna datos 3 "R"
end

to graficar-columna [datos columna nombre-lapiz]
  set-current-plot-pen nombre-lapiz
  foreach datos [ fila -> plotxy (item 0 fila) (item columna fila) ]
end
@#$#@#$#@
GRAPHICS-WINDOW
200
65
398
263
-1
-1
6.0
1
10
1
1
1
0
1
1
1
-16
16
-16
16
0
0
1
ticks
30.0

BUTTON
10
10
190
43
1. Preparar
preparar
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
10
50
190
83
2. Avanzar (forever)
avanzar
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
10
90
190
123
Ejecutar todo (automatico)
ejecutar-todo
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
10
130
190
163
3. Cargar Python (CSV)
cargar-python
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
10
170
190
203
4. Exportar NetLogo (CSV)
exportar-netlogo
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
10
210
190
243
Actualizar graficas
actualizar-graficas-importadas
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
200
10
280
55
Susceptibles
count turtles with [estado-sir = "S"]
0
1
11

MONITOR
290
10
370
55
Infectados
count turtles with [estado-sir = "I"]
0
1
11

MONITOR
380
10
460
55
Recuperados
count turtles with [estado-sir = "R"]
0
1
11

MONITOR
470
10
550
55
Tiempo (ticks)
ticks
0
1
11

MONITOR
560
10
640
55
R0
numero-reproductivo-basico
2
1
11

PLOT
410
65
700
263
SIR NetLogo
Tiempo (pasos)
Personas
0.0
100.0
0.0
100.0
true
true
"" ""
PENS
"S" 1.0 0 -13345367 true "" ""
"I" 1.0 0 -2674135 true "" ""
"R" 1.0 0 -10899396 true "" ""

PLOT
710
65
1000
263
SIR Python
Tiempo (pasos)
Personas
0.0
100.0
0.0
100.0
true
true
"" ""
PENS
"S" 1.0 0 -13345367 true "" ""
"I" 1.0 0 -2674135 true "" ""
"R" 1.0 0 -10899396 true "" ""

PLOT
10
275
330
495
Comparacion infectados
Tiempo (pasos)
Personas
0.0
100.0
0.0
100.0
true
true
"" ""
PENS
"Python" 1.0 0 -955883 true "" ""
"NetLogo" 1.0 0 -8630108 true "" ""

PLOT
340
275
660
495
Comparacion susceptibles
Tiempo (pasos)
Personas
0.0
100.0
0.0
100.0
true
true
"" ""
PENS
"Python" 1.0 0 -955883 true "" ""
"NetLogo" 1.0 0 -8630108 true "" ""

PLOT
670
275
990
495
Comparacion recuperados
Tiempo (pasos)
Personas
0.0
100.0
0.0
100.0
true
true
"" ""
PENS
"Python" 1.0 0 -955883 true "" ""
"NetLogo" 1.0 0 -8630108 true "" ""
@#$#@#$#@
## QUE ES

Practica 004 (Simulacion, UNL): modelo SIR con N=100, I(0)=5, beta=0.30, gamma=0.10, 100 pasos.
NetLogo ejecuta su propia simulacion de agentes e IMPORTA el CSV generado por Python/SimPy para compararlos.

## COMO USARLO

1. Guardar este archivo en la MISMA carpeta que resultados_python.csv.
2. Pulsar "Ejecutar todo (automatico)" o bien: Preparar, Avanzar, Cargar Python.
3. Revisar las graficas de comparacion (infectados, susceptibles, recuperados).

@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

circle
false
0
Circle -7500403 true true 0 0 300

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105
@#$#@#$#@
NetLogo 6.4.0
@#$#@#$#@

@#$#@#$#@

@#$#@#$#@

@#$#@#$#@

@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
