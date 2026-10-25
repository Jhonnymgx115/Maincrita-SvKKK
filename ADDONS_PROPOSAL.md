# 🧪 Banco de Pruebas — Propuesta de Nuevos Mods (`feature/custom-addons`)

Esta rama está reservada exclusivamente para probar, perfilar e incorporar mods adicionales que la comunidad o los administradores deseen integrar con el tiempo.

---

## 📋 Formulario para Proponer un Nuevo Mod

Al crear un Pull Request o commit en esta rama, completa la siguiente ficha técnica:

```markdown
### Ficha Técnica de Mod
- **Nombre del Mod**: 
- **Versión exacta**: 
- **Loader**: NeoForge 1.21.1
- **Enlace (Modrinth / CurseForge)**: 
- **Lado requerido**: [ ] Servidor [ ] Cliente [ ] Ambos (Híbrido)
- **Librerías / Dependencias obligatorias**:
- **¿Reemplaza o colisiona con algún mod actual?**: 
- **Resultado prueba local de arranque**: [ ] OK sin errores de Mixin
- **Impacto de TPS medido (Spark)**: ___ ms por tick
```

---

## 🚦 Criterios de Aceptación para Fusionar a un Modpack

1. **Cero errores de Mixin** en el arranque limpio del servidor.
2. **Uso de memoria**: No generar fugas de memoria (Memory Leaks) en periodos de prueba prolongados.
3. **No romper recetas existentes** ni IDs de biomas/bloques de los mundos guardados.
4. **Actualizar la tabla** en [MODS_COMPATIBILITY.md](./MODS_COMPATIBILITY.md) con el veredicto final.
