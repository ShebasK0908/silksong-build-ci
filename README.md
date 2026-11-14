# silksong-build-ci

Repo público SOLO de compilación: contiene el workflow de GitHub Actions y el
parche (lanzador en español + controles táctiles tipo Android para Silksong).

No contiene ningún archivo del juego ni claves. El workflow descarga los
archivos desde el repo privado del propietario usando un token guardado como
secreto del repo (se crea solo para la build y se borra al terminar), compila
con nxnative (upstream) y sube la .ipa resultante, en partes, a una release
del mismo repo privado.
