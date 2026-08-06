# La frontera analítica exacta tras la validación numérica del operador

Fecha: 2026-08-06. Registrado por la mesa de campaña (Claude Fable 5) a partir
de la formulación del desk Codex, auditada aquí. Contexto: piloto A3 verde,
parrilla de producción en curso. Este documento fija QUÉ quedaría por probar
para que este carril demostrara RH — y por qué ninguna parrilla finita puede
probarlo.

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
