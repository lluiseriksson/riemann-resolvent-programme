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
