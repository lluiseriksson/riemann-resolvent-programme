# La frontera analítica exacta tras la validación numérica del operador

Fecha: 2026-08-06. Documento base registrado por la mesa de campaña (Claude
Fable 5) a partir de la formulación del desk Codex; reducción residuo/gap
añadida y auditada por Codex. Contexto: piloto A3 verde, parrilla de producción
en curso. Este documento fija QUÉ quedaría por probar para que este carril
demostrara RH — y por qué ninguna parrilla finita puede probarlo.

## El objetivo mínimo, auditado

Sea ξ_λ el vector mínimo normalizado de la forma QW_λ completa (existencia y
discreción: Thm 3.6/Cor 3.7 de arXiv:2511.22755, probadas), y k_λ un
aproximante explícito elegido de modo que k̂_λ → Ξ. **Bastaría demostrar**:
existen escalares a_λ ≠ 0 tales que, para todo 0 ≤ η < 1/2,

    λ^η · ‖ a_λ ξ_λ − k_λ ‖_{L¹(d*u)}  →  0    (λ → ∞).

La palanca es correcta y elemental (verificada): para soporte en [λ^{-1}, λ],
|u^{-iz}| = u^{Im z} ≤ λ^{|Im z|}, luego sobre |Im z| ≤ η

    | a_λ ξ̂_λ(z) − k̂_λ(z) | ≤ λ^η ‖a_λ ξ_λ − k_λ‖_{L¹(d*u)},

y el límite daría convergencia uniforme de a_λ ξ̂_λ hacia Ξ en cada subfranja
cerrada de |Im z| < 1/2. Como los ξ̂ tienen solo ceros reales, Hurwitz
excluiría ceros no reales de Ξ: RH.

## Una reducción cuantitativa adicional: residuo/gap

La condición anterior puede reducirse a dos cantidades escalares que ya están
nombradas en `riemann-prime-resolvent/RiemannPrimeResolvent/SpectralDefect.lean`.
Esta es una reducción, no una verificación de esas cantidades para QW_λ.

Supongamos λ > 1 y trabajemos en

    H_λ = L²([λ⁻¹, λ], d*u).

Sea QW_λ una forma cerrada y acotada inferiormente, cuyo operador autoadjunto
asociado tiene valor propio mínimo simple E_λ, vector propio normalizado ξ_λ
y gap Δ_λ > 0 hasta el resto del espectro. Sea k_λ ≠ 0 del dominio de la forma,
κ_λ = k_λ / ‖k_λ‖₂, y sea

    r_λ = QW_λ[κ_λ] − E_λ ≥ 0

su exceso de Rayleigh. Entonces existe una fase e^{iθ_λ} tal que

    ‖e^{iθ_λ} ξ_λ − κ_λ‖₂ ≤ √(2 r_λ / Δ_λ).

En efecto, escribiendo κ_λ = c_λ ξ_λ + w_λ con w_λ ⟂ ξ_λ, el teorema
espectral da r_λ ≥ Δ_λ ‖w_λ‖₂². Tras elegir la fase para que c_λ ≥ 0,

    ‖e^{iθ_λ} ξ_λ − κ_λ‖₂²
      = 2(1 − |c_λ|)
      ≤ 2(1 − |c_λ|²)
      = 2 ‖w_λ‖₂².

Como la medida multiplicativa del intervalo es
∫_[λ⁻¹,λ] d*u = 2 log λ, Cauchy--Schwarz da, para
a_λ = ‖k_λ‖₂ e^{iθ_λ},

    ‖a_λ ξ_λ − k_λ‖₁
      ≤ 2 ‖k_λ‖₂ √(log λ · r_λ / Δ_λ).                 (RG)

Por tanto basta demostrar, para todo 0 ≤ η < 1/2,

    λ^η ‖k_λ‖₂ √(log λ · r_λ / Δ_λ) → 0.              (RG-η)

Una forma uniforme y fácil de auditar es obtener un q > 1/2 y C finito con

    ‖k_λ‖₂ √(2 r_λ / Δ_λ) ≤ C λ^{-q}.                 (RATE)

Entonces (RG-η) sigue de
λ^{η-q}√(log λ) → 0. Al parametrizar una sucesión cofinal λ_n comparable con
n, esto explica matemáticamente el umbral estricto `BeatsHalfThreshold` de
`RiemannPrimeResolvent/PublicationFrontier.lean`: no es decorativo; absorbe
exactamente la pérdida √(log λ) del paso L² → L¹ y deja margen para toda
subfranja η < 1/2.

La versión Galerkin añade el término de cola que ya aparece en
`rayleighGapDefect`; el producto √(2 log λ) debe multiplicar el defecto total.
La versión por residuo usa `residualGapDefect`, pero además debe certificar que
el valor propio aislado seleccionado es el fundamental: un residuo pequeño por
sí solo también puede aproximar un estado excitado.

### Qué aportan y qué no aportan los otros satélites

* `lean-transfer-matrix` prueba gaps explícitos para el Ising 1D y conserva
  hipótesis para modelos genéricos; no identifica su operador con QW_λ.
* `lean-os-positivity` prueba RP ⟺ núcleo PSD en el modelo de un enlace; no
  produce simplicidad, Δ_λ ni (RATE) para QW_λ.
* Los repos de árboles/Catalan/polímeros pueden servir para acotar la cola o el
  residuo solo después de construir una expansión convergente del operador
  concreto. Hoy no existe ese teorema de identificación en los repos.

Así, la nueva frontera escalar es inequívoca: certificar (RATE), junto con la
convergencia independiente k̂_λ → Ξ y la afirmación de ceros reales de los
aproximantes completos. Un contraejemplo a simplicidad/gap, o una sucesión con
λ^q·rayleighGapDefect no acotada para todo q > 1/2, mata esta subruta de tasa
potencial; no excluye por sí solo cualquier otra estimación de convergencia.

## Cuatro matices que el enunciado debe cargar (auditoría de esta mesa)

1. **La norma es L¹ respecto de d*u = du/u** (la medida de Haar
   multiplicativa); con du a secas la palanca no es la escrita.
2. **Hay DOS ingredientes, no uno**: el límite cuantitativo de arriba Y la
   convergencia k̂_λ → Ξ del propio aproximante — ahí es donde vive toda la
   cancelación aritmética primo-vs-arquimediano. Elegir k_λ no es gratis.
3. **Los ceros reales de ξ̂_λ (λ fijo, forma completa)** se obtienen en la
   fuente vía el límite N → ∞ del caso finito (Sec. 7, nota 2: convergencia
   det_reg uniforme sobre compactos) — AFIRMADO en la fuente, no probado según
   nuestra extracción. Hurwitz lo necesita.
4. **Este objetivo ES la conjetura abierta del programa de
   Connes–Consani–Moscovici** (su propia estrategia de la Sec. 7), cuantificada
   con la palanca λ^η. No es una reducción nueva ni un paso técnico menor: es
   el frente abierto del carril L2, en manos de sus autores desde 2021.

## Lo que la campaña T3 puede y no puede

* PUEDE: falsificar (un KILL mata el brazo concreto), acotar comportamientos a
  escalas sondeadas, y validar que el objeto implementado es el de la fuente
  (hecho: z₁ − γ₁ ≈ 4.8e−9 con los ceros consultados solo como benchmark
  posterior).
* NO PUEDE: probar el límite de arriba. Ninguna cantidad finita de puntos
  prueba un límite λ → ∞. `SURVIVE-AT-PROBED-SCALES` licencia exactamente
  "sin acumulación de baja energía a las escalas sondeadas", nunca
  sup < ∞ (design.md, cláusula de alcance).
* El T3 literal (sup del trazo del operador completo) es FALSO/vacuo — probado
  pen-and-paper en design.md §2.1; la campaña estudia la reformulación
  infrarroja operativa, y aun probada a toda escala quedarían T4 y la
  convergencia del determinante.

## Consecuencia para el programa

Con el operador validado numéricamente, la distancia a RH por este carril se
reduce EXACTAMENTE al límite cuantitativo de arriba (o una estimación de
determinantes equivalente). Es un problema de investigación de escala
años/abierto en la literatura, no una tarea de campaña. La regla permanente:
la importancia solo se transfiere por reducción probada; este documento
registra la reducción QUE FALTA, no una que exista.

## El argumento al absurdo completo (formulado por Codex, auditado 2026-08-06)

Cadena condicional VERIFICADA (dos verificadores adversariales independientes,
Fable 5; veredicto CORRECT_WITH_CAVEATS con las correcciones ya incorporadas
aquí). Supóngase que Ξ tiene un cero no real z₀. **Elíjase un disco cerrado D
alrededor de z₀, disjunto del eje real, sin ceros de Ξ en su frontera, Y
CONTENIDO EN LA SUBFRANJA ABIERTA |Im z| < 1/2** — esta última condición es
portante (sin ella la palanca λ^η no cierra) y está disponible
INCONDICIONALMENTE: todo cero de Ξ tiene |Im z| < 1/2 estricto, por el
producto de Euler en Re s > 1, Hadamard/de la Vallée Poussin en Re s = 1, y
la ecuación funcional para Re s ≤ 0 — entrada clásica de fuerza PNT que debe
citarse, no usarse en silencio. Si (RATE) valiera, entonces sobre ∂D:
|a_λξ̂_λ(z) − k̂_λ(z)| ≤ λ^η‖a_λξ_λ−k_λ‖₁ = O(λ^{η−q}√log λ) → 0; junto con
k̂_λ → Ξ uniforme en subfranjas cerradas, a_λξ̂_λ → Ξ uniformemente sobre ∂D.
Como min_{∂D}|Ξ| > 0 (frontera compacta sin ceros), Rouché — o Hurwitz con
multiplicidades — fuerza un cero de ξ̂_λ dentro de D para λ grande. Si los
ceros de ξ̂_λ son reales, contradicción con D ∩ ℝ = ∅. Luego Ξ no tendría
ceros no reales: RH.

El libro de premisas completo (a)–(j) fue auditado; los puntos (b)–(g), (i),
(j) están ESTABLECIDOS (ceros aislados, Ξ ≢ 0 con testigo ξ(1/2) ≈ 0.497,
mínimo positivo en frontera, restricción de subfranja a compactos, ξ̂_λ
entera por soporte compacto, a_λ = ‖k_λ‖₂e^{iθ} ≠ 0, aplicación de Rouché,
cuantificación sobre z₀). Quedan abiertas EXACTAMENTE CUATRO premisas:

1. **(RATE)**: ‖k_λ‖₂√(2r_λ/Δ_λ) = O(λ^{−q}), q > 1/2 — la caja.
2. **k̂_λ → Ξ uniforme en subfranjas cerradas** — y CON EL MISMO k_λ de
   (RATE): el acoplamiento mismo-k_λ es contenido real, no un tecnicismo
   (para el candidato natural la convergencia es barata, pero entonces (RATE)
   debe probarse para ESE k_λ; toda la cancelación primo-vs-arquimediano vive
   en esta pareja).
3. **Ceros reales de ξ̂_λ para la forma completa** — la transferencia N → ∞
   (fuente, Sec. 7 nota 2: AFIRMADA, no probada).
4. **Simplicidad/paridad del estado fundamental y gap Δ_λ > 0** del QW_λ
   concreto (T1 abierto).

## Dos atajos cerrados (verificados con computación exacta)

**Atajo 1 — "par + Fourier-invariante ⟹ ceros reales": FALSO, exacto.**
Con F f(y) = ∫f(x)e^{−2πixy}dx y h_n las funciones de Hermite normalizadas
(F h_n = (−i)ⁿ h_n; h₀ y h₄ pares con autovalor +1): f_C = h₄ + C·h₀ =
e^{−πx²}(Ax⁴ − Bx² + D_C) con A = (4/3)·2^{3/4}√3·π², B = 2·2^{3/4}√3·π,
D_C = 2^{1/4}(C + √6/4). Discriminante en w = z²:
Disc = −(16π²/3)(2√3·C − 3√2) < 0 ⟺ **C > C* = √6/2 ≈ 1.2247**. Para C = 2:
cuatro ceros no reales z = ±0.51157 ± 0.15157i (para C = 1, los cuatro
reales — el umbral es agudo). NOTA DE ALCANCE: f_C tiene orden 2 y Ξ orden 1;
el contraejemplo mata exactamente el atajo ingenuo y NADA contra argumentos
que usen orden ≤ 1 / género 0 / clase Laguerre–Pólya — donde vive RH.

**Atajo 2 — "PSD/Perron–Frobenius ⟹ simplicidad y gap": CERRADO en (2,6),
con el testigo correcto.** I es PSD y degenerada; diag(0,ε) es PSD con gap
arbitrario. Y la matriz implementada QW₂⁶ (ensamblaje del probe registrado,
dps 30, error de cuadratura ≤ 1e−77, mínima entrada 4.1e−3 — signos
robustos): 64 positivas / 14 negativas fuera de diagonal (convención
TRIÁNGULO SUPERIOR; el conjunto completo es 128/28). El conteo mixto NO
basta por sí solo para excluir un gauge diagonal de signos; el testigo que
SÍ lo prueba es el ciclo impar: el triángulo (n = −6,−5,−4) tiene sus tres
aristas negativas (−0.1551, −0.1900, −0.2249), producto −1, lo que mata el
objetivo todo-no-negativo; el triángulo (−6,−5,−2) tiene producto +1 y mata
el todo-no-positivo. Frustración masiva: 110 de 286 triángulos. Luego ningún
cambio diagonal de signos reduce QW₂⁶ a forma Perron–Frobenius. Alcance:
probado en (λ,N) = (2,6); otros puntos de la parrilla requerirían repetir el
censo.

Con esto, la ruta hacia RH por este carril queda en su forma terminal: un
absurdo condicional completo con CUATRO premisas abiertas nombradas, dos
atajos falsos cerrados con testigos exactos, y el instrumento de falsación
(la parrilla T3) corriendo. Nada de lo anterior demuestra RH ni lo pretende.

## Cierre del círculo: la caja (TP) y lo que ya está probado sobre ella

La "pista definitiva" negro/rojo — D^k b_n(x₀) = Σ_T W(T), W(T) ≥ 0,
Σ_T W(T) < ∞ — es EXACTAMENTE el lema (TP) con el que abrió este carril
(2026-08-05, `reduccion-al-absurdo-riemann.md` §4, y Prop. 4.1 del paper de
6 pp). Sobre esa caja este programa ya tiene tres resultados auditados que
cualquier intento futuro debe conocer antes de gastar una hora:

1. **Equivalencia**: [∀n,k: D^k b_n(x₀) ≥ 0] ⟺ RH por cada x₀ > 1/4 fijo
   (dictamen 2026-08-05; recíproco vía producto de Hadamard par; el paper la
   contiene entera). Probar la caja ES probar RH — "introducirla como
   hipótesis sería renombrar RH" es correcto y ya estaba medido.
2. **Determinación**: la medida representante es ÚNICA (Hausdorff), con
   átomos exactamente en v_j = x₀/(x₀+γ_j²) — los AGREGADOS de cualquier
   sistema de pesos válido SON los ceros; solo el reparto entre árboles es
   libre. El testigo canónico existe bajo RH (un átomo por par de ceros):
   (TP) es verdadera-pero-dura-de-certificar, no falsa.
3. **Barrera** (`barrera-bosques-factorizacion-rh.md`, verificada
   adversarialmente): ninguna prueba de la caja confinada a insumos
   invariantes bajo sustitución de sistema de primos (positividad de
   coeficientes Λ ≥ 0, estatus CM de las piezas arquimedianas, combinatoria
   de factorización/Catalan/polímeros) puede existir — los falsificados G₂ y
   DMV comparten todos esos insumos y su batería es FALSA. "Probar esta caja
   directamente desde los primos" con esa caja de herramientas está
   TEOREMÁTICAMENTE cerrado; una prueba real debe usar entrada no invariante
   (la ecuación funcional junto al producto de Euler, o localización de
   ceros).

Lo verificado hoy de la formulación Codex (citas verbatim comprobadas):
el repo de polímeros declara que empieza DESPUÉS de construido el peso y que
su forma no negativa es majorante del |coeficiente de Ursell|, no identidad
firmada (docs/paper/11-limitations.md:3, 02-polymer-systems.md:49); la
recursión de Schur por primos está en cuarentena como programa
(IDEAS-3-8-QUARANTINE.md:41); Connes–Kreimer no tiene aún coproducto,
bialgebra, antípodo ni consumidor (HYPOTHESIS_FRONTIER.md:148) — el
candidato natural a codificar la cancelación firmada no existe como teorema.

**El puente cuantitativo nuevo entre carriles** (aporte real de esta
formulación, verificado): la asignación ingenua de actividades primas da
Σ_{m≤λ²} Λ(m)/√m ~ 2λ (Chebyshev + sumación parcial), CRECIENTE, mientras
(RATE) exige un defecto o(λ^{−1/2}). Tomar valores absolutos — que es lo
único que la maquinaria Catalan/polímeros sabe hacer — destruye exactamente
la cancelación que ambas cajas necesitan. La identidad de cancelación
firmada específica (de QW_λ en el carril espectral; de los pesos W(T) en el
carril de bosques) es EL MISMO objeto ausente visto desde dos lados, y en
ambos la barrera/la estimación 2λ explican por qué ninguna contabilidad
positiva lo produce.

## La cuarta forma terminal: convergencia de momentos (MC) — auditada 2026-08-06

Formulada por Codex, verificada adversarialmente (Fable 5, veredicto
CORRECT_WITH_CAVEATS con las correcciones incorporadas aquí). Para D_m
autoadjunto finito y b_n^(m) = (x₀ⁿ/2)·Tr(D_m²+x₀I)^{−(n+1)}:

**Identidad incondicional (verificada, álgebra exacta):** con R = (D²+x₀)^{−1}
vale I − x₀R = D²R, y de ahí D^k b_n^(m) = ½Tr[x₀ⁿD^{2k}R^{n+k+1}] ≥ 0 —
factores conmutantes PSD, autovalor a autovalor x₀ⁿz^{2k}/(z²+x₀)^{n+k+1} ≥ 0.
Forma OS equivalente: b_n = ⟨Ω,TⁿΩ⟩ con T = x₀R, 0 ≤ T ≤ I, y
D^k b_n = ⟨Ω,Tⁿ(I−T)^kΩ⟩ ≥ 0. Cero contenido aritmético: vale para CUALQUIER
familia autoadjunta finita.

**Criterio (MC), verificado:** si b_n^(m) → b_n^Ξ(x₀) para CADA n (en un solo
x₀ > 1/4), entonces D^k b_n^Ξ ≥ 0 para todo n,k (cada desigualdad involucra
finitos términos — sin convergencia dominada, sin uniformidad, sin tasa: la
limpieza técnica genuina de esta forma) y el criterio de Hausdorff de un punto
da RH. Inventario completo de hipótesis: (a) un x₀ fijo; (b) el límite para
TODO n; (c) finitud (automática); (d) la identificación b_n^Ξ con las
derivadas de S_Ξ — donde entra TODA la aritmética; (e) el criterio de un
punto (re-derivado independientemente por el verificador).

**Calibración de honestidad (la corrección importante):** con T = x₀R,
b_n^(m) = (1/2x₀)·Tr T^{n+1}, así que (MC) dice exactamente que las medidas
espectrales ponderadas μ_m = (1/2x₀)Σ t_iδ_{t_i} convergen débilmente (en
[0,1], momentos = débil) a la ÚNICA medida de Hausdorff de b_n^Ξ — la medida
SOPORTADA EN LOS CEROS, átomo EN v_j = x₀/(x₀+γ_j²) con MASA 1/(x₀+γ_j²) por
par. **(MC) es re-empaquetado, no reducción**: quita el andamiaje (franjas,
q>1/2, Rouché) y deja intacto el contenido — equidistribución exacta de los
espectros finitos sobre los ceros. Cuarta forma equivalente:
(TP) ↔ (RATE) ↔ determinantes ↔ (MC).

**Matices registrados:** (1) la dirección del límite (λ,N) → m debe
registrarse para la familia biparamétrica (cautela U6); (2) b_0^(m) = S_IR
[conv:S-half] EXACTO solo si 0 no es autovalor de D″ (ξ_0 ≠ 0) — un punto así
falla la puerta de conteo y es INVALID, luego en todo punto J2-válido la
identidad es exacta; y S_IR es la MITAD de la traza de la prosa-T3 (factor 2,
nota U9); (3) **regla dura del testigo:** la monotonía completa son
INFINITAS desigualdades — el acuerdo numérico en finitos momentos NUNCA es
evidencia a favor de (MC); el testigo `mc_moments.py` (sha
4a2821a9d86703cc5e47ba428fa1b211477ad5db3bf812ade2b82e974ddf3033, solo
lectura, líneas MC-WITNESS, sin puertas) es un FALSIFICADOR y sonda de
consistencia: una desviación sistemática mataría el brazo concreto; la
convergencia observada no licencia nada.

## La quinta forma terminal: compacidad (SC) = bridgeA∘bridgeC — auditada 2026-08-06

Formulada por Codex, verificada adversarialmente (CORRECT_WITH_CAVEATS; las
DOS reparaciones del verificador ya incorporadas al enunciado):

**Criterio (SC), forma reparada.** Sea x₀ > 1/4 (portante: el criterio de un
punto es por x₀ > 1/4, ausente en la formulación original), T_m = x₀(D_m²+x₀)^{−1},
F_m(z) = (1/2x₀)Tr[T_m(I−zT_m)^{−1}] = ½Tr(D_m²+x₀(1−z))^{−1} (formas
verificadas iguales; holomorfa en |z| < 1). Si (1) sup_m F_m(0) < ∞ y
(2) F_m(z) → S_Ξ(x₀(1−z)) en un conjunto E ⊂ (−1,1) **con punto de
acumulación EN (−1,1)** (segunda reparación: E = {1−1/n} rompe el argumento
tal como estaba — la parte Stieltjes no es holomorfa en z = +1 si μ carga
t = 1), entonces RH. Prueba: masas = F_m(0) acotadas ⟹ Helly en [0,1] ⟹
límite débil subsecuencial μ ⟹ transformadas convergen puntualmente en
(−1,1) ⟹ identidad sobre un entorno conexo de (−1,1) donde S_Ξ(x₀(1−z)) es
holomorfa INCONDICIONALMENTE (0 < β < 1 y γ ≠ 0 impiden singularidad en w
real positivo — mismas entradas clásicas fuerza-PNT ya citables del registro)
⟹ coeficientes de Taylor = momentos de Hausdorff ⟹ batería ⟹ RH.

**Identificación bridgeC, precisa.** Condición (1) ES
`PrimeResolventData.uniform_bound` VERBATIM (misma convención S-half, mismo
x₀ marcado — el factor 2 respecto a la traza prosa-T3 viaja con el número,
nota U9). Condición (2) ocupa el hueco de T4 pero es MÁS DÉBIL en forma
(puntual sobre E vs uniforme en ventana) y MÁS FUERTE en contenido (nombra a
S_Ξ, que el repo difiere a bridgeC — `approx` solo acopla S a los
aproximantes primos P). (SC) no instancia literalmente
bridgeC → SlitPlaneStieltjesExtension: es una descarga alternativa del
COMPUESTO bridgeA∘bridgeC, con bridgeA sustituido por el criterio de un
punto (núcleo Lagarias 1999) en vez de la ruta de reflexión — aunque la μ
límite sí factoriza como testigo de SlitPlaneStieltjesExtension si se desea.

**Lo notable: ~el 70% de la prueba de (SC) YA está en Lean** en
`riemann-one-point-resolvent` para datos atómicos finitos — la construcción
de la medida compactificada, la igualdad EXACTA masa = valor en un punto
(`compactifiedStieltjesFiniteMeasure_mass_eq`), la compacidad de Helly vía
Prokhorov, la continuidad del núcleo en todo el plano cortado, la identidad
de transformadas, débil ⟹ puntual, y la batería finita de Hausdorff. NO
formalizado (y los ficheros lo declaran): extracción de subsucesión
(metrizabilidad), el puente del principio de identidad de E al disco, la
identidad de momentos a nivel de medida, TODA identificación con S_Ξ
(riemannXi no aparece en el subproyecto), y el criterio de un punto. La
prosa de nueve vueltas ha convergido sobre la interfaz que el programa ya
tenía tipada — señal de diseño correcto, no casualidad.

**Calibración de honestidad (veredicto del verificador):** (SC) es la QUINTA
forma equivalente — dado (1), (2) sobre E equivale a (MC) (todo límite débil
subsecuencial iguala su transformada a S_Ξ en E ⟹ por identidad +
determinación ES la medida de los ceros ⟹ convergencia de toda la sucesión y
de todos los momentos; el recíproco es inmediato). El libro queda:
(TP) ↔ (RATE) ↔ determinantes ↔ (MC) ↔ (SC). Lo que SÍ es genuino:
**economía de prueba en el lado de verificación** — puntual-sobre-E con una
acumulación interior basta donde el `approx` registrado pedía uniforme en
ventana; menos que comprobar el día que alguien tenga el límite. No
transfiere importancia: la equivalencia, no el empaquetado, es lo que estaba
medido, y el contenido — equidistribución exacta de los espectros finitos
sobre los ceros — vive íntegro dentro de la condición (2).

## (H₀) y RATE₀: el primer debilitamiento cuantitativo genuino — auditado 2026-08-06

Formulados por Codex, verificados adversarialmente por dos auditores
independientes (ambos CORRECT_WITH_CAVEATS; reparaciones incorporadas).

**(H₀), verificado:** el criterio de un punto RH ⟺ [Dᵏbₙ(x₀) ≥ 0 ∀n,k] vale
para TODO x₀ > 0, no solo x₀ > 1/4. Clave: ξ(s) > 0 en todo ℝ — en (0,1) vía
η(s) = (1−2^{1−s})ζ(s) con η > 0 (serie alternante, lo que PRUEBA la ausencia
de ceros reales en (0,1) en vez de asumirla) y 1−2^{1−s} < 0, luego
ζ < 0 y s(s−1) < 0 dan ξ > 0; ξ(1) = 1/2 por la cancelación (s−1)ζ(s);
s > 1 todo positivo; s ≤ 0 por ecuación funcional. La re-caminata completa
del Teorema 2.1 del paper con x₀ ∈ (0,1/4] localiza los TRES puntos cuya
justificación usaba x₀ > 1/4 y los reemplaza (finitud de bₙ; el segmento de
coincidencia — la frase impresa "because 1/2+y>1" FALLA y se sustituye por
ξ(1/2±y) > 0 en todo ℝ; nada más depende de x₀). El paper puede REFORZARSE a
x₀ > 0 con nueve ediciones concretas (registradas en el veredicto del
auditor; se suman a la cola v2). En x₀ = 1/4 exacto la finitud vive de la
cancelación (s−1)ζ(s) — debe quedar visible: el criterio se extiende para
ξ'/ξ, no para ζ'/ζ.

**RATE₀, verificado con tres reparaciones:** si A_λ = ‖k_λ‖₂√(2r_λ/Δ_λ) =
O(λ^{−q}) para ALGÚN q > 0, junto con las premisas cualitativas (ceros
reales del límite, k̂_λ → Ξ en un entorno compacto FINO de un segmento
imaginario, simplicidad/paridad), entonces RH. Reparaciones: (i) interponer
a₂ < a₃ < min(q,1/2) — la convergencia de derivadas por Cauchy en el borde
|Im z| = a₂ exige margen; costless. (ii) RE-BASADO que DESACOPLA de (H₀): no
instanciar (SC) en x₀ = a₂² (< 1/4, rompería la condición depositada) sino
mantener x₀ = 1/2 — parámetro LIBRE — y mapear el intervalo de convergencia
a E = [1−2a₂², 1−2a₁²] ⊂ (0,1), con acumulación interior y lejos de z = 1;
la cota de masa sale gratis de convergencia-en-un-punto + monotonía término
a término (que usa los ceros reales). (iii) (SC) debe re-enunciarse para
medidas atómicas INFINITAS de masa acotada (la red UV entra en μ_λ); la
prueba sobrevive verbatim (Helly/Prokhorov solo pide masa acotada en [0,1]),
pero la capa Lean ~70% es atómica-finita y no cubre esta instanciación.
Contabilidad del origen: un cero de ξ̂ en 0 (multiplicidad par) da átomos en
t = 1 — inocuo con E lejos de z = 1, pero el enunciado debe cargarlo.

**El veredicto de honestidad, y es la frase de la campaña:** la caída
q > 1/2 → q > 0 es un debilitamiento GENUINO de la condición suficiente. El
umbral ½ era geografía — perseguir un cero hipotético por toda la franja
|Im z| < 1/2 con la palanca λ^η. La ruta nueva toca la transformada solo en
un entorno fino de un segmento imaginario y deja la amplificación al
principio de identidad. ¿Sobrevive alguna exigencia de anchura? UNA — y
localizarla es el núcleo honesto: **el ½ migra a la hipótesis x₀ > 1/4 del
criterio de un punto (1/4 = (1/2)², el peor desplazamiento cuadrado de un
cero fuera de línea) — pero x₀ es un parámetro LIBRE que el probador elige,
no una tasa que los aproximantes deban batir. La anchura ahora cuesta cero.**
Ninguna de las cuatro premisas abiertas se cierra: RATE₀ sigue conteniendo
toda la aritmética (la contabilidad prima ingenua sigue dando crecimiento
~2λ, y CUALQUIER decaimiento polinómico — hasta q = 0.01 — sigue exigiendo
la cancelación firmada que la barrera prueba inaccesible a toda contabilidad
positiva); la premisa 2 se debilita genuinamente (subfranja fina, Re
acotado); la transferencia N → ∞ sigue abierta y portante; y la PARIDAD
queda ahora consumida DOS veces — no solo el gap: sin ella ξ̂_λ no es par ni
real y la estructura Stieltjes entera falla (itemización nueva). El libro de
equivalencias (TP) ↔ (RATE) ↔ det ↔ (MC) ↔ (SC) NO debe leerse como que
q > 1/2 fuera necesario: era un artefacto de la ruta, y esta vuelta lo
demuestra.
