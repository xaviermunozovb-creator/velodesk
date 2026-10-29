# Ejecuta diagnostico-udp.sh en IslaTortuga sin copiarlo (va por stdin). Pide la contraseña de root.
$sh = Join-Path $PSScriptRoot "diagnostico-udp.sh"
Get-Content $sh -Raw | ssh root@46.225.99.214 "bash -s"
