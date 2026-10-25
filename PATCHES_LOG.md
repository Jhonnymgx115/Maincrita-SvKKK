# 🛠️ Registro de Parches y Correcciones (`fix/patches`)

Esta rama está destinada a recibir hotfixes urgentes, resolución de colisiones entre mods, ajustes finos de configuración y scripts correctivos de KubeJS.

---

## 🎯 Tipos de Correcciones en esta Rama

- **Conflictos de Mixin**: Supresión de inyecciones redundantes o actualización de dependencias problemáticas.
- **Ajustes de Configuración**: Modificación de `config/*.json` y `config/*.toml` para mitigar lag, deshabilitar entidades bugeadas o corregir balances.
- **Hotfixes de Bloques / Items**: Corrección de IDs duplicados o recetas rotas mediante scripts en `kubejs/server_scripts/`.
- **Estabilidad de Red**: Ajustes de paquetes de red y timeouts en entornos de Azure y Pterodactyl.

---

## 📝 Plantilla de Registro de Parche

```markdown
### [FIX-YYYYMMDD-01] - Título del Fix
- **Modpack afectado**: `modpack/horror-land-2` / `modpack/atm10` / etc.
- **Problema detectado**: Descripción del crash, error de log o caída de TPS.
- **Causa raíz**: Mod X intentaba inyectar en clase Y al mismo tiempo que mod Z.
- **Acción realizada**: Deshabilitado feature X en `config/mod_x.toml` / Añadido script correctivo.
- **Impacto**: Servidor vuelve a 20.0 TPS sin errores en consola.
```
